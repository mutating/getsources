import hashlib
from typing import Any, Callable
from ast import parse, Expr, Constant, get_source_segment

from getsources import getclearsource

ALPHABET = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'


def get_body_text(source: str, skip_docstring: bool) -> str:
    tree = parse(source)

    function_node = tree.body[0]
    body_nodes = function_node.body
    first = body_nodes[0]

    if skip_docstring and body_nodes and (isinstance(first, Expr) and isinstance(first.value, Constant) and isinstance(first.value.value, str)):
        body_nodes = body_nodes[1:]

    return '\n'.join([get_source_segment(source, statement) for statement in body_nodes])


def getsourcehash(function: Callable[..., Any], size: int = 6, only_body: bool = False, skip_docstring: bool = False) -> str:
    if not 4 <= size <= 8:
        raise ValueError('The hash string size must be in range 4..8.')
    if skip_docstring and not only_body:
        raise ValueError('You can omit the docstring only if the `only_body=True` option is set.')

    source_code = getclearsource(function)
    if not only_body:
        interesting_part = source_code
    else:
        interesting_part = get_body_text(source_code, skip_docstring=skip_docstring)

    digest = hashlib.sha256(interesting_part.encode('utf-8')).digest()
    number = int.from_bytes(digest, 'big')
    base = len(ALPHABET)

    chars = []
    for _ in range(size):
        number, rem = divmod(number, base)
        chars.append(ALPHABET[rem])

    return ''.join(reversed(chars))
