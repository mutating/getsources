from types import FunctionType
from typing import Any, Callable


def is_lambda(function: Callable[..., Any]) -> bool:
    return isinstance(function, FunctionType) and function.__name__ == "<lambda>"
