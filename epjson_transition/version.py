from typing import Dict

from epjson_transition.exceptions import BadEpJSONVersion


class KnownVersions:
    Invalid = -1
    Version95 = 0
    Version96 = 1
    Version2022Point1 = 2

    VersionMap = {
        '9.5': Version95,
        '9.6': Version96,
        '2022.1': Version2022Point1,
    }

    VersionStrings = {
        Version95: '9.5',
        Version96: '9.6',
        Version2022Point1: '2022.1'
    }

    NextVersion = {
        Version95: Version96,
        Version96: Version2022Point1,
        Version2022Point1: Invalid
    }

    @staticmethod
    def version_enum_from_string(version_string: str) -> int:
        version_string = str(version_string)  # just in case the version gets processed into a numeric value
        version_tokens = version_string.split('.')
        if len(version_tokens) < 2:
            raise BadEpJSONVersion(version_string)
        major_minor = f"{version_tokens[0]}.{version_tokens[1]}"
        if major_minor in KnownVersions.VersionMap:
            return KnownVersions.VersionMap[major_minor]
        return KnownVersions.Invalid


# Captures the interpretation of the Version object in the EpJSON inputs
#     "Version": {
#         "Version 1": {
#             "version_identifier": "9.6"
#         }
#     },

class EpJSONVersion:
    def __init__(self, epjson_version_object: Dict):
        # the version object should have one single key, "Version 1", since it is an unnamed unique object
        # need to add protection for this
        sub_object = epjson_version_object["Version 1"]
        version_id = sub_object["version_identifier"]
        self.known_version = KnownVersions.version_enum_from_string(version_id)
