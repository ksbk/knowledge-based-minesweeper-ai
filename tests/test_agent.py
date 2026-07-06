"""Tests for the Minesweeper AI agent."""

from minesweeper_ai.agent import MinesweeperAgent
from minesweeper_ai.board import Board
from minesweeper_ai.sentence import Sentence
from minesweeper_ai.trace import TraceEventKind


def test_agent_starts_with_empty_knowledge_state() -> None:
    board = Board(height=3, width=3)
    agent = MinesweeperAgent(board=board)

    assert agent.moves_made == set()
    assert agent.safes == set()
    assert agent.mines == set()
    assert agent.knowledge == []


def test_mark_safe_records_safe_cell() -> None:
    board = Board(height=3, width=3)
    agent = MinesweeperAgent(board=board)

    agent.mark_safe((0, 0))

    assert agent.safes == {(0, 0)}


def test_mark_mine_records_mine_cell() -> None:
    board = Board(height=3, width=3)
    agent = MinesweeperAgent(board=board)

    agent.mark_mine((0, 0))

    assert agent.mines == {(0, 0)}


def test_mark_safe_updates_existing_sentences() -> None:
    board = Board(height=3, width=3)
    agent = MinesweeperAgent(
        board=board,
        knowledge=[
            Sentence(cells={(0, 0), (0, 1)}, count=1),
            Sentence(cells={(0, 0), (1, 0)}, count=1),
        ],
    )

    agent.mark_safe((0, 0))

    assert agent.knowledge == [
        Sentence(cells={(0, 1)}, count=1),
        Sentence(cells={(1, 0)}, count=1),
    ]


def test_mark_mine_updates_existing_sentences() -> None:
    board = Board(height=3, width=3)
    agent = MinesweeperAgent(
        board=board,
        knowledge=[
            Sentence(cells={(0, 0), (0, 1)}, count=1),
            Sentence(cells={(0, 0), (1, 0)}, count=1),
        ],
    )

    agent.mark_mine((0, 0))

    assert agent.knowledge == [
        Sentence(cells={(0, 1)}, count=0),
        Sentence(cells={(1, 0)}, count=0),
    ]


def test_add_knowledge_records_move_and_marks_cell_safe() -> None:
    agent = MinesweeperAgent(board=Board(height=3, width=3))

    agent.add_knowledge((0, 0), count=1)

    assert agent.moves_made == {(0, 0)}
    assert agent.safes == {(0, 0)}


def test_add_knowledge_adds_sentence_for_unknown_neighbors() -> None:
    agent = MinesweeperAgent(board=Board(height=3, width=3))

    agent.add_knowledge((0, 0), count=1)

    assert agent.knowledge == [Sentence(cells={(0, 1), (1, 0), (1, 1)}, count=1)]


def test_add_knowledge_excludes_known_safe_neighbors() -> None:
    agent = MinesweeperAgent(
        board=Board(height=3, width=3),
        safes={(0, 1)},
    )

    agent.add_knowledge((0, 0), count=1)

    assert agent.knowledge == [Sentence(cells={(1, 0), (1, 1)}, count=1)]


def test_add_knowledge_excludes_known_mine_neighbors_and_adjusts_count() -> None:
    agent = MinesweeperAgent(
        board=Board(height=3, width=3),
        mines={(0, 1)},
    )

    agent.add_knowledge((0, 0), count=1)

    assert agent.safes == {(0, 0), (1, 0), (1, 1)}
    assert agent.mines == {(0, 1)}
    assert agent.knowledge == []


def test_add_knowledge_excludes_known_safes_and_mines_together() -> None:
    agent = MinesweeperAgent(
        board=Board(height=3, width=3),
        safes={(0, 1)},
        mines={(1, 0)},
    )

    agent.add_knowledge((0, 0), count=1)

    assert agent.safes == {(0, 0), (0, 1), (1, 1)}
    assert agent.mines == {(1, 0)}
    assert agent.knowledge == []


def test_add_knowledge_does_not_add_sentence_when_no_unknown_neighbors_remain() -> None:
    agent = MinesweeperAgent(
        board=Board(height=3, width=3),
        safes={(0, 1), (1, 0), (1, 1)},
    )

    agent.add_knowledge((0, 0), count=0)

    assert agent.safes == {(0, 0), (0, 1), (1, 0), (1, 1)}
    assert agent.knowledge == []


def test_add_knowledge_updates_existing_sentences_with_safe_cell() -> None:
    agent = MinesweeperAgent(
        board=Board(height=3, width=3),
        knowledge=[
            Sentence(cells={(0, 0), (0, 1)}, count=1),
        ],
    )

    agent.add_knowledge((0, 0), count=1)

    assert agent.safes == {(0, 0), (1, 0), (1, 1)}
    assert agent.mines == {(0, 1)}
    assert agent.knowledge == []


def test_add_knowledge_marks_all_neighbors_safe_when_count_is_zero() -> None:
    agent = MinesweeperAgent(board=Board(height=3, width=3))

    agent.add_knowledge((0, 0), count=0)

    assert agent.safes == {(0, 0), (0, 1), (1, 0), (1, 1)}
    assert agent.mines == set()
    assert agent.knowledge == []


def test_add_knowledge_marks_all_unknown_neighbors_as_mines() -> None:
    agent = MinesweeperAgent(board=Board(height=3, width=3))

    agent.add_knowledge((0, 0), count=3)

    assert agent.mines == {(0, 1), (1, 0), (1, 1)}
    assert agent.safes == {(0, 0)}
    assert agent.knowledge == []


def test_update_known_cells_propagates_safe_cell_to_other_sentences() -> None:
    agent = MinesweeperAgent(
        board=Board(height=3, width=3),
        knowledge=[
            Sentence(cells={(0, 1)}, count=0),
            Sentence(cells={(0, 1), (1, 0)}, count=1),
        ],
    )

    agent.update_knowledge()

    assert agent.safes == {(0, 1)}
    assert agent.mines == {(1, 0)}
    assert agent.knowledge == []


def test_update_known_cells_propagates_mine_to_other_sentences() -> None:
    agent = MinesweeperAgent(
        board=Board(height=3, width=3),
        knowledge=[
            Sentence(cells={(0, 1)}, count=1),
            Sentence(cells={(0, 1), (1, 0)}, count=1),
        ],
    )

    agent.update_knowledge()

    assert agent.mines == {(0, 1)}
    assert agent.safes == {(1, 0)}
    assert agent.knowledge == []


def test_update_knowledge_infers_safe_cell_from_subset_relationship() -> None:
    agent = MinesweeperAgent(
        board=Board(height=3, width=3),
        knowledge=[
            Sentence(cells={(0, 1), (1, 0), (1, 1)}, count=1),
            Sentence(cells={(0, 1), (1, 0)}, count=1),
        ],
    )

    agent.update_knowledge()

    assert agent.safes == {(1, 1)}
    assert agent.mines == set()
    assert agent.knowledge == [Sentence(cells={(0, 1), (1, 0)}, count=1)]


def test_update_knowledge_infers_mine_from_subset_relationship() -> None:
    agent = MinesweeperAgent(
        board=Board(height=3, width=3),
        knowledge=[
            Sentence(cells={(0, 1), (1, 0), (1, 1)}, count=2),
            Sentence(cells={(0, 1), (1, 0)}, count=1),
        ],
    )

    agent.update_knowledge()

    assert agent.mines == {(1, 1)}
    assert agent.safes == set()
    assert agent.knowledge == [Sentence(cells={(0, 1), (1, 0)}, count=1)]


def test_update_knowledge_does_not_duplicate_inferred_sentences() -> None:
    agent = MinesweeperAgent(
        board=Board(height=3, width=3),
        knowledge=[
            Sentence(cells={(0, 1), (1, 0), (1, 1)}, count=1),
            Sentence(cells={(0, 1), (1, 0)}, count=1),
            Sentence(cells={(1, 1)}, count=0),
        ],
    )

    agent.update_knowledge()

    assert agent.safes == {(1, 1)}
    assert agent.knowledge == [Sentence(cells={(0, 1), (1, 0)}, count=1)]


def test_add_knowledge_applies_subset_inference() -> None:
    agent = MinesweeperAgent(
        board=Board(height=3, width=3),
        knowledge=[
            Sentence(cells={(0, 1), (1, 0)}, count=1),
        ],
    )

    agent.add_knowledge((0, 0), count=1)

    assert agent.safes == {(0, 0), (1, 1)}
    assert agent.mines == set()
    assert agent.knowledge == [Sentence(cells={(0, 1), (1, 0)}, count=1)]


def test_make_safe_move_returns_known_safe_move_not_already_made() -> None:
    agent = MinesweeperAgent(
        board=Board(height=3, width=3),
        safes={(0, 0), (0, 1)},
        moves_made={(0, 0)},
    )

    assert agent.make_safe_move() == (0, 1)


def test_make_safe_move_returns_none_when_no_safe_move_is_available() -> None:
    agent = MinesweeperAgent(
        board=Board(height=3, width=3),
        safes={(0, 0)},
        moves_made={(0, 0)},
    )

    assert agent.make_safe_move() is None


def test_make_random_move_excludes_known_mines() -> None:
    agent = MinesweeperAgent(
        board=Board(height=1, width=2),
        mines={(0, 0)},
    )

    assert agent.make_random_move() == (0, 1)


def test_make_random_move_excludes_moves_already_made() -> None:
    agent = MinesweeperAgent(
        board=Board(height=1, width=2),
        moves_made={(0, 0)},
    )

    assert agent.make_random_move() == (0, 1)


def test_make_random_move_returns_none_when_no_moves_are_available() -> None:
    agent = MinesweeperAgent(
        board=Board(height=1, width=2),
        moves_made={(0, 0)},
        mines={(0, 1)},
    )

    assert agent.make_random_move() is None


def test_mark_safe_records_trace_event() -> None:
    board = Board(height=2, width=2)
    agent = MinesweeperAgent(board=board)

    agent.mark_safe((0, 0))

    assert agent.trace[-1].kind == TraceEventKind.MARK_SAFE
    assert agent.trace[-1].cells == frozenset({(0, 0)})


def test_mark_mine_records_trace_event() -> None:
    board = Board(height=2, width=2)
    agent = MinesweeperAgent(board=board)

    agent.mark_mine((0, 0))

    assert agent.trace[-1].kind == TraceEventKind.MARK_MINE
    assert agent.trace[-1].cells == frozenset({(0, 0)})


def test_subset_inference_records_trace_event() -> None:
    board = Board(height=3, width=3)
    agent = MinesweeperAgent(board=board)
    agent.knowledge = [
        Sentence(cells={(0, 1), (1, 0)}, count=1),
        Sentence(cells={(0, 1), (1, 0), (1, 1)}, count=1),
    ]

    agent.update_knowledge()

    assert any(
        event.kind == TraceEventKind.INFER_SENTENCE
        and event.sentence == Sentence(cells={(1, 1)}, count=0)
        for event in agent.trace
    )
