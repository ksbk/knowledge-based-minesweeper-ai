# Knowledge-Based Minesweeper AI

A professional Python implementation of a knowledge-based Minesweeper agent.

The project focuses on symbolic knowledge representation, deterministic inference, and testable software design. The core AI engine is kept separate from any graphical interface so the reasoning logic can be audited directly.

## Current Status

Implemented:

- logical `Sentence` model
- deterministic `Board` model
- unit tests for sentence behavior
- unit tests for board boundaries, neighbors, and nearby mine counting
- development commands through `make`

Planned:

- agent memory model
- knowledge-base updates
- subset-based inference
- reasoning trace example
- optional visual demo

## Development

Install dependencies:

```bash
make install
