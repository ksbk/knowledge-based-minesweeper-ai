"""Logical sentence representation for Minesweeper knowledge."""

from __future__ import annotations

from dataclasses import dataclass

from minesweeper_ai.types import Cell


@dataclass
class Sentence:
    """A logical constraint over a set of Minesweeper cells.

    Example:
        {(0, 1), (1, 0), (1, 1)} = 1

    This means exactly one of those cells is a mine.
    """

    cells: set[Cell]
    count: int

    def is_empty(self) -> bool:
        """Return True when the sentence no longer contains any cells."""
        return not self.cells

    def known_mines(self) -> set[Cell]:
        """Return cells that must be mines."""
        if len(self.cells) == self.count and self.count > 0:
            return set(self.cells)

        return set()

    def known_safes(self) -> set[Cell]:
        """Return cells that must be safe."""
        if self.count == 0:
            return set(self.cells)

        return set()

    def mark_mine(self, cell: Cell) -> None:
        """Update this sentence after a cell is known to be a mine."""
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell: Cell) -> None:
        """Update this sentence after a cell is known to be safe."""
        self.cells.discard(cell)
