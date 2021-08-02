import unittest

from epjson_transition.logger import SimpleLogger
from epjson_transition.rules.Transition95to96 import EnergyPlus9596


class TestEPlus9596Rule(unittest.TestCase):
    def setUp(self) -> None:
        self.muted_logger = SimpleLogger(console=False)

    def test_worker_functions(self):
        t = EnergyPlus9596()
        self.assertIsInstance(t.message(), str)
        self.assertIsInstance(t.old_version(), float)
        self.assertIsInstance(t.new_version(), float)
        self.assertIsInstance(t.variable_map(), dict)

    def test_transform(self):
        file_contents = {
            "AirLoopHVAC:OutdoorAirSystem": {
                "OA Sys 1": {
                    "availability_manager_list_name": "Outdoor Air 1 Avail List",
                    "controller_list_name": "OA Sys 1 Controllers",
                    "outdoor_air_equipment_list_name": "OA Sys 1 Equipment"
                }
            }
        }
        t = EnergyPlus9596()
        updated_contents = t.transform(file_contents, self.muted_logger)
        expected_contents = {
            "AirLoopHVAC:OutdoorAirSystem": {
                "OA Sys 1": {
                    "controller_list_name": "OA Sys 1 Controllers",
                    "outdoor_air_equipment_list_name": "OA Sys 1 Equipment"
                }
            }
        }
        self.assertDictEqual(expected_contents, updated_contents)
