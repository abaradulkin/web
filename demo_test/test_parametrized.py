import pytest


@pytest.mark.parametrize(
    "first, second",
    [
        (0, False),
        (1, True),
        ("", False),
        ("Right answer", True)
    ]
)
def test_simple_parametrized(first, second):
    if first:
        assert second
    else:
        assert not second


@pytest.mark.parametrize(
    "param_a",
    [
        0,
        0.1,
        "String",
        ["a", "b"],
        ("a", "b")
    ]
)
@pytest.mark.parametrize(
    "param_b",
    [
        0,
        0.1,
        "String",
        ["a", "b"],
        ("a", "b")
    ]
)
def test_combination_parameters(param_a, param_b):
    print(param_a, param_b)


class DemoClass(object):
    def __init__(self, param):
        self.param = param

    def __repr__(self):
        return "Class WithRepr(param: {})".format(self.param)


def id_func(param):
    # TODO: add check that object is class
    if isinstance(param, object):
        return 'class {}'.format(param)
    return param


@pytest.mark.parametrize(
    "param",
    [
        DemoClass("first"),
        "Simple param"
    ],
    ids=id_func,
)
def test_parameters_wits_ids(param):
    pass
