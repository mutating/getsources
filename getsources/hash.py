import hashlib
from ast import Constant, Expr, Lambda, get_source_segment, parse, walk
from typing import Any, Callable

from getsources import getclearsource
from getsources.helpers.is_lambda import is_lambda

ALPHABET = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'


def get_body_text(function: Callable[..., Any], source: str, skip_docstring: bool) -> str:
    tree = parse(source)

    if is_lambda(function):
        body_nodes = []

        for node in walk(tree):
            if isinstance(node, Lambda):
                body_nodes.append(node.body)

    else:
        function_node = tree.body[0]
        body_nodes = function_node.body  # type: ignore[attr-defined]
        first = body_nodes[0]

        if skip_docstring and body_nodes and (isinstance(first, Expr) and isinstance(first.value, Constant) and isinstance(first.value.value, str)):
            body_nodes = body_nodes[1:]

    return '\n'.join([get_source_segment(source, statement) for statement in body_nodes])  # type: ignore[misc]


def getsourcehash(function: Callable[..., Any], size: int = 6, only_body: bool = False, skip_docstring: bool = False) -> str:
    if not 4 <= size <= 8:
        raise ValueError('The hash string size must be in range 4..8.')
    if skip_docstring and not only_body:
        raise ValueError('You can omit the docstring only if the `only_body=True` option is set.')

    source_code = getclearsource(function)
    if not only_body:
        interesting_part = source_code
    else:
        interesting_part = get_body_text(function, source_code, skip_docstring=skip_docstring)

    digest = hashlib.sha256(interesting_part.encode('utf-8')).digest()
    number = int.from_bytes(digest, 'big')
    base = len(ALPHABET)

    chars = []
    for _ in range(size):
        number, rem = divmod(number, base)
        chars.append(ALPHABET[rem])

    return ''.join(reversed(chars))
