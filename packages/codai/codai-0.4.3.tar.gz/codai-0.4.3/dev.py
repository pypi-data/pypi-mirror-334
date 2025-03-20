# ruff: noqa
# imports
import json
import codai

from rich import print
from pydantic_ai.models import KnownModelName

from codai import hci
from codai.bot import *
from codai.repl import *
from codai.utils import *

from codai.flows.batch_edit import *

from codai.bots.codai import bot
from codai.bots.refactor import *

# all models
all_models = list(KnownModelName.__args__)

# config
ibis.options.interactive = True
ibis.options.repr.interactive.max_rows = 40
ibis.options.repr.interactive.max_depth = 8
ibis.options.repr.interactive.max_columns = None

# load secrets (redundant; see src/codai/__init__.py)
load_codai_dotenv()
