from src.interpreter.parser.node.binary import CalcBinary
from src.interpreter.parser.node.factory import Variable
from src.interpreter.parser.node.node import AstNode
from src.interpreter.visitor.environment import VariableEnvironment
from src.interpreter.visitor.calculator import Calculator
from src.operators import calc_node


# noinspection PyPep8Naming
class Simplifier(Calculator):
    def visit_Variable(self, node: Variable, env: VariableEnvironment) -> (int, AstNode):
        found = env.lookup(node.name)
        return found if found is not None else node

    def visit_CalcOp(self, node: CalcBinary, env: VariableEnvironment) -> (int, AstNode):
        op = node.op
        left_node = self.visit(node.left_expr, env)
        right_node = self.visit(node.right_expr, env)
        return calc_node(op, left_node, right_node)
