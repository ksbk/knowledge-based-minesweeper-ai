"""Knowledge-based Minesweeper agent."""

from dataclasses import dataclass, field

from minesweeper_ai.board import Board
from minesweeper_ai.sentence import Sentence
from minesweeper_ai.types import Cell


def _empty_cell_set() -> set[Cell]:
    """Return a new empty set of cells."""
    return set()


def _empty_knowledge_base() -> list[Sentence]:
    """Return a new empty knowledge base."""
    return []


@dataclass
class MinesweeperAgent:
    """AI agent that tracks Minesweeper knowledge."""

    board: Board
    moves_made: set[Cell] = field(default_factory=_empty_cell_set)
    safes: set[Cell] = field(default_factory=_empty_cell_set)
    mines: set[Cell] = field(default_factory=_empty_cell_set)
    knowledge: list[Sentence] = field(default_factory=_empty_knowledge_base)

    def mark_safe(self, cell: Cell) -> None:
        """Mark a cell as safe and update knowledge."""
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def mark_mine(self, cell: Cell) -> None:
        """Mark a cell as a mine and update knowledge."""
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def add_knowledge(self, cell: Cell, count: int) -> None:
        """Add knowledge from a revealed safe cell."""
        self.moves_made.add(cell)
        self.mark_safe(cell)

        unknown_neighbors: set[Cell] = set()
        adjusted_count = count

        for neighbor in self.board.neighbors(cell):
            if neighbor in self.safes:
                continue
            if neighbor in self.mines:
                adjusted_count -= 1
                continue
            unknown_neighbors.add(neighbor)

        if unknown_neighbors:
            new_sentence = Sentence(unknown_neighbors, adjusted_count)
            self.knowledge.append(new_sentence)

        self._update_known_cells()

    def _update_known_cells(self) -> None:
        """Infer known safe cells and mines from current knowledge."""
        changed = True

        while changed:
            changed = False

            known_safes: set[Cell] = set()
            known_mines: set[Cell] = set()

            for sentence in self.knowledge:
                known_safes.update(sentence.known_safes())
                known_mines.update(sentence.known_mines())

            for cell in known_safes - self.safes:
                self.mark_safe(cell)
                changed = True

            for cell in known_mines - self.mines:
                self.mark_mine(cell)
                changed = True

            self.knowledge = [
                sentence for sentence in self.knowledge if not sentence.is_empty()
            ]
