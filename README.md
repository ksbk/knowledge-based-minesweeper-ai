# Knowledge-Based Minesweeper AI

A portfolio-ready implementation of Minesweeper built around a tested Python
symbolic AI engine, an interface-independent game session, and a dependency-free
static web demo.

The project focuses on symbolic knowledge representation, deterministic
inference, structured reasoning traces, and testable software design. The core
AI engine remains separate from user interfaces so its reasoning can be audited
directly.

## Current Status

Version 1.2.0 includes:

- a tested Python engine with direct and subset-based logical inference
- an interface-independent `GameSession`
- structured reasoning trace output
- command-line examples and simulation
- a configurable static web gameplay demo
- a Python-backed browser client served by a local API
- development and validation commands through `make`

## Web Modes

### Static Browser-Only Demo

The static web UI supports reveal, flag, restart, win/loss status, a session
trace, and configurable gameplay:

| Setting | Options | Behavior |
| --- | --- | --- |
| Difficulty | Easy, Intermediate, Hard | Uses 8x8 with 8 mines, 10x10 with 15 mines, or 12x12 with 25 mines. |
| Reveal style | Classic, Tactical | Classic expands connected empty safe areas; Tactical reveals only the selected cell. |
| Helper | Available, Hidden | Shows or hides the browser-side Helper move control. |

Open [`ui/web/index.html`](ui/web/index.html) directly in a browser. On macOS:

```bash
open ui/web/index.html
```

The web demo has no runtime dependencies. Its gameplay state and Helper logic
run in browser-side JavaScript.

### Python-Backed Browser Client

The Python-backed client is a separate browser experience backed by the Python
`GameSession` and `MinesweeperAgent`. It uses only the Python standard library
and does not modify or replace the static browser demo.

Start the server:

```bash
uv run python examples/web_server.py
```

Then open:

```text
http://127.0.0.1:8000/client/
```

The client displays Python game state and reasoning output. Reveals, flags, new
games, AI suggestions, and Helper moves all flow through the local JSON API.
Unlike the standalone demo, `ui/api/index.html` requires the server and should
be opened through the `/client/` URL.

The API remains available directly for inspection:

```bash
curl http://127.0.0.1:8000/api/game

curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"row": 0, "col": 0}' \
  http://127.0.0.1:8000/api/game/reveal
```

`ui/web/index.html` remains the independent browser-side experience and does
not require the Python server.

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
  session.py    Interface-independent game session
  trace.py      Structured reasoning trace events
  web_adapter.py
                Serializable adapter for Python-backed web actions

tests/
  ...           Unit tests for the engine, session, and traces

examples/
  reasoning_trace.py
  simulate_game.py
  web_server.py Local standard-library JSON API server

ui/web/
  index.html    Static gameplay demo
  app.js        Browser-side game state and interactions
  styles.css    Web UI presentation

ui/api/
  index.html    Python-backed browser client
  app.js        JSON API interactions and rendering
  styles.css    API client presentation
```

## Design Direction

See [`docs/design-notes.md`](docs/design-notes.md) for the project design notes.
