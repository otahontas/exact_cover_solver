"""Solver service, handles different solving modes."""

from typing import Optional

from exact_cover_solver.algos import AlgorithmX
from exact_cover_solver.algos.dlx import DLX
from exact_cover_solver.algos.dictx import DictX
from exact_cover_solver.data_creators import Universe, SetCollection
from exact_cover_solver.data_creators.pentomino_creator import PentominoCreator
from exact_cover_solver.datastructures.dlxmatrix import DLXMatrix
from exact_cover_solver.services.pentomino_browser import PentominoBoardBrowser

import time


class AlgorithmNotChosenError(Exception):
    """Exception raised when algorithm is not chosen.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Algorithm is not chosen."):
        """Initialize error with message."""
        self.message = message
        super().__init__(self.message)


class Solver:
    """Class for solving an exact cover problem from given input.

    Algorithms list define possible algorithms used by class instances.
    """

    _algorithms = [DLX, DictX]

    def __init__(self):
        """Initialize algorithm variable."""
        self._algorithm: Optional[AlgorithmX] = None

    @property
    def algorithm(self) -> Optional[str]:
        """Maintain a reference to one of the algorithm X objects.

        Returns:
            Name of the algorithm currently in use.

        Raises:
            AlgorithmNotChosenError: Raised if algorithm not chosen.
        """
        try:
            return self._algorithm.__name__
        except AttributeError:
            raise AlgorithmNotChosenError

    @algorithm.setter
    def algorithm(self, algorithm_name: str) -> None:
        """Replace algorithm object at runtime.

        Try to filter correct algorithm class, then create instance of that class.

        Args:
            algorithm_name: Name of the algorithm to be used
        """
        try:
            algo_class = next(
                algo_class
                for algo_class in self._algorithms
                if algo_class.__name__ == algorithm_name
            )
        except StopIteration:
            valid_names = [algo_class.__name__ for algo_class in self._algorithms]
            raise ValueError(
                f"Algorithm {algorithm_name} is not valid algorithm. "
                f"Valid algorithms are: {valid_names}"
            )
        self._algorithm = algo_class()

    def solve_generic_problem(
        self, universe: Universe, set_collection: SetCollection
    ) -> None:
        """Not implemented."""
        raise NotImplementedError

    def solve_pentomino_problem(
        self, board_height: int, board_width: int
    ) -> PentominoBoardBrowser:
        """Generate needed data, solve cover problem and return solution browser.

        Currently only dlxmatrix is used.
        TODO: change this to abstract version, which matches currently used algo.

        Args:
            board_height: Height of the pentomino board
            board_width: Width of the pentomino board

        Returns:
            PentominoBoardBrowser which can be used to browse generated solutions.
        """
        pc = PentominoCreator()
        pc.change_board_size(board_height, board_width)
        universe, set_collection = pc.create_universe_and_set_collection()
        solutions = self._algorithm.solve(DLXMatrix(universe, set_collection))
        return PentominoBoardBrowser(
            board_height, board_width, solutions, set_collection
        )

    def solve_sudoku_problem(self) -> None:
        """Not implemented."""
        raise NotImplementedError
