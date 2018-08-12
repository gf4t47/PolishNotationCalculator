import pytest

from src.main import stack_calc
from src.main import interpreter_calc


@pytest.mark.parametrize("expr, expected", [
    ('1', 1),
    ('( 1 )', 1),
    ('(( 1 ))', 1),
    ('+ 1 1', 2),
    ('( + 1 1 )', 2),
    ('+ 1 1 1', 3),
    ('( + 1 1 1 )', 3),
    ('+ 1 ( + 1 1 1 )', 4),
    ('(((( + 1 ( + 1 1 1 )))))', 4),
    ('+ 1 ( + 1 1 1 ) 1 1', 6),
    ('+ 1 ( + 1 1 1 ) (- 1 1) 1 1', 6),
    ('(((( + 1 ( + 1 (( + (1) 1 ))) 1))))', 5),
])
@pytest.mark.parametrize("binary_op", [False])
@pytest.mark.parametrize('calc', [stack_calc, interpreter_calc])
def test_free_op(expr, expected, binary_op, calc):
    assert expected == calc(expr, binary_op)


@pytest.mark.parametrize("expr, expected", [
    ('1', 1),
    ('( 1 )', 1),
    ('(( 1 ))', 1),
    ('+ 1 1', 2),
    ('( + 1 1 )', 2),
    ('+ (+ 1 1) 1', 3),
    ('+ 1 (+ 1 1)', 3),
    ('(+ (+ 1 1) (+ 1 1) )', 4),
    ('(+ (((+ 1 1))) (+ (1) 1) )', 4),
    ('(+ (+ (+ 1 1) (+ 1 1) ) (+ 1 1))', 6),
])
@pytest.mark.parametrize("binary_op", [True])
@pytest.mark.parametrize('calc', [stack_calc, interpreter_calc])
def test_binary_op(expr, expected, binary_op, calc):
    assert expected == calc(expr, binary_op)