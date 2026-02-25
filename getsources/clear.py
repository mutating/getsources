from typing import Any, Callable

from getsources import getsource


def getclearsource(function: Callable[..., Any]) -> str:
    source_code = getsource(function)

    splitted_source_code = source_code.split('\n')

    indent = 0
    for letter in splitted_source_code[0]:  # pragma: no branch
        if letter.isspace():
            indent += 1
        else:
            break

    new_splitted_source_code = [x[indent:] for x in splitted_source_code]

    return '\n'.join(new_splitted_source_code).rstrip('\n')
