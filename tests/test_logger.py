from tempfile import mkstemp
import unittest

from epjson_transition.logger import SimpleLogger


class TestLoggerOperations(unittest.TestCase):

    def setUp(self) -> None:
        _, self.log_file_path = mkstemp()

    def test_construction(self):
        # default mode would report to console but no error file
        s = SimpleLogger()
        s.close()
        # muted mode will not report anything to console or error file
        s = SimpleLogger(console=False)
        s.close()
        # error file mode will not report to console...only error file
        s = SimpleLogger(console=False, log_file_path=self.log_file_path)
        s.close()  # close if you are running output file mode
        # verbose mode will report to both the console and the error file
        s = SimpleLogger(console=True, log_file_path=self.log_file_path)
        s.close()  # close if you are running output file mode

    def test_output(self):
        # we will use error file mode only so we don't muddy up standard output during testing
        log = SimpleLogger(console=False, log_file_path=self.log_file_path)
        log.print("It")
        log.add_prefix()
        log.print("Was")
        log.remove_prefix()
        log.print("The")
        log.add_prefix()
        log.print("Best")
        log.add_prefix()
        log.print("Of")
        log.remove_prefix()
        log.remove_prefix()
        log.print("Times")
        expected_match = [
            ": It",
            ":  Was",
            ": The",
            ":  Best",
            ":   Of",
            ": Times"
        ]
        log.close()
        with open(self.log_file_path, 'r') as f:
            lines = f.readlines()
            self.assertEqual(6, len(lines))
            for i, line in enumerate(lines):
                self.assertIn(expected_match[i], line)
