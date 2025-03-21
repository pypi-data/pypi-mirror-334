from rewrite import ExecutionContext, Recipe, TreeVisitor
from rewrite.python import PythonVisitor
from rewrite.python.tree import Space


class PythonTestRecipe(Recipe):
    """
    A recipe to test recipe authorship and running
    """

    def get_visitor(self) -> TreeVisitor:
        class Visitor(PythonVisitor):
            def visit_space(self, space: Space, loc: Space.Location, p: ExecutionContext) -> Space:
                if space.comments:
                    return space.with_comments([tc.with_text(" " + tc.text.strip()) for tc in space.comments])
                return space

        return Visitor()
