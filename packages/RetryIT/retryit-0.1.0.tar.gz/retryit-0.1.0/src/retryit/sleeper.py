"""Sleeping time calculator functions for the decorator.

Each function takes a number of initial configurations as arguments,
and returns a function that can be passed to the decorator.
"""


from typing import Callable


def constant_until_max_duration(
    sleep_seconds: float,
    total_seconds: float
) -> Callable[[int, float], float]:
    """
    Calculate the sleeping time for the next retry.

    Parameters
    ----------
    sleep_seconds : float
        Sleeping time between retries.
    total_seconds : float
        Maximum total sleeping time.

    Returns
    -------
    float
        Sleeping time for the next retry.
    """
    def sleeper(count_tries: int, current_total_sleep_seconds: float) -> float:
        if current_total_sleep_seconds >= total_seconds:
            return 0
        return sleep_seconds
    return sleeper
