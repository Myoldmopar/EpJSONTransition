from json import dumps, load as load_json
from pathlib import Path
from tempfile import mkstemp
import unittest

from epjson_transition.exceptions import MissingEpJSONVersion, BadEpJSONVersion, MalformedEpJSONFile
from epjson_transition.logger import SimpleLogger
from epjson_transition.version import KnownVersions
from epjson_transition.file import EpJSONFile


class TestFileObject(unittest.TestCase):

    def setUp(self) -> None:
        self.resource_dir = Path(__file__).parent.resolve() / 'resources'
        _, epjson_file = mkstemp()
        self.epjson_file_path = Path(epjson_file)
        _, out_file_path = mkstemp()
        self.output_file = Path(out_file_path)
        self.muted_logger = SimpleLogger(console=False)

    def test_works_on_minimal_file(self):
        with self.epjson_file_path.open('w') as f:
            f.write(dumps(
                {
                    "Version": {
                        "Version 1": {
                            "version_identifier": "9.6"
                        }
                    }
                }
            ))
        f = EpJSONFile(self.epjson_file_path, self.output_file, self.muted_logger)
        self.assertEqual(f.original_version.known_version, KnownVersions.Version96)

    def test_catches_empty_file(self):
        with self.epjson_file_path.open('w') as f:
            f.write(dumps({}))
        with self.assertRaises(MissingEpJSONVersion):
            EpJSONFile(self.epjson_file_path, self.output_file, self.muted_logger)

    def test_catches_non_json_file(self):
        with self.epjson_file_path.open('w') as f:
            f.write("Hello, world!")
        with self.assertRaises(MalformedEpJSONFile):
            EpJSONFile(self.epjson_file_path, self.output_file, self.muted_logger)

    def test_catches_bad_version(self):
        with self.epjson_file_path.open('w') as f:
            f.write(dumps(
                {
                    "Version": {
                        "Version 1": {
                            "version_identifier": "9"
                        }
                    }
                }
            ))
        with self.assertRaises(BadEpJSONVersion):
            EpJSONFile(self.epjson_file_path, self.output_file, self.muted_logger)

    def test_transform_95(self):
        with self.epjson_file_path.open('w') as f:
            f.write(dumps(
                {
                    "Version": {
                        "Version 1": {
                            "version_identifier": "9.5"
                        }
                    }
                }
            ))
        f = EpJSONFile(self.epjson_file_path, self.output_file, self.muted_logger)
        self.assertEqual(f.original_version.known_version, KnownVersions.Version95)
        f.transform(self.muted_logger)
        with self.output_file.open() as f:
            data = load_json(f)
            self.assertEqual(data['Version']['Version 1']['version_identifier'], "9.6")
