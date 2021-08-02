# Contains class(es) that can be reused by each version's transition class
# These can contain things that are generally common to every version, though they could change occasionally

from copy import deepcopy
from typing import Dict

from epjson_transition.logger import SimpleLogger
from epjson_transition.version import KnownVersions


class OutputVariable:
    def __init__(self, output_variable_changes_this_version: Dict):
        self.output_variable_map = output_variable_changes_this_version
        self.modified_content = None
        self.upper_case_variable_map = None

    def _upper_case_variable_map(self):
        new_variable_map = {}
        for k, v in self.output_variable_map.items():
            new_variable_map[k.upper()] = v
        return new_variable_map

    def replace_one_variable_type(self, file_contents: Dict, object_name: str, field_key: str, logger: SimpleLogger):
        if object_name in file_contents:
            objects = file_contents[object_name]
            # replace the output variable name
            for name, input_object in objects.items():
                ov_original = input_object[field_key]
                ov_original_upper = ov_original.upper()
                if ov_original_upper in self.upper_case_variable_map:
                    ov_new = self.upper_case_variable_map[ov_original.upper()]
                    if ov_new is None:
                        logger.print(f"Found {object_name} to delete: {ov_original}")
                        del self.modified_content[object_name][name]
                    elif isinstance(ov_new, list):
                        logger.print(f"Found {object_name} to replace, spawning {len(ov_new)} new {object_name}'s")
                        for i, ov_new_item in enumerate(ov_new):
                            item_to_copy = deepcopy(self.modified_content[object_name][name])
                            item_to_copy[field_key] = ov_new_item
                            self.modified_content[object_name][f"{ov_original}_{i + 1}"] = item_to_copy
                        # now delete the parent
                        del self.modified_content[object_name][name]
                    else:
                        logger.print(f"Found {object_name} to replace, going from {ov_original} to {ov_new}")
                        self.modified_content[object_name][name][field_key] = ov_new

    def transform(self, file_contents: Dict, logger: SimpleLogger) -> Dict:
        logger.print("Processing Output Variable Changes")
        self.modified_content = deepcopy(file_contents)
        self.upper_case_variable_map = self._upper_case_variable_map()
        object_name = 'Output:Variable'
        field_key = 'variable_name'
        self.replace_one_variable_type(file_contents, object_name, field_key, logger)
        object_name = 'EnergyManagementSystem:Sensor'
        field_key = 'output_variable_or_output_meter_name'
        self.replace_one_variable_type(file_contents, object_name, field_key, logger)
        object_name = 'Output:Meter'
        field_key = 'key_name'
        self.replace_one_variable_type(file_contents, object_name, field_key, logger)
        object_name = 'Output:Meter:MeterFileOnly'
        field_key = 'key_name'
        self.replace_one_variable_type(file_contents, object_name, field_key, logger)
        object_name = 'Output:Meter:Cumulative'
        field_key = 'key_name'
        self.replace_one_variable_type(file_contents, object_name, field_key, logger)
        object_name = 'Output:Meter:Cumulative:MeterFileOnly'
        field_key = 'key_name'
        self.replace_one_variable_type(file_contents, object_name, field_key, logger)

        return self.modified_content


class Version:

    @staticmethod
    def transform(file_contents: Dict, logger: SimpleLogger) -> Dict:
        logger.print("Processing Version Number Change")
        epjson_version_object = file_contents['Version']
        sub_object = epjson_version_object["Version 1"]
        version_id = sub_object["version_identifier"]
        original_version = KnownVersions.version_enum_from_string(version_id)
        # TODO: Validate original version
        new_version = KnownVersions.NextVersion[original_version]
        new_version_string = KnownVersions.VersionStrings[new_version]
        file_contents['Version']['Version 1']['version_identifier'] = new_version_string
        return file_contents
