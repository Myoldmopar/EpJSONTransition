import unittest

from epjson_transition.logger import SimpleLogger
from epjson_transition.rules.Transition95to96 import EnergyPlus9596


class TestEPlus9596Rule(unittest.TestCase):
    def setUp(self) -> None:
        self.muted_logger = SimpleLogger(console=False)

    def test_worker_functions(self):
        t = EnergyPlus9596()
        self.assertIsInstance(t.message(), str)
        self.assertIsInstance(t.old_version(), float)
        self.assertIsInstance(t.new_version(), float)
        self.assertIsInstance(t.variable_map(), dict)

    def test_transform(self):
        file_contents = {
            "Hello": "World"
        }
        t = EnergyPlus9596()
        updated_contents = t.transform(file_contents, self.muted_logger)
        expected_contents = {'Hello': 'World', 'Foo': 'Bar'}
        self.assertDictEqual(expected_contents, updated_contents)
