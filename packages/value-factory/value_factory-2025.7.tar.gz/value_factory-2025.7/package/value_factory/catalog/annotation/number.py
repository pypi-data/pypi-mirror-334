"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2025
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d
import typing as h

from logger_36 import L
from value_factory.extension.hint import hint_h

number_h = int | float


@d.dataclass(slots=True, repr=False, eq=False)
class number_t:
    INFINITY_NEG: h.ClassVar[float] = -float("inf")
    INFINITY_POS: h.ClassVar[float] = float("inf")
    INFINITE_PRECISION: h.ClassVar[float] = 0.0

    type: hint_h = number_h
    min: number_h = INFINITY_NEG
    max: number_h = INFINITY_POS
    min_inclusive: bool = True
    max_inclusive: bool = True
    precision: number_h = INFINITE_PRECISION

    def __post_init__(self) -> None:
        """"""
        n_staged_issues = L.n_staged_issues
        stripe = self.__class__

        if (self.min != stripe.INFINITY_NEG) and not isinstance(
            self.min, number_h.__args__
        ):
            L.StageIssue(
                f"Invalid type for min value {self.min}",
                actual=type(self.min).__name__,
                expected=number_h,
            )
        if (self.max != stripe.INFINITY_POS) and not isinstance(
            self.max, number_h.__args__
        ):
            L.StageIssue(
                f"Invalid type for max value {self.max}",
                actual=type(self.max).__name__,
                expected=number_h,
            )
        if (self.precision != stripe.INFINITE_PRECISION) and not isinstance(
            self.precision, number_h.__args__
        ):
            L.StageIssue(
                f"Invalid type for precision {self.precision}",
                actual=type(self.precision).__name__,
                expected=number_h,
            )
        if self.precision < 0:
            L.StageIssue(f"Invalid, negative precision {self.precision}")
        if (self.min > self.max) or (
            (self.min == self.max) and not (self.min_inclusive and self.max_inclusive)
        ):
            if self.min_inclusive:
                opening = "["
            else:
                opening = "]"
            if self.max_inclusive:
                closing = "]"
            else:
                closing = "["
            L.StageIssue(
                f"Empty value interval {opening}{self.min},{self.max}{closing}"
            )

        if L.n_staged_issues > n_staged_issues:
            issues = L.PopIssues()
            raise ValueError("\n".join(issues))

    def __call__(self, value: h.Any, /) -> bool:
        """"""
        if not isinstance(value, self.type):
            return False

        if self.min <= value <= self.max:
            if ((value == self.min) and not self.min_inclusive) or (
                (value == self.max) and not self.max_inclusive
            ):
                return False

            if (self.precision != self.__class__.INFINITE_PRECISION) and (
                self.precision * int(value / self.precision) != value
            ):
                return False

            return True

        return False


"""
COPYRIGHT NOTICE

This software is governed by the CeCILL  license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights,  and the successive licensors  have only  limited
liability.

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or
data to be ensured and,  more generally, to use and operate it in the
same conditions as regards security.

The fact that you are presently reading this means that you have had
knowledge of the CeCILL license and that you accept its terms.

SEE LICENCE NOTICE: file README-LICENCE-utf8.txt at project source root.

This software is being developed by Eric Debreuve, a CNRS employee and
member of team Morpheme.
Team Morpheme is a joint team between Inria, CNRS, and UniCA.
It is hosted by the Centre Inria d'Université Côte d'Azur, Laboratory
I3S, and Laboratory iBV.

CNRS: https://www.cnrs.fr/index.php/en
Inria: https://www.inria.fr/en/
UniCA: https://univ-cotedazur.eu/
Centre Inria d'Université Côte d'Azur: https://www.inria.fr/en/centre/sophia/
I3S: https://www.i3s.unice.fr/en/
iBV: http://ibv.unice.fr/
Team Morpheme: https://team.inria.fr/morpheme/
"""
