"""Exception handler functions for the decorator."""


from typing import Callable, Type


def on_type(*types: Type[Exception]) -> Callable[[Exception], bool]:
    """
    Return an exception handler function that accepts exceptions of the given type(s),
    and rejects all others.

    Parameters
    ----------
    *types : Type[Exception]
        Exception type(s) to accept.
        All other exceptions will be raised immediately.

    Returns
    -------
    Callable[[Exception], bool]
        Function that returns True if the exception is an instance of the given type(s),
        and False otherwise.
    """
    def handler(exception: Exception) -> bool:
        return isinstance(exception, types)

    return handler
