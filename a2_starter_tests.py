from expression_tree import ExprTree, construct_from_list
from expression_tree_puzzle import ExpressionTreePuzzle
from solver import BfsSolver, DfsSolver

def test_expression_tree_eval_doctest() -> None:
    """Test ExprTree.eval on the provided doctest"""
    exp_t = ExprTree('+', [ExprTree(3, []),
                           ExprTree('*', [ExprTree('x', []),
                                          ExprTree('y', [])]),
                           ExprTree('x', [])])
    look_up = {}
    exp_t.populate_lookup(look_up)
    assert exp_t.eval(look_up) == 3

    look_up['x'] = 7
    look_up['y'] = 3
    assert exp_t.eval(look_up) == 31

    exp_t = ExprTree('+', [ExprTree('*', [ExprTree(7, []),
                                          ExprTree('+',
                                                   [ExprTree(6, []),
                                                    ExprTree('z', [])])]),
                           ExprTree(5, [])])
    look_up = {}
    exp_t.populate_lookup(look_up)
    assert exp_t.eval(look_up) == 47

    look_up['z'] = 111
    assert exp_t.eval(look_up) == 824

    exp_t = ExprTree(None, [])
    look_up = {}
    exp_t.populate_lookup(look_up)
    assert exp_t.eval(look_up) == 0

    exp_t = ExprTree('*', [ExprTree(4, []), ExprTree(5, [])])
    look_up = {}
    exp_t.populate_lookup(look_up)
    assert exp_t.eval(look_up) == 20


def test_expression_tree_populate_lookup_doctest() -> None:
    """Test ExprTree.populate_lookup on the provided doctest"""
    expr_t = ExprTree('a', [])
    look_up = {}
    expr_t.populate_lookup(look_up)
    assert look_up['a'] == 0
    assert len(look_up) == 1

    expr_t = ExprTree('+', [ExprTree(3, []),
                            ExprTree('*', [ExprTree('x', []),
                                           ExprTree('y', [])]),
                            ExprTree('x', [])])
    look_up = {}
    expr_t.populate_lookup(look_up)
    assert look_up['x'] == 0
    assert look_up['y'] == 0
    assert len(look_up) == 2

    exp_t = ExprTree(None, [])
    look_up = {}
    exp_t.populate_lookup(look_up)
    assert len(look_up) == 0


def test_expression_tree_construct_from_list_doctest() -> None:
    """Test ExprTree.construct_from_list on the provided doctest"""
    # This test relies on ExprTree.__str__ working correctly.
    example = []
    exp_t = construct_from_list(example)
    assert str(exp_t) == '()'

    example = [[5]]
    exp_t = construct_from_list(example)
    assert isinstance(exp_t, ExprTree)
    assert str(exp_t) == '5'

    example = [['+'], [3, 'a']]
    exp_t = construct_from_list(example)
    assert isinstance(exp_t, ExprTree)
    assert str(exp_t) == '(3 + a)'

    example = [['+'], [3, '*', 'a', '+'], ['a', '+'], [5, 'c'], [2, 'd']]
    exp_t = construct_from_list(example)
    assert str(exp_t) == '(3 + (a * (2 + d)) + a + (5 + c))'


def test_expression_tree_substitute_doctest() -> None:
    """Test ExprTree.substitute on the provided doctest"""
    # This test relies on ExprTree.__str__ working correctly.
    exp_t = ExprTree('a', [])
    exp_t.substitute({'a': 1})
    assert str(exp_t) == '1'

    exp_t = ExprTree('*', [ExprTree('a', []),
                           ExprTree('*', [ExprTree('a', []),
                                          ExprTree(1, [])])])
    exp_t.substitute({'a': 2, '*': '+'})
    assert str(exp_t) == '(2 + (2 + 1))'


def test_expression_tree_str_doctest() -> None:
    """Test ExprTree.__str__ on the provided doctest"""

    exp_t = ExprTree('+', [ExprTree('a', []),
                           ExprTree('b', []),
                           ExprTree(3, [])])
    assert str(exp_t) == '(a + b + 3)'

    exp_t = ExprTree(None, [])
    assert str(exp_t) == '()'

    exp_t = ExprTree(5, [])
    assert str(exp_t) == '5'

    exp_t = ExprTree('+', [ExprTree('*', [ExprTree(7, []),
                                          ExprTree('+',
                                                   [ExprTree(6, []),
                                                    ExprTree(6, [])])]),
                           ExprTree(5, [])])
    assert str(exp_t) == '((7 * (6 + 6)) + 5)'

    exp_t = ExprTree('+', [ExprTree(3, []),
                           ExprTree('*', [ExprTree('x', []),
                                          ExprTree('y', [])]),
                           ExprTree('x', [])])
    assert str(exp_t) == '(3 + (x * y) + x)'


def test_expression_tree_eq_doctest() -> None:
    """Test ExprTree.__eq__ on the provided doctest"""
    t1 = ExprTree(5, [])
    assert t1.__eq__(ExprTree(5, []))

    t2 = ExprTree('*', [ExprTree(5, []), ExprTree(2, [])])
    assert t2.__eq__(ExprTree('*', [ExprTree(5, []), ExprTree(2, [])]))
    assert t2.__eq__(ExprTree('*', [])) is False


def test_expression_tree_puzzle_is_solved_doctest() -> None:
    """Test ExpressionTreePuzzle.is_solved on the provided doctest"""
    exp_t = ExprTree('+', [ExprTree('a', []), ExprTree('b', [])])
    puz = ExpressionTreePuzzle(exp_t, 7)
    assert puz.is_solved() is False
    puz.variables['a'] = 7
    assert puz.is_solved() is False
    puz.variables['a'] = 5
    puz.variables['b'] = 2
    assert puz.is_solved() is True


def test_expression_tree_puzzle_str_doctest() -> None:
    """Test ExpressionTreePuzzle.__str__ on the provided doctest"""
    exp_t = ExprTree('+', [ExprTree('*',
                                    [ExprTree('a', []),
                                     ExprTree('+', [ExprTree('b', []),
                                                    ExprTree(6, []),
                                                    ExprTree(6, []),
                                                    ])]),
                           ExprTree(5, [])])
    puz = ExpressionTreePuzzle(exp_t, 61)
    assert str(puz) == "{'a': 0, 'b': 0}\n((a * (b + 6 + 6)) + 5) = 61"


def test_expression_tree_puzzle_extensions_doctest() -> None:
    """Test ExpressionTreePuzzle.extensions on the provided doctest"""
    exp_t = ExprTree('a', [])
    puz = ExpressionTreePuzzle(exp_t, 7)
    exts_of_puz = puz.extensions()
    assert len(exts_of_puz) == 9

    exts_of_an_ext = exts_of_puz[0].extensions()
    assert len(exts_of_an_ext) == 0

    exp_t = ExprTree('+', [ExprTree('a', []), ExprTree('b', [])])
    puz = ExpressionTreePuzzle(exp_t, 8)
    exts_of_puz = puz.extensions()
    assert len(exts_of_puz) == 18


def test_expression_tree_puzzle_fail_fast_true() -> None:
    """Test ExpressionTreePuzzle.fail_fast on an unsolvable puzzle."""
    exp_t = ExprTree('+', [ExprTree('a', []), ExprTree('b', [])])
    puz = ExpressionTreePuzzle(exp_t, 7)
    puz.variables['a'] = 9

    assert puz.fail_fast() is True

    exp_t = ExprTree('+', [ExprTree('a', []), ExprTree('b', [])])
    puz = ExpressionTreePuzzle(exp_t, -5)
    puz.variables['a'] = 2

    assert puz.fail_fast() is True

    exp_t = ExprTree('+', [ExprTree(-5, []), ExprTree('b', [])])
    puz = ExpressionTreePuzzle(exp_t, 20)
    puz.variables['a'] = 9

    assert puz.fail_fast() is True

    exp_t = ExprTree('/', [ExprTree(5, []), ExprTree('b', [])])
    puz = ExpressionTreePuzzle(exp_t, 20)
    puz.variables['a'] = 9

    assert puz.fail_fast() is True

    exp_t = construct_from_list([['+'], [3, 'a']])
    puz = ExpressionTreePuzzle(exp_t, 20)
    puz.variables['a'] = 9

    assert puz.fail_fast() is True


def test_expression_tree_puzzle_fail_fast_false() -> None:
    """Test ExpressionTreePuzzle.fail_fast on a solvable puzzle."""
    exp_t = ExprTree('+', [ExprTree('a', []), ExprTree('b', [])])
    puz = ExpressionTreePuzzle(exp_t, 7)
    puz.variables['a'] = 2

    assert puz.fail_fast() is False

    exp_t = ExprTree('+', [ExprTree('*',
                                    [ExprTree('a', []),
                                     ExprTree('+', [ExprTree('b', []),
                                                    ExprTree(6, []),
                                                    ExprTree(6, []),
                                                    ])]),
                           ExprTree(5, [])])
    puz = ExpressionTreePuzzle(exp_t, 61)

    assert puz.fail_fast() is False

    exp_t = ExprTree(5, [])
    puz = ExpressionTreePuzzle(exp_t, 61)

    assert puz.fail_fast() is False

    exp_t = ExprTree('b', [])
    puz = ExpressionTreePuzzle(exp_t, 5)

    assert puz.fail_fast() is False


if __name__ == '__main__':
    import pytest

    pytest.main(['a2_starter_tests.py'])
