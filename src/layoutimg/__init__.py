
from importlib import resources as _resources
import tomli as _tomli

from .layoutimg import LayoutImage

__version__ = "0.2.0"

CONFIG = _tomli.loads(_resources.read_text("layoutimg", "config.toml"))