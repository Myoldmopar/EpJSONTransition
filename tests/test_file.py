import pathlib
import unittest

from epjson_transition.exceptions import MissingEpJSONVersion, BadEpJSONVersion
from epjson_transition.version import KnownVersions
from epjson_transition.file import EpJSONFile


class TestFileObject(unittest.TestCase):

    def setUp(self) -> None:
        self.resource_dir = pathlib.Path(__file__).parent.resolve() / 'resources'

    def test_works_on_minimal_file(self):
        valid_epjson = self.resource_dir / 'minimal_valid_epjson_file.epJSON'
        f = EpJSONFile(valid_epjson)
        self.assertEqual(f.version.known_version, KnownVersions.Version96)

    def test_catches_empty_file(self):
        empty_epjson = self.resource_dir / 'empty_epjson_file.epJSON'
        with self.assertRaises(MissingEpJSONVersion):
            EpJSONFile(empty_epjson)

    def test_catches_bad_version(self):
        broken_epjson = self.resource_dir / 'minimal_epjson_file_bad_version.epJSON'
        with self.assertRaises(BadEpJSONVersion):
            EpJSONFile(broken_epjson)
