# Architecture

This project separates the Minesweeper reasoning engine from command-line and browser interfaces.

## Design Goal

The core AI should be testable without a UI. Browser and command-line layers should call into the same game-session and reasoning code instead of duplicating the AI logic.

## Module Map

```text
src/minesweeper_ai/
  types.py      Shared type aliases
  sentence.py   Logical sentence representation
  board.py      Board model and neighboring-cell logic
  agent.py      Knowledge-based inference agent
  session.py    Interface-independent game session
  trace.py      Structured reasoning trace events
  web_adapter.py
                Serializable adapter for Python-backed web actions
```

## Core Modules

### `sentence.py`

Represents a logical constraint:

```text
set of cells = mine count
```

A sentence can identify definite mines, identify definite safe cells, and update itself when a cell becomes known.

### `agent.py`

Maintains the knowledge base and applies inference rules. The agent tracks known safe cells, known mines, moves already made, and derived sentences.

### `board.py`

Models board dimensions, mine locations, neighboring cells, and nearby mine counts. It supports predictable setups for tests.

### `session.py`

Coordinates board state and agent behavior without depending on any particular interface. CLI examples and browser-facing adapters use the same session layer.

### `trace.py`

Defines structured reasoning events so AI behavior can be inspected without relying only on printed text.

### `web_adapter.py`

Converts session state and actions into JSON-friendly data for the Python-backed browser client.

## Interface Layers

```text
examples/
  reasoning_trace.py  CLI reasoning trace
  simulate_game.py    CLI board simulation
  web_server.py       Local standard-library JSON API server

ui/web/
  index.html          Standalone browser demo
  app.js              Browser-side game state and interactions
  styles.css          Static demo presentation

ui/api/
  index.html          Python-backed browser client
  app.js              JSON API interactions and rendering
  styles.css          API client presentation
```

## Data Flow

### CLI examples

```text
example script -> GameSession / MinesweeperAgent -> trace or console output
```

### Static browser demo

```text
ui/web JavaScript -> browser-side game state -> browser UI
```

The static demo is dependency-free and does not call the Python engine.

### Python-backed browser client

```text
browser client -> local JSON API -> GameSession -> MinesweeperAgent -> JSON response -> browser UI
```

This mode uses the tested Python game-session and reasoning code through a local server.

## Why This Separation Matters

- The AI engine can be unit tested directly.
- UI changes do not require changing inference logic.
- CLI and browser tools can share the same game-session behavior.
- Limitations are easier to inspect because reasoning is not hidden inside the UI.
