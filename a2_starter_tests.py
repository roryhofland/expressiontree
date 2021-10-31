"""
CSC148, Winter 2021
Assignment 2: Automatic Puzzle Solver
==============================
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Jonathan Calver, Sophia Huynh,
         Maryam Majedi, and Jaisie Sin.

All of the files in this directory are:
Copyright (c) 2021 Diane Horton, Jonathan Calver, Sophia Huynh,
                   Maryam Majedi, and Jaisie Sin.

===== Module Description =====

This module contains sample test cases that you can use to test your code.
These are a very incomplete set of test cases! We will be testing your code on
a much more thorough set of tests.

The self-test on MarkUs runs all of the tests below, along with a few others.
Make sure you run the self-test on MarkUs after submitting your code!

Once you have the entire program completed, that is, after Task 5, your
code should pass all of the tests we've provided. As you develop your code,
test cases for parts that you haven't written yet will fail, of course.

But as you work through the earlier phases of the assignment, you can run the
individual tests below for each method as you complete it. We encourage you to
add further test cases in this file to improve your confidence in your code.

Tip: if you put your mouse inside a pytest function and right click, the "run"
menu will give you the option of running just that test function.
"""
from sudoku_puzzle import SudokuPuzzle
from word_ladder_puzzle import WordLadderPuzzle, EASY, TRIVIAL, MEDIUM, HARD, \
    IMPOSSIBLE
from expression_tree import ExprTree, construct_from_list
from expression_tree_puzzle import ExpressionTreePuzzle
from solver import BfsSolver, DfsSolver


# Below is an incomplete set of tests: these tests are mostly the provided
# doctest examples.
#
# We encourage you to write additional test cases and test your own code,
# using the provided test cases as a template!


def test_sudoku_fail_fast_doctest() -> None:
    """Test SudokuPuzzle.fail_fast on the provided doctest."""
    s = SudokuPuzzle(4, [["A", "B", "C", "D"],
                         ["C", "D", " ", " "],
                         [" ", " ", " ", " "],
                         [" ", " ", " ", " "]],
                     {"A", "B", "C", "D"})

    assert s.fail_fast() is False

    s = SudokuPuzzle(4, [["B", "D", "A", "C"],
                         ["C", "A", "B", "D"],
                         ["D", "B", "C", "A"],
                         ["A", "C", "D", " "]],
                     {"A", "B", "C", "D"})

    assert s.fail_fast() is False

    s = SudokuPuzzle(4, [["B", "D", "A", "C"],
                         ["C", "A", "B", "D"],
                         ["A", "B", " ", " "],
                         [" ", " ", " ", " "]],
                     {"A", "B", "C", "D"})

    assert s.fail_fast() is True

    s = SudokuPuzzle(4, [["D", "C", "B", "A"],
                         ["B", "A", "D", "C"],
                         ["C", " ", "A", " "],
                         ["A", " ", "C", " "]],
                     {"A", "B", "C", "D"})

    assert s.fail_fast() is False

    s = SudokuPuzzle(4, [[" ", "C", "B", "A"],
                         ["B", "A", "D", "C"],
                         ["C", "B", "A", "D"],
                         ["A", "D", "C", "B"]],
                     {"A", "B", "C", "D"})

    assert s.fail_fast() is False

    s = SudokuPuzzle(4, [[" ", "C", "B", "D"],
                         ["B", "A", "D", "C"],
                         ["C", "B", "A", "A"],
                         ["A", "D", "C", "B"]],
                     {"A", "B", "C", "D"})

    assert s.fail_fast() is True


def test_has_unique_solution_doctest() -> None:
    """Test has_unique_solution on a SudokuPuzzle with a non-unique solution."""
    s = SudokuPuzzle(4, [["D", "C", "B", "A"],
                         ["B", "A", "D", "C"],
                         ["C", " ", "A", " "],
                         ["A", " ", "C", " "]],
                     {"A", "B", "C", "D"})

    assert s.has_unique_solution() is False

    s = SudokuPuzzle(4, [[" ", " ", " ", " "],
                         [" ", " ", " ", " "],
                         [" ", " ", " ", " "],
                         [" ", " ", " ", " "]],
                     {"A", "B", "C", "D"})

    assert s.has_unique_solution() is False

    s = SudokuPuzzle(4, [["D", "C", "B", "A"],
                         ["B", "A", "D", "C"],
                         ["C", "D", "A", "B"],
                         ["A", "B", "C", "D"]],
                     {"A", "B", "C", "D"})

    assert s.has_unique_solution() is True

    s = SudokuPuzzle(4, [["D", "C", "B", "A"],
                         ["B", "A", "D", "C"],
                         ["C", "B", "A", " "],
                         ["A", " ", "C", " "]],
                     {"A", "B", "C", "D"})

    assert s.has_unique_solution() is True


def test_dfs_solver_sudoku() -> None:
    """Test DfsSolver.solve on a SudokuPuzzle."""
    # This SudokuPuzzle is a more filled-in version of the one in the
    # example from the handout.
    s = SudokuPuzzle(4, [["C", "D", "B", "A"],
                         ["B", "A", "D", "C"],
                         ["D", " ", "A", " "],
                         ["A", " ", "C", " "]],
                     {"A", "B", "C", "D"})
    solver = DfsSolver()
    actual = solver.solve(s)[-1]
    expected = SudokuPuzzle(4, [["C", "D", "B", "A"],
                                ["B", "A", "D", "C"],
                                ["D", "C", "A", "B"],
                                ["A", "B", "C", "D"]],
                            {"A", "B", "C", "D"})
    assert actual == expected

    s = SudokuPuzzle(4, [["B", "D", "A", "C"],
                         ["C", "A", "B", "D"],
                         ["A", "B", " ", " "],
                         [" ", " ", " ", " "]],
                     {"A", "B", "C", "D"})
    actual = solver.solve(s)
    expected = []
    assert actual == expected

    s = SudokuPuzzle(4, [["D", "C", "B", "A"],
                         ["B", "A", "D", "C"],
                         ["C", " ", "A", " "],
                         ["A", " ", "C", " "]],
                     {"A", "B", "C", "D"})
    s2 = SudokuPuzzle(4, [["D", "C", "B", "A"],
                          ["B", "A", "D", "C"],
                          ["C", "B", "A", "D"],
                          ["A", "D", "C", "B"]],
                      {"A", "B", "C", "D"})
    s3 = SudokuPuzzle(4, [["D", "C", "B", "A"],
                          ["B", "A", "D", "C"],
                          ["C", "D", "A", "B"],
                          ["A", "B", "C", "D"]],
                      {"A", "B", "C", "D"})
    s4 = set()
    s4.add(str(s2))
    actual = solver.solve(s, s4)[-1]
    assert actual == s3

    s = SudokuPuzzle(4, [["C", "D", "B", "A"],
                         ["B", "A", "D", "C"],
                         ["D", " ", "A", " "],
                         ["A", " ", "C", " "]],
                     {"A", "B", "C", "D"})

    path = solver.solve(s)
    assert path[0] == SudokuPuzzle(4, [["C", "D", "B", "A"],
                                       ["B", "A", "D", "C"],
                                       ["D", " ", "A", " "],
                                       ["A", " ", "C", " "]],
                                   {"A", "B", "C", "D"})
    assert path[1] == SudokuPuzzle(4, [["C", "D", "B", "A"],
                                       ["B", "A", "D", "C"],
                                       ["D", "C", "A", " "],
                                       ["A", " ", "C", " "]],
                                   {"A", "B", "C", "D"})
    assert path[2] == SudokuPuzzle(4, [["C", "D", "B", "A"],
                                       ["B", "A", "D", "C"],
                                       ["D", "C", "A", "B"],
                                       ["A", " ", "C", " "]],
                                   {"A", "B", "C", "D"})
    assert path[3] == SudokuPuzzle(4, [["C", "D", "B", "A"],
                                       ["B", "A", "D", "C"],
                                       ["D", "C", "A", "B"],
                                       ["A", "B", "C", " "]],
                                   {"A", "B", "C", "D"})
    assert path[4] == SudokuPuzzle(4, [["C", "D", "B", "A"],
                                       ["B", "A", "D", "C"],
                                       ["D", "C", "A", "B"],
                                       ["A", "B", "C", "D"]],
                                   {"A", "B", "C", "D"})

    s = SudokuPuzzle(4, [["D", "C", "B", "A"],
                         ["B", "A", "D", "C"],
                         ["C", " ", "A", " "],
                         ["A", " ", "C", " "]],
                     {"A", "B", "C", "D"})
    s2 = SudokuPuzzle(4, [["D", "C", "B", "A"],
                          ["B", "A", "D", "C"],
                          ["C", "B", "A", "D"],
                          ["A", "D", "C", "B"]],
                      {"A", "B", "C", "D"})
    s3 = SudokuPuzzle(4, [["D", "C", "B", "A"],
                          ["B", "A", "D", "C"],
                          ["C", "D", "A", "B"],
                          ["A", "B", "C", "D"]],
                      {"A", "B", "C", "D"})
    s4 = set()
    s4.add(str(s3))
    path = solver.solve(s, s4)
    assert path[0] == SudokuPuzzle(4, [["D", "C", "B", "A"],
                                       ["B", "A", "D", "C"],
                                       ["C", " ", "A", " "],
                                       ["A", " ", "C", " "]],
                                   {"A", "B", "C", "D"})
    assert path[1] == SudokuPuzzle(4, [["D", "C", "B", "A"],
                                       ["B", "A", "D", "C"],
                                       ["C", "B", "A", " "],
                                       ["A", " ", "C", " "]],
                                   {"A", "B", "C", "D"})
    assert path[2] == SudokuPuzzle(4, [["D", "C", "B", "A"],
                                       ["B", "A", "D", "C"],
                                       ["C", "B", "A", "D"],
                                       ["A", " ", "C", " "]],
                                   {"A", "B", "C", "D"})
    assert path[3] == SudokuPuzzle(4, [["D", "C", "B", "A"],
                                       ["B", "A", "D", "C"],
                                       ["C", "B", "A", "D"],
                                       ["A", "D", "C", " "]],
                                   {"A", "B", "C", "D"})
    assert path[4] == SudokuPuzzle(4, [["D", "C", "B", "A"],
                                       ["B", "A", "D", "C"],
                                       ["C", "B", "A", "D"],
                                       ["A", "D", "C", "B"]],
                                   {"A", "B", "C", "D"})


def test_dfs_solver_word_ladder() -> None:
    solver = DfsSolver()
    w = WordLadderPuzzle("me", "my", {"me", "my", "ma"})
    actual = solver.solve(w)[-1]
    expected = WordLadderPuzzle("my", "my", {"me", "my", "ma"})
    assert actual == expected

    w = WordLadderPuzzle("coat", "goal", {"coal", "coat", "goal", "meal",
                                          "meat", "moat"})
    actual = solver.solve(w)[-1]
    expected = WordLadderPuzzle("goal", "goal", {"coal", "coat", "goal", "meal",
                                                 "meat", "moat"})
    assert actual == expected

    w = WordLadderPuzzle("coat", "yeet", {"coal", "coat", "goal", "meal",
                                          "meat", "yeet"})
    actual = solver.solve(w)
    expected = []
    assert actual == expected

    w = WordLadderPuzzle("coat", "goal", {"coal", "coat", "goal", "meal",
                                          "meat", "moat"})
    path = solver.solve(w)

    assert path[0] == WordLadderPuzzle("coat", "goal", {"coal", "coat", "goal",
                                                        "meal", "meat", "moat"})

    assert path[1] == WordLadderPuzzle("coal", "goal", {"coal", "coat", "goal",
                                                        "meal", "meat", "moat"})

    assert path[2] == WordLadderPuzzle("goal", "goal", {"coal", "coat", "goal",
                                                        "meal", "meat", "moat"})


def test_bfs_solver_sudoku() -> None:
    """Test BfsSolver.solve on a SudokuPuzzle."""
    # This SudokuPuzzle is a more filled-in version of the one in the
    # example from the handout.
    s = SudokuPuzzle(4, [["C", "D", "B", "A"],
                         ["B", "A", "D", "C"],
                         ["D", " ", "A", " "],
                         ["A", " ", "C", " "]],
                     {"A", "B", "C", "D"})
    solver = BfsSolver()
    actual = solver.solve(s)[-1]
    expected = SudokuPuzzle(4, [["C", "D", "B", "A"],
                                ["B", "A", "D", "C"],
                                ["D", "C", "A", "B"],
                                ["A", "B", "C", "D"]],
                            {"A", "B", "C", "D"})
    assert actual == expected

    s = SudokuPuzzle(4, [["C", "D", "B", "A"],
                         ["B", "A", "D", "C"],
                         ["D", " ", "C", " "],
                         ["A", " ", " ", " "]],
                     {"A", "B", "C", "D"})
    actual = solver.solve(s)
    expected = []
    assert actual == expected

    s = SudokuPuzzle(4, [["D", "C", "B", "A"],
                         ["B", "A", "D", "C"],
                         ["C", " ", "A", " "],
                         ["A", " ", "C", " "]],
                     {"A", "B", "C", "D"})
    s2 = SudokuPuzzle(4, [["D", "C", "B", "A"],
                          ["B", "A", "D", "C"],
                          ["C", "B", "A", "D"],
                          ["A", "D", "C", "B"]],
                      {"A", "B", "C", "D"})
    s3 = SudokuPuzzle(4, [["D", "C", "B", "A"],
                          ["B", "A", "D", "C"],
                          ["C", "D", "A", "B"],
                          ["A", "B", "C", "D"]],
                      {"A", "B", "C", "D"})
    s4 = set()
    s4.add(str(s3))
    path = solver.solve(s, s4)

    for item in path:
        print(item)

    assert path[0] == SudokuPuzzle(4, [["D", "C", "B", "A"],
                                       ["B", "A", "D", "C"],
                                       ["C", " ", "A", " "],
                                       ["A", " ", "C", " "]],
                                   {"A", "B", "C", "D"})
    assert path[1] == SudokuPuzzle(4, [["D", "C", "B", "A"],
                                       ["B", "A", "D", "C"],
                                       ["C", "B", "A", " "],
                                       ["A", " ", "C", " "]],
                                   {"A", "B", "C", "D"})
    assert path[2] == SudokuPuzzle(4, [["D", "C", "B", "A"],
                                       ["B", "A", "D", "C"],
                                       ["C", "B", "A", "D"],
                                       ["A", " ", "C", " "]],
                                   {"A", "B", "C", "D"})
    assert path[3] == SudokuPuzzle(4, [["D", "C", "B", "A"],
                                       ["B", "A", "D", "C"],
                                       ["C", "B", "A", "D"],
                                       ["A", "D", "C", " "]],
                                   {"A", "B", "C", "D"})
    assert path[4] == SudokuPuzzle(4, [["D", "C", "B", "A"],
                                       ["B", "A", "D", "C"],
                                       ["C", "B", "A", "D"],
                                       ["A", "D", "C", "B"]],
                                   {"A", "B", "C", "D"})


def test_bfs_solver_word_ladder() -> None:
    solver = BfsSolver()

    w = WordLadderPuzzle("me", "my", {"me", "my", "ma"})
    actual = solver.solve(w)[-1]
    expected = WordLadderPuzzle("my", "my", {"me", "my", "ma"})
    assert actual == expected

    w = WordLadderPuzzle("coat", "goal", {"coal", "coat", "goal", "meal",
                                          "meat", "moat"})
    actual = solver.solve(w)[-1]
    expected = WordLadderPuzzle("goal", "goal", {"coal", "coat", "goal", "meal",
                                                 "meat", "moat"})
    assert actual == expected

    w = WordLadderPuzzle("coat", "yeet", {"coal", "coat", "goal", "meal",
                                          "meat", "yeet"})
    actual = solver.solve(w)
    expected = []
    assert actual == expected

    w = WordLadderPuzzle("come", "chum", {"come", "chum"})
    actual = solver.solve(w)
    expected = []
    assert actual == expected

    w = WordLadderPuzzle("coat", "goal", {"coal", "coat", "goal", "meal",
                                          "meat", "moat"})
    path = solver.solve(w)

    assert path[0] == WordLadderPuzzle("coat", "goal", {"coal", "coat", "goal",
                                                        "meal", "meat", "moat"})

    assert path[1] == WordLadderPuzzle("coal", "goal", {"coal", "coat", "goal",
                                                        "meal", "meat", "moat"})

    assert path[2] == WordLadderPuzzle("goal", "goal", {"coal", "coat", "goal",
                                                        "meal", "meat", "moat"})


def test_word_ladder_eq_doctest() -> None:
    """Test WordLadder.__eq__ on the provided doctest"""
    wl1 = WordLadderPuzzle("me", "my", {"me", "my", "ma"})
    wl2 = WordLadderPuzzle("me", "my", {"me", "my", "mu"})
    wl3 = WordLadderPuzzle("me", "my", {"ma", "me", "my"})
    wl4 = WordLadderPuzzle("me", "ma", {"me", "my", "ma"})
    assert wl1.__eq__(wl2) is False
    assert wl1.__eq__(wl3) is True
    assert wl1.__eq__(wl4) is False


def test_word_ladder_str_doctest() -> None:
    """Test WordLadder.__str__ on the provided doctest"""
    wl1 = WordLadderPuzzle("me", "my", {"me", "my", "ma"})
    wl2 = WordLadderPuzzle("me", "my", {"me", "my", "mu"})
    assert str(wl1) == 'me -> my'
    assert str(wl2) == 'me -> my'
    wl3 = WordLadderPuzzle("coat", "goal", {"coal", "coat", "goal", "meal",
                                            "meat", "moat"})
    assert str(wl3) == 'coat -> goal'


def test_word_ladder_extensions_doctest() -> None:
    """Test WordLadder.__str__ on the provided doctest"""
    wl1 = WordLadderPuzzle("me", "my", {"me", "be", "my"})
    wl2 = WordLadderPuzzle("be", "my", {"me", "be", "my"})
    wl3 = WordLadderPuzzle("my", "my", {"me", "be", "my"})

    msg1 = f"{wl1.extensions()} is missing some valid puzzle states"
    msg2 = f"{wl1.extensions()} contains extra invalid puzzle states"

    assert all([wlp in wl1.extensions() for wlp in [wl2, wl3]]), msg1
    assert all([wlp in [wl2, wl3] for wlp in wl1.extensions()]), msg2

    w1 = WordLadderPuzzle("coat", "goal", {"coal", "coat", "goal", "meal",
                                           "meat", "moat"})
    w2 = WordLadderPuzzle("coal", "goal", {"coal", "coat", "goal", "meal",
                                           "meat", "moat"})
    w3 = WordLadderPuzzle("moat", "goal", {"coal", "coat", "goal", "meal",
                                           "meat", "moat"})

    assert all([wlp in w1.extensions() for wlp in [w2, w3]]), msg1
    assert all([wlp in [w2, w3] for wlp in w1.extensions()]), msg2


def test_word_ladder_is_solved_doctest() -> None:
    """Test WordLadder.is_solved on the provided doctest"""
    wl1 = WordLadderPuzzle("me", "me", {"me", "my"})
    wl2 = WordLadderPuzzle("me", "my", {"me", "my"})
    assert wl1.is_solved() is True
    assert wl2.is_solved() is False


def test_word_ladder_get_difficulty() -> None:
    """Test WordLadder.get_difficulty on TRIVIAL and EASY puzzles."""
    wl1 = WordLadderPuzzle("done", "done", {"done"})
    assert wl1.get_difficulty() == TRIVIAL

    wl2 = WordLadderPuzzle("come", "done", {"come", "cone", "done"})
    assert wl2.get_difficulty() == EASY

    wl3 = WordLadderPuzzle("come", "dove", {"come", "cone", "done", "dove"})
    assert wl3.get_difficulty() == MEDIUM

    wl4 = WordLadderPuzzle("come", "jive", {"come", "cone", "done", "dove",
                                            "dive", "jive"})
    assert wl4.get_difficulty() == HARD

    wl5 = WordLadderPuzzle("come", "chum", {"come", "chum"})
    assert wl5.get_difficulty() == IMPOSSIBLE


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
