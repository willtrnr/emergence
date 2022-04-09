from __future__ import annotations

import unittest

import libcst as cst
import libcst.matchers as m

from emergence.matchers import _literals


class TestMatchersLiterals(unittest.TestCase):
    def test_none(self) -> None:
        tree = cst.parse_expression("None")
        self.assertTrue(m.matches(tree, _literals.NONE))

    def test_true(self) -> None:
        tree = cst.parse_expression("True")
        self.assertTrue(m.matches(tree, _literals.TRUE))
        self.assertFalse(m.matches(tree, _literals.FALSE))
        self.assertTrue(m.matches(tree, _literals.BOOL))

    def test_false(self) -> None:
        tree = cst.parse_expression("False")
        self.assertFalse(m.matches(tree, _literals.TRUE))
        self.assertTrue(m.matches(tree, _literals.FALSE))
        self.assertTrue(m.matches(tree, _literals.BOOL))

    def test_empty_string(self) -> None:
        tree = cst.parse_expression("''")
        self.assertTrue(m.matches(tree, _literals.EMPTY_STRING))

        tree = cst.parse_expression('""')
        self.assertTrue(m.matches(tree, _literals.EMPTY_STRING))
