import dataclasses as d
import typing as h

type_wanted_h = type
type_passed_h = type
value_wanted_h = h.Any
value_passed_h = h.Any

NewFromPassed_h = h.Callable[[value_passed_h], value_wanted_h]


@d.dataclass(slots=True, repr=False, eq=False, init=False)
class factories_t(dict[type_wanted_h, dict[type_passed_h, NewFromPassed_h]]):
    _NewFromStr: h.ClassVar[NewFromPassed_h | None] = None

    @property
    def NewFromStr(self) -> NewFromPassed_h | None:
        """"""
        return self.__class__._NewFromStr

    @NewFromStr.setter
    def NewFromStr(self, NewFromStr: NewFromPassed_h, /) -> None:
        """"""
        self.__class__._NewFromStr = NewFromStr

    def Converter(
        self, passed: type | h.Any, type_wanted: type, /
    ) -> NewFromPassed_h | None:
        """"""
        if isinstance(passed, type):
            type_passed = passed
        else:
            type_passed = type(passed)

        if (type_wanted in self) and (type_passed in self[type_wanted]):
            return self[type_wanted][type_passed]

        if type_passed is str:
            return self.__class__._NewFromStr

        return None
