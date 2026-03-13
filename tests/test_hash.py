import ast

import pytest
from full_match import match

from getsources import getclearsource, getsourcehash
from getsources.errors import UncertaintyWithLambdasError


def test_hash_lenth(transformed):
    @transformed
    def function():
        ...

    assert len(getsourcehash(function)) == 6
    assert len(getsourcehash(function, size=4)) == 4
    assert len(getsourcehash(function, size=5)) == 5
    assert len(getsourcehash(function, size=6)) == 6
    assert len(getsourcehash(function, size=7)) == 7
    assert len(getsourcehash(function, size=8)) == 8

    with pytest.raises(ValueError, match=match('The hash string size must be in range 4..8.')):
        getsourcehash(function, size=3)

    with pytest.raises(ValueError, match=match('The hash string size must be in range 4..8.')):
        getsourcehash(function, size=9)

    with pytest.raises(ValueError, match=match('The hash string size must be in range 4..8.')):
        getsourcehash(function, size=0)

    with pytest.raises(ValueError, match=match('The hash string size must be in range 4..8.')):
        getsourcehash(function, size=-5)


def test_equality(transformed):
    @transformed
    def function():
        ...

    first_hash = getsourcehash(function)

    @transformed
    def function():
        ...

    second_hash = getsourcehash(function)

    assert first_hash == second_hash


def test_not_equality(transformed):
    @transformed
    def function():
        ...

    first_hash = getsourcehash(function)

    @transformed
    def function():
        pass

    second_hash = getsourcehash(function)

    assert first_hash != second_hash


def test_contain_ilou(transformed):
    @transformed
    def function1():
        ...

    @transformed
    def function2():
        ...

    @transformed
    def function3():
        return 1 + 2 + 3

    @transformed
    def function4():
        return 1 + 2 + 3 + 4

    for function in (function1, function2, function3, function4):
        for size in range(4, 9):
            for letter in ('I', 'L', 'O', 'U'):
                assert letter not in getsourcehash(function, size=size)


def test_only_body_off(transformed):
    @transformed
    def function1():
        return 1234

    @transformed
    def function2(a=5):  # noqa: ARG001
        return 1234

    @transformed
    def function3():
        return 12345

    assert getsourcehash(function1) != getsourcehash(function2)
    assert getsourcehash(function3) != getsourcehash(function2)


def test_only_body_on(transformed):
    @transformed
    def function1():
        return 1234

    @transformed
    def function2(a=5):  # noqa: ARG001
        return 1234

    @transformed
    def function3():
        return 12345

    assert getsourcehash(function1, only_body=True) == getsourcehash(function2, only_body=True)
    assert getsourcehash(function3, only_body=True) != getsourcehash(function2, only_body=True)


def test_only_body_on_and_skip_docstring_off(transformed):
    @transformed
    def function1():
        return 1234

    @transformed
    def function2(a=5):  # noqa: ARG001
        return 1234

    @transformed
    def function3():
        """kek"""
        return 1234

    @transformed
    def function4(a=5):  # noqa: ARG001
        """kek"""
        return 1234

    assert getsourcehash(function1, only_body=True) == getsourcehash(function2, only_body=True)
    assert getsourcehash(function3, only_body=True) == getsourcehash(function4, only_body=True)

    assert getsourcehash(function1, only_body=True) != getsourcehash(function3, only_body=True)


def test_only_body_on_and_skip_docstring_on(transformed):
    @transformed
    def function1():
        return 1234

    @transformed
    def function2(a=5):  # noqa: ARG001
        return 1234

    @transformed
    def function3():
        """kek"""
        return 1234

    @transformed
    def function4(a=5):  # noqa: ARG001
        """kek"""
        return 1234

    assert getsourcehash(function1, only_body=True, skip_docstring=True) == getsourcehash(function2, only_body=True, skip_docstring=True)
    assert getsourcehash(function3, only_body=True, skip_docstring=True) == getsourcehash(function4, only_body=True, skip_docstring=True)

    assert getsourcehash(function1, only_body=True, skip_docstring=True) == getsourcehash(function3, only_body=True, skip_docstring=True)


def test_try_to_skip_doctstring_if_only_body_option_isnt_sen(transformed):
    @transformed
    def function():
        ...

    with pytest.raises(ValueError, match=match('You can omit the docstring only if the `only_body=True` option is set.')):
        getsourcehash(function, skip_docstring=True)

    with pytest.raises(ValueError, match=match('You can omit the docstring only if the `only_body=True` option is set.')):
        getsourcehash(function, only_body=False, skip_docstring=True)


def test_hash_simple_lambda():
    lambda_hash = getsourcehash(lambda x: x)
    assert lambda_hash == 'HVND1V'


def test_hash_lambda_only_body():
    first_hash = getsourcehash(lambda x: x, only_body=True)
    second_hash = getsourcehash(lambda x, y: x, only_body=True)  # noqa: ARG005

    assert first_hash == '91MJ41'
    assert first_hash == second_hash


def test_try_to_get_hash_of_changed_lambda():
    function = lambda x, y: x  # noqa: ARG005

    tree = ast.parse(getclearsource(function), mode='eval')
    tree.body.body = ast.Name(id="y", ctx=ast.Load(), lineno=1, col_offset=1)
    code = compile(tree, filename="<ast>", mode="eval")
    new_function = eval(code)

    with pytest.raises(UncertaintyWithLambdasError, match=match('It seems that the AST for the lambda function has been modified; can\'t extract the source code.')):
        getsourcehash(new_function)
