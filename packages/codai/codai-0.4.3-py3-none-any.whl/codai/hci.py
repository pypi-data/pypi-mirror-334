# TODO: this file is a mess; reconcile w/ repl.py and clean up
# imports
import os
import glob
import rich
import pyperclip
import subprocess
import shlex

from difflib import unified_diff

from rich.panel import Panel
from rich.console import Console
from rich.markdown import Markdown

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory, InMemoryHistory
from prompt_toolkit.completion import Completer, Completion

from codai.utils import get_codai_dir

console = Console()


# classes
class PathCompleter(Completer):
    def get_completions(self, document, complete_event):
        # Only run autocompletion for commands starting with '!'
        full_text = document.text_before_cursor
        if not full_text.startswith("!"):
            return

        # Only show completions when explicitly requested (e.g., on Tab press)
        if not complete_event.completion_requested:
            return

        # If text ends with a space, assume the token is complete
        if full_text.endswith(" "):
            file_fragment = ""
        else:
            try:
                parts = shlex.split(full_text)
            except ValueError:
                parts = full_text.split()
            file_fragment = parts[-1] if parts else ""

        start_position = -len(file_fragment)
        expanded = os.path.expanduser(file_fragment)
        matches = glob.glob(expanded + "*")
        for match in matches:
            yield Completion(match, start_position=start_position)


# functions
def get_input(prompt_text: str, history: FileHistory | InMemoryHistory) -> str:
    session = PromptSession(history=history, completer=PathCompleter())
    return session.prompt(prompt_text)


def get_user_input(prompt_text: str) -> str:
    """Ask the user for input.

    Args:
        prompt_text (str): The text to prompt the user with.
    Returns:
        str: The user's input.
    """
    history = FileHistory(os.path.join(get_codai_dir(), "bots.history"))
    return get_input(prompt_text, history)


def confirm(text: str, *args, **kwargs) -> bool:
    confirmed = get_input(f"{text} (y/n): ", InMemoryHistory())
    if confirmed.lower() in ["y", "yes"]:
        return True
    else:
        return False


def echo(text: str, *args, **kwargs) -> None:
    rich.print(text, *args, **kwargs)


def print(
    text: str, as_markdown: bool = True, as_panel: bool = True, header: str = "codai"
) -> None:
    # style map
    style_map = {
        "user": "bold cyan",
        "codai": "bold violet",
    }

    if as_markdown:
        text = Markdown(text)

    if as_panel:
        text = Panel(text, title=header, border_style=style_map[header])

    console.print(text)


def clear() -> None:
    console.clear()


def run_command(command: str) -> str:
    confirmed = confirm(f"Run command: {command}?")
    if not confirmed:
        echo("Aborted.")
        return "User aborted running the command. Do not try to run it again."

    res = subprocess.run(command, shell=True, capture_output=True)
    stdout = res.stdout.decode("utf-8")
    stderr = res.stderr.decode("utf-8")

    # goofy
    to_return = f"Command '{command}' executed with status code '{res.returncode}'."
    if stdout and not stderr:
        to_return += f"\n\n{stdout}"
    elif not stdout and stderr:
        to_return += f"\n\n{stderr}"
    else:
        to_return += f"\n\n{stdout}\n\n{stderr}"

    return to_return


def _copy_to_clipboard(text: str) -> None:
    pyperclip.copy(text)


def copy_to_clipboard(text: str) -> str:
    _copy_to_clipboard(text)
    return "Successfully copied text to to clipboard"


def read_file(file_path: str) -> str:
    """read file content"""
    with open(file_path, "r") as file:
        return file.read()


def git_diff(old_text: str, new_text: str) -> str:
    old_lines = old_text.splitlines(keepends=True)
    new_lines = new_text.splitlines(keepends=True)

    diff = unified_diff(old_lines, new_lines, lineterm="")

    return "\n".join(diff)


def write_file(file_path: str, content: str) -> str:
    if os.path.exists(file_path):
        old_content = read_file(file_path)
    else:
        old_content = ""
    diff = git_diff(old_content, content)

    confirmed = confirm(f"Write to {file_path}?\n\nDiff:\n{diff}")
    if not confirmed:
        print("Aboring the write operation...")
        return "User aborted the write! Check why with them."

    with open(file_path, "w") as file:
        file.write(content)

    return f"Successfully written to {file_path}"
