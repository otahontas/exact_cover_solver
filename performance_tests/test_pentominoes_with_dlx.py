"""Test finding all solutions for different pentomino boards with dlx.

Correct solution amounts are from wikipedia:
https://en.wikipedia.org/wiki/Pentomino#Constructing_rectangular_dimensions
"""

from exact_cover_solver.data_creators.pentomino_creator import PentominoCreator
from exact_cover_solver.datastructures.dlxmatrix import DLXMatrix
from exact_cover_solver.algos.dlx import DLX
import time


def generate_pentomino_board_solutions(
    pg: PentominoCreator, board_height: int, board_width: int, correct_amount: int
) -> None:
    """Test that 6x10 board gets correct amount of solutions."""
    universe, set_collection = pg.generate(board_height, board_width)
    matrix = DLXMatrix(universe, set_collection)
    dlx = DLX()
    start_time = time.time()
    solutions = dlx.solve(matrix)
    time_solving = time.time() - start_time
    print(
        f"There should be {correct_amount} solutions for {board_height}x{board_width} "
        f"board. Algorithm found {len(solutions)} solutions in {time_solving} seconds"
    )


pg = PentominoCreator()
generate_pentomino_board_solutions(pg, 3, 20, 2)
generate_pentomino_board_solutions(pg, 4, 15, 368)
generate_pentomino_board_solutions(pg, 5, 12, 1010)
generate_pentomino_board_solutions(pg, 6, 10, 2339)
