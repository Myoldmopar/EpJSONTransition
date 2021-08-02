from copy import deepcopy
from typing import Dict

from epjson_transition.logger import SimpleLogger
from epjson_transition.rules.base import EpJSONTransitionRuleBase


class EnergyPlus9596(EpJSONTransitionRuleBase):

    def message(self):
        return "Converting EpJSON 9.5 to 9.6"

    def old_version(self) -> float:
        return 9.5

    def new_version(self) -> float:
        return 9.6

    def transform(self, file_contents: Dict, logger: SimpleLogger) -> Dict:
        logger.print("Transitioning File Now")
        modified_contents = deepcopy(file_contents)
        modified_contents["Foo"] = "Bar"
        return modified_contents

    def variable_map(self):
        """
        Output variable replacements, map each input output variable name to a new name for direct replacement,
        or map it to None to delete it, or map it to an array if it should spawn multiple.
        :return:
        """
        return {'Site Outdoor Air Drybulb Temperature': 'Fake Outdoor DB Temp'}
