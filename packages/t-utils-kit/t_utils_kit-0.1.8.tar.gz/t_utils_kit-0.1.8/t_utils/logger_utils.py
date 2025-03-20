"""Module for logger."""
import logging
import sys
from logging import LogRecord


class CustomFormatter(logging.Formatter):
    """CustomFormatter class."""

    grey = "\x1b[0m"
    yellow = "\x1b[33m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    def __init__(self, fmt: str):
        """Init method."""
        super().__init__()
        self.FORMATS = {
            logging.DEBUG: self.grey + fmt + self.reset,
            logging.INFO: self.grey + fmt + self.reset,
            logging.WARNING: self.yellow + fmt + self.reset,
            logging.ERROR: self.bold_red + fmt + self.reset,
            logging.CRITICAL: self.bold_red + fmt + self.reset,
        }

    def format(self, record: LogRecord) -> str:
        """Override 'format' method."""
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger(__name__)
log_level = logging.DEBUG

handler = logging.StreamHandler(sys.stdout)
format = r"%(asctime)s - %(levelname)-7s %(threadName)-12s [%(filename)s:%(lineno)s - %(funcName)s()] - %(message)s"
if logger.hasHandlers():
    logger.handlers = []
logger.setLevel(log_level)
logger.propagate = False

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(log_level)
handler.setFormatter(CustomFormatter(format))
logger.addHandler(handler)
