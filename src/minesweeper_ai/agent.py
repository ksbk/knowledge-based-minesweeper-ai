"""Knowledge-based Minesweeper agent."""



from dataclasses import dataclass, field

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
    
    height: int 
    width: int
    moves_made: set[Cell] = field(default_factory=_empty_cell_set)
    mines: set[Cell] = field(default_factory=_empty_cell_set)
    safes: set[Cell] = field(default_factory=_empty_cell_set)
    knowledge: list[Sentence] = field(default_factory=_empty_knowledge_base)

    def mark_mine(self, cell: Cell) -> None:
        """Mark a cell as a mine and update knowledge."""
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)
            
    def mark_safe(self, cell: Cell) -> None:
        """Mark a cell as safe and update knowledge."""
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
