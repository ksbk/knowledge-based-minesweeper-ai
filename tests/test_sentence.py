"""Tests for Minesweeper knowledge sentences."""

from minesweeper_ai.sentence import Sentence


def test_sentence_is_empty_when_no_cells_remain() -> None:
    sentence = Sentence(cells=set(), count=0)

    assert sentence.is_empty()


def test_sentence_is_not_empty_when_cells_remain() -> None:
    sentence = Sentence(cells={(0, 0)}, count=0)

    assert not sentence.is_empty()


def test_known_mines_when_count_equals_number_of_cells() -> None:
    sentence = Sentence(cells={(0, 0), (0, 1)}, count=2)

    assert sentence.known_mines() == {(0, 0), (0, 1)}


def test_known_mines_returns_empty_set_when_not_all_cells_are_mines() -> None:
    sentence = Sentence(cells={(0, 0), (0, 1)}, count=1)

    assert sentence.known_mines() == set()


def test_known_safes_when_count_is_zero() -> None:
    sentence = Sentence(cells={(0, 0), (0, 1)}, count=0)

    assert sentence.known_safes() == {(0, 0), (0, 1)}


def test_known_safes_returns_empty_set_when_count_is_not_zero() -> None:
    sentence = Sentence(cells={(0, 0), (0, 1)}, count=1)

    assert sentence.known_safes() == set()


def test_mark_mine_removes_cell_and_decreases_count() -> None:
    sentence = Sentence(cells={(0, 0), (0, 1)}, count=1)

    sentence.mark_mine((0, 0))

    assert sentence.cells == {(0, 1)}
    assert sentence.count == 0


def test_mark_mine_does_nothing_when_cell_is_absent() -> None:
    sentence = Sentence(cells={(0, 0), (0, 1)}, count=1)

    sentence.mark_mine((1, 1))

    assert sentence.cells == {(0, 0), (0, 1)}
    assert sentence.count == 1


def test_mark_safe_removes_cell_without_changing_count() -> None:
    sentence = Sentence(cells={(0, 0), (0, 1)}, count=1)

    sentence.mark_safe((0, 0))

    assert sentence.cells == {(0, 1)}
    assert sentence.count == 1


def test_mark_safe_does_nothing_when_cell_is_absent() -> None:
    sentence = Sentence(cells={(0, 0), (0, 1)}, count=1)

    sentence.mark_safe((1, 1))

    assert sentence.cells == {(0, 0), (0, 1)}
    assert sentence.count == 1


def test_known_mines_returns_copy_of_cells() -> None:
    sentence = Sentence(cells={(0, 0), (0, 1)}, count=2)

    mines = sentence.known_mines()
    mines.clear()

    assert sentence.cells == {(0, 0), (0, 1)}


def test_known_safes_returns_copy_of_cells() -> None:
    sentence = Sentence(cells={(0, 0), (0, 1)}, count=0)

    safes = sentence.known_safes()
    safes.clear()

    assert sentence.cells == {(0, 0), (0, 1)}
