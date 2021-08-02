from json import dumps
import io
from platform import system
import sys
from tempfile import mkstemp
import unittest

from epjson_transition.main import main


class TestMainEntryPoint(unittest.TestCase):

    def setUp(self) -> None:
        # mute stdout to avoid usage statement, but not on Windows
        if system() != 'Windows':
            suppress_text = io.StringIO()
            sys.stdout = suppress_text

    def tearDown(self) -> None:
        # reset stdout here
        if system() != 'Windows':
            sys.stdout = sys.__stdout__

    def test_main_function_not_enough_args(self):
        sys.argv = ['ScriptName', 'Not Enough']
        self.assertEqual(1, main())

    def test_main_successful_transition(self):
        _, epjson_file = mkstemp()
        _, out_file_path = mkstemp()
        _, err_file_path = mkstemp()
        with open(epjson_file, 'w') as f:
            f.write(dumps(
                {
                    "Version": {
                        "Version 1": {
                            "version_identifier": "9.5"
                        }
                    }
                }
            ))
        sys.argv = ['script name', epjson_file, out_file_path, err_file_path]
        self.assertEqual(0, main())

    def test_main_blank_input_file(self):
        _, epjson_file = mkstemp()
        _, out_file_path = mkstemp()
        _, err_file_path = mkstemp()
        sys.argv = ['script name', epjson_file, out_file_path, err_file_path]
        self.assertEqual(1, main())

    # def setUp(self) -> None:
    #     self.resource_dir = Path(__file__).parent.resolve() / 'resources'
    #     _, out_file_path = mkstemp()
    #     self.output_file = Path(out_file_path)
    #     _, epjson_file = mkstemp()
    #     self.epjson_file_path = Path(epjson_file)
    #     self.muted_logger = SimpleLogger(console=False)
    #
    # def test_missing_input_file(self):
    #     missing_input_path = Path('missing_input_file_here')
    #     with self.assertRaises(MissingEpJSONFile):
    #         EpJSONTransition(missing_input_path, self.output_file)
    #
    # def test_transform_interface(self):
    #     with self.epjson_file_path.open('w') as f:
    #         f.write(dumps(
    #             {
    #                 "Version": {
    #                     "Version 1": {
    #                         "version_identifier": "9.5"
    #                     }
    #                 }
    #             }
    #         ))
    #     EpJSONTransition(self.epjson_file_path, self.output_file).transform(self.muted_logger)
    #     # not much to assert here, it should just work -- more testing in the transform function tests
    #     with self.output_file.open() as f:
    #         data = load_json(f)
    #         self.assertEqual(data['Version']['Version 1']['version_identifier'], "9.6")
