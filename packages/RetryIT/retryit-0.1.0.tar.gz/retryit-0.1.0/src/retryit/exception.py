from typing import Any


class RetryError(Exception):
    """
    Exception class for return value errors.
    """

    def __init__(
        self,
        count_tries: int,
        total_sleep_seconds: float,
        history: list[tuple[bool, Any | Exception]],
    ):
        self.count_tries = count_tries
        self.total_sleep_seconds = total_sleep_seconds
        self.history = history
        error_msg = f"Validation failed after {count_tries} tries totaling {total_sleep_seconds} seconds."
        super().__init__(error_msg)
        return
