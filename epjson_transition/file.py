from json.decoder import JSONDecodeError
from json import dumps, loads
from pathlib import Path

from epjson_transition.exceptions import MissingEpJSONVersion, MalformedEpJSONFile
from epjson_transition.logger import SimpleLogger
from epjson_transition.version import EpJSONVersion, KnownVersions
from epjson_transition.rules.common import OutputVariable, Version
from epjson_transition.rules.Transition95to96 import EnergyPlus9596


class EpJSONFile:
    def __init__(self, path_to_input_file: Path, path_to_output_file: Path, logger: SimpleLogger):
        """

        :param path_to_input_file: pathlib.Path instance, existence already verified
        :param path_to_output_file:
        :param logger:
        """
        # allow a read_text call to raise whatever exceptions it wants
        self.file_contents = path_to_input_file.read_text(encoding='utf-8', errors='ignore')
        logger.print(f"EpJSON contents loaded; file length = {len(self.file_contents)} characters")
        try:
            self.original_data = loads(self.file_contents)
        except JSONDecodeError:
            raise MalformedEpJSONFile("Could not read in EpJSON file, are contents actually JSON?")
        logger.print(f"EpJSON contents interpreted into dictionary; contains {len(self.original_data.keys())} keys")
        if 'Version' not in self.original_data:
            raise MissingEpJSONVersion()
        self.original_version = EpJSONVersion(self.original_data['Version'])
        original_version_key = self.original_version.known_version
        self.output_file_path = path_to_output_file
        logger.print(
            f"EpJSON version found, sanitized version string = {KnownVersions.VersionStrings[original_version_key]}"
        )
        logger.print("File interpretation complete")

    def transform(self, logger: SimpleLogger):
        logger.print("EpJSON Content Transition Beginning")
        transition_instance = EnergyPlus9596()  # TODO: Remove and make the IF block exhaustive or fatal
        if self.original_version.known_version == KnownVersions.Version95:
            transition_instance = EnergyPlus9596()
        else:
            ...

        # initialize the transitioned data dictionary
        transitioned_data = self.original_data

        logger.print("First Transition the Version Object")
        logger.add_prefix()
        transitioned_data = Version.transform(transitioned_data, logger)
        logger.remove_prefix()

        logger.print("Next Transitioning Any Output Variables and Related Objects and Fields")
        logger.add_prefix()
        transitioned_data = OutputVariable(transition_instance.variable_map()).transform(transitioned_data, logger)
        logger.remove_prefix()

        logger.print("Now Calling Main Transition Routine for this Version")
        logger.add_prefix()
        transitioned_data = transition_instance.transform(transitioned_data, logger)
        logger.remove_prefix()
        logger.print(f"Writing Updated Output File at {self.output_file_path} (pretend)")
        with self.output_file_path.open('w') as f:
            f.write(dumps(transitioned_data, indent=2))
        logger.print("File Transformation Complete")
