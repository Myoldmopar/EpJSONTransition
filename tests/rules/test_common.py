import unittest

from epjson_transition.logger import SimpleLogger
from epjson_transition.rules.common import OutputVariable


class TestOutputVariableRule(unittest.TestCase):
    def setUp(self) -> None:
        self.muted_logger = SimpleLogger(console=False)

    def test_upper_case_process(self):
        ov = OutputVariable({'foo': 'bar', 'HELLO': 'WORLD', 'Nick': 'EDWIN'})
        upper_case = ov._upper_case_variable_map()
        self.assertEqual(3, len(upper_case))
        expected_dict = {'FOO': 'bar', 'HELLO': 'WORLD', 'NICK': 'EDWIN'}
        self.assertDictEqual(expected_dict, upper_case)

    def test_transform_no_outputs(self):
        file_contents = {'Foo': 'Bar'}
        ov = OutputVariable({})
        updated_contents = ov.transform(file_contents, self.muted_logger)
        self.assertDictEqual(file_contents, updated_contents)

    def test_transform_some_outputs(self):
        file_contents = {
            'Output:Variable': {
                'Output:Variable 1': {
                    "key_value": "*",
                    "reporting_frequency": "Hourly",
                    "variable_name": "Site Outdoor Air Drybulb Temperature"
                },
                'Output:Variable 2': {
                    "key_value": "*",
                    "reporting_frequency": "Hourly",
                    "variable_name": "Boiler Inlet Temperature"
                },
                'Output:Variable 3': {
                    "key_value": "Plant Loop 1",
                    "reporting_frequency": "Daily",
                    "variable_name": "Plant Supply Side Unmet Demand Rate"
                },
                'Output:Variable 4': {
                    "key_value": "Zone 1",
                    "reporting_frequency": "Hourly",
                    "variable_name": "Zone Mean Air Temperature"
                }
            }
        }
        ov = OutputVariable({
            "Site Outdoor Air Drybulb Temperature": "New Outdoor TEMP",
            "Plant Supply Side Unmet Demand Rate": "ALL UPPER CASE FOR FUN"
        })
        updated_contents = ov.transform(file_contents, self.muted_logger)
        expected_outputs = file_contents
        expected_outputs['Output:Variable']['Output:Variable 1']['variable_name'] = "New Outdoor TEMP"
        expected_outputs['Output:Variable']['Output:Variable 3']['variable_name'] = "ALL UPPER CASE FOR FUN"
        self.assertDictEqual(expected_outputs, updated_contents)

    def test_transform_some_ems_variables(self):
        file_contents = {
            'EnergyManagementSystem:Sensor': {
                'EnergyManagementSystem:Sensor 1': {
                    "output_variable_or_output_meter_index_key_name": "*",
                    "output_variable_or_output_meter_name": "Site Outdoor Air Drybulb Temperature"
                },
                'EnergyManagementSystem:Sensor 2': {
                    "output_variable_or_output_meter_index_key_name": "*",
                    "output_variable_or_output_meter_name": "Boiler Inlet Temperature"
                },
                'EnergyManagementSystem:Sensor 3': {
                    "output_variable_or_output_meter_index_key_name": "Plant Loop 1",
                    "output_variable_or_output_meter_name": "Plant Supply Side Unmet Demand Rate"
                },
                'EnergyManagementSystem:Sensor 4': {
                    "output_variable_or_output_meter_index_key_name": "Zone 1",
                    "output_variable_or_output_meter_name": "Zone Mean Air Temperature"
                }
            }
        }
        ov = OutputVariable({
            "Site Outdoor Air Drybulb Temperature": "New Outdoor TEMP",
            "Plant Supply Side Unmet Demand Rate": "ALL UPPER CASE FOR FUN",
            "Boiler Inlet Temperature": None,
            "Zone Mean Air Temperature": ['A', 'B']
        })
        updated_contents = ov.transform(file_contents, self.muted_logger)
        expected_outputs = file_contents
        expected_outputs['EnergyManagementSystem:Sensor']['EnergyManagementSystem:Sensor 1'][
            'output_variable_or_output_meter_name'] = "New Outdoor TEMP"
        expected_outputs['EnergyManagementSystem:Sensor']['EnergyManagementSystem:Sensor 3'][
            'output_variable_or_output_meter_name'] = "ALL UPPER CASE FOR FUN"
        del expected_outputs['EnergyManagementSystem:Sensor']['EnergyManagementSystem:Sensor 2']
        del expected_outputs['EnergyManagementSystem:Sensor']['EnergyManagementSystem:Sensor 4']
        expected_outputs['EnergyManagementSystem:Sensor']['Zone Mean Air Temperature_1'] = {
            'output_variable_or_output_meter_index_key_name': 'Zone 1', 'output_variable_or_output_meter_name': 'A'
        }
        expected_outputs['EnergyManagementSystem:Sensor']['Zone Mean Air Temperature_2'] = {
            'output_variable_or_output_meter_index_key_name': 'Zone 1', 'output_variable_or_output_meter_name': 'B'
        }
        self.assertDictEqual(expected_outputs, updated_contents)

    def test_transform_some_meters_variables(self):
        file_contents = {
            'Output:Meter': {'Output:Meter 1': {"key_name": "m"}},
            'Output:Meter:MeterFileOnly': {'Output:Meter:MeterFileOnly 1': {"key_name": "m"}},
            'Output:Meter:Cumulative': {'Output:Meter:Cumulative 1': {"key_name": "m"}},
            'Output:Meter:Cumulative:MeterFileOnly': {'Output:Meter:Cumulative:MeterFileOnly 1': {"key_name": "m"}},
        }
        ov = OutputVariable({"m": "n"})
        updated_contents = ov.transform(file_contents, self.muted_logger)
        expected_outputs = {
            'Output:Meter': {'Output:Meter 1': {"key_name": "n"}},
            'Output:Meter:MeterFileOnly': {'Output:Meter:MeterFileOnly 1': {"key_name": "n"}},
            'Output:Meter:Cumulative': {'Output:Meter:Cumulative 1': {"key_name": "n"}},
            'Output:Meter:Cumulative:MeterFileOnly': {'Output:Meter:Cumulative:MeterFileOnly 1': {"key_name": "n"}},
        }
        self.assertDictEqual(expected_outputs, updated_contents)

    def test_output_variable_is_deleted(self):
        file_contents = {
            'Output:Variable': {
                'Output:Variable 1': {
                    "key_value": "*",
                    "reporting_frequency": "Hourly",
                    "variable_name": "Site Outdoor Air Drybulb Temperature"
                },
                'Output:Variable 2': {
                    "key_value": "*",
                    "reporting_frequency": "Hourly",
                    "variable_name": "Boiler Inlet Temperature"
                },
                'Output:Variable 3': {
                    "key_value": "Plant Loop 1",
                    "reporting_frequency": "Daily",
                    "variable_name": "Plant Supply Side Unmet Demand Rate"
                }
            }
        }
        ov = OutputVariable({
            "Site Outdoor Air Drybulb Temperature": "New Outdoor TEMP",
            "Boiler Inlet Temperature": None
        })
        updated_contents = ov.transform(file_contents, self.muted_logger)
        expected_outputs = {
            'Output:Variable': {
                'Output:Variable 1': {
                    "key_value": "*",
                    "reporting_frequency": "Hourly",
                    "variable_name": "New Outdoor TEMP"
                },
                'Output:Variable 3': {
                    "key_value": "Plant Loop 1",
                    "reporting_frequency": "Daily",
                    "variable_name": "Plant Supply Side Unmet Demand Rate"
                }
            }
        }
        self.assertDictEqual(expected_outputs, updated_contents)

    def test_output_variable_is_list(self):
        file_contents = {
            'Output:Variable': {
                'Output:Variable 1': {
                    "key_value": "*",
                    "reporting_frequency": "Hourly",
                    "variable_name": "Site Outdoor Air Drybulb Temperature"
                },
                'Output:Variable 2': {
                    "key_value": "*",
                    "reporting_frequency": "Hourly",
                    "variable_name": "Boiler Inlet Temperature"
                },
                'Output:Variable 3': {
                    "key_value": "Plant Loop 1",
                    "reporting_frequency": "Daily",
                    "variable_name": "Plant Supply Side Unmet Demand Rate"
                }
            }
        }
        ov = OutputVariable({
            "Site Outdoor Air Drybulb Temperature": "New Outdoor TEMP",
            "Boiler Inlet Temperature": ['A', 'B', 'C']
        })
        updated_contents = ov.transform(file_contents, self.muted_logger)
        expected_outputs = {
            'Output:Variable': {
                'Output:Variable 1': {
                    "key_value": "*",
                    "reporting_frequency": "Hourly",
                    "variable_name": "New Outdoor TEMP"
                },
                'Output:Variable 3': {
                    "key_value": "Plant Loop 1",
                    "reporting_frequency": "Daily",
                    "variable_name": "Plant Supply Side Unmet Demand Rate"
                },
                'Boiler Inlet Temperature_1': {
                    "key_value": "*",
                    "reporting_frequency": "Hourly",
                    "variable_name": "A"
                },
                'Boiler Inlet Temperature_2': {
                    "key_value": "*",
                    "reporting_frequency": "Hourly",
                    "variable_name": "B"
                },
                'Boiler Inlet Temperature_3': {
                    "key_value": "*",
                    "reporting_frequency": "Hourly",
                    "variable_name": "C"
                },
            }
        }
        self.assertDictEqual(expected_outputs, updated_contents)
