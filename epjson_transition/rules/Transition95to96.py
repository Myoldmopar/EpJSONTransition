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
        file_contents["Foo"] = "Bar"
        return file_contents

    def variable_map(self):
        return {'Site Outdoor Air Drybulb Temperature': 'Fake Outdoor DB Temp'}
