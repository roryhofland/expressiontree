from __future__ import annotations

from typing import List, Optional, Set

# You may remove this import if you don't use it in your code.
from adts import Queue

from puzzle import Puzzle


class Solver:
    """"
    A solver for full-information puzzles. This is an abstract class
    and purely provides the interface for our solve method.
    """

    # You may NOT change the interface to the solve method.
    # Note the optional parameter seen and its type.
    # Your implementations of this method in the two subclasses should use seen
    # to keep track of all puzzle states that you encounter during the
    # solution process.
    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.
        """
        raise NotImplementedError


# Your solve method MUST be a recursive function (i.e. it must make
# at least one recursive call to itself)
# You may NOT change the interface to the solve method.
class DfsSolver(Solver):
    """"
    A solver for full-information puzzles that uses
    a depth first search strategy.
    """

    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.
        """
        # solved case
        if puzzle.is_solved() and not str(puzzle) in seen:
            return [puzzle]
        # dead end
        elif puzzle.fail_fast() or seen is not None and str(puzzle) in seen:
            return []
        else:
            solution_path = []
            if seen is None:
                seen = set()
            # updating seen with current puzzle
            seen.add(str(puzzle))
            # iterate through each possible next step
            for extension in puzzle.extensions():
                solution_path.extend(self.solve(extension, seen))
            # only string together if the solution is at the end
            if solution_path:
                return [puzzle] + solution_path
            return solution_path


# Hint: You may find a Queue useful here.
class BfsSolver(Solver):
    """"
    A solver for full-information puzzles that uses
    a breadth first search strategy.
    """

    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.
        """
        # if sudoku is already unable to be solved
        if puzzle.fail_fast():
            return []

        state = Queue()
        state.enqueue([puzzle])
        a_path = None
        if seen is None:
            seen = set()
        found_solution = False

        # loop while there are more board states available
        while not state.is_empty():
            a_path = state.dequeue()
            # if we reach a solution, return the solution and add the leftover
            # states to seen
            if a_path[-1].is_solved() and str(a_path[-1]) not in seen:
                while not state.is_empty():
                    seen.add(str(state.dequeue()[-1]))
                found_solution = True
            # if we haven't seen this board state before, add it to seen
            elif str(a_path[-1]) not in seen:
                seen.add(str(a_path[-1]))
                for extension in a_path[-1].extensions():
                    # if the extension is valid enqueue it
                    enqueue_if_not_fail_fast(extension, state, a_path)
            # if there are no more states, the puzzle is unsolvable
            if state.is_empty() and not found_solution:
                return []

        return a_path


def enqueue_if_not_fail_fast(extension: Puzzle, state: Queue,
                             a_path: List[Puzzle]) -> None:
    """
    If <extension> does not fail fast, enqueue <a_path + [extension]> to <state>
    """
    if not extension.fail_fast():
        state.enqueue(a_path + [extension])


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={'pyta-reporter': 'ColorReporter',
                                'allowed-io': [],
                                'allowed-import-modules': ['doctest',
                                                           'python_ta',
                                                           'typing',
                                                           '__future__',
                                                           'puzzle',
                                                           'adts'],
                                'disable': ['E1136'],
                                'max-attributes': 15}
                        )
