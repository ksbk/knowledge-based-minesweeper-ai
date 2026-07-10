"""Tests for public package exports."""

from minesweeper_ai import Board, GameSession, MinesweeperAgent, Sentence
from minesweeper_ai.agent import MinesweeperAgent as AgentModuleExport
from minesweeper_ai.board import Board as BoardModuleExport
from minesweeper_ai.sentence import Sentence as SentenceModuleExport
from minesweeper_ai.session import GameSession as SessionModuleExport


def test_public_package_exports_match_module_classes() -> None:
    assert Board is BoardModuleExport
    assert GameSession is SessionModuleExport
    assert MinesweeperAgent is AgentModuleExport
    assert Sentence is SentenceModuleExport
