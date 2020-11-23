"""Wrappers to represent dancing links data and column objects as matrix."""

from typing import Optional

from exact_cover_solver.datastructures.dlxdataobjects import DataObject, ColumnObject
from exact_cover_solver.data_creators import Universe, SetCollection


class DLXMatrix:
    """Matrix representation and initialization methods for circular linked lists."""

    def __init__(self, universe: Universe, set_collection: SetCollection) -> None:
        """Create column and data objects and link them to this matrix object.

        Args:
            universe: a list of integers representing some set of elements
            set_collection: a list of lists, each made from integers in the universe

        Raises:
            ValueError: Error is raised if universe or set_collection is empty.
        """
        if not universe:
            raise ValueError("Not possible to create matrix with empty universe.")
        if not set_collection:
            raise ValueError("Not possible to create matrix with empty set collection.")

        self.id = "root"
        self.right: Optional[ColumnObject] = None
        self.left: Optional[ColumnObject] = None
        self._universe = universe
        self._set_collection = set_collection
        self._create_columns()
        self._create_nodes()

    def _create_columns(self) -> None:
        """Create column columns and attach them to root."""
        previous = self
        for element in self._universe:
            column = ColumnObject(column_id=element)
            column.left = previous
            previous.right = column
            previous = column
        self.left = previous
        previous.right = self

    def _create_nodes(self) -> None:
        """Create nodes representing elements in each set in set collection.

        All sets are iterated through. For each element in set the element is
        linked to the correct column and columns column. Elements in set are
        also linked together to form a circular row.
        """

        def find_column(_id: int) -> ColumnObject:
            """Find column with given id."""
            correct_column = self
            while correct_column.id != _id:
                correct_column = correct_column.right
            return correct_column

        for set_number, set_elements in enumerate(self._set_collection):
            previous = None
            first = None
            for element in set_elements:
                column = find_column(element)
                cell = DataObject(column, row=set_number)
                prev_up = column.up
                prev_up.down = cell
                cell.up = prev_up
                cell.down = column
                column.up = cell
                if previous:
                    previous.right = cell
                    cell.left = previous
                else:
                    first = cell
                previous = cell
                column.size += 1
            previous.right = first
            first.left = previous

    def __repr__(self) -> str:
        """Return printable representation of matrix."""
        s = ""
        column = self.right
        while column != self:
            data = column.down
            data_str = ""
            while data != column:
                data_str = f"{data_str} {data.row}"
                data = data.down
            s = f"{s}Column {column.id} has {column.size} rows:{data_str}\n"
            column = column.right
        return s


# Add all private methods to pdoc when generating documentation
__pdoc__ = {
    f"DLXMatrix.{func}": True
    for func in dir(DLXMatrix)
    if callable(getattr(DLXMatrix, func)) and func.startswith("_")
}
