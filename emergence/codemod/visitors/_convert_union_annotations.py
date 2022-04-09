from __future__ import annotations

from typing import Sequence, cast

import libcst as cst
import libcst.matchers as m
from libcst.codemod import CodemodContext, ContextAwareTransformer

from emergence._utils import reduce

ELEMENT_MATCHER = m.SubscriptElement(
    slice=m.Index(
        value=m.SaveMatchedNode(m.DoNotCare(), name="type"),
    ),
)

OPTIONAL_MATCHER = m.Subscript(
    value=m.Name("Optional"),
    slice=(ELEMENT_MATCHER,),
)

UNION_MATCHER = m.Subscript(
    value=m.Name("Union"),
    slice=(
        m.SaveMatchedNode(
            m.AtLeastN(ELEMENT_MATCHER, n=1),
            name="types",
        ),
    ),
)


class ConvertUnionAnnotationsVisitor(ContextAwareTransformer):
    _in_annotation: bool

    def __init__(self, context: CodemodContext) -> None:
        super().__init__(context)
        self._in_annotation = False

    def visit_Annotation(self, node: cst.Annotation) -> bool | None:
        self._in_annotation = True
        return super().visit_Annotation(node)

    def leave_Annotation(
        self,
        original_node: cst.Annotation,
        updated_node: cst.Annotation,
    ) -> cst.Annotation:
        self._in_annotation = False
        return super().leave_Annotation(original_node, updated_node)

    def leave_Subscript(
        self,
        _original_node: cst.Subscript,
        updated_node: cst.Subscript,
    ) -> cst.BaseExpression:
        if not self._in_annotation:
            # Not inside an annotation, noop
            return updated_node

        if match := m.extract(updated_node, OPTIONAL_MATCHER):
            # Optional annotation, replace with None union
            return cst.BinaryOperation(
                left=cst.ensure_type(match["type"], cst.BaseExpression),
                operator=cst.BitOr(),
                right=cst.Name("None"),
            )

        if match := m.extract(updated_node, UNION_MATCHER):
            # Union annotation, replace with chained OR expression
            return reduce(
                (
                    cst.ensure_type(
                        cst.ensure_type(node, cst.SubscriptElement).slice, cst.Index
                    ).value
                    for node in cast(Sequence[cst.CSTNode], match["types"])
                ),
                lambda expr, v: cst.BinaryOperation(
                    left=expr,
                    operator=cst.BitOr(),
                    right=v,
                ),
            )

        return updated_node
