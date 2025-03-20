import typing as h

from value_factory.extension.hint import hint_h
from value_factory.type.factory import value_passed_h

IsInstance_h = h.Callable[[value_passed_h, hint_h], bool]
