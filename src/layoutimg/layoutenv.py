
from typing import Any

class LayoutEnv:
    """ An environment which keeps track of  """

    def __init__(self):
        """ Constructor """
        # Environment variables
        self._vars: 'dict[str, str]' = {}

    def set_defauts(self, tag: str):
        """ Set this environment to the default values for a specific tag """
        self._vars = self._get_defaults(tag)
    
    def __getitem__(self, name: str):
        """ Get an environment variable """
        return self._vars[name]
    
    def __setitem__(self, name: str, value: str):
        """ Set an environment variable """
        self._vars[name] = value

    __getattr__ = __getitem__
    __setattr__ = __setitem__

    def __iter__(self):
        """ Iterator over environment variables """
        yield from self._vars

    def inherit(self, parent_env: 'LayoutEnv'):
        """ Process environment inheritence by replacing all "inherit" values in
            the current environment with ones from the given parent environment
            """
        for name in filter(lambda n: self._vars[n] == "inherit", self._vars):
            assert parent_env[name] != "inherit"
            self._vars[name] = parent_env[name]

    def _get_defaults(self, tag: str):
        """ Get the default environment variable values for a specific tag """
        values = {
            "image": {
                "continue": "none",
                "width": "auto",
                "height": "auto",
                "text-color": "black",
                "background-color": "none",
                "font": "default",
                "render-text": "false",
            },
            "row": {
                "continue": "y",
                "width": "auto",
                "height": "auto",
                "text-color": "inherit",
                "background-color": "none",
                "font": "inherit",
                "render-text": "false",
            },
            "col": {
                "continue": "x",
                "width": "auto",
                "height": "auto",
                "text-color": "inherit",
                "background-color": "none",
                "font": "inherit",
                "render-text": "false",
            },
            "text": {
                "continue": "xy",
                "width": "auto",
                "height": "auto",
                "text-color": "inherit",
                "background-color": "none",
                "font": "inherit",
                "render-text": "true",
            }
        }
        if tag not in values:
            raise ValueError(f"Tag {tag} is not allowed")
        return values[tag]
