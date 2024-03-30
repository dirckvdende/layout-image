
from importlib import resources
import tomli
from .layoutimg import LayoutImage

__version__ = "1.0.0"

CONFIG = tomli.loads(resources.read_text("layoutimg", "config.toml"))