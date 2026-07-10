# Demo and Usage

This project has two browser-facing modes and two command-line examples.

## Public Static Demo

The public static demo is available through GitHub Pages:

```text
https://ksbk.github.io/knowledge-based-minesweeper-ai/
```

It supports reveal, flag, restart, win/loss status, a session trace, and configurable gameplay.

| Setting | Options | Behavior |
| --- | --- | --- |
| Difficulty | Beginner, Easy, Intermediate, Hard | Uses 5x5 with 3 mines, 8x8 with 8 mines, 10x10 with 15 mines, or 12x12 with 25 mines. |
| Reveal style | Classic, Tactical | Classic expands connected empty safe areas; Tactical reveals only the selected cell. |
| Helper | Available, Hidden | Shows or hides the browser-side Helper move control. |

The static demo has no runtime dependencies. Its gameplay state and helper logic run in browser-side JavaScript.

## Run the Static Demo Locally

Open [`ui/web/index.html`](../ui/web/index.html) directly in a browser.

macOS:

```bash
open ui/web/index.html
```

Linux:

```bash
xdg-open ui/web/index.html
```

Windows PowerShell:

```powershell
start ui/web/index.html
```

## Python-Backed Browser Client

The Python-backed client is a separate browser experience backed by the Python `GameSession` and `MinesweeperAgent`. It uses only the Python standard library and does not modify or replace the static browser demo.

Start the server:

```bash
uv run python examples/web_server.py
```

Then open:

```text
http://127.0.0.1:8000/client/
```

The client displays Python game state and reasoning output. Reveals, flags, new games, AI suggestions, and helper moves all flow through the local JSON API.

Unlike the standalone demo, `ui/api/index.html` requires the server and should be opened through the `/client/` URL.

## API Inspection

The local API remains available directly for inspection:

```bash
curl http://127.0.0.1:8000/api/game
```

Reveal a cell:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"row": 0, "col": 0}' \
  http://127.0.0.1:8000/api/game/reveal
```

## GitHub Pages Publishing Notes

This repository includes a Pages workflow that publishes only the static demo from `ui/web/`. It does not deploy the Python server or API-backed client.

If GitHub Pages is not already enabled for this repository:

1. Open repository Settings > Pages.
2. Set Source to GitHub Actions.
3. Push to `main` or run the Pages workflow manually.

After deployment, verify the public demo at:

```text
https://ksbk.github.io/knowledge-based-minesweeper-ai/
```

Verification checklist:

1. The page loads without starting `examples/web_server.py`.
2. Reveal, flag, and restart interactions work in the browser.
3. Difficulty, reveal style, and helper visibility controls update gameplay.
4. Browser developer tools show no requests to `/api/` endpoints.
