"""Plain Python adapter for exposing Minesweeper sessions to web clients."""

from __future__ import annotations

import random

from minesweeper_ai.agent import MinesweeperAgent
from minesweeper_ai.board import Board
from minesweeper_ai.session import GameSession
from minesweeper_ai.types import Cell

DIFFICULTIES = {
    "easy": {"height": 8, "width": 8, "mine_count": 8},
    "intermediate": {"height": 10, "width": 10, "mine_count": 15},
    "hard": {"height": 12, "width": 12, "mine_count": 25},
}


def _serialize_cell(cell: Cell) -> dict[str, int]:
    """Return a JSON-serializable cell representation."""
    row, col = cell
    return {"row": row, "col": col}


class WebGameAdapter:
    """Adapt ``GameSession`` operations to serializable Python dictionaries."""

    def __init__(self, rng: random.Random | None = None) -> None:
        self._rng = rng or random.Random()
        self.difficulty = "easy"
        self.session: GameSession
        self.new_game()

    def new_game(self, difficulty: str = "easy") -> dict[str, object]:
        """Start and return a new game for the selected difficulty."""
        if difficulty not in DIFFICULTIES:
            choices = ", ".join(DIFFICULTIES)
            raise ValueError(f"Unknown difficulty. Choose one of: {choices}.")

        config = DIFFICULTIES[difficulty]
        height = config["height"]
        width = config["width"]
        mine_count = config["mine_count"]
        cells = [(row, col) for row in range(height) for col in range(width)]
        mines = set(self._rng.sample(cells, mine_count))
        board = Board(height=height, width=width, mines=mines)

        self.difficulty = difficulty
        self.session = GameSession(
            board=board,
            agent=MinesweeperAgent(board=board),
        )
        return self.state()

    def reveal(self, row: int, col: int) -> dict[str, object]:
        """Reveal a cell through the active Python game session."""
        cell = self._validated_cell(row, col)
        if not self._is_game_over():
            self.session.reveal_cell(cell)
        return self.state()

    def toggle_flag(self, row: int, col: int) -> dict[str, object]:
        """Toggle a cell flag through the active Python game session."""
        cell = self._validated_cell(row, col)
        if not self._is_game_over():
            self.session.toggle_flag(cell)
        return self.state()

    def suggest_move(self) -> dict[str, int] | None:
        """Return the Python agent's suggested move without applying it."""
        move = self._suggest_valid_move()
        return _serialize_cell(move) if move is not None else None

    def helper_move(self) -> dict[str, object]:
        """Apply one Python agent move and return the updated game state."""
        move = self._suggest_valid_move()

        if move is not None:
            was_lost = self.session.lost
            self.session.reveal_cell(move)
            move_was_applied = (
                move in self.session.revealed or self.session.lost != was_lost
            )
            if not move_was_applied:
                move = None

        state = self.state()
        state["helper_move"] = _serialize_cell(move) if move is not None else None
        return state

    def state(self) -> dict[str, object]:
        """Return the active game state using JSON-serializable values."""
        board = self.session.board
        revealed = [
            {
                **_serialize_cell(cell),
                "nearby_mines": board.nearby_mines(cell),
            }
            for cell in sorted(self.session.revealed)
        ]
        visible_mines = (
            [_serialize_cell(cell) for cell in sorted(board.mines)]
            if self._is_game_over()
            else []
        )
        trace = [
            {
                "kind": event.kind.value,
                "message": event.message,
                "cells": [_serialize_cell(cell) for cell in sorted(event.cells)],
            }
            for event in self.session.agent.trace
        ]

        return {
            "difficulty": self.difficulty,
            "height": board.height,
            "width": board.width,
            "mine_count": len(board.mines),
            "revealed": revealed,
            "flags": [_serialize_cell(cell) for cell in sorted(self.session.flags)],
            "lost": self.session.lost,
            "won": self.session.won,
            "status": self._status(),
            "known_safes": [
                _serialize_cell(cell) for cell in sorted(self.session.agent.safes)
            ],
            "known_mines": [
                _serialize_cell(cell) for cell in sorted(self.session.agent.mines)
            ],
            "visible_mines": visible_mines,
            "trace": trace,
        }

    def _validated_cell(self, row: int, col: int) -> Cell:
        """Return a valid board cell or raise a client-facing error."""
        if (
            isinstance(row, bool)
            or not isinstance(row, int)
            or isinstance(col, bool)
            or not isinstance(col, int)
        ):
            raise ValueError("Cell row and col must be integers.")

        cell = (row, col)
        if not self.session.board.is_inside(cell):
            raise ValueError(f"Cell {cell} is outside the board.")
        return cell

    def _is_game_over(self) -> bool:
        """Return whether the active session has ended."""
        return self.session.lost or self.session.won

    def _suggest_valid_move(self) -> Cell | None:
        """Return an unflagged, unrevealed move while preserving AI preference."""
        if self._is_game_over():
            return None

        blocked = (
            self.session.flags | self.session.revealed | self.session.agent.moves_made
        )
        suggested = self.session.suggest_ai_move()

        if (
            suggested is not None
            and suggested not in blocked
            and suggested not in self.session.agent.mines
            and self.session.board.is_inside(suggested)
        ):
            return suggested

        safe_moves = self.session.agent.safes - blocked - self.session.agent.mines
        if safe_moves:
            return next(iter(safe_moves))

        available_moves = (
            self.session.board.cells() - blocked - self.session.agent.mines
        )
        return next(iter(available_moves), None)

    def _status(self) -> str:
        """Return a short serializable game status."""
        if self.session.lost:
            return "lost"
        if self.session.won:
            return "won"
        return "in_progress"
