import pytest

from src.interpreter.input.string_stream import MovableStream
from src.interpreter.lexer.lexer import Lexer
from src.interpreter.parser.token_stream import TokenStream
from src.interpreter.parser.parser import Parser


@pytest.mark.parametrize("expr", [
    '1',
    '( 1 )',
    '+ 1 1',
    '( + 1 1 )',
    '+ 1 1 1',
    '( + 1 1 1 )',
    '+ 1 ( + 1 1 1 )',
])
def test(expr):
    string = MovableStream(expr)
    lexer = Lexer(string)
    tokens = TokenStream(lexer)
    parser = Parser(tokens, False)
    ast = parser.parse()

    print(ast)
