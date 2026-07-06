"""Run a small command-line Minesweeper AI simulation."""

from minesweeper_ai.agent import MinesweeperAgent
from minesweeper_ai.board import Board
from minesweeper_ai.session import GameSession
from minesweeper_ai.types import Cell


def format_cells(cells: set[Cell]) -> str:
    """Return a stable string representation of cells."""
    return "{" + ", ".join(str(cell) for cell in sorted(cells)) + "}"


def print_session_state(session: GameSession) -> None:
    """Print the current session and agent state."""
    print(f"Revealed:    {format_cells(session.revealed)}")
    print(f"Flags:       {format_cells(session.flags)}")
    print(f"Known safes: {format_cells(session.agent.safes)}")
    print(f"Known mines: {format_cells(session.agent.mines)}")

    if session.lost:
        print("Session:     lost")
    elif session.won:
        print("Session:     won")
    else:
        print("Session:     active")

    print("Knowledge:")
    if not session.agent.knowledge:
        print("  <empty>")
    else:
        for sentence in session.agent.knowledge:
            print(f"  {format_cells(sentence.cells)} = {sentence.count}")


def move_type(session: GameSession, move: Cell) -> str:
    """Return whether a move was known safe or uncertain."""
    if move in session.agent.safes - session.agent.moves_made:
        return "known safe"
    return "uncertain"


def run_simulation() -> None:
    """Run a deterministic Minesweeper simulation."""
    board = Board(height=3, width=3, mines={(0, 2), (2, 0)})
    agent = MinesweeperAgent(board=board)
    session = GameSession(board=board, agent=agent)

    print("Minesweeper AI simulation")
    print("=========================")
    print(f"Board size: {board.height}x{board.width}")
    print(f"Mines: {len(board.mines)}")
    print(f"Hidden mines for this demo: {format_cells(board.mines)}")
    print()

    step = 1

    while True:
        move = session.suggest_ai_move()

        if move is None:
            print("No legal moves remain.")
            break

        kind = move_type(session, move)

        print(f"Step {step}")
        print(f"Move: {move}")
        print(f"Move type: {kind}")

        if move in board.mines:
            session.reveal_cell(move)
            print("Result: hit a mine.")
            print_session_state(session)
            break

        nearby_count = board.nearby_mines(move)
        session.reveal_cell(move)
        print(f"Result: safe cell with {nearby_count} nearby mine(s).")
        print_session_state(session)
        print()

        if session.revealed | session.agent.mines == board.cells():
            print("All non-mine cells have been explored.")
            break

        step += 1


if __name__ == "__main__":
    run_simulation()
