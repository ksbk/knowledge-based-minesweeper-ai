"""Run a small command-line Minesweeper AI simulation."""

from minesweeper_ai.agent import MinesweeperAgent
from minesweeper_ai.board import Board
from minesweeper_ai.types import Cell


def format_cells(cells: set[Cell]) -> str:
    """Return a stable string representation of cells."""
    return "{" + ", ".join(str(cell) for cell in sorted(cells)) + "}"


def print_agent_state(agent: MinesweeperAgent) -> None:
    """Print the current agent state."""
    print(f"Moves made:  {format_cells(agent.moves_made)}")
    print(f"Known safes: {format_cells(agent.safes)}")
    print(f"Known mines: {format_cells(agent.mines)}")

    print("Knowledge:")
    if not agent.knowledge:
        print("  <empty>")
    else:
        for sentence in agent.knowledge:
            print(f"  {format_cells(sentence.cells)} = {sentence.count}")


def choose_move(agent: MinesweeperAgent) -> Cell | None:
    """Choose a safe move if possible, otherwise choose an uncertain move."""
    safe_move = agent.make_safe_move()
    if safe_move is not None:
        return safe_move

    return agent.make_random_move()


def run_simulation() -> None:
    """Run a deterministic Minesweeper simulation."""
    board = Board(height=3, width=3, mines={(0, 2), (2, 0)})
    agent = MinesweeperAgent(board=board)

    print("Minesweeper AI simulation")
    print("=========================")
    print(f"Board size: {board.height}x{board.width}")
    print(f"Hidden mines for this demo: {format_cells(board.mines)}")
    print()

    step = 1

    while True:
        move = choose_move(agent)

        if move is None:
            print("No legal moves remain.")
            break

        print(f"Step {step}: choose {move}")

        if move in board.mines:
            print("Result: hit a mine.")
            break

        nearby_count = board.nearby_mines(move)
        print(f"Result: safe cell with {nearby_count} nearby mine(s).")

        agent.add_knowledge(move, nearby_count)
        print_agent_state(agent)
        print()

        if agent.moves_made | agent.mines == board.cells():
            print("All non-mine cells have been explored.")
            break

        step += 1


if __name__ == "__main__":
    run_simulation()
