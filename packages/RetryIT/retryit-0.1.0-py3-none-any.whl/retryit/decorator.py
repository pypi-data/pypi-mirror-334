from typing import Any, Callable
import time
from functools import wraps
import retryit


def retry(
    function: Callable | None = None,
    *,
    sleeper: Callable[
        [int, float], float
    ] = retryit.sleeper.constant_until_max_duration(10, 600),
    exception_handler: Callable[[Exception], bool] | None = retryit.exception_handler.on_type(Exception),
    return_handler: Callable[[Any], bool] | None = None,
    logger: Callable[
        [
            Callable,
            Callable,
            Callable | None,
            Callable | None,
            int,
            float,
            float | None,
            Exception | None,
            Any | None,
            bool | None,
            bool | None,
        ], None
    ] | None = None,
) -> Callable:
    """
    Retry a function call.


    Returns
    -------
    callable
        Decorated function.
    """
    if not (exception_handler or return_handler):
        raise ValueError("Either exception_handler or return_handler must be provided.")

    def retry_decorator(func: Callable):

        @wraps(func)
        def retry_wrapper(*args, **kwargs):

            def log():
                if logger:
                    logger(
                        func,
                        sleeper,
                        exception_handler,
                        return_handler,
                        count_tries,
                        current_total_sleep_seconds,
                        next_sleep_seconds,
                        exception,
                        return_value,
                        exception_handler_response,
                        return_handler_response,
                    )
                return

            count_tries = 0
            current_total_sleep_seconds = 0
            history = []

            while True:
                exception_handler_response = None
                return_handler_response = None
                next_sleep_seconds = None
                try:
                    return_value = func(*args, **kwargs)
                    exception = None
                except Exception as e:
                    return_value = None
                    exception = e
                count_tries += 1
                history.append((exception is not None, exception or return_value))
                if exception:
                    if exception_handler:
                        exception_handler_response = exception_handler(exception)
                        if exception_handler_response:
                            next_sleep_seconds = sleeper(count_tries, current_total_sleep_seconds)
                            log()
                            if next_sleep_seconds == 0:
                                raise retryit.exception.RetryError(
                                    count_tries=count_tries,
                                    total_sleep_seconds=current_total_sleep_seconds,
                                    history=history
                                )
                            current_total_sleep_seconds += next_sleep_seconds
                        else:
                            log()
                            raise exception
                    else:
                        log()
                        raise exception
                elif return_handler and return_handler(return_value):
                    next_sleep_seconds = sleeper(count_tries, current_total_sleep_seconds)
                    log()
                    if next_sleep_seconds == 0:
                        raise retryit.exception.RetryError(
                            count_tries=count_tries,
                            total_sleep_seconds=current_total_sleep_seconds,
                            history=history
                        )
                    current_total_sleep_seconds += next_sleep_seconds
                else:
                    log()
                    return return_value
                time.sleep(next_sleep_seconds)

        return retry_wrapper

    return retry_decorator(function) if function else retry_decorator
