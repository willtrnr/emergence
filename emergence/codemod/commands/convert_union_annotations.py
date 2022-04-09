from __future__ import annotations

from libcst.codemod import CodemodCommand

from emergence.codemod.visitors import ConvertUnionAnnotationsVisitor


class ConvertUnionAnnotationsCommand(ConvertUnionAnnotationsVisitor, CodemodCommand):
    DESCRIPTION = "Convert Union and Optional annotations to OR syntax."
