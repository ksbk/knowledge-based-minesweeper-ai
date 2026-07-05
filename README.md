# Knowledge-Based Minesweeper AI

A professional Python implementation of a knowledge-based Minesweeper agent.

The project focuses on symbolic knowledge representation, deterministic inference, and testable software design. The core AI engine is kept separate from any graphical interface so the reasoning logic can be audited directly.

## Current Status

Implemented:

- logical `Sentence` model
- deterministic `Board` model
- agent knowledge state
- knowledge-base updates from revealed cells
- direct inference for known safe cells and mines
- subset-based inference
- safe and random move selection
- reasoning trace example
- command-line simulation mode
- unit tests for sentence, board, and agent behavior
- development commands through `make`

Planned:

- optional visual demo
- richer reasoning traces
- benchmark statistics across multiple boards

## Development

Install dependencies:

```bash
make install
```

Run tests and linting:

```bash
make check
```

Run tests only:

```bash
make test
```

Run linting only:

```bash
make lint
```

Format code:

```bash
make format
```

Clean generated files:

```bash
make clean
```

## Reasoning Trace Example

Run:

```bash
make example
```

This prints a deterministic reasoning trace showing how the agent uses subset inference.

Example output:

```text
Initial knowledge:
Known safes: {}
Known mines: {}
Knowledge:
  {(0, 1), (1, 0)} = 1

Reveal safe cell (0, 0) with nearby mine count 1.

After update:
Known safes: {(0, 0), (1, 1)}
Known mines: {}
Knowledge:
  {(0, 1), (1, 0)} = 1

Next safe move:
  (1, 1)
```

## Command-Line Simulation

Run:

```bash
make simulate
```

This runs a small board through the agent loop.

The simulation demonstrates the full engine flow:

- choose a known safe move when available
- choose an uncertain legal move when no safe move is known
- reveal nearby mine counts
- update the knowledge base
- infer new safe cells and mines where possible

Because the agent uses deterministic inference rather than probability, it may hit a mine when no safe move can be inferred.

## Project Structure

```text
src/minesweeper_ai/
  types.py      Shared type aliases
  sentence.py   Logical sentence representation
  board.py      Board model and neighboring-cell logic
  agent.py      Knowledge-based AI agent

tests/
  test_sentence.py
  test_board.py
  test_agent.py

examples/
  reasoning_trace.py
  simulate_game.py
```

## Design Direction

See [`docs/design-notes.md`](docs/design-notes.md) for the project design notes.
