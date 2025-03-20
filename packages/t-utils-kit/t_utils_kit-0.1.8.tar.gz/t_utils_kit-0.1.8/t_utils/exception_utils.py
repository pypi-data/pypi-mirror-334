"""Repeatable exception class."""

from t_utils.logger_utils import logger


class RepeatableExceptionCounter:
    """Keeps track of how many times the same exception is thrown in a row."""

    def __init__(self):
        """Initialize the counter."""
        self.repeating_same_exception_count = 0
        self.__previous_exception = ""

    def new_exception(self, exception: Exception) -> None:
        """Handle a new exception. If it's the same as the previous one, increase the counter."""
        exception_str = f"{type(exception)}:{exception}"
        if exception_str == self.__previous_exception:
            self.repeating_same_exception_count += 1
            logger.debug(f"Repeating exception: {exception_str}. Count: {self.repeating_same_exception_count}")
        else:
            self.repeating_same_exception_count = 1
            self.__previous_exception = exception_str
            logger.debug(f"New exception: {exception_str}. Resetting counter to 1")
