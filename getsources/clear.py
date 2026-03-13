from ast import Lambda, get_source_segment, parse, walk
from typing import Any, Callable

from getsources import getsource
from getsources.errors import UncertaintyWithLambdasError
from getsources.helpers.is_lambda import is_lambda


def getclearsource(function: Callable[..., Any]) -> str:
    source_code = getsource(function)

    if is_lambda(function):
        stripped_source_code = source_code.strip()
        tree = parse(stripped_source_code)

        first = True
        lambda_node = None
        for node in walk(tree):
            if isinstance(node, Lambda):
                if not first:
                    raise UncertaintyWithLambdasError('Several lambda functions are defined in a single line of code, can\'t pick the one.')
                lambda_node = node
                first = False

        segment_source = get_source_segment(stripped_source_code, lambda_node)  # type: ignore[arg-type]
        if segment_source is None:
            raise UncertaintyWithLambdasError('It seems that the AST for the lambda function has been modified; can\'t extract the source code.')
        return segment_source


    splitted_source_code = source_code.split('\n')

    indent = 0
    for letter in splitted_source_code[0]:  # pragma: no branch
        if letter.isspace():
            indent += 1
        else:
            break

    new_splitted_source_code = [x[indent:] for x in splitted_source_code]

    return '\n'.join(new_splitted_source_code).rstrip('\n')
