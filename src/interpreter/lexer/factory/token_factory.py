from typing import Tuple, Optional

from src.interpreter.input.string_stream import PeekableStream
from src.interpreter.lexer.token import Token


class TokenFactory:
    def __init__(self, stream: PeekableStream):
        self.__stream = stream

    @property
    def _peekable_stream(self) -> PeekableStream:
        return self.__stream

    def query(self, step: int) -> Tuple[bool, str]:
        return self._peekable_stream.peek(step)

    def match(self) -> Tuple[int, Optional[Token]]:
        raise NotImplemented(f'{self.match.__name__} is not implemented in {type(self).__name__}')
