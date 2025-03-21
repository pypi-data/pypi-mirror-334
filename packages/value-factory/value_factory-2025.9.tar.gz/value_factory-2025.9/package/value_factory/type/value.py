import collections.abc as c
import dataclasses as d
import typing as h

from logger_36 import L
from value_factory.catalog.factory import ATOMIC_FACTORIES
from value_factory.constant.console import TREE_DEPTH_MARGIN
from value_factory.constant.value import UNSET
from value_factory.extension.hint import hint_h
from value_factory.type.hint import hint_t


@d.dataclass(slots=True, repr=False, eq=False)
class _node_t:
    """
    Leave elements to the tree.
    node_value: Value (before or after cast) for leaves, UNSET for non-leaf nodes.
    """

    type: type
    node_value: h.Any = UNSET


@d.dataclass(slots=True, repr=False, eq=False)
class value_t(_node_t):
    elements: tuple[h.Self, ...] | None = None

    @property
    def is_leaf(self) -> bool:
        """"""
        return self.elements is None

    @property
    def value(self) -> h.Any:
        """"""
        if self.is_leaf:
            return self.node_value

        return self.type(_.value for _ in self.elements)

    @classmethod
    def New(cls, value: h.Any, /) -> h.Self:
        """"""
        if isinstance(value, c.Mapping):
            elements = tuple(map(cls.New, value.items()))
            return cls(type=type(value), elements=elements)

        if isinstance(value, c.Sequence) and not isinstance(value, str):
            elements = tuple(map(cls.New, value))
            return cls(type=type(value), elements=elements)

        return cls(type=type(value), node_value=value)

    def Cast(self, hint: hint_h | hint_t, /) -> list[str]:
        """"""
        assert not L.has_staged_issues

        if not isinstance(hint, hint_t):
            hint = hint_t.New(hint)

        self._Cast(hint)

        return L.PopIssues(should_remove_context=True)

    def _Cast(self, hint_node: hint_t, /) -> None:
        """"""
        if L.has_staged_issues:
            return

        hn_type = hint_node.type
        assert hn_type is not Ellipsis

        if hint_node.is_universal:
            self._CheckConformity(hint_node)
        #
        elif hint_node.only_matches_none:
            # None is not supposed to have annotations. They are ignored if it does.
            if self.node_value is not None:
                L.StageIssue("Invalid value", actual=self.value, expected=None)
        #
        elif hint_node.is_leaf:
            # If self is not a leaf, the type hint does not fully specify valid values.
            # So, the procedure cannot be more specific than for the case where self is
            # also a leaf.
            if issubclass(self.type, hn_type):
                self._CheckConformity(hint_node)
            else:
                self._CastNode(hint_node)
        #
        elif hint_node.is_union:
            self._CastUnion(hint_node)
        #
        elif hint_node.is_literal:
            self._CastLiteral(hint_node)
        #
        # For then on, hint_node is a sequence or a mapping...
        elif self.is_leaf:  # ... so this is an invalid case.
            L.StageIssue(
                "Invalid value",
                actual=self.node_value,
                expected=f"Collection of type {hn_type.__name__}",
                expected_op=":",
            )
        #
        elif hint_node.is_sequence:
            self._CastSequence(hint_node)
        #
        elif hint_node.is_mapping:
            self._CastMapping(hint_node)
        else:
            raise ValueError(f"Unhandled hint type {hint_node.type}.")

    def _CastNode(self, hint_node: hint_t, /) -> None:
        """"""
        hn_type = hint_node.type

        NewConverted = ATOMIC_FACTORIES.Converter(self.type, hn_type)
        if NewConverted is None:
            L.StageIssue(
                f"No {self.type.__name__}->{hn_type.__name__} "
                f"type conversion for {self.value}"
            )
            return

        try:
            converted = NewConverted(self.value)
        except (SyntaxError, ValueError):
            L.StageIssue(
                f"Type conversion {self.type.__name__}->{hn_type.__name__} "
                f"failed for {self.value}"
            )
        else:
            if isinstance(converted, hn_type):
                self.type = hn_type
                if self.is_leaf:
                    self.node_value = converted
                self._CheckConformity(hint_node)
            else:
                L.StageIssue(
                    f"Type conversion {self.type.__name__}->{hn_type.__name__} "
                    f"failed for {self.value}"
                )

    def _CastLiteral(self, hint_node: hint_t, /) -> None:
        """
        Note: There is no need to check conformity if the value is among the choices.
        """
        expected = f"Value among {str(hint_node.literal_s)[1:-1]}"

        if not self.is_leaf:
            L.StageIssue(
                "Invalid value", actual=self.value, expected=expected, expected_op=":"
            )
            return

        if self.node_value in hint_node.literal_s:
            return

        self._CastUnion(hint_node)
        if L.has_staged_issues:
            return

        if self.node_value not in hint_node.literal_s:
            L.StageIssue(
                "Invalid value",
                actual=self.node_value,
                expected=expected,
                expected_op=":",
            )

    def _CastUnion(self, hint_node: hint_t, /) -> None:
        """"""
        issues = []
        for element in hint_node.elements:
            self._Cast(element)
            if L.has_staged_issues:
                issues.extend(L.PopIssues(should_remove_context=True))
            else:
                self._CheckConformity(hint_node)
                return

        for issue in issues:
            L.StageIssue(issue)

    def _CastSequence(self, hint_node: hint_t, /) -> None:
        """"""
        if not issubclass(self.type, c.Sequence):
            L.StageIssue(
                "Invalid value",
                actual=self.value,
                expected=f"Sequence of type {hint_node.type.__name__}",
                expected_op=":",
            )
            return

        hn_elements = hint_node.elements
        if hint_node.is_infinite:
            adjusted_hn_elements = self.elements.__len__() * (hn_elements[0],)
        elif self.elements.__len__() == hn_elements.__len__():
            adjusted_hn_elements = hn_elements
        else:
            L.StageIssue(
                f"Invalid number of element(s) in {self.value}",
                actual=self.elements.__len__(),
                expected=hn_elements.__len__(),
            )
            return

        for value, hint in zip(self.elements, adjusted_hn_elements, strict=True):
            value: value_t
            hint: hint_t
            value._Cast(hint)

        if not L.has_staged_issues:
            self._CheckConformity(hint_node)

    def _CastMapping(self, hint_node: hint_t, /) -> None:
        """"""
        if not issubclass(self.type, c.Mapping):
            L.StageIssue(
                "Invalid value",
                actual=self.value,
                expected=f"Mapping of type {hint_node.type.__name__}",
                expected_op=":",
            )
            return

        hn_key, hn_value = hint_node.elements

        for element in self.elements:
            key, value = element.elements
            key._Cast(hn_key)
            value._Cast(hn_value)

        if not L.has_staged_issues:
            self._CheckConformity(hint_node)

    def _CheckConformity(self, hint_node: hint_t, /) -> None:
        """"""
        if (nnts := hint_node.annotations) is None:
            return

        # TODO: Document the various returned values of callables ConformityReport. If
        #  bool, True means "passed"="is conform".
        value = self.value
        for ConformityReport in nnts:
            if not callable(ConformityReport):
                continue

            report = ConformityReport(value)
            if report is None:
                pass
            elif isinstance(report, bool):
                if not report:
                    L.StageIssue(
                        f'Value "{value}" did not pass conformity check '
                        f'"{ConformityReport}"'
                    )
            elif isinstance(report, h.Sequence) and all(
                isinstance(_, str) for _ in report
            ):
                for issue in report:
                    L.StageIssue(issue)

    def __str__(self) -> str:
        """"""
        return self._AsStr(0)

    __repr__ = __str__

    def _AsStr(self, depth: int, /) -> str:
        """"""
        if self.node_value is UNSET:
            value = ""
        else:
            value = f"={self.node_value}"
        type_as_str = f"{depth * TREE_DEPTH_MARGIN}{self.type.__name__}{value}"

        if self.is_leaf:
            elements = ""
        else:
            elements = "\n" + "\n".join(_._AsStr(depth + 1) for _ in self.elements)

        return f"{type_as_str}{elements}"
