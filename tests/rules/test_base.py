import unittest

from epjson_transition.rules.base import EpJSONTransitionRuleBase


class TestAbstractBaseRule(unittest.TestCase):
    def test_abstract_interface(self):
        r = EpJSONTransitionRuleBase()
        with self.assertRaises(NotImplementedError):
            r.transform("dummy")


