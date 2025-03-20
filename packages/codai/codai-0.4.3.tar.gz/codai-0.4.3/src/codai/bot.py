# imports
import os
import ibis
import ibis.expr.datatypes as dt

from typing import Any, Callable
from pydantic import BaseModel
from pydantic_ai.agent import Agent, AgentRunResult
from pydantic_ai.models import Model
from pydantic_ai.messages import ModelMessagesTypeAdapter

from codai.utils import now, generate_uuid, get_codai_dir, dedent_and_unwrap

# constants
DEFAULT_MODEL = "openai:gpt-4o-mini"
DEFAULT_SYSTEM_PROMPT = """
# codai

You are Codai, a highly technical research and development assistant.
You interface with the user to achieve a goal.
"""
DEFAULT_SYSTEM_PROMPT = dedent_and_unwrap(DEFAULT_SYSTEM_PROMPT)


# class
class Bot:
    # init
    def __init__(
        self,
        name: str = "bot",
        username: str = "dev",
        system_prompt: str = None,
        tools: list[Callable] = [],
        model: str | Model = None,
        result_type: BaseModel | Any = str,
        dbpath: str = "bots.db",
    ) -> None:
        # set attributes
        self.id = generate_uuid()
        self.name = name
        self.username = username
        self.model = model or DEFAULT_MODEL
        self.system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT
        self.tools = tools
        self.result_type = result_type
        self.dbpath = os.path.join(get_codai_dir(), dbpath)

        # create Pydantic AI Agent
        self.agent = Agent(
            model=self.model,
            system_prompt=self.system_prompt,
            tools=self.tools,
            result_type=self.result_type,
        )

        # bootstrap tables
        self._bootstrap_tables()

        # create bot record
        self.append_bot(
            id=self.id,
            name=self.name,
            model=self.model.model_name
            if isinstance(self.model, Model)
            else self.model,
            system_prompt=self.system_prompt,
            tools=",".join([tool.__name__ for tool in self.tools]),
            result_type=str(self.result_type),
        )

    # call
    # NOTE: bots can/should override the __call__ method to provide custom behavior
    def __call__(
        self, text: str, message_history: list = None, *args, **kwargs
    ) -> AgentRunResult:
        # get the message history
        message_history = message_history or self.get_messages(bot_id=self.id)

        # run the agent
        res = self.agent.run_sync(
            text, message_history=message_history, *args, **kwargs
        )

        # append the new messages to the message history
        self.append_message(
            bot_id=self.id,
            data=res.new_messages_json(),
        )

        # return the result
        return res

    # manage message history
    def clear_messages(self) -> None:
        # "clear" messages by simply setting a new bot id, reusing the other metadata
        self.id = generate_uuid()

    def copy_messages(self, from_bot_id: str = None, to_bot_id: str = None) -> None:
        # switch models/agents mid-conversation by copying messages from one bot to another
        from_bot_id = from_bot_id or self.id
        assert to_bot_id, "to_bot_id must be provided"

        messages = self.get_messages(bot_id=from_bot_id)
        for message in messages:
            self.append_message(bot_id=to_bot_id, data=message["data"])

    # define connections
    def get_wcon(self) -> ibis.BaseBackend:
        wcon = ibis.sqlite.connect(self.dbpath)
        return wcon

    def get_rcon(self) -> ibis.BaseBackend:
        rcon = ibis.duckdb.connect()
        for table_name in self.get_wcon().list_tables():
            rcon.read_sqlite(self.dbpath, table_name=table_name)
        return rcon

    # define state
    def _bootstrap_tables(self) -> None:
        # create write connection
        wcon = self.get_wcon()

        # create tables in write connection
        self.bots_table_name = "bots"
        schema = ibis.schema(
            {
                "idx": dt.timestamp,
                "id": str,
                "name": str,
                "model": str,
                "system_prompt": str,
                "tools": str,
                "result_type": str,
            }
        )
        if self.bots_table_name not in wcon.list_tables():
            wcon.create_table(self.bots_table_name, schema=schema)

        self.messages_table_name = "messages"
        schema = ibis.schema(
            {
                "idx": dt.timestamp,
                "id": str,
                "bot_id": str,
                "data": bytes,
            }
        )
        if self.messages_table_name not in wcon.list_tables():
            wcon.create_table(self.messages_table_name, schema=schema)

    # tables
    def bots_t(self, id: str = None, name: str = None):
        # get bots data
        t = self.get_rcon().table(self.bots_table_name)

        # filter
        if id:
            t = t.filter(ibis._["id"] == id)
        if name:
            t = t.filter(ibis._["name"] == name)

        # get only the latest metadata
        t = (
            t.mutate(
                rank=ibis.row_number().over(
                    ibis.window(
                        group_by=ibis._["id"],
                        order_by=ibis.desc("idx"),
                    )
                )
            )
            .filter(ibis._["rank"] == 0)
            .drop("rank")
        )

        # order
        t = t.order_by(ibis.desc("idx"))

        # return the data
        return t

    def messages_t(self, id: str = None, bot_id: str = None):
        # get messages data
        t = self.get_rcon().table(self.messages_table_name)

        # filter
        if id:
            t = t.filter(ibis._["id"] == id)
        if bot_id:
            t = t.filter(ibis._["bot_id"] == bot_id)

        # order
        t = t.order_by(ibis.asc("idx"))

        # return the data
        return t

    # contains
    def contains_bot(self, id: str = None, name: str = None) -> bool:
        t = self.bots_t(id=id, name=name)
        return t.count().to_pyarrow().as_py() > 0

    def contains_message(self, id: str = None, bot_id: str = None) -> bool:
        t = self.messages_t(id=id, bot_id=bot_id)
        return t.count().to_pyarrow().as_py() > 0

    # get record(s)
    def get_bot(self, id: str = None, name: str = None):
        t = self.bots_t(id=id, name=name)

        if id:
            return t.to_pyarrow().to_pylist()[0]
        else:
            return t.to_pyarrow().to_pylist()

    def get_message(self, id: str = None, bot_id: str = None):
        t = self.messages_t(id=id, bot_id=bot_id)

        if id:
            record = t.to_pyarrow().to_pylist()[0]
            record["data"] = self.bytes_to_messages(record["data"])
        else:
            records = t.to_pyarrow().to_pylist()
            for record in records:
                record["data"] = self.bytes_to_messages(record["data"])
            return records

    # goofy, but this gets the Pydantic AI messages instead of an Ibis table of message data
    def get_messages(self, bot_id: str):
        messages = self.get_message(bot_id=bot_id)
        return [message for record in messages for message in record["data"]]

    # append records
    def append_bot(
        self,
        id: str,
        name: str,
        model: str,
        system_prompt: str,
        tools: str,
        result_type: str,
    ):
        record = {
            "idx": [now()],
            "id": [id],
            "name": [name],
            "model": [model],
            "system_prompt": [system_prompt],
            "tools": [tools],
            "result_type": [result_type],
        }
        self.get_wcon().insert(self.bots_table_name, record)

        return self.get_bot(name=name)

    def append_message(
        self,
        bot_id: str,
        data: bytes,
    ):
        id = generate_uuid()
        record = {
            "idx": [now()],
            "id": [id],
            "bot_id": [bot_id],
            "data": [data],
        }
        self.get_wcon().insert(self.messages_table_name, record)

        return self.get_message(id=id, bot_id=bot_id)

    # convert bytes to Pydantic AI messages
    @classmethod
    def bytes_to_messages(cls, data: bytes) -> list:
        return ModelMessagesTypeAdapter.validate_json(data)
