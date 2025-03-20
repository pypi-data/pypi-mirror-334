"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2025
SEE COPYRIGHT NOTICE BELOW
"""

"""
Alternative: use of
https://beartype.readthedocs.io/en/latest/api_door/
but not until the On beartype.BeartypeStrategy is implemented.
"""

import collections.abc as c
import dataclasses as d
import re as r
import types as t
import typing as h

from value_factory.constant.console import TREE_DEPTH_MARGIN
from value_factory.extension.hint import UNION_TYPE, HintComponents, hint_h


@d.dataclass(slots=True, repr=False, eq=False)
class _node_t:
    """
    Leave the attribute "elements" to the tree.

    type:
    - Possible values (besides builtin types): None, h.Any, UNION_TYPE, Ellipsis,
    - For more coherence, None and Ellipsis values should be replaced with
      t.NoneType and t.EllipsisType.

    literal_s: the accepted (literal) values if the hint is a typing.Literal, None
    otherwise.
    """

    type: h.Any
    annotations: tuple[h.Any, ...] | None = None
    literal_s: tuple[h.Any, ...] | None = None

    @property
    def only_matches_none(self) -> bool:
        """"""
        return self.type is None

    @property
    def is_universal(self) -> bool:
        """"""
        return self.type is h.Any

    @property
    def is_literal(self) -> bool:
        """
        /!\\ Literals are also leaves in principle, but as implemented, they are not.
        This should be taken into account when dealing with the node types sequentially.
        """
        return self.literal_s is not None

    @property
    def is_str_literal(self) -> bool:
        """
        Literals with mixed types have a UNION_TYPE type.
        """
        return (self.type is str) and self.is_literal

    @property
    def is_sequence(self) -> bool:
        """
        "True" sequence, i.e. not an str.
        """
        return issubclass(self.type, c.Sequence) and (self.type is not str)

    @property
    def is_mapping(self) -> bool:
        """"""
        return issubclass(self.type, c.Mapping)

    @property
    def is_union(self) -> bool:
        """
        Literals are implemented as unions but are actually leaves.
        """
        return (self.type is UNION_TYPE) and (self.literal_s is None)

    def FirstAnnotationWithType(self, stripe: type, /) -> h.Any:
        """"""
        if self.annotations is None:
            return None

        for annotation in self.annotations:
            if isinstance(annotation, stripe):
                return annotation

        return None


@d.dataclass(slots=True, repr=False, eq=False)
class hint_t(_node_t):
    """
    elements: tuple if the hint is a container, None otherwise. In terms of tree
    structure, it plays the role of the (hint) node children.
    """

    elements: tuple[h.Self, ...] | None = None
    _is_infinite: bool | None = None
    _could_match_str: bool | None = None

    @property
    def could_match_str(self) -> bool:
        """"""
        if self._could_match_str is None:
            explicit = self.type is str
            implicit = self.is_union and any(_.type is str for _ in self.elements)

            self._could_match_str = explicit or implicit

        return self._could_match_str

    @property
    def is_leaf(self) -> bool:
        """"""
        return self.elements is None

    @property
    def is_infinite(self) -> bool:
        """
        Note: No check done => call only on sequences.
        """
        if self._is_infinite is None:
            n_elements = self.elements.__len__()

            explicit = (n_elements == 2) and (self.elements[1].type is Ellipsis)
            implicit = (n_elements == 1) and issubclass(self.type, (list, set))

            self._is_infinite = explicit or implicit

        return self._is_infinite

    @property
    def template(self) -> h.Any | dict[int, h.Any] | None:
        """"""
        if self.type is t.NoneType:
            return None

        if self.type is t.UnionType:
            return {_key: _elm.template for _key, _elm in enumerate(self.elements)}

        if self.elements is None:
            return self.type

        try:
            output = self.type(_elm.template for _elm in self.elements)
        except TypeError:
            output = None
        if output is not None:
            return output

        # TODO: Does it work all the time?
        if self.elements.__len__() == 1:
            # For example, self.type is typing.Sequence.
            return self.type[self.elements[0].template]

        # TODO: Can something better be done?
        return self.type

    @property
    def template_as_str(self) -> str:
        """"""
        output = (
            str(self.template)
            .replace(str(t.EllipsisType), "...")
            .replace("<class '", "")
            .replace("'>", "")
        )
        output = r.sub(r"{\d: ", "{", output, flags=r.ASCII)
        output = r.sub(r", \d:", " |", output, flags=r.ASCII)

        return output

    @classmethod
    def New(cls, hint: hint_h, /) -> h.Self:
        """
        Note that type hints cannot translate into hint trees with an OR-node having a
        child OR-node. For example: str | (int | float) is interpreted as str | int |
        float. This is important when creating a type selector for multi-type parameters
        since only direct child nodes are taken into account for widget creation, so
        these nodes must be types, not an OR subtree.
        """
        # Dealing with hint_additions_h first.
        if (hint is None) or (hint is t.NoneType):  # t.NoneType: from h.get_args.
            return cls(type=None)
        if hint is Ellipsis:
            return cls(type=Ellipsis)

        origin, arguments, nnts = HintComponents(hint)

        if arguments is None:
            return cls(type=origin, annotations=nnts)

        if origin is h.Literal:  # arguments=literal_s.
            stripes = set(map(type, arguments))
            if stripes.__len__() > 1:
                origin = UNION_TYPE
                elements = tuple(map(cls.New, stripes))
            else:
                origin = stripes.pop()
                elements = None
            return cls(
                type=origin, literal_s=arguments, elements=elements, annotations=nnts
            )

        return cls(
            type=origin, elements=tuple(map(cls.New, arguments)), annotations=nnts
        )

    def AddLiteral(self, value: h.Any, /) -> None:
        """
        /!\\ h.Literal does not accept any values. No such check is made here.
        """
        assert self.is_literal, self
        self.literal_s = tuple(sorted(self.literal_s + (value,)))

    def __str__(self) -> str:
        """"""
        return self._AsStr(0)

    __repr__ = __str__

    def _AsStr(self, depth: int, /) -> str:
        """"""
        stripe = getattr(self.type, "__name__", self.type)
        type_as_str = f"{depth * TREE_DEPTH_MARGIN}{stripe}"
        if self.literal_s is not None:
            type_as_str += ": " + " | ".join(
                map(
                    lambda _: f'"{_}"' if isinstance(_, str) else str(_), self.literal_s
                )
            )

        if self.is_leaf:
            elements = ""
        else:
            elements = "\n" + "\n".join(_._AsStr(depth + 1) for _ in self.elements)

        return f"{type_as_str}{elements}"


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
