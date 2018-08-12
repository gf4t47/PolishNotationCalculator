from interpreter.parser.node.node import AstNode
from src.interpreter.visitor.enviroment import VariableEnviroment
from src.operators import op_calc_map
from src.interpreter.parser.node.binary import BinaryOp
from src.interpreter.parser.node.factory import Num, Variable
from src.interpreter.visitor.node_visitor import NodeVisitor


# noinspection PyMethodMayBeStatic,PyPep8Naming
class Calculator(NodeVisitor):
    def __init__(self, tree: AstNode, env: VariableEnviroment):
        self._ast = tree
        self.global_env = env

    @property
    def ast_tree(self):
        return self._ast

    @property
    def global_env(self):
        return self._global_env

    @global_env.setter
    def global_env(self, val: VariableEnviroment):
        self._global_env = val

    def visit_Num(self, node: Num)->int:
        return node.value

    def visit_Variable(self, node: Variable)->int:
        return self.global_env.lookup(node.name)

    def visit_BinaryOp(self, node: BinaryOp):
        op = node.op
        left_val = self.visit(node.left_expr)
        right_val = self.visit(node.right_expr)
        return op_calc_map[op.value](left_val, right_val)

    def evaluate(self):
        return self.visit(self.ast_tree)