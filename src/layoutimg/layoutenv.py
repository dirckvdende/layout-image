
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

    def __iter__(self):
        """ Iterator over environment variables """
        yield from self._vars

    def __contains__(self, name: str):
        return name in self._vars

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
                "background-color": "none",
                "background-image": "none",
                "flow": "none",
                "font": "default",
                "font-size": "64",
                "height": "auto",
                "max-height": "1000000",
                "max-width": "1000000",
                "min-height": "0",
                "min-width": "0",
                "render-text": "false",
                "text-align": "left",
                "text-color": "black",
                "width": "auto",
                "x": "auto",
                "y": "auto",
            },
            "row": {
                "background-color": "none",
                "background-image": "none",
                "flow": "y",
                "font": "inherit",
                "font-size": "inherit",
                "height": "auto",
                "max-height": "1000000",
                "max-width": "1000000",
                "min-height": "0",
                "min-width": "100%",
                "render-text": "false",
                "text-align": "inherit",
                "text-color": "inherit",
                "width": "auto",
                "x": "auto",
                "y": "auto",
            },
            "col": {
                "background-color": "none",
                "background-image": "none",
                "flow": "x",
                "font": "inherit",
                "font-size": "inherit",
                "height": "auto",
                "max-height": "1000000",
                "max-width": "1000000",
                "min-height": "100%",
                "min-width": "0",
                "render-text": "false",
                "text-align": "inherit",
                "text-color": "inherit",
                "width": "auto",
                "x": "auto",
                "y": "auto",
            },
            "text": {
                "background-color": "none",
                "background-image": "none",
                "flow": "xy",
                "font": "inherit",
                "font-size": "inherit",
                "height": "auto",
                "max-height": "1000000",
                "max-width": "1000000",
                "min-height": "0",
                "min-width": "100%",
                "render-text": "true",
                "text-align": "inherit",
                "text-color": "inherit",
                "width": "auto",
                "x": "auto",
                "y": "auto",
            }
        }
        if tag not in values:
            raise ValueError(f"Tag {tag} is not allowed")
        return values[tag]
