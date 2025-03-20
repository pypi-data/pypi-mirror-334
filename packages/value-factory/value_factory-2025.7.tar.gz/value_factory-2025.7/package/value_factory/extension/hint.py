"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2025
SEE COPYRIGHT NOTICE BELOW
"""

import types as t
import typing as h

"""
t.GenericAlias: e.g., tuple[int, ...].

Hint additions:
    - Ellipsis: e.g., in tuple[int, ...].
    - None: for t.UnionType, e.g. in int | None.
"""

hint_raw_h = h.Any | type | t.GenericAlias | t.UnionType
hint_annotated_t = type(h.Annotated[object, None])
hint_h = hint_raw_h | hint_annotated_t

UNION_TYPE = h.Union


def HintComponents(
    hint: hint_h, /
) -> tuple[h.Any | type, tuple[h.Any, ...] | None, tuple[h.Any, ...] | None]:
    """"""
    if (origin := h.get_origin(hint)) is h.Annotated:
        nnts = tuple(hint.__metadata__)
        hint = hint.__args__[0]

        if (origin := h.get_origin(hint)) is None:
            origin = hint
    else:
        if origin is None:
            origin = hint  # Not necessarily a type; e.g., can be h.Any.
        nnts = None

    if origin is t.UnionType:
        origin = UNION_TYPE

    arguments = h.get_args(hint)  # /!\\ Returns t.NoneType for None.
    if arguments.__len__() == 0:
        arguments = None

    return origin, arguments, nnts


def OptionsOfLiteral(passed: h.Any, /) -> tuple[h.Any, ...] | None:
    """"""
    if h.get_origin(passed) is h.Literal:
        return h.get_args(passed)

    return None


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
