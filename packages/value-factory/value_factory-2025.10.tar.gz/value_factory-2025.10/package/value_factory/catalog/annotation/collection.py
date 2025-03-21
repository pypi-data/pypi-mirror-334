"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2025
SEE COPYRIGHT NOTICE BELOW
"""

import types as t
import typing as h

from value_factory.extension.hint import HintComponents, hint_h, hint_raw_h
from value_factory.task.casting import NewCastValue
from value_factory.type.annotation import annotation_a
from value_factory.type.hint import hint_t

sequence_h = list | set | tuple


class collection_t(annotation_a):
    """
    lengths: negative means any length.
    """

    ACCEPTED_TYPES: h.ClassVar[hint_h] = sequence_h

    stripe: hint_raw_h
    items_types: tuple[hint_t, ...]
    lengths: int | tuple[int, ...]

    @property
    def accepts_any_length(self) -> bool:
        """"""
        return isinstance(self.lengths, int) and (self.lengths < 0)

    def __init__(
        self,
        /,
        *,
        stripe: hint_raw_h = sequence_h,
        items_types: hint_h | h.Sequence[hint_h] = object,
        lengths: int | h.Sequence[int] = -1,
    ) -> None:
        """
        items_types: h.Any cannot be used as default since it cannot be used in
        isinstance.
        """
        accepted_types = self.__class__.ACCEPTED_TYPES
        if stripe is accepted_types:
            self.stripe = accepted_types
        else:
            origin, arguments, _ = HintComponents(stripe)
            if issubclass(origin, accepted_types):
                self.stripe = origin
            else:
                assert origin is t.UnionType
                if all(issubclass(_, accepted_types) for _ in arguments):
                    self.stripe = stripe
                else:
                    raise TypeError(f"Type {stripe} invalid.")

        if not isinstance(items_types, h.Sequence):
            items_types = (items_types,)
        self.items_types = tuple(hint_t.New(_) for _ in items_types)

        if isinstance(lengths, h.Sequence):
            assert self.items_types.__len__() == 1
            assert all(_ >= 0 for _ in lengths)
            self.lengths = tuple(sorted(lengths))
        else:
            assert (self.items_types.__len__() == 1) or (
                self.items_types.__len__() == lengths
            )
            self.lengths = lengths

    def __call__(self, value: h.Any, /) -> bool:
        """"""
        if not isinstance(value, self.stripe):
            return False

        n_values = value.__len__()
        if (
            isinstance(self.lengths, int)
            and (self.lengths >= 0)
            and (n_values != self.lengths)
        ) or (isinstance(self.lengths, h.Sequence) and (n_values not in self.lengths)):
            return False

        if self.items_types.__len__() > 1:
            items_types = self.items_types
        else:
            items_types = n_values * self.items_types
        for element, hint in zip(value, items_types, strict=True):
            issues = NewCastValue(element, hint, only_check_validity=True)
            if issues.__len__() > 0:
                return False

        return True

    def __str__(self) -> str:
        """"""
        if self.items_types.__len__() > 1:
            items_types = " or ".join(map(str, self.items_types))
        else:
            items_types = self.items_types[0]

        if self.accepts_any_length:
            lengths = "..."
        elif isinstance(self.lengths, int):
            lengths = self.lengths
        else:
            lengths = " or ".join(map(str, self.lengths))

        return f"{self.__class__.ACCEPTED_TYPES}[{items_types} x {lengths}]"

    __repr__ = __str__


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
