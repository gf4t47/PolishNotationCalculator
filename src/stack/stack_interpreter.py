import functools
import logging
import sys

from attr import dataclass

from src.interpreter.visitor.environment import VariableEnvironment
from src.operators import calc_op_map

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


@dataclass
class NumberToken:
    value: int


NumberToken.terminal = NumberToken(-1)


class StackInterpreter:
    def __init__(self: object, binary_op: bool, env: VariableEnvironment) -> None:
        self.__number_stack = []
        self._global_env = env
        self._binary_op = binary_op

    @property
    def _global_env(self)-> VariableEnvironment:
        return self.__global_env

    @_global_env.setter
    def _global_env(self, val: VariableEnvironment)->None:
        self.__global_env = val

    @property
    def _number_stack(self):
        return self.__number_stack

    def _binary_op_calc(self, char):
        left = self._number_stack.pop()
        right = self._number_stack.pop()
        # logging.debug(f'{char} {left.value} {right.value}')
        return calc_op_map[char](left.value, right.value)

    def _free_op_calc(self, char):
        operands = []

        while len(self._number_stack) > 0:
            cur_token = self._number_stack.pop()
            if cur_token is not NumberToken.terminal:
                operands.append(cur_token.value)
            else:
                break

        # logging.debug(f'{char} {operands}')
        return functools.reduce(calc_op_map[char], operands)

    def _calc(self, char):
        capability = len(self._number_stack)
        if capability < 2:
            raise BufferError(f'Not enough operands, length = {capability}')
        return self._binary_op_calc(char) if self._binary_op else self._free_op_calc(char)

    def evaluate(self, expression: str) -> int:
        """
        :type expression: str
        :param expression: input expression
        :rtype: int
        :return:
        """
        index = len(expression) - 1
        while index >= 0:
            cur = expression[index]
            if cur.isspace() or cur == '(':  # ignore character
                index -= 1
            elif cur in calc_op_map:
                ret = self._calc(cur)
                self._number_stack.append(NumberToken(ret))
                index -= 1
            elif cur.isdigit():
                num_str = ''
                while index >= 0 and cur.isdigit():
                    num_str += cur
                    index -= 1
                    cur = expression[index]
                if cur == '-':
                    index -= 1
                    num = int(num_str[::-1]) * -1
                else:
                    num = int(num_str[::-1])
                self._number_stack.append(NumberToken(num))
            elif cur.isalpha():
                var_str = ''
                while index >= 0 and cur.isalpha():
                    var_str += cur
                    index -= 1
                    cur = expression[index]
                self._number_stack.append(NumberToken(self._global_env.lookup(var_str[::-1])))
            elif cur == ')':
                if not self._binary_op:
                    self._number_stack.append(NumberToken.terminal)
                index -= 1
            else:
                raise SyntaxError(f'unrecognized character: {cur}')

        return self._number_stack.pop().value
