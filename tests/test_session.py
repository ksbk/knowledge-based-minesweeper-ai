"""Tests for interface-independent Minesweeper game sessions."""

from minesweeper_ai.agent import MinesweeperAgent
from minesweeper_ai.board import Board
from minesweeper_ai.session import GameSession


def make_session() -> GameSession:
    """Return a small deterministic game session."""
    board = Board(height=2, width=2, mines={(0, 1)})
    agent = MinesweeperAgent(board=board)
    return GameSession(board=board, agent=agent)


def test_reveal_safe_cell_records_revealed_cell() -> None:
    session = make_session()

    session.reveal_cell((0, 0))

    assert session.revealed == {(0, 0)}


def test_reveal_safe_cell_updates_agent_knowledge() -> None:
    session = make_session()

    session.reveal_cell((0, 0))

    assert (0, 0) in session.agent.moves_made
    assert (0, 0) in session.agent.safes


def test_reveal_mine_marks_session_lost() -> None:
    session = make_session()

    session.reveal_cell((0, 1))

    assert session.lost is True


def test_cannot_reveal_flagged_cell() -> None:
    session = make_session()

    session.toggle_flag((0, 0))
    session.reveal_cell((0, 0))

    assert session.revealed == set()


def test_toggle_flag_adds_and_removes_flag() -> None:
    session = make_session()

    session.toggle_flag((0, 1))
    session.toggle_flag((0, 1))

    assert session.flags == set()


def test_cannot_flag_revealed_cell() -> None:
    session = make_session()

    session.reveal_cell((0, 0))
    session.toggle_flag((0, 0))

    assert session.flags == set()


def test_won_when_all_mines_are_flagged() -> None:
    session = make_session()

    session.toggle_flag((0, 1))

    assert session.won is True


def test_not_won_when_flags_do_not_match_mines() -> None:
    session = make_session()

    session.toggle_flag((1, 1))

    assert session.won is False


def test_ai_move_reveals_selected_cell() -> None:
    session = make_session()

    move = session.make_ai_move()

    assert move is not None
    assert move in session.revealed or session.lost
