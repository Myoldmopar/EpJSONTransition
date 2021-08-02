from pathlib import Path

from epjson_transition.exceptions import MissingEpJSONFile
from epjson_transition.file import EpJSONFile
from epjson_transition.logger import SimpleLogger


class EpJSONTransition:

    def __init__(self, input_file_object: Path, output_file_object: Path):
        if not input_file_object.exists():
            raise MissingEpJSONFile("Could not locate EpJSON file, expected at " + str(input_file_object))
        self.input_file_object = input_file_object
        self.output_file_object = output_file_object

    def transform(self, logger: SimpleLogger):
        logger.print("Transition Process Starting")
        logger.print(f"Input File Path: {self.input_file_object}")
        logger.print(f"Output File Path: {self.output_file_object}")
        logger.print("Reading File Contents to Determine Version")
        logger.add_prefix()
        file = EpJSONFile(self.input_file_object, self.output_file_object, logger)
        logger.remove_prefix()
        logger.print("Calling Transition Routine")
        logger.add_prefix()
        file.transform(logger)
        logger.remove_prefix()
        logger.print("Transition Process Completed")
        logger.close()
