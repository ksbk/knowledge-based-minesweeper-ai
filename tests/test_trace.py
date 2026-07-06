"""Tests for structured reasoning trace events."""

from minesweeper_ai.sentence import Sentence
from minesweeper_ai.trace import TraceEvent, TraceEventKind


def test_trace_event_records_safe_cell_explanation() -> None:
    event = TraceEvent(
        kind=TraceEventKind.MARK_SAFE,
        message="Cell is known safe.",
        cells=frozenset({(0, 0)}),
    )

    assert event.kind == TraceEventKind.MARK_SAFE
    assert event.message == "Cell is known safe."
    assert event.cells == frozenset({(0, 0)})


def test_trace_event_can_reference_inferred_sentence() -> None:
    sentence = Sentence(cells={(1, 1)}, count=0)

    event = TraceEvent(
        kind=TraceEventKind.INFER_SENTENCE,
        message="Derived a new sentence from subset inference.",
        sentence=sentence,
    )

    assert event.kind == TraceEventKind.INFER_SENTENCE
    assert event.sentence == sentence


def test_trace_event_can_reference_subset_source_sentences() -> None:
    source_sentence = Sentence(cells={(0, 1), (1, 0)}, count=1)
    other_sentence = Sentence(cells={(0, 1), (1, 0), (1, 1)}, count=1)
    inferred_sentence = Sentence(cells={(1, 1)}, count=0)

    event = TraceEvent(
        kind=TraceEventKind.INFER_SENTENCE,
        message="Derived a new sentence from subset inference.",
        sentence=inferred_sentence,
        source_sentence=source_sentence,
        other_sentence=other_sentence,
    )

    assert event.source_sentence == source_sentence
    assert event.other_sentence == other_sentence
    assert event.sentence == inferred_sentence
