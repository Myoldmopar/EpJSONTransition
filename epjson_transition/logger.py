from datetime import datetime
from typing import Union


class SimpleLogger:
    def __init__(self, console=True, log_file_path: Union[str, None] = None):
        self.console = console
        self.prefix = ""
        if log_file_path is None:
            self.output_file = None
        else:
            self.output_file = open(log_file_path, 'w')

    def close(self):
        if self.output_file:
            self.output_file.close()

    def add_prefix(self):
        self.prefix += ' '

    def remove_prefix(self):
        if len(self.prefix) > 0:
            self.prefix = self.prefix[:-1]

    def print(self, message):
        line = f"{datetime.now()} : {self.prefix}{message}"
        if self.console:
            print(line)  # pragma: no cover - not muddying up the console output during testing
        if self.output_file:
            print(line, file=self.output_file)
