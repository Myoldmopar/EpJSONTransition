# Contains class(es) that can be reused by each version's transition class
# These can contain things that are generally common to every version, though they could change occasionally

from copy import deepcopy
from typing import Dict

from epjson_transition.logger import SimpleLogger
from epjson_transition.version import KnownVersions


class OutputVariable:
    def __init__(self, output_variable_changes_this_version: Dict):
        self.output_variable_map = output_variable_changes_this_version

    def _upper_case_variable_map(self):
        new_variable_map = {}
        for k, v in self.output_variable_map.items():
            new_variable_map[k.upper()] = v
        return new_variable_map

    def transform(self, file_contents: Dict, logger: SimpleLogger) -> Dict:
        logger.print("Processing Output Variable Changes")
        if 'Output:Variable' not in file_contents:
            return file_contents
        output_variables = file_contents['Output:Variable']
        upper_case_variable_map = self._upper_case_variable_map()
        modified_content = deepcopy(file_contents)
        # replace the output variable name
        for name, ov in output_variables.items():
            ov_original = ov['variable_name']
            ov_original_upper = ov_original.upper()
            if ov_original_upper in upper_case_variable_map:
                ov_new = upper_case_variable_map[ov_original.upper()]
                if ov_new is None:
                    logger.print(f"Found output variable to delete: {ov_original}")
                    del modified_content['Output:Variable'][name]
                elif isinstance(ov_new, list):
                    logger.print(f"Found output variable to replace, spawning {len(ov_new)} new variables")
                    for i, ov_new_item in enumerate(ov_new):
                        item_to_copy = deepcopy(modified_content['Output:Variable'][name])
                        item_to_copy['variable_name'] = ov_new_item
                        modified_content['Output:Variable'][f"{ov_original}_{i+1}"] = item_to_copy
                    # now delete the parent
                    del modified_content['Output:Variable'][name]
                else:
                    logger.print(f"Found output variable to replace, going from {ov_original} to {ov_new}")
                    modified_content['Output:Variable'][name]['variable_name'] = ov_new
        return modified_content


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
