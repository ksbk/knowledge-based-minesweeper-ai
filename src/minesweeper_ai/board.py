"""Board model for Minesweeper AI."""

from dataclasses import dataclass, field

from minesweeper_ai.types import Cell


def _empty_cell_set() -> set[Cell]:
    """Return a new empty set of cells."""
    return set()


@dataclass
class Board:
    """A Minesweeper board with fixed dimensions and mine locations."""

    height: int
    width: int
    mines: set[Cell] = field(default_factory=_empty_cell_set)

    def is_inside(self, cell: Cell) -> bool:
        """Return True if the cell is inside the board."""
        row, col = cell
        return 0 <= row < self.height and 0 <= col < self.width

    def neighbors(self, cell: Cell) -> set[Cell]:
        """Return the set of neighboring cells for a given cell."""
        row, col = cell
        candidates = {
            (row - 1, col - 1),
            (row - 1, col),
            (row - 1, col + 1),
            (row, col - 1),
            (row, col + 1),
            (row + 1, col - 1),
            (row + 1, col),
            (row + 1, col + 1),
        }
        return {candidate for candidate in candidates if self.is_inside(candidate)}

    def nearby_mines(self, cell: Cell) -> int:
        """Return the number of mines neighboring a cell."""
        return len(self.neighbors(cell) & self.mines)
