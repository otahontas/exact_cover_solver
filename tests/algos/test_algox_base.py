import pytest
from exact_cover_solver.algos import AlgorithmX


def test_not_possible_to_call_solve_without_real_implementation():
    class FakeAlgoX(AlgorithmX):
        def solve(self, matrix):
            super(FakeAlgoX, self).solve(matrix)

    with pytest.raises(NotImplementedError):
        algo = FakeAlgoX()
        algo.solve(None)