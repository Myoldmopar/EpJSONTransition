import unittest

from epjson_transition.exceptions import BadEpJSONVersion, MissingEpJSONVersion


class TestMissingException(unittest.TestCase):
    def test_missing_version_signature(self):
        with self.assertRaises(MissingEpJSONVersion):
            raise MissingEpJSONVersion()

    def test_missing_version_to_string_works(self):
        e = MissingEpJSONVersion()
        self.assertIsInstance(e.to_string(), str)


class TestBadException(unittest.TestCase):
    def test_bad_version_signature(self):
        with self.assertRaises(BadEpJSONVersion):
            raise BadEpJSONVersion("9.q.2")

    def test_bad_version_to_string_works(self):
        e = BadEpJSONVersion("9.3.xz")
        self.assertIsInstance(e.to_string(), str)
