
from importlib import resources
import tomli

__version__ = "1.0.0"

config = tomli.loads(resources.read_text("layoutimg", "config.toml"))
DISPLAY_TEXT = config["main"]["display_text"]