from getsources.helpers.is_lambda import is_lambda


def test_lambdas_are_lambdas():
    assert is_lambda(lambda x: x)
    assert is_lambda(lambda x: None)
    assert is_lambda(lambda: None)


def test_are_not_lambdas(transformed):
    @transformed
    def function():
        ...

    assert not is_lambda(function)
