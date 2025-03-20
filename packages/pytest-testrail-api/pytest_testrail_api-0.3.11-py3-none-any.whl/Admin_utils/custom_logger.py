import logging
import os

from Admin_utils.custom_logger_formatter import CustomColoredFormatter

LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL", logging.INFO)


class CustomLogger:
    def __init__(
            self,
            name: str = __name__,
            level: int = LOGGING_LEVEL,
            log_to_file: bool = False,
            file_name: str = "testing_log.log",
            formatter_str: str = "%(asctime)s - %(levelname)s - %(message)s",
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        if not self.logger.handlers:
            formatter = CustomColoredFormatter(formatter_str)
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

            if log_to_file:
                file_handler = logging.FileHandler(file_name)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger


logger = CustomLogger().get_logger()
