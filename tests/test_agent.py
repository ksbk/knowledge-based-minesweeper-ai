"""Tests for the Minesweeper AI agent."""

from minesweeper_ai.agent import MinesweeperAgent
from minesweeper_ai.sentence import Sentence


def test_agent_starts_with_empty_knowledge_state() -> None:
    agent = MinesweeperAgent(height=3, width=3)

    assert agent.moves_made == set()
    assert agent.safes == set()
    assert agent.mines == set()
    assert agent.knowledge == []


def test_mark_safe_records_safe_cell() -> None:
    agent = MinesweeperAgent(height=3, width=3)

    agent.mark_safe((0, 0))

    assert agent.safes == {(0, 0)}


def test_mark_mine_records_mine_cell() -> None:
    agent = MinesweeperAgent(height=3, width=3)

    agent.mark_mine((0, 0))

    assert agent.mines == {(0, 0)}


def test_mark_safe_updates_existing_sentences() -> None:
    agent = MinesweeperAgent(
        height=3,
        width=3,
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
    agent = MinesweeperAgent(
        height=3,
        width=3,
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