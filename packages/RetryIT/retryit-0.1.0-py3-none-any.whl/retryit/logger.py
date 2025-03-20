"""Logger functions for the decorator."""


from typing import Any, Callable


def full(
    log_function: Callable,
    title: str = "Try function '{function.__qualname__}' (attempt {count_tries})",
    details: tuple[str, ...] | list[str] = (
        "Function: {function}",
        "Sleeper Function: {sleeper}",
        "Exception Handler Function: {exception_handler}",
        "Return Handler Function: {return_handler}",
        "Current Tries: {count_tries}",
        "Current Total Sleep Duration: {current_total_sleep_seconds} seconds",
        "Next Sleep Duration: {next_sleep_seconds} seconds",
        "Exception: {exception.__class__.__name__}: {exception}",
        "Return Value: {value}",
        "Exception Handler Response: {exception_handler_response}",
        "Return Handler Response: {return_handler_response}",
    ),
    case_exception_without_handler: tuple[Any, str] = (
        "error",
        "The function raised an exception while no exception handler was provided; "
        "the exception will be raised."
    ),
    case_exception_rejected: tuple[Any, str] = (
        "error",
        "The function raised an exception that was rejected by the exception handler; "
        "the exception will be raised."
    ),
    case_exception_accepted_and_timeout: tuple[Any, str] = (
        "error",
        "The function raised an exception that was suppressed by the exception handler, "
        "but the retry limit has been reached; a RetryError exception will be raised."
    ),
    case_exception_accepted_and_retry: tuple[Any, str] = (
        "notice",
        "The function raised an exception that was suppressed by the exception handler; "
        "the function will be retried in {next_sleep_seconds} seconds."
    ),
    case_return_without_handler: tuple[Any, str] = (
        "info",
        "The function executed successfully while no return handler was provided; "
        "the return value will be returned."
    ),
    case_return_accepted: tuple[Any, str] = (
        "info",
        "The function executed successfully and the return value was accepted by the return handler; "
        "the return value will be returned."
    ),
    case_return_rejected_and_timeout: tuple[Any, str] = (
        "error",
        "The function executed successfully, but the return value was rejected by the return handler "
        "and the retry limit has been reached; a RetryError exception will be raised."
    ),
    case_return_rejected_and_retry: tuple[Any, str] = (
        "notice",
        "The function executed successfully, but the return value was rejected by the return handler; "
        "the function will be retried in {next_sleep_seconds} seconds."
    ),
):
    def log(
        function: Callable,
        sleeper: Callable,
        exception_handler: Callable | None,
        return_handler: Callable | None,
        count_tries: int,
        current_total_sleep_seconds: float,
        next_sleep_seconds: float,
        exception: Exception | None,
        value: Any,
        exception_handler_response: bool | None,
        return_handler_response: bool | None,
    ):
        kwargs = locals()
        if exception:
            if exception_handler_response is None:
                case = case_exception_without_handler
            elif not exception_handler_response:
                case = case_exception_rejected
            elif not next_sleep_seconds:
                case = case_exception_accepted_and_timeout
            else:
                case = case_exception_accepted_and_retry
        elif return_handler_response is None:
            case = case_return_without_handler
        elif not return_handler_response:
            case = case_return_accepted
        elif not next_sleep_seconds:
            case = case_return_rejected_and_timeout
        else:
            case = case_return_rejected_and_retry
        log_function(
            case[0],
            title.format(**kwargs),
            case[1].format(**kwargs),
            [detail.format(**kwargs) for detail in details]
        )
        return

    return log
