"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2025
SEE COPYRIGHT NOTICE BELOW
"""

import typing as h
from enum import Enum as enum_t
from pathlib import Path as pl_path_t

from logger_36.api.content import MessageWithActualExpected
from value_factory.extension.hint import hint_h


class kind_e(enum_t):
    document = 1
    folder = 2
    any = 3


class purpose_e(enum_t):
    input = 1
    output = 2
    any = 3


_KINDS = tuple(kind_e.__members__.keys())
_KIND_INITIALS = "".join(_[0] for _ in _KINDS)

_PURPOSES = tuple(purpose_e.__members__.keys())
_PURPOSE_INITIALS = "".join(_[0] for _ in _PURPOSES)


class path_t:
    """
    mandatory: If false, None will be considered a valid path value.
    """

    ACCEPTED_TYPES: h.ClassVar[hint_h] = pl_path_t

    kind: kind_e
    purpose: purpose_e
    mandatory: bool

    def __init__(
        self,
        /,
        *,
        kind: str | kind_e = kind_e.any,
        purpose: str | purpose_e = purpose_e.any,
        mandatory: bool = True,
    ) -> None:
        """
        kind: If str, can be d[...], f[...], or a[...].
        purpose: If str, can be i[...], o[...], or a[...].
        """
        self.kind = _NewStandard(
            kind, _KIND_INITIALS, _KINDS, kind_e, "Invalid path kind"
        )
        self.purpose = _NewStandard(
            purpose, _PURPOSE_INITIALS, _PURPOSES, purpose_e, "Invalid path purpose"
        )
        self.mandatory = mandatory

    def __call__(self, value: h.Any, /) -> bool:
        """
        None: Unspecified path.
        """
        if value is None:
            return not self.mandatory

        if not isinstance(value, self.__class__.ACCEPTED_TYPES):
            return False

        if self.purpose is not purpose_e.input:
            return True

        if value.exists():
            if self.kind is kind_e.any:
                if value.is_file() or value.is_dir():
                    return True
                return False

            if (self.kind is kind_e.document) and value.is_file():
                return True

            if (self.kind is kind_e.folder) and value.is_dir():
                return True

        return False


def _NewStandard(
    value: h.Any,
    standard_initials: str,
    standard_values: tuple[str, ...],
    standard_type: type[enum_t],
    error_message: str,
    /,
) -> enum_t:
    """"""
    if isinstance(value, str):
        index = standard_initials.index(value[0].lower())
        return standard_type[standard_values[index]]

    if isinstance(value, standard_type):
        return value

    raise ValueError(
        MessageWithActualExpected(
            error_message, actual=value, expected=" or ".join(standard_values)
        )
    )


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
