import re
from io import StringIO
from os import environ
from sys import platform

import pytest

from getsources import getclearsource


def global_function_1():
    ...

def global_function_2(a, b):
    ...

global_function_3 = lambda x: x

class GlobalClass:
    def simple_method(self):
        pass

    def method_with_parameters(self, a, b):
        pass

    @classmethod
    def class_method(cls, a, b):
        pass

    @staticmethod
    def static_method(a, b):
        pass


def test_usual_functions():
    def function_1():
        pass

    def function_2(a, b):
        pass

    assert getclearsource(function_1).splitlines() == ['def function_1():', '    pass']
    assert getclearsource(function_2).splitlines() == ['def function_2(a, b):', '    pass']

    assert getclearsource(global_function_1).splitlines() == ['def global_function_1():', '    ...']
    assert getclearsource(global_function_2).splitlines() == ['def global_function_2(a, b):', '    ...']


def test_lambda():
    function = lambda x: x

    assert getclearsource(function) == 'function = lambda x: x'
    assert getclearsource(global_function_3) == 'global_function_3 = lambda x: x'


def test_usual_methods():
    class A:
        def method(self):
            pass

    class B:
        def method(self, a, b):
            pass

    assert getclearsource(A().method).splitlines() == ['def method(self):', '    pass']
    assert getclearsource(B().method).splitlines() == ['def method(self, a, b):', '    pass']

    assert getclearsource(GlobalClass().simple_method).splitlines() == ['def simple_method(self):', '    pass']
    assert getclearsource(GlobalClass().method_with_parameters).splitlines() == ['def method_with_parameters(self, a, b):', '    pass']


def test_usual_classmethods():
    class A:
        @classmethod
        def method(cls):
            pass

    class B:
        @classmethod
        def method(cls, a, b):
            pass

    assert getclearsource(A().method).splitlines() == ['@classmethod', 'def method(cls):', '    pass']
    assert getclearsource(B().method).splitlines() == ['@classmethod', 'def method(cls, a, b):', '    pass']
    assert getclearsource(A.method).splitlines() == ['@classmethod', 'def method(cls):', '    pass']
    assert getclearsource(B.method).splitlines() == ['@classmethod', 'def method(cls, a, b):', '    pass']

    assert getclearsource(GlobalClass().class_method).splitlines() == ['@classmethod', 'def class_method(cls, a, b):', '    pass']
    assert getclearsource(GlobalClass.class_method).splitlines() == ['@classmethod', 'def class_method(cls, a, b):', '    pass']


def test_usual_staticmethods():
    class A:
        @staticmethod
        def method():
            pass

    class B:
        @staticmethod
        def method(a, b):
            pass

    assert getclearsource(A().method).splitlines() == ['@staticmethod', 'def method():', '    pass']
    assert getclearsource(B().method).splitlines() == ['@staticmethod', 'def method(a, b):', '    pass']

    assert getclearsource(A.method).splitlines() == ['@staticmethod', 'def method():', '    pass']
    assert getclearsource(B.method).splitlines() == ['@staticmethod', 'def method(a, b):', '    pass']

    assert getclearsource(GlobalClass().static_method).splitlines() == ['@staticmethod', 'def static_method(a, b):', '    pass']
    assert getclearsource(GlobalClass.static_method).splitlines() == ['@staticmethod', 'def static_method(a, b):', '    pass']


@pytest.mark.skipif(platform == "win32", reason='I wait this: https://github.com/raczben/wexpect/issues/55')
def test_usual_functions_in_REPL():  # noqa: N802
    from pexpect import spawn  # type: ignore[import-untyped] # noqa: PLC0415

    env = environ.copy()
    env["PYTHON_COLORS"] = "0"
    child = spawn('python3', ["-i"], encoding="utf-8", env=env, timeout=5)

    buffer = StringIO()
    child.logfile = buffer

    child.expect(">>> ")
    child.sendline('from getsources import getclearsource')
    child.expect(">>> ")
    child.sendline('def function(): ...')
    child.sendline('')
    child.expect(">>> ")

    before = buffer.getvalue()

    child.sendline("print(getclearsource(function), end='')")
    child.expect(">>> ")

    after = buffer.getvalue()
    after = re.compile(r'(?:\x1B[@-_]|\x9B)[0-?]*[ -/]*[@-~]').sub('', after.lstrip(before))
    after = ''.join(ch for ch in after if ch >= ' ' or ch in '\n\r\t')
    after = after.splitlines()

    child.sendline("exit()")

    assert any('def function(): ...' in x for x in after)


@pytest.mark.skipif(platform == "win32", reason='I wait this: https://github.com/raczben/wexpect/issues/55')
def test_lambda_in_REPL():  # noqa: N802
    from pexpect import spawn  # type: ignore[import-untyped] # noqa: PLC0415

    env = environ.copy()
    env["PYTHON_COLORS"] = "0"
    child = spawn('python3', ["-i"], encoding="utf-8", env=env, timeout=5)

    buffer = StringIO()
    child.logfile = buffer

    child.expect(">>> ")
    child.sendline('from getsources import getclearsource')
    child.expect(">>> ")
    child.sendline('function = lambda x: x')
    child.expect(">>> ")

    before = buffer.getvalue()

    child.sendline("print(getclearsource(function), end='')")
    child.expect(">>> ")

    after = buffer.getvalue().lstrip(before)
    after = after.splitlines()

    child.sendline("exit()")

    assert any('function = lambda x: x' in x for x in after)
