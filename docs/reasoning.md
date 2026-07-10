# Reasoning Model

This project uses deterministic symbolic inference rather than machine learning.

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

## Direct Inference

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

## Subset Inference

If one sentence is a subset of another, the agent may derive a new sentence.

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

## Limitations

The agent does not use probability or machine learning. It can infer safe cells and mines only when the current knowledge base logically supports that conclusion.

When deterministic inference is exhausted, the agent may choose an uncertain legal move and can lose. This is an expected limitation of the current design, not a hidden failure mode.
