# Knowledge-Based Minesweeper AI

A Python implementation of Minesweeper built around a tested symbolic AI engine, structured reasoning traces, and browser interfaces.

The project focuses on symbolic knowledge representation, deterministic inference, interface-independent design, and testable software behavior. The core AI engine remains separate from user interfaces so its reasoning can be inspected directly.

## Links

- Demo: https://ksbk.github.io/knowledge-based-minesweeper-ai/
- Repository: https://github.com/ksbk/knowledge-based-minesweeper-ai
- Releases: https://github.com/ksbk/knowledge-based-minesweeper-ai/releases

## Overview

This project is an incremental Python implementation of symbolic Minesweeper reasoning, built through tagged releases from a bare AI engine to a configurable two-interface application.

- **Knowledge-based inference:** logical constraint sentences identify safe cells and mines without guessing where possible.
- **Interface-independent design:** the Python game session and AI engine are separate from command-line and browser interfaces.
- **Multiple interfaces:** command-line examples, a standalone static browser demo, and a local Python-backed browser client exercise the project from different layers.
- **Reasoning traces:** AI behavior can be inspected rather than treated as a black box.
- **Testing:** core reasoning behavior is covered by unit tests and checked with linting.
- **Known limits:** the agent uses deterministic inference and can lose when no safe move is logically known.

## Usage

Requires Python 3.13 or newer.

Install dependencies:

```bash
make install
```

Run tests and linting:

```bash
make check
```

Run a reasoning trace:

```bash
make example
```

Run a board simulation:

```bash
make simulate
```

Run the Python-backed browser client:

```bash
uv run python examples/web_server.py
```

Then open:

```text
http://127.0.0.1:8000/client/
```

The dependency-free static browser demo can also be opened directly from `ui/web/index.html`. See [`docs/demo.md`](docs/demo.md) for cross-platform commands and demo details.

## Architecture

```text
src/minesweeper_ai/
  sentence.py   Logical constraint sentences
  agent.py      Knowledge-based inference agent
  board.py      Board and neighboring-cell model
  session.py    Interface-independent game session
  trace.py      Structured reasoning trace events
  web_adapter.py JSON-friendly web adapter
```

Detailed architecture notes are in [`docs/architecture.md`](docs/architecture.md).

## Testing

- Unit tests for core reasoning behavior
- Ruff linting through `make check`
- Interface-independent Python engine
- Browser and command-line interfaces
- Structured reasoning trace output
- Tagged release history
- Documented limitations

## Limitations

The agent uses deterministic symbolic inference. When no safe move can be inferred, it may choose an uncertain legal move and can reveal a mine. This is an expected limitation of the current design.

## Documentation

- [`docs/README.md`](docs/README.md) — documentation index
- [`docs/architecture.md`](docs/architecture.md) — module boundaries, data flow, and interface separation
- [`docs/reasoning.md`](docs/reasoning.md) — knowledge representation, inference rules, trace example, and simulation flow
- [`docs/demo.md`](docs/demo.md) — static demo, Python-backed browser client, and API examples
- [`docs/design-notes.md`](docs/design-notes.md) — design principles and project rationale
- [`docs/roadmap.md`](docs/roadmap.md) — released milestones and planned improvements
- [`docs/reviews/project-readiness.md`](docs/reviews/project-readiness.md) — technical readiness review

## Development Commands

```bash
make test
make lint
make format
make clean
```
