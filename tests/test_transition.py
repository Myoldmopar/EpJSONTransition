import pathlib
import unittest

from epjson_transition.transition import EpJSONTransition
from epjson_transition.version import KnownVersions


class TestTransition(unittest.TestCase):

    def setUp(self) -> None:
        self.resource_dir = pathlib.Path(__file__).parent.resolve() / 'resources'

    def test_construction(self):
        valid_epjson = self.resource_dir / 'full_epjson_file.epJSON'
        t = EpJSONTransition(valid_epjson)
        self.assertEqual(t.original_version, KnownVersions.Version96)
