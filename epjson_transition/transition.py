from pathlib import Path

from epjson_transition.file import EpJSONFile


class EpJSONTransition:
    # main class for transitioning an EpJSON file
    def __init__(self, file_object: Path):
        if not file_object.exists():
            ...  # fatal
        self.file = EpJSONFile(file_object)
        self.original_version = self.file.version.known_version
