from json import dumps, load as load_json
from pathlib import Path
from tempfile import mkstemp
import unittest

from epjson_transition.exceptions import MissingEpJSONFile
from epjson_transition.logger import SimpleLogger
from epjson_transition.transition import EpJSONTransition


class TestTransition(unittest.TestCase):

    def setUp(self) -> None:
        self.resource_dir = Path(__file__).parent.resolve() / 'resources'
        _, out_file_path = mkstemp()
        self.output_file = Path(out_file_path)
        _, epjson_file = mkstemp()
        self.epjson_file_path = Path(epjson_file)
        self.muted_logger = SimpleLogger(console=False)

    def test_missing_input_file(self):
        missing_input_path = Path('missing_input_file_here')
        with self.assertRaises(MissingEpJSONFile):
            EpJSONTransition(missing_input_path, self.output_file)

    def test_transform_interface(self):
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
        EpJSONTransition(self.epjson_file_path, self.output_file).transform(self.muted_logger)
        # not much to assert here, it should just work -- more testing in the transform function tests
        with self.output_file.open() as f:
            data = load_json(f)
            self.assertEqual(data['Version']['Version 1']['version_identifier'], "9.6")
