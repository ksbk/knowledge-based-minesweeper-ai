"""Knowledge-based Minesweeper agent."""

from dataclasses import dataclass, field

from minesweeper_ai.board import Board
from minesweeper_ai.sentence import Sentence
from minesweeper_ai.trace import TraceEvent, TraceEventKind
from minesweeper_ai.types import Cell


def _empty_cell_set() -> set[Cell]:
    """Return a new empty set of cells."""
    return set()


def _empty_knowledge_base() -> list[Sentence]:
    """Return a new empty knowledge base."""
    return []


def _empty_trace() -> list[TraceEvent]:
    """Return a new empty reasoning trace."""
    return []


def _copy_sentence(sentence: Sentence) -> Sentence:
    """Return a copy of a sentence for trace snapshots."""
    return Sentence(cells=set(sentence.cells), count=sentence.count)


@dataclass
class MinesweeperAgent:
    """AI agent that tracks Minesweeper knowledge."""

    board: Board
    moves_made: set[Cell] = field(default_factory=_empty_cell_set)
    safes: set[Cell] = field(default_factory=_empty_cell_set)
    mines: set[Cell] = field(default_factory=_empty_cell_set)
    knowledge: list[Sentence] = field(default_factory=_empty_knowledge_base)
    trace: list[TraceEvent] = field(default_factory=_empty_trace)

    def mark_safe(self, cell: Cell) -> None:
        """Mark a cell as safe and update all existing knowledge."""
        already_known = cell in self.safes

        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

        if not already_known:
            self.trace.append(
                TraceEvent(
                    kind=TraceEventKind.MARK_SAFE,
                    message=f"Marked {cell} as safe.",
                    cells=frozenset({cell}),
                )
            )

    def mark_mine(self, cell: Cell) -> None:
        """Mark a cell as a mine and update all existing knowledge."""
        already_known = cell in self.mines

        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

        if not already_known:
            self.trace.append(
                TraceEvent(
                    kind=TraceEventKind.MARK_MINE,
                    message=f"Marked {cell} as a mine.",
                    cells=frozenset({cell}),
                )
            )

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
            new_sentence = Sentence(cells=unknown_neighbors, count=adjusted_count)
            self.knowledge.append(new_sentence)
            self.trace.append(
                TraceEvent(
                    kind=TraceEventKind.INFER_SENTENCE,
                    message="Derived a new sentence from revealed cell.",
                    sentence=_copy_sentence(new_sentence),
                )
            )

        self.update_knowledge()

    def _deduplicate_knowledge(self) -> None:
        """Remove duplicate sentences from the knowledge base."""
        unique: list[Sentence] = []

        for sentence in self.knowledge:
            if sentence not in unique:
                unique.append(sentence)

        self.knowledge = unique

    def _infer_new_sentences(self) -> list[Sentence]:
        """Infer new sentences from existing subset relationships."""
        inferred_knowledge: list[Sentence] = []

        for first in self.knowledge:
            for second in self.knowledge:
                if first == second:
                    continue

                if not first.cells or not second.cells:
                    continue

                if first.cells < second.cells:
                    new_cells = second.cells - first.cells
                    new_count = second.count - first.count
                    new_sentence = Sentence(cells=new_cells, count=new_count)

                    if (
                        new_sentence not in self.knowledge
                        and new_sentence not in inferred_knowledge
                    ):
                        inferred_knowledge.append(new_sentence)
                        self.trace.append(
                            TraceEvent(
                                kind=TraceEventKind.INFER_SENTENCE,
                                message="Derived a new sentence from subset inference.",
                                sentence=_copy_sentence(new_sentence),
                                source_sentence=_copy_sentence(first),
                                other_sentence=_copy_sentence(second),
                            )
                        )

        return inferred_knowledge

    def update_knowledge(self) -> None:
        """Infer known safe cells, mines, and new constraints until stable."""
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

            before_cleanup = list(self.knowledge)

            self.knowledge = [
                sentence for sentence in self.knowledge if not sentence.is_empty()
            ]

            self._deduplicate_knowledge()

            if self.knowledge != before_cleanup:
                changed = True

            new_sentences = self._infer_new_sentences()
            if new_sentences:
                self.knowledge.extend(new_sentences)
                self._deduplicate_knowledge()
                changed = True

    def make_safe_move(self) -> Cell | None:
        """Return a safe cell to choose on the Minesweeper board."""
        available_safe_moves = self.safes - self.moves_made

        if not available_safe_moves:
            return None

        return next(iter(available_safe_moves))

    def make_random_move(self) -> Cell | None:
        """Return an available move that is not known to be a mine."""
        available_moves = self.board.cells() - self.moves_made - self.mines

        if not available_moves:
            return None

        return next(iter(available_moves))
