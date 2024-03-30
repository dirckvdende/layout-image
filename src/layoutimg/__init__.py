
from importlib import resources
import tomli
from . import arith

__version__ = "1.0.0"

CONFIG = tomli.loads(resources.read_text("layoutimg", "config.toml"))