from __future__ import annotations

from libcst.codemod import CodemodTest

from emergence.codemod.visitors._convert_union_annotations import (
    ConvertUnionAnnotationsVisitor,
)


class TestCodemodConvertUnionAnnotations(CodemodTest):
    TRANSFORM = ConvertUnionAnnotationsVisitor

    def test_optional(self) -> None:
        before = """
            bar: Optional[FooBar] = None

            def foo(a: Optional[int]) -> Optional["FooBar"]:
                pass
        """
        after = """
            bar: FooBar | None = None

            def foo(a: int | None) -> "FooBar" | None:
                pass
        """
        self.assertCodemod(before, after)

    def test_union(self) -> None:
        before = """
            bar: Union[FooBar, Union[str, bytes]] = None

            def foo(a: Union[str, int]) -> Union["FooBar", str]:
                pass
        """
        after = """
            bar: FooBar | str | bytes = None

            def foo(a: str | int) -> "FooBar" | str:
                pass
        """
        self.assertCodemod(before, after)
