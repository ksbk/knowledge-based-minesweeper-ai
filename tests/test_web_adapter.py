"""Tests for the plain Python web game adapter."""

import json
import random

import pytest

from minesweeper_ai.agent import MinesweeperAgent
from minesweeper_ai.board import Board
from minesweeper_ai.session import GameSession
from minesweeper_ai.web_adapter import WebGameAdapter


def make_adapter() -> WebGameAdapter:
    """Return an adapter with deterministic mine placement."""
    return WebGameAdapter(rng=random.Random(7))


def make_adapter_with_flagged_safe() -> tuple[WebGameAdapter, tuple[int, int]]:
    """Return an adapter whose session suggests a flagged safe cell first."""
    adapter = make_adapter()
    flagged_safe = next(
        iter(adapter.session.board.cells() - adapter.session.board.mines)
    )
    adapter.session.agent.safes = {flagged_safe}
    adapter.session.flags = {flagged_safe}
    return adapter, flagged_safe


def test_new_game_uses_beginner_difficulty() -> None:
    adapter = make_adapter()

    state = adapter.new_game("beginner")

    assert state["difficulty"] == "beginner"
    assert state["height"] == 5
    assert state["width"] == 5
    assert state["mine_count"] == 3


def test_new_game_uses_selected_difficulty() -> None:
    adapter = make_adapter()

    state = adapter.new_game("intermediate")

    assert state["difficulty"] == "intermediate"
    assert state["height"] == 10
    assert state["width"] == 10
    assert state["mine_count"] == 15


def test_reveal_flows_through_session_and_updates_agent() -> None:
    adapter = make_adapter()
    board = adapter.session.board
    safe_cell = next(iter(board.cells() - board.mines))

    state = adapter.reveal(*safe_cell)

    assert safe_cell in adapter.session.revealed
    assert safe_cell in adapter.session.agent.moves_made
    assert safe_cell in adapter.session.agent.safes
    assert any((cell["row"], cell["col"]) == safe_cell for cell in state["revealed"])


def test_toggle_flag_flows_through_session() -> None:
    adapter = make_adapter()
    cell = (0, 0)

    flagged_state = adapter.toggle_flag(*cell)
    unflagged_state = adapter.toggle_flag(*cell)

    assert flagged_state["flags"] == [{"row": 0, "col": 0}]
    assert unflagged_state["flags"] == []


def test_suggestion_and_helper_move_use_python_agent() -> None:
    adapter = make_adapter()

    suggestion = adapter.suggest_move()
    state = adapter.helper_move()

    assert suggestion is not None
    assert state["helper_move"] == suggestion
    assert state["revealed"] or state["lost"]


def test_suggestion_does_not_return_flagged_cell() -> None:
    adapter, flagged_safe = make_adapter_with_flagged_safe()

    suggestion = adapter.suggest_move()

    assert suggestion != {
        "row": flagged_safe[0],
        "col": flagged_safe[1],
    }
    if suggestion is not None:
        suggested_cell = (suggestion["row"], suggestion["col"])
        assert suggested_cell not in adapter.session.flags
        assert suggested_cell not in adapter.session.revealed


def test_suggestion_does_not_return_revealed_cell() -> None:
    adapter = make_adapter()
    revealed_safe = next(
        iter(adapter.session.board.cells() - adapter.session.board.mines)
    )
    adapter.session.agent.safes = {revealed_safe}
    adapter.session.revealed = {revealed_safe}

    suggestion = adapter.suggest_move()

    assert suggestion != {
        "row": revealed_safe[0],
        "col": revealed_safe[1],
    }


def test_helper_does_not_report_flagged_move_as_applied() -> None:
    adapter, flagged_safe = make_adapter_with_flagged_safe()

    state = adapter.helper_move()

    assert state["helper_move"] != {
        "row": flagged_safe[0],
        "col": flagged_safe[1],
    }
    assert flagged_safe in adapter.session.flags


def test_helper_reports_applied_valid_move_or_no_move() -> None:
    adapter, _ = make_adapter_with_flagged_safe()
    blocked_before = adapter.session.flags | adapter.session.revealed

    state = adapter.helper_move()
    move = state["helper_move"]

    if move is not None:
        moved_cell = (move["row"], move["col"])
        assert moved_cell not in blocked_before
        assert moved_cell in adapter.session.revealed or adapter.session.lost

    adapter = make_adapter()
    adapter.session.flags = adapter.session.board.cells()

    assert adapter.helper_move()["helper_move"] is None


def test_state_hides_mines_until_game_over() -> None:
    adapter = make_adapter()
    mine = next(iter(adapter.session.board.mines))

    initial_state = adapter.state()
    lost_state = adapter.reveal(*mine)

    assert initial_state["visible_mines"] == []
    assert lost_state["lost"] is True
    assert len(lost_state["visible_mines"]) == lost_state["mine_count"]


def test_state_is_json_serializable() -> None:
    adapter = make_adapter()

    encoded = json.dumps(adapter.state())

    assert '"difficulty": "beginner"' in encoded


def test_classic_reveal_expands_empty_cells() -> None:
    mines = {(2, 2)}
    board = Board(height=3, width=3, mines=mines)
    adapter = make_adapter()
    adapter.session = GameSession(board=board, agent=MinesweeperAgent(board=board))
    adapter.reveal_style = "classic"

    adapter.reveal(0, 0)

    # Classic reveal flood-fills all safe cells reachable from (0, 0).
    assert len(adapter.session.revealed) > 1
    assert (2, 2) not in adapter.session.revealed


def test_tactical_reveal_reveals_only_selected_cell() -> None:
    mines = {(2, 2)}
    board = Board(height=3, width=3, mines=mines)
    adapter = make_adapter()
    adapter.session = GameSession(board=board, agent=MinesweeperAgent(board=board))
    adapter.reveal_style = "tactical"

    adapter.reveal(0, 0)

    assert adapter.session.revealed == {(0, 0)}


def test_new_game_stores_reveal_style() -> None:
    adapter = make_adapter()

    state = adapter.new_game("beginner", "tactical")

    assert state["reveal_style"] == "tactical"
    assert adapter.reveal_style == "tactical"


def test_state_includes_reveal_style() -> None:
    adapter = make_adapter()

    state = adapter.state()

    assert state["reveal_style"] == "classic"


def test_new_game_rejects_unknown_reveal_style() -> None:
    adapter = make_adapter()

    with pytest.raises(ValueError, match="Unknown reveal style"):
        adapter.new_game("beginner", "fancy")


@pytest.mark.parametrize(
    ("row", "col"),
    [
        (-1, 0),
        (0, 8),
        (True, 0),
        (0, "1"),
    ],
)
def test_actions_reject_invalid_cells(row: object, col: object) -> None:
    adapter = make_adapter()

    with pytest.raises(ValueError):
        adapter.reveal(row, col)  # type: ignore[arg-type]


def test_new_game_rejects_unknown_difficulty() -> None:
    adapter = make_adapter()

    with pytest.raises(ValueError, match="Unknown difficulty"):
        adapter.new_game("expert")
