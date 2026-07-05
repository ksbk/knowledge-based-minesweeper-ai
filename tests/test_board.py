"""Tests for the Minesweeper board model."""

from minesweeper_ai.board import Board


def test_cell_inside_board() -> None:
    board = Board(height=3, width=3)

    assert board.is_inside((0, 0))
    assert board.is_inside((2, 2))


def test_cell_outside_board() -> None:
    board = Board(height=3, width=3)

    assert not board.is_inside((-1, 0))
    assert not board.is_inside((0, -1))
    assert not board.is_inside((3, 0))
    assert not board.is_inside((0, 3))


def test_corner_cell_has_three_neighbors() -> None:
    board = Board(height=3, width=3)

    assert board.neighbors((0, 0)) == {(0, 1), (1, 0), (1, 1)}


def test_edge_cell_has_five_neighbors() -> None:
    board = Board(height=3, width=3)

    assert board.neighbors((0, 1)) == {
        (0, 0),
        (0, 2),
        (1, 0),
        (1, 1),
        (1, 2),
    }


def test_middle_cell_has_eight_neighbors() -> None:
    board = Board(height=3, width=3)

    assert board.neighbors((1, 1)) == {
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 2),
        (2, 0),
        (2, 1),
        (2, 2),
    }


def test_nearby_mines_counts_neighboring_mines() -> None:
    board = Board(height=3, width=3, mines={(0, 0), (0, 2), (2, 2)})

    assert board.nearby_mines((1, 1)) == 3


def test_nearby_mines_does_not_count_the_cell_itself() -> None:
    board = Board(height=3, width=3, mines={(1, 1)})

    assert board.nearby_mines((1, 1)) == 0
