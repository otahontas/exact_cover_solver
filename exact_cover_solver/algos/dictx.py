"""Dictionary based implementation for algorithm X."""

from typing import List, Optional, Generic

from .algox_base import AlgorithmX
from exact_cover_solver.types import Solution, SubsetCollection, UniverseElement
from exact_cover_solver.datastructures import DictMatrix, ColumnDict, ColumnValue


class DictX(AlgorithmX[DictMatrix], Generic[UniverseElement]):
    """Dictionary based implementation for algorithm X.

    Inheriting from generic type UniverseElement allows its bounded usage inside this
    class.
    """

    def __init__(self) -> None:
        """Initialize object by calling parent constructor."""
        super().__init__()

    def solve(self, matrix: DictMatrix) -> List[Solution]:
        """Solve which rows cover the given matrix.

        Clears solutions bookkeeping from previous runs, then calls
        recursive method.

        Args:
            matrix: Matrix representation implemented with dictionaries and sets.

        Returns:
            List of solutions. Solution is a list identifiers of rows that were
            picked to solution.
        """
        self._solutions.clear()
        column_dict, set_collection = matrix.data
        partial: Solution = []
        self._search(column_dict, set_collection, partial)
        return self._solutions

    def _search(
        self,
        column_dict: ColumnDict,
        set_collection: SubsetCollection,
        partial: Solution,
    ) -> None:
        """Perform algorithm X recursively and collect solutions.

        Args:
            column_dict: Matrix representation as a dictionary.
            set_collection: Original set collection used to create the matrix.
            partial: List including rows collected this far in recursion.
        """
        if not column_dict:
            self._solutions.append(partial[:])
            return

        column = self._choose_optimal_column(column_dict)

        if not column_dict[column]:
            return

        rows = list(column_dict[column])

        for row in rows:
            partial.append(row)
            removed_columns = self._cover(column_dict, set_collection, row)
            self._search(column_dict, set_collection, partial)
            self._uncover(column_dict, set_collection, row, removed_columns)
            partial.pop()

    @staticmethod
    def _choose_optimal_column(column_dict: ColumnDict) -> UniverseElement:
        """Find column with smallest size to minimize the branching factor.

        Args:
            column_dict: Dictionary of each column on current iteration.

        Returns:
            Key of optimal column.

        Raises:
            ValueError: if not possible to find any column from given dict.
        """
        key: Optional[UniverseElement] = None
        size: Optional[int] = None
        for element, subset_ids in column_dict.items():
            key = element if key is None else key
            size = len(subset_ids) if size is None else size
            key, size = (
                (element, len(subset_ids)) if len(subset_ids) < size else (key, size)
            )
        if key is not None and size is not None:
            return key
        raise ValueError("Not possible to choose optimal column from empty dict.")

    @staticmethod
    def _cover(
        column_dict: ColumnDict, set_collection: SubsetCollection, set_index: int
    ) -> List[ColumnValue]:
        """Cover columns in given set.

        Go through each element in given set and for each row where element is present,
        remove all other elements. Then remove column representing iterated element
        from column dictionary.

        Args:
            column_dict: Matrix representation as a dictionary
            set_collection: Original set collection used to create the matrix
            set_index: Which set elements to cover

        Returns:
            List including sets that have been removed from column dict.
        """
        removed_columns = []
        for element in set_collection[set_index]:
            for row in column_dict[element]:
                for other_element in set_collection[row]:
                    if other_element != element:
                        column_dict[other_element].remove(row)
            removed_columns.append(column_dict.pop(element))
        return removed_columns

    @staticmethod
    def _uncover(
        column_dict: ColumnDict,
        set_collection: SubsetCollection,
        set_index: int,
        removed_columns: List[ColumnValue],
    ) -> None:
        """Uncover columns.

        Restores removed columns in reversed order to dictionary.

        Args:
            column_dict: Matrix representation as a dictionary
            set_collection: Original set collection used to create the matrix
            set_index: Which set elements to uncover
            removed_columns: Columns removed while covering set
        """
        for counter, element in enumerate(reversed(set_collection[set_index])):
            index = len(removed_columns) - 1 - counter
            column_dict[element] = removed_columns[index]
            for row in column_dict[element]:
                for other_element in set_collection[row]:
                    if other_element != element:
                        column_dict[other_element].add(row)
