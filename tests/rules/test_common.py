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
