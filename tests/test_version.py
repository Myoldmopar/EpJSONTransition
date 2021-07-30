import unittest

from epjson_transition.exceptions import BadEpJSONVersion
from epjson_transition.version import EpJSONVersion, KnownVersions


class TestKnownVersions(unittest.TestCase):
    def test_95_versions(self):
        version_95_keys = ['9.5', '9.5.0']
        for v in version_95_keys:
            identified_version = KnownVersions.version_enum_from_string(v)
            self.assertEqual(identified_version, KnownVersions.Version95)

    def test_96_versions(self):
        version_96_keys = ['9.6', '9.6.0']
        for v in version_96_keys:
            identified_version = KnownVersions.version_enum_from_string(v)
            self.assertEqual(identified_version, KnownVersions.Version96)

    def test_2022_1_versions(self):
        version_22_1_keys = ['2022.1', '2022.1.0']
        for v in version_22_1_keys:
            identified_version = KnownVersions.version_enum_from_string(v)
            self.assertEqual(identified_version, KnownVersions.Version2022Point1)

    def test_next_expected_version(self):
        # will need to be updated each new version
        version_22_2_keys = ['2022.2', '2022.2.0']
        for v in version_22_2_keys:
            identified_version = KnownVersions.version_enum_from_string(v)
            self.assertEqual(identified_version, KnownVersions.Invalid)

    def test_unknown_versions(self):
        invalid_versions = ['9.4', 'q.2', 'Foo.Bar']
        for v in invalid_versions:
            identified_version = KnownVersions.version_enum_from_string(v)
            self.assertEqual(identified_version, KnownVersions.Invalid)

    def test_invalid_form(self):
        bad_form_versions = ['apple', '9', '2022']
        for v in bad_form_versions:
            with self.assertRaises(BadEpJSONVersion):
                KnownVersions.version_enum_from_string(v)


class TestVersionProcessing(unittest.TestCase):
    def test_good_version(self):
        proper_ep_json_with_version = {
            'Version': {
                'Version 1': {
                    'version_identifier': '9.5'
                }
            }
        }
        e = EpJSONVersion(proper_ep_json_with_version['Version'])
        self.assertEqual(e.known_version, KnownVersions.Version95)
