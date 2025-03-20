class Config:
    def __init__(self) -> None:
        self._settings_file_pattern = r"settings__(.+)\.xml"

    @property
    def settings_file_pattern(self) -> str:
        return self._settings_file_pattern
