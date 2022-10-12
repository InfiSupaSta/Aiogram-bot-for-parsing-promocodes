import logging
import os
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent


class CustomFileHandler(logging.Handler):

    def __init__(self, filename: str):
        logging.Handler.__init__(self)
        self.path_to_logfile = f'{ROOT_PATH}/logs'
        self.filename = filename

    def emit(self, record: logging.LogRecord) -> None:
        if not os.path.exists(self.path_to_logfile):
            os.mkdir(self.path_to_logfile)

        log_record_to_string = f"{self.format(record)}"
        full_path_to_logfile = f"{self.path_to_logfile}/{self.filename}"

        with open(full_path_to_logfile, 'a+') as log_file:
            log_file.write(log_record_to_string)
