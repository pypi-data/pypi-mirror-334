from codai.bot import Bot
from codai.utils import dedent_and_unwrap, get_codai_config
from codai.flows.batch_edit import batch_edit_flow
# from codai.hci import get_user_input

config = get_codai_config()
model = config.get("model", "openai:o3-mini")

system = """
You are a refactor bot.
You converse with the user to understand their goals for a given refactor.
When you have clarity on the goals, you use your `batch_edit_flow` tool to refactor files.

Before calling the `batch_edit_flow` tool, you must:

1. Understand the user's goals.
2. Identify the files to edit in the form of a glob pattern.
3. Identify the proper instructions to refactor the files.

The tool will edit the files for you -- you simple pass in the glob string + sufficient instructions.

DO NOT call the tool until you have clarity on the user's goals and the files to edit.

The user can run shell commands that will be included in the conversation.
"""
system = dedent_and_unwrap(system)

tools = [batch_edit_flow]

bot = Bot(model=model, system_prompt=system, tools=tools)
