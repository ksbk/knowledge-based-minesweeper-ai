# Design Notes: Knowledge-Based Minesweeper AI

## Purpose

This project builds a Minesweeper AI agent as a small, professional Python package.

The goal is not only to make the agent play Minesweeper. The goal is to make the reasoning process clear, testable, and auditable by another developer.

The project focuses on:

- symbolic knowledge representation
- deterministic inference
- clean separation between reasoning logic and user interface
- tests that demonstrate the behavior of the AI engine
- documentation that explains both strengths and limitations

## Why Minesweeper Is a Good AI Problem

Minesweeper is useful because each revealed cell gives partial information about nearby hidden cells.

For example, if a revealed cell says `1`, and it has three unrevealed neighboring cells, then exactly one of those neighboring cells is a mine.

This creates a constraint:

```text
{A, B, C} = 1
```

The AI can collect many constraints like this and use them to infer which cells are safe and which cells must be mines.

## Core Idea

The AI maintains a knowledge base of logical sentences.

A sentence has two parts:

```text
set of cells = mine count
```

Example:

```text
{(0, 1), (1, 0), (1, 1)} = 1
```

This means exactly one of those three cells is a mine.

The AI updates its knowledge after every revealed safe cell.

## Main Components

The project is designed around a small set of focused modules.

```text
src/minesweeper_ai/
  types.py      Shared type aliases
  sentence.py   Logical sentence representation
  agent.py      Knowledge-based AI agent
  board.py      Minesweeper board model
```

The reasoning engine should not depend on Pygame or any graphical interface.

A graphical demo can be added later, but the core AI must be testable from the command line.

## Sentence Model

A `Sentence` represents one logical statement about the board.

Example:

```text
cells = {(0, 1), (1, 0), (1, 1)}
count = 1
```

This means one of those cells is a mine.

The sentence should be able to answer:

- Which cells are definitely mines?
- Which cells are definitely safe?
- How should the sentence change when a cell is known to be safe?
- How should the sentence change when a cell is known to be a mine?

## Basic Inference Rules

The first level of inference is direct knowledge.

If the mine count is `0`, all cells in the sentence are safe:

```text
{A, B, C} = 0
=> A, B, and C are safe
```

If the mine count equals the number of cells, all cells in the sentence are mines:

```text
{A, B, C} = 3
=> A, B, and C are mines
```

The second level of inference uses subset relationships.

If one sentence is a subset of another, the AI may derive a new sentence.

Example:

```text
{A, B, C} = 1
{A, B} = 1
```

Since `{A, B}` already contains one mine, `C` must be safe:

```text
{C} = 0
```

Another example:

```text
{A, B, C} = 2
{A, B} = 1
```

The remaining cell must contain one mine:

```text
{C} = 1
```

## Agent Responsibilities

The AI agent is responsible for:

- remembering moves already made
- remembering cells known to be safe
- remembering cells known to be mines
- adding new knowledge after a safe cell is revealed
- updating old sentences when new safe cells or mines are discovered
- deriving new sentences through inference
- choosing a known safe move when possible
- choosing an uncertain move only when no safe move is known

The agent should not be responsible for rendering graphics.

## Board Responsibilities

The board model is responsible for:

- storing board dimensions
- storing mine locations
- counting nearby mines
- checking whether a cell is inside the board
- returning neighboring cells
- supporting deterministic tests

The board should support predictable setups for tests instead of relying only on random mine placement.

## Testing Strategy

The tests should make the reasoning behavior auditable.

Important tests include:

- a sentence with count `0` marks all cells safe
- a sentence where count equals number of cells marks all cells as mines
- marking a mine removes it from a sentence and reduces the count
- marking a safe cell removes it from a sentence without reducing the count
- subset inference derives new knowledge correctly
- the agent never chooses a known mine as a random move
- the agent prefers known safe moves over uncertain moves
- board neighbor counting works on corners, edges, and middle cells

## Design Principle

The core design principle is:

```text
Make the AI reasoning inspectable before making the game visually impressive.
```

The professional value of this project comes from the clarity of the reasoning engine, tests, and documentation.

The Pygame interface is optional. The AI engine is the main artifact.

## Limitations

This AI uses deterministic logical inference.

When no safe move can be inferred, the agent may need to choose an uncertain move. This means the agent cannot guarantee perfect play in every board state.

This limitation is acceptable because the purpose of the project is to demonstrate symbolic reasoning, knowledge representation, and constraint-based inference.

## Future Improvements

Possible future improvements include:

- probability-based move selection when deterministic inference is exhausted
- richer reasoning traces for debugging
- command-line simulation mode
- Pygame visual demo
- benchmark statistics across many random boards
- improved documentation diagrams
- CI checks with tests and linting

## Portfolio Positioning

This project should be presented as a case study in symbolic AI and professional Python engineering.

The portfolio page should focus on:

- the problem
- the knowledge representation
- the inference algorithm
- the testing strategy
- the limitations
- what the project demonstrates professionally

The project should be honest about its learning origin while showing that it has been rebuilt into an auditable software artifact.
