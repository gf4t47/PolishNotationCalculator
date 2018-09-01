import pytest

from src.interpreter.visitor.environment import VariableEnvironment
from src.main import interpreter_calc
from src.main import stack_calc


@pytest.mark.parametrize('env', [
    {
        'x': -1,
        'ya': 0,
        'zbc': 1,
    },
])
@pytest.mark.parametrize("expr, expected", [
    ('-1', -1),
    ('+ 1 -1', 0),
    ('+ x -1', -2),
    ('+ ya 1', 1),
    ('+ zbc 1', 2),
])
@pytest.mark.parametrize("binary_op", [False, True])
@pytest.mark.parametrize('calc', [stack_calc, interpreter_calc])
def test_variable(expr, expected, binary_op, calc, env):
    assert expected == calc(expr, binary_op, VariableEnvironment(env))


@pytest.mark.parametrize('env', [
    {
        'x': -1,
        'X': 0,
        'y': 1,
        'Y': 2
    },
])
@pytest.mark.parametrize("expr, expected", [
    ('+ x -1', -2),
    ('+ X 1', 1),
    ('+ y 1', 2),
    ('+ Y 1', 3),
    ('+ x y', 0),
    ('+ X Y', 2),
    ('+ x X', -1),
    ('+ y Y', 3),
])
@pytest.mark.parametrize("binary_op", [False, True])
@pytest.mark.parametrize('calc', [stack_calc, interpreter_calc])
def test_variable_case(expr, expected, binary_op, calc, env):
    assert expected == calc(expr, binary_op, VariableEnvironment(env))


@pytest.mark.parametrize('env', [
    {
        'x': 1,
        'y': 2,
        'z': 3,
    },
])
@pytest.mark.parametrize("expr, expected", [
    ('1', 1),
    ('+ 1 1', 2),
    ('+ x 1', 2),
    ('= x 0 + x 1', 1),
    ('+ (= x -10 x) (= y -20 y)', -30),
    ('+ (+ x y) z', 6),
    ('= x 0 = y 0 = z 0 + (+ x y) z', 0),
])
@pytest.mark.parametrize("binary_op", [False, True])
@pytest.mark.parametrize('calc', [interpreter_calc])
def test_assignment(expr, expected, binary_op, calc, env):
    assert expected == calc(expr, binary_op, VariableEnvironment(env))


@pytest.mark.parametrize('env', [
    {
        'x': 1,
        'y': 2,
        'z': 3,
    },
])
@pytest.mark.parametrize("expr, expected", [
    ('= x y + x 1', 3),
    ('= x z + x 1', 4),
])
@pytest.mark.parametrize("binary_op", [False, True])
@pytest.mark.parametrize('calc', [interpreter_calc])
def test_variable_assignment(expr, expected, binary_op, calc, env):
    assert expected == calc(expr, binary_op, VariableEnvironment(env))


@pytest.mark.parametrize('env', [
    {
        'x': 1,
        'y': 2,
        'z': 3,
    },
])
@pytest.mark.parametrize("expr, expected", [
    ('= x (+ 1 -1) + x 1', 1),
    ('= x (/ 4 2) + x 1', 3),
])
@pytest.mark.parametrize("binary_op", [False, True])
@pytest.mark.parametrize('calc', [interpreter_calc])
def test_expr_assignment(expr, expected, binary_op, calc, env):
    assert expected == calc(expr, binary_op, VariableEnvironment(env))


@pytest.mark.parametrize('env', [
    {
        'x': 1,
        'y': 2,
        'z': 3,
    },
])
@pytest.mark.parametrize("expr, expected", [
    ('= y 10 = x (+ 1 y) (+ x 1)', 12),
    ('= x (/ 4 z) + x 1', 2),
])
@pytest.mark.parametrize("binary_op", [False, True])
@pytest.mark.parametrize('calc', [interpreter_calc])
def test_var_expr_assignment(expr, expected, binary_op, calc, env):
    assert expected == calc(expr, binary_op, VariableEnvironment(env))


@pytest.mark.parametrize('env', [
    {
        'x': 1,
        'y': 1,
        'z': 1,
    },
])
@pytest.mark.parametrize("expr, expected", [
    ('1', 1),
    ('+ 1 1', 2),
    ('+ x 1', 2),
    ('= x 0 + x 1', 1),
    ('= x 10 + x (+ x y)', 21),
    ('= x 10 = y 10 + x (= x 0 + x y)', 20),
    ('+ (= x 10 = y 10 + x (= x 0 + (= y 0 + x y) y)) x', 21),
    ('+ (= x 10 = y 10 + (= x 7 (= x 6 x)) (= x 0 (+ (= y 0 + x y) y))) x', 17),
])
@pytest.mark.parametrize("binary_op", [False, True])
@pytest.mark.parametrize('calc', [interpreter_calc])
def test_scoped_assignment(expr, expected, binary_op, calc, env):
    assert expected == calc(expr, binary_op, VariableEnvironment(env))


@pytest.mark.parametrize('env', [
    {
        'x': 1,
        'y': 1,
        'z': 1,
    },
])
@pytest.mark.parametrize("expr, expected", [
    ('+ x ( = x (+ x 1) x )', 3)
])
@pytest.mark.parametrize("binary_op", [False, True])
@pytest.mark.parametrize('calc', [interpreter_calc])
def test_scoped_self_assignment(expr, expected, binary_op, calc, env):
    assert expected == calc(expr, binary_op, VariableEnvironment(env))
