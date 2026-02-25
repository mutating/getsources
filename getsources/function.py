from typing import Callable, Any
from inspect import getsource as original_getsource
from dill.source import getsource as dill_getsource


def getsource(function: Callable[..., Any]) -> str:
    try:
        return original_getsource(function)
    except OSError:
        return dill_getsource(function)
