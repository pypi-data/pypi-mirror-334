import ast as a
import collections.abc as c
import pathlib
import typing as h

from value_factory.type.factory import factories_t


def NewFromStrWithLiteralEval(
    string: str, /, *, should_run_recursively: bool = False
) -> h.Any:
    """"""
    assert isinstance(string, str)

    try:
        value = a.literal_eval(string)
    except (SyntaxError, ValueError):
        value = string

    if (not should_run_recursively) or isinstance(value, str):
        return value

    if isinstance(value, c.Sequence):
        stripe = type(value)
        elements = []
        for element in value:
            if isinstance(element, str):
                element = NewFromStrWithLiteralEval(
                    element, should_run_recursively=True
                )
            elements.append(element)
        value = stripe(elements)
    elif isinstance(value, c.Mapping):
        stripe = type(value)
        elements = []
        for key, value in value.items():
            if isinstance(key, str):
                key = NewFromStrWithLiteralEval(key, should_run_recursively=True)
            if isinstance(value, str):
                value = NewFromStrWithLiteralEval(value, should_run_recursively=True)
            elements.append((key, value))
        value = stripe(elements)

    return value


def _NewPathFromStr(path: str, /) -> pathlib.Path | None:
    """
    /!\\ pathlib.Path("") == pathlib.Path(".").
    """
    if path.__len__() > 0:
        return pathlib.Path(path)
    return None


ATOMIC_FACTORIES = {
    # type_wanted: {type_passed: NewFromPassed_h}
    dict: {list: dict, set: dict, tuple: dict},
    float: {int: float, str: float},
    int: {str: int},
    list: {range: list, set: list, tuple: list},
    set: {list: set, range: set, tuple: set},
    str: {h.Any: str},
    tuple: {list: tuple, range: tuple, set: tuple},
    pathlib.Path: {str: _NewPathFromStr},
}

ATOMIC_FACTORIES = factories_t(ATOMIC_FACTORIES)
ATOMIC_FACTORIES.NewFromStr = NewFromStrWithLiteralEval
