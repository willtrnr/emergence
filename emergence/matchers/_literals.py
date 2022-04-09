from __future__ import annotations

import ast

import libcst.matchers as m

NONE = m.Name("None")

TRUE = m.Name("True")
FALSE = m.Name("False")

BOOL = m.OneOf(TRUE, FALSE)

EMPTY_STRING = m.SimpleString(m.MatchIfTrue(lambda v: ast.literal_eval(v) == ""))

EMPTY_COLLECTION = m.OneOf(
    m.List(elements=()),
    m.Dict(elements=()),
    m.Tuple(elements=()),
    m.Set(elements=()),
    m.Call(
        func=m.OneOf(
            m.Name("list"),
            m.Name("dict"),
            m.Name("tuple"),
            m.Name("set"),
        ),
        args=(),
    ),
    EMPTY_STRING,
)

ZERO_INT = m.Integer(m.MatchIfTrue(lambda v: ast.literal_eval(v) == 0))
ZERO_FLOAT = m.Float(m.MatchIfTrue(lambda v: ast.literal_eval(v) == 0))

ZERO = m.OneOf(
    ZERO_INT,
    ZERO_FLOAT,
)

FALSEY_LITERAL = m.OneOf(
    NONE,
    FALSE,
    ZERO,
    EMPTY_COLLECTION,
)
