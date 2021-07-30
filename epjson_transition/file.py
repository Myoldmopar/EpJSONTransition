from json import loads
from pathlib import Path

from epjson_transition.exceptions import MissingEpJSONVersion
from epjson_transition.version import EpJSONVersion


class EpJSONFile:
    def __init__(self, path_to_file: Path):
        self.path = path_to_file
        self.file_contents = self.path.read_text(encoding='utf-8', errors='ignore')
        self.data = loads(self.file_contents)
        if 'Version' not in self.data:
            raise MissingEpJSONVersion()
        self.version = EpJSONVersion(self.data['Version'])
