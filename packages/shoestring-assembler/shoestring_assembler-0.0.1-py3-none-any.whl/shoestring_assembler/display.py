from rich.console import Console
from rich.panel import Panel

root_console = Console()
debug = False

# TODO: tee to file here

def _get_console(console):
    if console:
        return console
    else:
        return root_console

## Display Utilities
def print_top_header(text,console=None):
    console = _get_console(console)
    console.rule(f"[bold cyan]{text}", align="center")
    
def print_header(text, console=None):
    console = _get_console(console)
    # console.rule(f"[bold bright_magenta]{text}", style="bright_magenta", align="center")
    console.print(Panel(f"{text}", style="bright_magenta"))


def print_complete(text, console=None):
    console = _get_console(console)
    # console.rule(
    #     f"[bold green]:white_check_mark: {text}",
    #     style="green",
    #     align="center",
    # )
    # console.print(Panel(f":white_check_mark: {text}", style="green"))
    console.print(f":white_check_mark:\t{text}", style="green")


def print_error(text, console=None):
    console = _get_console(console)
    console.print(
        Panel(
            f"[bold red]{text}",
            title="[bold red]:warning:  Error",
            title_align="left",
            style="red",
        )
    )


def print_log(text, console=None):
    console = _get_console(console)
    console.print(text)

def print_debug(text,console = None):
    if not debug:
        return
    console = _get_console(console)
    console.print(
        Panel(
            f"[bold grey58]{text}",
            title="[bold grey58]Verbose log",
            title_align="left",
            style="grey58",
        )
    )
