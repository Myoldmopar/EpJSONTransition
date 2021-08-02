class EpJSONTransitionError(Exception):
    """
    Catch-all for EpJSON exceptions
    """
    ...


class MissingEpJSONFile(EpJSONTransitionError):
    ...


class MalformedEpJSONFile(EpJSONTransitionError):
    ...


class BadEpJSONVersion(EpJSONTransitionError):
    def __init__(self, entered_version: str):
        super().__init__()
        self.found_version = entered_version

    def to_string(self) -> str:
        return f"Found an invalid version in the EpJSON file: \"{self.found_version}\""


class MissingEpJSONVersion(EpJSONTransitionError):
    @staticmethod
    def to_string() -> str:
        return "Version missing from EpJSON file, root object must have a \"Version\" key"
