import code
from contextlib import redirect_stdout
from io import StringIO
from sys import version_info

import pytest

from getsources import getsource


def test_usual_functions():
    def function_1():
        pass

    def function_2(a, b):
        pass

    assert getsource(function_1).splitlines() == ['    def function_1():', '        pass']
    assert getsource(function_2).splitlines() == ['    def function_2(a, b):', '        pass']


def test_lambda():
    function = lambda x: x

    assert getsource(function).strip() == 'function = lambda x: x'


def test_usual_methods():
    class A:
        def method(self):
            pass

    class B:
        def method(self, a, b):
            pass

    assert getsource(A().method).splitlines() == ['        def method(self):', '            pass']
    assert getsource(B().method).splitlines() == ['        def method(self, a, b):', '            pass']


def test_usual_classmethods():
    class A:
        @classmethod
        def method(cls):
            pass

    class B:
        @classmethod
        def method(cls, a, b):
            pass

    assert getsource(A().method).splitlines() == ['        @classmethod', '        def method(cls):', '            pass']
    assert getsource(B().method).splitlines() == ['        @classmethod', '        def method(cls, a, b):', '            pass']


def test_usual_staticmethods():
    class A:
        @staticmethod
        def method():
            pass

    class B:
        @staticmethod
        def method(a, b):
            pass

    assert getsource(A().method).splitlines() == ['        @staticmethod', '        def method():', '            pass']
    assert getsource(B().method).splitlines() == ['        @staticmethod', '        def method(a, b):', '            pass']


@pytest.mark.skipif(version_info >= (3, 14), reason='I wait this: https://github.com/uqfoundation/dill/issues/745')
def test_usual_functions_in_REPL():  # noqa: N802
    console = code.InteractiveConsole({})
    buffer = StringIO()

    console.push("from getsources import getsource")
    console.push("def function(): pass")
    console.push("")

    with redirect_stdout(buffer):
        console.push("print(getsource(function), end='')")

    assert buffer.getvalue() == 'def function(): pass'


@pytest.mark.skipif(version_info >= (3, 14), reason='I wait this: https://github.com/uqfoundation/dill/issues/745')
def test_lambda_in_REPL():  # noqa: N802
    function = lambda x: x

    assert getsource(function).strip() == 'function = lambda x: x'

    console = code.InteractiveConsole({})
    buffer = StringIO()

    console.push("from getsources import getsource")
    console.push('function = lambda x: x')

    with redirect_stdout(buffer):
        console.push("print(getsource(function), end='')")

    assert buffer.getvalue() == 'function = lambda x: x'
