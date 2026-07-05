"""Interface-independent Minesweeper game session."""

from __future__ import annotations

from dataclasses import dataclass, field

from minesweeper_ai.agent import MinesweeperAgent
from minesweeper_ai.board import Board
from minesweeper_ai.types import Cell


def _empty_cell_set() -> set[Cell]:
    """Return a new empty set of cells."""
    return set()


@dataclass
class GameSession:
    """Manage gameplay state independently from any user interface."""

    board: Board
    agent: MinesweeperAgent
    revealed: set[Cell] = field(default_factory=_empty_cell_set)
    flags: set[Cell] = field(default_factory=_empty_cell_set)
    lost: bool = False

    @property
    def won(self) -> bool:
        """Return True when every mine has been flagged."""
        return self.flags == self.board.mines

    def reveal_cell(self, cell: Cell) -> None:
        """Reveal a cell and update AI knowledge when the cell is safe."""
        if self.lost or cell in self.flags or cell in self.revealed:
            return

        if cell in self.board.mines:
            self.lost = True
            return

        nearby = self.board.nearby_mines(cell)
        self.revealed.add(cell)
        self.agent.add_knowledge(cell, nearby)

    def toggle_flag(self, cell: Cell) -> None:
        """Toggle a flag on an unrevealed cell."""
        if self.lost or cell in self.revealed:
            return

        if cell in self.flags:
            self.flags.remove(cell)
        else:
            self.flags.add(cell)

    def suggest_ai_move(self) -> Cell | None:
        """Return the AI's preferred next move without revealing it."""
        safe_move = self.agent.make_safe_move()
        if safe_move is not None:
            return safe_move
        return self.agent.make_random_move()

    def make_ai_move(self) -> Cell | None:
        """Let the AI choose and reveal one move."""
        move = self.suggest_ai_move()
        if move is None:
            return None

        self.reveal_cell(move)
        return move
