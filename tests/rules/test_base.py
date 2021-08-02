import unittest

from epjson_transition.logger import SimpleLogger
from epjson_transition.rules.base import EpJSONTransitionRuleBase


class TestAbstractBaseRule(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = SimpleLogger()

    def test_abstract_interface(self):
        r = EpJSONTransitionRuleBase()
        with self.assertRaises(NotImplementedError):
            r.message()
        with self.assertRaises(NotImplementedError):
            r.old_version()
        with self.assertRaises(NotImplementedError):
            r.new_version()
        with self.assertRaises(NotImplementedError):
            r.transform("dummy", self.logger)
        with self.assertRaises(NotImplementedError):
            r.variable_map()
