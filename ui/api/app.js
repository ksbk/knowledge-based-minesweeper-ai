const boardElement = document.querySelector("#board");
const statusElement = document.querySelector("#status");
const connectionElement = document.querySelector("#connection-message");
const difficultyElement = document.querySelector("#difficulty");
const suggestButton = document.querySelector("#suggest-button");
const helperButton = document.querySelector("#helper-button");
const newGameButton = document.querySelector("#new-game-button");
const knownSafesElement = document.querySelector("#known-safes");
const knownMinesElement = document.querySelector("#known-mines");
const suggestedMoveElement = document.querySelector("#suggested-move");
const helperMoveElement = document.querySelector("#helper-move");
const traceListElement = document.querySelector("#trace-list");

let game = null;
let suggestion = null;
let suggestionRequested = false;
let helperMove = null;
let requestInFlight = false;

function cellKey(cell) {
  return `${cell.row},${cell.col}`;
}

function cellLabel(cell) {
  return `(${cell.row}, ${cell.col})`;
}

function formatCells(cells) {
  return cells.length > 0 ? cells.map(cellLabel).join(", ") : "None yet";
}

async function requestJson(path, options = {}) {
  const response = await fetch(path, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  });

  const payload = await response.json();

  if (!response.ok) {
    throw new Error(payload.error || `Request failed with status ${response.status}.`);
  }

  return payload;
}

function setConnection(message, state) {
  connectionElement.textContent = message;
  connectionElement.dataset.state = state;
}

function showConnected() {
  setConnection("Connected to the local Python API.", "connected");
}

function showError(error) {
  setConnection(
    `Unable to use the Python API. Run "uv run python examples/web_server.py" and reload this page. ${error.message}`,
    "error",
  );
}

function setBusy(isBusy) {
  requestInFlight = isBusy;

  if (isBusy) {
    renderControls();
  } else {
    render();
  }
}

async function runAction(action) {
  setBusy(true);

  try {
    await action();
    showConnected();
  } catch (error) {
    showError(error);
  } finally {
    setBusy(false);
  }
}

function isGameOver() {
  return game?.lost || game?.won;
}

function renderControls() {
  const hasGame = game !== null;
  const gameOver = hasGame && isGameOver();

  difficultyElement.disabled = requestInFlight;
  newGameButton.disabled = requestInFlight;
  suggestButton.disabled = requestInFlight || !hasGame || gameOver;
  helperButton.disabled = requestInFlight || !hasGame || gameOver;
}

function renderStatus() {
  if (game === null) {
    statusElement.textContent = "Waiting for game state.";
    return;
  }

  if (game.won) {
    statusElement.textContent = "Game won. All mines have been flagged.";
    return;
  }

  if (game.lost) {
    statusElement.textContent = "Game over. A mine was revealed.";
    return;
  }

  statusElement.textContent =
    `${game.difficulty} game: ${game.height}x${game.width} board with ` +
    `${game.mine_count} mines. Left-click to reveal; right-click to flag.`;
}

function renderBoard() {
  boardElement.innerHTML = "";

  if (game === null) {
    return;
  }

  boardElement.style.setProperty("--board-width", game.width);

  const revealed = new Map(game.revealed.map((cell) => [cellKey(cell), cell]));
  const flags = new Set(game.flags.map(cellKey));
  const visibleMines = new Set(game.visible_mines.map(cellKey));

  for (let row = 0; row < game.height; row += 1) {
    for (let col = 0; col < game.width; col += 1) {
      const cell = { row, col };
      const key = cellKey(cell);
      const revealedCell = revealed.get(key);
      const isFlagged = flags.has(key);
      const isVisibleMine = visibleMines.has(key);
      const button = document.createElement("button");

      button.className = "cell";
      button.type = "button";

      if (isVisibleMine) {
        button.dataset.state = "mine";
        button.textContent = "✹";
        button.setAttribute("aria-label", `Mine at ${cellLabel(cell)}`);
      } else if (revealedCell !== undefined) {
        button.dataset.state = "revealed";
        button.textContent =
          revealedCell.nearby_mines > 0
            ? String(revealedCell.nearby_mines)
            : "";
        button.setAttribute(
          "aria-label",
          `Revealed safe cell ${cellLabel(cell)} with ${revealedCell.nearby_mines} nearby mine(s)`,
        );
      } else if (isFlagged) {
        button.dataset.state = "flagged";
        button.textContent = "⚑";
        button.setAttribute("aria-label", `Flagged cell ${cellLabel(cell)}`);
      } else {
        button.dataset.state = "hidden";
        button.textContent = "";
        button.setAttribute("aria-label", `Hidden cell ${cellLabel(cell)}`);
      }

      button.disabled = requestInFlight || isGameOver() || revealedCell !== undefined;
      button.addEventListener("click", () => revealCell(cell));
      button.addEventListener("contextmenu", (event) => {
        event.preventDefault();
        toggleFlag(cell);
      });
      boardElement.append(button);
    }
  }
}

function renderKnowledge() {
  if (game === null) {
    knownSafesElement.textContent = "None yet";
    knownMinesElement.textContent = "None yet";
  } else {
    knownSafesElement.textContent = formatCells(game.known_safes);
    knownMinesElement.textContent = formatCells(game.known_mines);
  }

  suggestedMoveElement.textContent = suggestionRequested
    ? suggestion === null
      ? "No valid move available"
      : cellLabel(suggestion)
    : "Not requested yet";

  helperMoveElement.textContent =
    helperMove === null ? "None yet" : cellLabel(helperMove);
}

function renderTrace() {
  traceListElement.innerHTML = "";
  const events = game?.trace.slice(-8).reverse() || [];

  if (events.length === 0) {
    const item = document.createElement("li");
    item.textContent = "No reasoning events yet.";
    traceListElement.append(item);
    return;
  }

  for (const event of events) {
    const item = document.createElement("li");
    item.textContent = event.message;
    traceListElement.append(item);
  }
}

function render() {
  if (game !== null) {
    difficultyElement.value = game.difficulty;
  }

  renderControls();
  renderStatus();
  renderBoard();
  renderKnowledge();
  renderTrace();
}

async function loadGame() {
  game = await requestJson("/api/game");
  render();
}

async function startNewGame() {
  game = await requestJson("/api/game", {
    method: "POST",
    body: JSON.stringify({ difficulty: difficultyElement.value }),
  });
  suggestion = null;
  suggestionRequested = false;
  helperMove = null;
  render();
}

async function revealCell(cell) {
  if (requestInFlight || isGameOver()) {
    return;
  }

  await runAction(async () => {
    game = await requestJson("/api/game/reveal", {
      method: "POST",
      body: JSON.stringify(cell),
    });
    suggestion = null;
    suggestionRequested = false;
    render();
  });
}

async function toggleFlag(cell) {
  if (requestInFlight || isGameOver()) {
    return;
  }

  await runAction(async () => {
    game = await requestJson("/api/game/flag", {
      method: "POST",
      body: JSON.stringify(cell),
    });
    suggestion = null;
    suggestionRequested = false;
    render();
  });
}

suggestButton.addEventListener("click", () => {
  runAction(async () => {
    const payload = await requestJson("/api/game/suggestion");
    game = payload.game;
    suggestion = payload.suggestion;
    suggestionRequested = true;
    render();
  });
});

helperButton.addEventListener("click", () => {
  runAction(async () => {
    game = await requestJson("/api/game/helper", { method: "POST" });
    helperMove = game.helper_move;
    suggestion = null;
    suggestionRequested = false;
    render();
  });
});

newGameButton.addEventListener("click", () => {
  runAction(startNewGame);
});

render();
runAction(loadGame);
