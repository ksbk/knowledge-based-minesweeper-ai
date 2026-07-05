"""Demonstrate a reasoning trace for the Minesweeper AI agent."""

from minesweeper_ai.agent import MinesweeperAgent
from minesweeper_ai.board import Board
from minesweeper_ai.sentence import Sentence


def format_cells(cells: set[tuple[int, int]]) -> str:
    """Return a stable string representation of cells."""
    return "{" + ", ".join(str(cell) for cell in sorted(cells)) + "}"


def print_agent_state(agent: MinesweeperAgent) -> None:
    """Print the current agent knowledge state."""
    print(f"Known safes: {format_cells(agent.safes)}")
    print(f"Known mines: {format_cells(agent.mines)}")

    print("Knowledge:")
    if not agent.knowledge:
        print("  <empty>")
        return

    for sentence in agent.knowledge:
        print(f"  {format_cells(sentence.cells)} = {sentence.count}")


def main() -> None:
    """Run a small deterministic reasoning example."""
    board = Board(height=3, width=3)
    agent = MinesweeperAgent(
        board=board,
        knowledge=[
            Sentence(cells={(0, 1), (1, 0)}, count=1),
        ],
    )

    print("Initial knowledge:")
    print_agent_state(agent)

    print()
    print("Reveal safe cell (0, 0) with nearby mine count 1.")
    agent.add_knowledge((0, 0), count=1)

    print()
    print("After update:")
    print_agent_state(agent)

    print()
    print("Next safe move:")
    print(f"  {agent.make_safe_move()}")


if __name__ == "__main__":
    main()