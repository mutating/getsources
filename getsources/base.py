from inspect import getsource as original_getsource
from typing import Any, Callable

from dill.source import getsource as dill_getsource  # type: ignore[import-untyped]


def getsource(function: Callable[..., Any]) -> str:
    try:
        return original_getsource(function)
    except OSError:  # pragma: no cover
        return dill_getsource(function)  # type: ignore[no-any-return]
