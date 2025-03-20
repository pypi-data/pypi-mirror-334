"""Console script for shoestring_assembler."""

from shoestring_assembler import assembler, display

import typer
from typing_extensions import Annotated
import time
import os
import sys

from rich.live import Live
from rich.table import Table

__version__ = "0.0.1"

typer_app = typer.Typer(name="Shoestring Assembler", no_args_is_help=True)


cwd = os.getcwd()


@typer_app.command()
def update(recipe: str = "./recipe.toml"):
    display.print_log(
        "For help - go to [link=https://community.digitalshoestring.net]the Shoestring Community[/link]!"
    )


@typer_app.command(help="Fetch all base service modules")
def pull(recipe: str = "./recipe.toml"):
    with Live(console=display.root_console, transient=True) as live:
        live.console.print("[bold blue]Starting work!")
        time.sleep(1)
        live.console.print("1")
        time.sleep(1)
        live.console.print("2")
        time.sleep(1)
        live.console.print("3")


@typer_app.command()
def bootstrap(
    recipe: str = "./recipe.toml",
    verbose: Annotated[
        bool, typer.Option("--verbose", help="enable verbose output")
    ] = False,
):
    """
    Uses templates to bootstrap the solution config for the specified sources
    """
    pass


@typer_app.command()
def assemble(
    recipe: str = "./recipe.toml",
    verbose: Annotated[
        bool, typer.Option("--verbose", help="enable verbose output")
    ] = False,
):
    """
    Assembles the solution using the provided recipe
    """
    if verbose:
        display.debug = True
    display.root_console.record = True
    try:
        display.print_top_header("Assembling Solution")
        assembler_inst = assembler.Assembler(recipe)
        assembler_inst.load_recipe()
        assembler_inst.validate_recipe()
        assembler_inst.clean()
        assembler_inst.verify_filestructure(check_sources=False)
        assembler_inst.gather_base_service_modules()
        assembler_inst.check_user_config()
        assembler_inst.generate_compose_file()
        display.print_top_header("Finished")
    finally:
        display.root_console.save_html("./console.log")


@typer_app.callback(invoke_without_command=True)
def main(
    version: Annotated[
        bool, typer.Option("--version", "-v", help="Assembler version")
    ] = False,
):
    if version:
        display.print_log(f"Shoestring Assembler version {__version__}")
    else:
        pass


def app():
    if os.geteuid() == 0:
        display.print_error(
            "To try prevent you from breaking things, this program won't run with sudo or as root! \nRun it again without sudo or change to a non-root user."
        )
        sys.exit(255)
    typer_app()


if __name__ == "__main__":
    app()
