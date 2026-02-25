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
