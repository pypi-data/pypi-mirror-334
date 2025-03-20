import os


class Maven:
    def __init__(self) -> None:
        self._m2_home = (
            os.environ["M2_HOME"]
            if "M2_HOME" in os.environ
            else os.path.expanduser("~/.m2")
        )
        self._maven_settings = f"{self._m2_home}/settings.xml"

    @property
    def m2_home(self) -> str:
        return self._m2_home

    @property
    def maven_settings(self) -> str:
        return self._maven_settings
