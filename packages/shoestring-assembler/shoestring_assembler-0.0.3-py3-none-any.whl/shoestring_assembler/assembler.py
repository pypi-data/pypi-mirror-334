"""Main module."""

import rich.progress
from rich.prompt import Prompt, Confirm
import json
import time
import sys
import subprocess
import hashlib
from pathlib import Path
from . import display

try:
    from pathlib import UnsupportedOperation
except ImportError:
    UnsupportedOperation = NotImplementedError
import os

try:
    import tomllib as toml
except ImportError:
    import tomli as toml

import yaml
import jsonschema
import re
import select
from . import minimal_mustache
from functools import cache

src_dir = os.path.dirname(os.path.realpath(__file__))


# CONSTANTS
SOLUTION_FILES_DIR = "solution_files"
BASE_MODULE_FILES_DIR = f"{SOLUTION_FILES_DIR}/sources"
SOLUTION_CONFIG_DIR = f"{SOLUTION_FILES_DIR}/config"
USER_CONFIG_SRC_DIR = f"{SOLUTION_FILES_DIR}/user_config_templates"
USER_CONFIG_VERSION_FILE = "__version__"

DATA_DIR = "data"
USER_CONFIG_DIR = "user_config"


DOCKER_NETWORK_NAME = "internal"


class Assembler:
    def __init__(self, recipe_filepath):
        self._recipe_filepath_provided = recipe_filepath
        self._recipe_location = Path.resolve(Path(recipe_filepath))
        self._recipe = None
        self._recipe_hash = None

    def load_recipe(self):
        display.print_header("Get Recipe")
        try:
            # check file type is supported and find parser
            ext = self._recipe_location.suffix

            if ext == ".yml" or ext == ".yaml":
                parser = self._parse_yaml
            elif ext == ".toml":
                parser = self._parse_toml
            elif ext == ".json":
                parser = self._parse_json
            else:
                display.print_error(
                    f"Recipe format unsupported - expects a json, yaml or toml file"
                )
                sys.exit(255)

            # parse file
            with display.open_file(
                self._recipe_location, "rb", description="Loading Recipe..."
            ) as file:
                self._recipe = parser(file)
                file.seek(0)  # reset file
                hash_fn = hashlib.sha256()
                hash_fn.update(file.read())
                self._recipe_hash = hash_fn.hexdigest()

            self.validate_recipe()

        except FileNotFoundError:
            display.print_error(
                f"Unable to find recipe file. Expected to find it at: {self._recipe_location}"
            )
            sys.exit(255)

        display.print_complete("Recipe loaded")

    def _parse_json(self, file):
        return json.load(file)

    def _parse_yaml(self, file):
        return yaml.safe_load(file)

    def _parse_toml(self, file):
        return toml.load(file)

    def validate_recipe(self):
        display.print_log("Validating Recipe")
        schema_location = os.path.join(src_dir, "schemas/recipe.schema.json")

        try:
            with display.open_file(
                schema_location, "rb", description="Loading Recipe Schema..."
            ) as file:
                schema = json.load(file)

            schema_validate(self._recipe, schema)

        except FileNotFoundError:
            display.print_error(
                f"Unable to find recipe schema. Expected to find it at: {schema_location}"
            )
            sys.exit(255)
        except jsonschema.ValidationError as v_err:
            display.print_error(
                f"Recipe error at {v_err.json_path}:\n\n{v_err.message}"
            )
            display.print_error(
                "Config File is not valid -- unable to start the solution -- please correct the issues flagged above and try again."
            )
            sys.exit(255)

        display.print_log("Recipe valid")

    def clean(self, clean_sources=True):
        display.print_header("Cleaning")
        # TODO
        if clean_sources:
            rmtree(Path(BASE_MODULE_FILES_DIR))
        display.print_complete("Old files cleared")

    def verify_filestructure(self, check_sources=False):
        display.print_header("Verifying filesystem structure")

        source_list = self._recipe["source"].keys()
        instance_list = [
            *self._recipe.get("service_module", {}).keys(),
            *self._recipe.get("infrastructure", {}).keys(),
        ]

        all_ok = True

        # check solution directories
        all_ok = check_dir(SOLUTION_FILES_DIR) and all_ok
        all_ok = check_dir(SOLUTION_CONFIG_DIR) and all_ok
        for source_name in source_list:
            all_ok = check_dir(f"{SOLUTION_CONFIG_DIR}/{source_name}") and all_ok

        all_ok = check_or_create_dir(BASE_MODULE_FILES_DIR) and all_ok
        if check_sources:
            for source_name in source_list:
                all_ok = check_dir(f"{BASE_MODULE_FILES_DIR}/{source_name}") and all_ok

        # check data directories
        all_ok = check_or_create_dir(DATA_DIR) and all_ok
        for instance in instance_list:
            all_ok = check_or_create_dir(f"data/{instance}") and all_ok

        # check user config directories
        all_ok = check_or_create_dir(USER_CONFIG_DIR) and all_ok
        for instance in instance_list:
            all_ok = check_or_create_dir(f"{USER_CONFIG_DIR}/{instance}") and all_ok

        # check log directories
        all_ok = check_or_create_dir("logs") and all_ok
        # for source_name in self._recipe["source"].keys():
        #     all_ok = check_or_create_dir(f"logs/{source_name}") and all_ok

        if not all_ok:
            display.print_error(
                "Filesystem structure failed validation - unable to continue"
            )
            sys.exit(255)
        else:
            display.print_complete("Filesystem structure valid")

    def gather_base_service_modules(self, do_gather):
        display.print_header("Gathering Service Module Sources")

        if not do_gather:
            display.print_complete(
                "Fetching service module sources disabled by command line arguements"
            )
        else:
            number_of_service_modules = len(self._recipe["source"])

            with (
                rich.progress.Progress() as progress
            ):  # displays progress bar on console
                task = progress.add_task(
                    "[cyan]  Gathering Service Module Sources",
                    total=number_of_service_modules,
                )

                listed_sources = self._recipe["source"]
                service_module_source_set = [
                    details["source"]
                    for details in self._recipe["service_module"].values()
                ]
                infrastructure_source_set = [
                    details["source"]
                    for details in self._recipe.get("infrastructure", {}).values()
                ]

                used_sources = {
                    source_name: listed_sources[source_name]
                    for source_name in service_module_source_set
                }
                used_sources.update(
                    {
                        source_name: listed_sources[source_name]
                        for source_name in infrastructure_source_set
                    }
                )

                for source_name, source_details in used_sources.items():
                    display.print_log(
                        f"Fetching {source_name}", console=progress.console
                    )

                    if "file" in source_details:
                        result = handle_file_source(
                            source_name,
                            source_details["file"],
                            console=progress.console,
                        )
                    elif "git" in source_details:
                        result = handle_git_source(
                            source_name,
                            source_details["git"],
                            console=progress.console,
                            progress=progress,
                        )
                    else:
                        # this should never happen due to recipe validation
                        display.print_error(
                            f"Source {source_name} does not include details on where to get it",
                            console=progress.console,
                        )
                        sys.exit(255)

                    if result:
                        display.print_complete(
                            f"Fetched '{source_name}' ", console=progress.console
                        )
                        progress.update(task, advance=1)  # updates progress bar
                    else:
                        progress.update(task, visible=False)
                        display.print_error(
                            f"An error occured while fetching '{source_name}'",
                            console=progress.console,
                        )
                        sys.exit(255)

            display.print_complete("All Service Module Sources Gathered")

    def check_user_config(self):
        display.print_header("Checking User Config")
        has_notifications = False
        for service_module_name, service_module_details in self._recipe[
            "service_module"
        ].items():
            # display.print_log(f"[cyan]*  {service_module_name}")
            source = service_module_details["source"]
            try:
                template_dir = f"{USER_CONFIG_SRC_DIR}/{source}"
                service_module_dir = f"{USER_CONFIG_DIR}/{service_module_name}"
                outcome = compare_template_versions(
                    template_dir,
                    service_module_dir,
                )
                display.print_log(
                    f"[green]\[{outcome}][/green] [white]{service_module_name}"
                )
                if outcome in ["new_version_major", "new_version_minor"]:
                    display.print_notification(
                        f"There is a new version of the user config files for {service_module_name}!"
                        + "You will need to transfer your current config to the new format otherwise the solution will not work as expected."
                        + f"You can find the current user config files at [purple]./{service_module_dir}[/purple] and the template files at [purple]./{template_dir}[/purple]"
                    )
                    has_notifications = True
                elif outcome == "empty":
                    transfer_user_config_from_template(template_dir, service_module_dir)

            except InvalidVersion as e:
                display.print_error(
                    f"The {e.source} version file contained an invalid version."
                )
                sys.exit(255)
            except FileNotFoundError:
                display.print_error(
                    f"Couldn't find version file in template directory. Directory expected at {template_dir}."
                )
                sys.exit(255)
            except TemplateOlderThanCurrentVersion as e:
                display.print_log(f"[yellow]\[warning][/yellow] {service_module_name}")
                display.print_warning(
                    f"Current user config version is {e.current_vsn} which is newer than the template version of {e.template_vsn}.\n"
                    + f"[red]This might be ok! [/red] - but it should be checked!\n"
                    + f"You can find the current user config files at [purple]./{service_module_dir}[/purple] and the template files at [purple]./{template_dir}[/purple]"
                )
                has_notifications = True
                # doesn't exit as this may be ok (e.g. roll back after update)

        if has_notifications:
            do_continue = Confirm.ask(
                "Please see the notifications above. continue?", default=True
            )
            if not do_continue:
                sys.exit()

        display.print_complete(f"User config ready")

    def generate_compose_file(self):
        display.print_header("Generating Compose File")
        compose_definition = {
            "services": {},
            "networks": {DOCKER_NETWORK_NAME: {"name": "shoestring-internal"}},
        }

        for service_module_name, service_module_details in self._recipe.get(
            "service_module", {}
        ).items():
            service_set = self.generate_docker_services_for_module(
                service_module_name, service_module_details, "service_module"
            )
            compose_definition["services"].update(service_set)

        for infra_module_name, infra_module_details in self._recipe.get(
            "infrastructure", {}
        ).items():
            service_set = self.generate_docker_services_for_module(
                infra_module_name, infra_module_details, "infrastructure"
            )
            compose_definition["services"].update(service_set)

        compose_definition["x-shoestring"] = {
            "filename": self._recipe_filepath_provided,
            "hash": self._recipe_hash,
        }

        with open(Path.resolve(Path.cwd()) / Path("compose.yml"), "w") as f:
            yaml.safe_dump(
                compose_definition, f, default_flow_style=False, sort_keys=False
            )
        display.print_complete(f"Compose file complete")

    def generate_docker_services_for_module(
        self, module_name, module_details, module_type
    ):
        display.print_log(f"[cyan]*  {module_name}")
        module_services = {}
        # load meta.toml
        source = module_details["source"]
        try:
            meta_file_path = f"./{BASE_MODULE_FILES_DIR}/{source}/meta.toml"
            meta_schema = load_meta_schema()
            with display.open_file(
                meta_file_path,
                "rb",
                description="Loading meta...",
            ) as file:
                meta = toml.load(file)
                schema_validate(meta, meta_schema)
        except FileNotFoundError:
            display.print_error(
                f"Unable to find meta file for {source}. Expected to find it at: {meta_file_path}"
            )
            sys.exit(255)
        except jsonschema.ValidationError as v_err:
            display.print_error(
                f"Error in meta file for source '{source}' at {v_err.json_path}:\n\n{v_err.message}"
            )
            display.print_error(
                f"Meta file for source '{source}' is not valid -- unable to start the solution"
            )
            sys.exit(255)

        container_list = module_details.get("containers", [])
        for container in container_list:
            entry_identifier = module_name

            if len(container_list) > 1:
                entry_identifier = f"{module_name}-{container}"
                display.print_log(f"[cyan]**  {entry_identifier}")

            network_alias = (
                module_details["alias"].get(container, entry_identifier)
                if "alias" in module_details
                else entry_identifier
            )

            container_meta = meta[container]
            # form base
            service_definition = {
                "build": {
                    "context": f"./{BASE_MODULE_FILES_DIR}/{source}/",
                    "dockerfile": f"./{container_meta.get('dockerfile','Dockerfile')}",
                    "additional_contexts": [
                        f"solution_config=./{SOLUTION_CONFIG_DIR}/{source}"
                    ],
                },
                "networks": {
                    DOCKER_NETWORK_NAME: {"aliases": [f"{network_alias}.docker.local"]}
                },
                "logging": {
                    "driver": "syslog",
                    "options": {"tag": f"docker-{entry_identifier}"},
                },
                "labels": {
                    "net.digitalshoestring.solution": self._recipe["solution"]["slug"],
                    "net.digitalshoestring.function": module_type,
                },
                "restart": "unless-stopped",
            }
            # extend with partials
            partials = {}
            if "compose_partial" in container_meta:
                try:
                    partial_file_path = f'./{BASE_MODULE_FILES_DIR}/{source}/{container_meta["compose_partial"]}'
                    with display.open_file(
                        partial_file_path,
                        "r",
                        description="Loading compose partials...",
                    ) as file:
                        template_applied_string = minimal_mustache.render(
                            file.read(), module_details.get("template", {})
                        )
                        partials = yaml.safe_load(template_applied_string)
                except FileNotFoundError:
                    display.print_error(
                        f"Unable to find compose partial file for {source}. Expected to find it at: {partial_file_path}"
                    )
                    sys.exit(255)

            service_definition = {
                **partials,
                **service_definition,
            }  # update in this way to prevent partials from overwriting service_definition keys

            # sort out volumes
            volumes = {
                "data": {"host": f"./{DATA_DIR}/{module_name}"},
                "user_config": {"host": f"./{USER_CONFIG_DIR}/{module_name}"},
            }  # defaults
            container_vols = container_meta.get("volume", {})
            # map in items
            for name, details in container_vols.items():
                if name not in volumes:
                    volumes[name] = {}
                volumes[name]["container"] = details

            compose_volumes = []
            for name, mapping in volumes.items():
                has_host = "host" in mapping
                has_cnt = "container" in mapping
                if has_host and has_cnt:  # everything as expected
                    if mapping["container"].get("ignore") == True:
                        continue  # container doesn't use this volume

                    if "mode" in mapping["container"]:
                        container_entry = f'{mapping["container"]["path"]}:{mapping["container"]["mode"]}'
                    else:
                        container_entry = f'{mapping["container"]["path"]}'

                    entry = f'{mapping["host"]}:{container_entry}'
                    compose_volumes.append(entry)
                elif has_host:
                    # no container entry to map to
                    display.print_error(
                        f"No corresponding container entry for volume {name} of {entry_identifier}."
                    )
                    sys.exit(255)
                elif has_cnt:
                    # no host entry to map to
                    display.print_error(
                        f"No corresponding host entry for volume {name} of {entry_identifier}."
                    )
                    sys.exit(255)
            if len(compose_volumes) > 0:
                service_definition["volumes"] = compose_volumes

            # map in ports
            ports = {}  # defaults

            # map in container ports
            container_ports = container_meta.get("ports", {})
            for name, port_number in container_ports.items():
                if name not in ports:
                    ports[name] = {}
                ports[name]["container"] = port_number
            # map in host ports
            host_ports = module_details.get("ports", {}).get(container, {})
            for name, port_number in host_ports.items():
                if name not in ports:
                    ports[name] = {}
                ports[name]["host"] = port_number

            # combine mappings
            compose_ports = []
            for name, mapping in ports.items():
                has_host = "host" in mapping
                has_cnt = "container" in mapping
                if has_host and has_cnt:  # everything as expected
                    entry = f'{mapping["host"]}:{mapping["container"]}'
                    compose_ports.append(entry)
                elif has_host:
                    # no container entry to map to
                    display.print_error(
                        f"No corresponding container entry for port {name} of {entry_identifier}."
                    )
                    sys.exit(255)
                elif has_cnt:
                    # no host entry to map to
                    display.print_error(
                        f"No corresponding host entry for port {name} of {entry_identifier}."
                    )
                    sys.exit(255)
            if len(compose_ports) > 0:
                service_definition["ports"] = compose_ports

            module_services[entry_identifier] = service_definition

        return module_services


## Filesystem Utilities
def check_dir(rel_path):
    full_path = Path.resolve(Path.cwd()) / Path(rel_path)
    if full_path.is_dir():
        display.print_log(f"[green]\[ok] [white] {rel_path}")
        return True
    else:
        display.print_log(f"[red]\[error - not found] {rel_path}")
        return False


def check_or_create_dir(rel_path):
    full_path = Path.resolve(Path.cwd()) / Path(rel_path)
    try:
        full_path.mkdir(exist_ok=False)
        display.print_log(f"[green]\[created] [white]{rel_path}")
    except FileExistsError:
        try:
            full_path.mkdir(exist_ok=True)
            display.print_log(f"[green]\[ok] [white] {rel_path}")
        except FileExistsError:
            display.print_log(f"[red]\[error - can't create] {rel_path}")
            return False
    except FileNotFoundError:
        display.print_log(f"[red]\[error - no parent] {rel_path}")
        return False

    return True


if sys.version_info[0] == 3 and sys.version_info[1] < 14:

    def do_copy(src_path, dest_path,create_dirs = False):
        import shutil

        shutil.copytree(src_path, dest_path, dirs_exist_ok=create_dirs)

else:

    def do_copy(src_path, dest_path,create_dirs = False):
        src_path.copy_into(dest_path)


if sys.version_info[0] == 3 and sys.version_info[1] < 12:

    def rmtree(root: Path):
        display.print_log(f"Clearing {root}")
        for walk_root, dirs, files in os.walk(root, topdown=False):
            walk_root = Path(walk_root)
            for name in files:
                (walk_root / name).unlink()
            for name in dirs:
                path = walk_root / name
                if path.is_symlink():
                    path.unlink()
                else:
                    path.rmdir()

else:

    def rmtree(root: Path):
        display.print_log(f"Clearing {root}")
        for root, dirs, files in root.walk(top_down=False):
            for name in files:
                (root / name).unlink()
            for name in dirs:
                (root / name).rmdir()


class InvalidVersion(Exception):
    def __init__(self, message="invalid version", source=""):
        super().__init__(message)
        self.source = source


class TemplateOlderThanCurrentVersion(Exception):

    def __init__(self, message="template older", current_vsn=[], template_vsn=[]):
        super().__init__(message)
        self.current_vsn = ".".join(list(current_vsn))
        self.template_vsn = ".".join(list(template_vsn))


def compare_template_versions(template_dir_path, dest_dir_path):
    template_version_dir = Path.resolve(Path.cwd()) / Path(template_dir_path)
    template_version_file = template_version_dir / USER_CONFIG_VERSION_FILE
    dest_version_file = (
        Path.resolve(Path.cwd()) / Path(dest_dir_path) / USER_CONFIG_VERSION_FILE
    )

    if not template_version_dir.exists():
        # continue - there is no template to apply
        return "no_template"

    # will throw file not found if template doesn't have version file
    with display.open_file(
        template_version_file, "r", description="Getting template version..."
    ) as f:
        template_version = get_version_from_file(f)
        if template_version is None:
            raise InvalidVersion(source="template")

    try:
        with display.open_file(
            dest_version_file, "r", description="Getting existing version..."
        ) as f:
            dest_version = get_version_from_file(f)
            if dest_version is None:
                raise InvalidVersion(source="destination")
    except FileNotFoundError:
        display.print_log("Destination Empty")
        return "empty"

    for index in range(3):
        if template_version[index] == dest_version[index]:
            continue
        if template_version[index] > dest_version[index]:
            return ["new_version_major", "new_version_minor", "new_version_patch"][
                index
            ]  # TODO improve how this is handled
        if template_version[index] < dest_version[index]:
            raise TemplateOlderThanCurrentVersion(
                current_vsn=dest_version, template_vsn=template_version
            )

    return "up-to-date"


version_regex = re.compile("^\s*(\d+)\.(\d+)\.(\d+)\s*$")


def get_version_from_file(file):
    match = version_regex.match(file.read())
    return match.groups() if match else None


def transfer_user_config_from_template(template_dir_path, dest_dir_path):
    template_dir = Path.resolve(Path.cwd()) / Path(template_dir_path)
    dest_dir = Path.resolve(Path.cwd()) / Path(dest_dir_path)
    do_copy(template_dir,dest_dir, True)
    display.print_log(f"Copied user config to {dest_dir_path} from template")


# schema utilities


@cache
def load_meta_schema():
    schema_location = os.path.join(src_dir, "schemas/meta.schema.json")

    try:
        with display.open_file(
            schema_location, "rb", description="Loading Meta Schema..."
        ) as file:
            schema = json.load(file)
            return schema

    except FileNotFoundError:
        display.print_error(
            f"Unable to find meta schema. Expected to find it at: {schema_location}"
        )
        sys.exit(255)


def schema_validate(config, schema):
    jsonschema.validate(
        instance=config,
        schema=schema,
        format_checker=jsonschema.Draft202012Validator.FORMAT_CHECKER,
    )


# source utilities


def handle_file_source(name, details, console=None):
    mode = details.get("mode", "copy")
    path = details["path"]  # could throw error but shouldn't due to validation

    display.print_log(f"type: file, mode: {mode}", console=console)

    src_path = Path.resolve(Path(path))
    dest_path = Path.resolve(Path.cwd()) / BASE_MODULE_FILES_DIR / name

    if mode == "copy":
        do_copy(src_path, dest_path)
        display.print_log(
            f"{src_path} [green]copied[/green] to {dest_path}", console=console
        )
    elif mode == "link":
        try:
            dest_path.symlink_to(src_path, target_is_directory=True)
            display.print_log(
                f"{src_path} [green]linked[/green] to {dest_path}", console=console
            )
        except UnsupportedOperation:
            display.print_error(
                f"Operating system does not support symlinks. Could not link [purple]{src_path}[/purple] to [purple]{dest_path}[/purple] for source {name}. Consider changing [cyan]mode[/cyan] to [cyan]copy[/cyan].",
                console=console,
            )
            return False
        except FileExistsError:
            display.print_error(
                f"Files already present at destination - Could not link [purple]{src_path}[/purple] to [purple]{dest_path}[/purple] for source {name}.",
                console=console,
            )
            return False

    return True


def handle_git_source(name, details, console, progress: rich.progress.Progress):
    tag = details.get("tag")
    branch = details.get("branch")
    path = details["path"]  # could throw error but shouldn't due to validation

    dest_path = Path.resolve(Path.cwd()) / BASE_MODULE_FILES_DIR / name

    num_slashes = path.count("/")
    if num_slashes == 0:
        url = f"https://github.com/DigitalShoestringSolutions/{path}"
    elif num_slashes == 1:
        url = f"https://github.com/{path}"
    else:
        url = path

    display.print_log(
        f"type: git, repo: {url} target:{ f'tag {tag}' if tag else f' branch {branch}'}",
        console=console,
    )

    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = (
        "0"  # prevents hanging on username input if url invalid
    )

    command = [
        "git",
        "clone",
        "--progress",  # force inclusion of progress updates
        "--depth",
        "1",  # only download latest commit - no history (massive speed up)
        "--branch",
        tag if tag else branch,
        url,
        dest_path,
    ]

    display.print_debug(f"command: {command}", console=console)

    process = subprocess.Popen(
        command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, env=env
    )  # git outputs updates over stderr

    # likely overkill but would be good to be able to relay updates
    buffer = bytearray()
    active_progress_tracker = None
    regex = re.compile("^(?P<label>.*)\d+% \((?P<progress>\d*)/(?P<total>\d*)\).*")
    while process.returncode == None:
        while True:
            line = None
            line_update = False

            read_list, _wlist, _xlist = select.select([process.stderr], [], [], 1)
            # display.print_log(read_list,console=console)
            if process.stderr in read_list:
                char = process.stderr.read(1)
                if char == b"\r" or char == b"\n":
                    if char == b"\r":
                        line_update = True
                    line = buffer.decode()
                    buffer.clear()
                elif char:
                    # display.print_log(f"char: {char}", console=console)
                    buffer += char
                else:
                    break  # end of file
            else:
                break  # timeout - break to check if process terminated

            if line:
                if active_progress_tracker or line_update:  # progress update line
                    m = regex.match(line)
                    if active_progress_tracker:
                        if line_update:  # update
                            progress.update(
                                active_progress_tracker,
                                completed=int(m.group("progress")),
                            )
                        else:  # end
                            if m:
                                progress.update(
                                    active_progress_tracker,
                                    completed=int(m.group("progress")),
                                )
                            else:
                                progress.update(active_progress_tracker, advance=100000)
                            progress.stop_task(active_progress_tracker)
                            progress.remove_task(active_progress_tracker)
                            active_progress_tracker = None
                            display.print_log(f"[white]{line}", console=console)
                    elif line_update:  # new
                        active_progress_tracker = progress.add_task(
                            m.group("label"),
                            start=True,
                            completed=int(m.group("progress")),
                            total=int(m.group("total")),
                        )
                else:  # normal line
                    display.print_log(f"[white]{line}", console=console)
            else:
                pass

        process.poll()

    return process.returncode == 0


"""
TO DO List:
* work out what clean means
* user_config templates
* solution config templates & bootstrapping

Longer term
* host side volume specification
* named volumes - when only has container entry?
    * would need warning if repeated
* Environment variables
* coveying port and alias mappings to services
*   external resources
"""
