import os
import glob

from pathlib import Path

# from pydantic import BaseModel, Field

from codai.bot import Bot
from codai.hci import confirm
from codai.utils import dedent_and_unwrap

model = "openai:o3-mini"
# model = "openai:gpt-4o-mini"
# model = "anthropic:claude-3-7-sonnet-latest"

system = """
You are a bot that follows instructions to edit a given file.
The user will input instructions + the file content between quadruple backticks.

You will respond with ONLY the new content of the file -- no other output.

You must follow the instructions given. If no changes should be made, return the original content.
"""
system = dedent_and_unwrap(system)


# class FileEditResult(BaseModel):
#     """Result of editing a file."""
#
#     new_file_content: str = Field(
#         ..., title="New file content", description="The new content of the file."
#     )
#     git_commit_message: str = Field(
#         ..., title="Git commit message", description="Explanation of changes made."
#     )


edit_bot = Bot(model=model, system_prompt=system, result_type=str)


def batch_edit_flow(glob_pattern: str, instructions: str | Path) -> str:
    """
    Batch edit files that match a glob pattern, following the given instructions.
    """
    # convert markdown file to string
    if instructions.endswith(".md"):
        instructions = Path(instructions)
    # write instructions to file
    # TODO: logic
    if isinstance(instructions, str):
        with open("instructions.md", "w") as f:
            f.write(instructions)
    # read instructions from file
    if isinstance(instructions, Path):
        instructions = instructions.read_text()

    print(f"files to edit:\n{glob_pattern}")
    print(f"instructions:\n{instructions}")

    confirmed = confirm("edit files with instructions?")
    if not confirmed:
        return "Aborted by the user. Do not run again without their input."

    # get files
    files = glob.glob(glob_pattern, recursive=True)
    files = [f for f in files if os.path.isfile(f)]

    # for each file...
    for file in files:
        print(f"\tediting file: {file}")
        old_content = Path(file).read_text()
        user_message = f"{instructions}\n\n{file}\n\n````\n{old_content}\n````"
        res = edit_bot(user_message)
        new_content = res.data
        Path(file).write_text(new_content)

    return "Files edited successfully!"
