"""Structured reasoning trace events for Minesweeper AI."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from minesweeper_ai.sentence import Sentence
from minesweeper_ai.types import Cell


class TraceEventKind(StrEnum):
    """Kinds of reasoning events the agent can record."""

    MARK_SAFE = "mark_safe"
    MARK_MINE = "mark_mine"
    INFER_SENTENCE = "infer_sentence"


@dataclass(frozen=True)
class TraceEvent:
    """A structured explanation of one reasoning step."""

    kind: TraceEventKind
    message: str
    cells: frozenset[Cell] = frozenset()
    sentence: Sentence | None = None
    source_sentence: Sentence | None = None
    other_sentence: Sentence | None = None
