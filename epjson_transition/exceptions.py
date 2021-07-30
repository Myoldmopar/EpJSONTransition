# TODO: Add MalformedEpJSON to catch bad version objects, or whatever

class BadEpJSONVersion(Exception):
    def __init__(self, entered_version: str):
        super().__init__()
        self.found_version = entered_version

    def to_string(self) -> str:
        return f"Found an invalid version in the EpJSON file: \"{self.found_version}\""


class MissingEpJSONVersion(Exception):
    @staticmethod
    def to_string() -> str:
        return "Version missing from EpJSON file, root object must have a \"Version\" key"
