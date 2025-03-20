import logging

# Define ANSI escape codes for colors
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"


class CustomColoredFormatter(logging.Formatter):
    """Custom logging formatter to add colors to log messages."""

    def __init__(self, fmt, datefmt=None):
        super().__init__(fmt, datefmt)
        self.FORMATS = {
            logging.DEBUG: BLUE + fmt + RESET,
            logging.INFO: GREEN + fmt + RESET,
            logging.WARNING: YELLOW + fmt + RESET,
            logging.ERROR: RED + fmt + RESET,
            logging.CRITICAL: RED + fmt + RESET,
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self._fmt)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
