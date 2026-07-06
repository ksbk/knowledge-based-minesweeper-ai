const boardElement = document.querySelector("#board");
const statusElement = document.querySelector("#status");
const restartButton = document.querySelector("#restart-button");
const helperButton = document.querySelector("#helper-button");
const knownSafesElement = document.querySelector("#known-safes");
const knownMinesElement = document.querySelector("#known-mines");
const suggestedMoveElement = document.querySelector("#suggested-move");
const traceListElement = document.querySelector("#trace-list");

const height = 8;
const width = 8;
const mineCount = 8;

let game = createGame();

function cellKey(row, col) {
  return `${row},${col}`;
}

function cellLabel(row, col) {
  return `(${row}, ${col})`;
}

function parseCellKey(key) {
  return key.split(",").map((value) => Number.parseInt(value, 10));
}

function createGame() {
  const mines = new Set();

  while (mines.size < mineCount) {
    const row = Math.floor(Math.random() * height);
    const col = Math.floor(Math.random() * width);
    mines.add(cellKey(row, col));
  }

  return {
    mines,
    revealed: new Set(),
    flags: new Set(),
    lost: false,
    trace: ["New game started. Click to reveal. Right-click to flag."],
  };
}

function hasWon() {
  if (game.flags.size !== game.mines.size) {
    return false;
  }

  for (const mine of game.mines) {
    if (!game.flags.has(mine)) {
      return false;
    }
  }

  return true;
}

function isGameOver() {
  return game.lost || hasWon();
}

function neighbors(row, col) {
  const cells = [];

  for (let rowOffset = -1; rowOffset <= 1; rowOffset += 1) {
    for (let colOffset = -1; colOffset <= 1; colOffset += 1) {
      if (rowOffset === 0 && colOffset === 0) {
        continue;
      }

      const neighborRow = row + rowOffset;
      const neighborCol = col + colOffset;

      if (
        neighborRow >= 0 &&
        neighborRow < height &&
        neighborCol >= 0 &&
        neighborCol < width
      ) {
        cells.push([neighborRow, neighborCol]);
      }
    }
  }

  return cells;
}

function nearbyMineCount(row, col) {
  return neighbors(row, col).filter(([neighborRow, neighborCol]) =>
    game.mines.has(cellKey(neighborRow, neighborCol)),
  ).length;
}

function revealCell(row, col) {
  if (isGameOver()) {
    return;
  }

  const key = cellKey(row, col);

  if (game.flags.has(key) || game.revealed.has(key)) {
    return;
  }

  if (game.mines.has(key)) {
    game.lost = true;
    revealAllMines();
    game.trace.unshift(`Mine revealed at ${cellLabel(row, col)}. Game over.`);
    render();
    return;
  }

  game.revealed.add(key);

  const count = nearbyMineCount(row, col);
  game.trace.unshift(
    `Safe cell ${cellLabel(row, col)} revealed with ${count} nearby mine(s).`,
  );

  if (count === 0) {
    revealEmptyNeighbors(row, col);
  }

  render();
}

function revealEmptyNeighbors(row, col) {
  for (const [neighborRow, neighborCol] of neighbors(row, col)) {
    const key = cellKey(neighborRow, neighborCol);

    if (game.revealed.has(key) || game.flags.has(key) || game.mines.has(key)) {
      continue;
    }

    game.revealed.add(key);

    if (nearbyMineCount(neighborRow, neighborCol) === 0) {
      revealEmptyNeighbors(neighborRow, neighborCol);
    }
  }
}

function toggleFlag(row, col) {
  if (isGameOver()) {
    return;
  }

  const key = cellKey(row, col);

  if (game.revealed.has(key)) {
    return;
  }

  if (game.flags.has(key)) {
    game.flags.delete(key);
    game.trace.unshift(`Flag removed from ${cellLabel(row, col)}.`);
  } else {
    game.flags.add(key);
    game.trace.unshift(`Flag placed on ${cellLabel(row, col)}.`);
  }

  if (hasWon()) {
    game.trace.unshift("All mines have been flagged. Game won.");
  }

  render();
}

function revealAllMines() {
  for (const key of game.mines) {
    game.revealed.add(key);
  }
}

function formatCells(keys) {
  return [...keys]
    .map((key) => {
      const [row, col] = parseCellKey(key);
      return cellLabel(row, col);
    })
    .join(", ");
}

function safeCells() {
  return new Set([...game.revealed].filter((key) => !game.mines.has(key)));
}

function suspectedMineCells() {
  return new Set(game.flags);
}

function availableMoves() {
  const moves = [];

  for (let row = 0; row < height; row += 1) {
    for (let col = 0; col < width; col += 1) {
      const key = cellKey(row, col);

      if (!game.revealed.has(key) && !game.flags.has(key)) {
        moves.push([row, col]);
      }
    }
  }

  return moves;
}

function findSafeStyleMove() {
  for (const key of game.revealed) {
    const [row, col] = parseCellKey(key);

    if (nearbyMineCount(row, col) !== 0) {
      continue;
    }

    for (const [neighborRow, neighborCol] of neighbors(row, col)) {
      const neighborKey = cellKey(neighborRow, neighborCol);

      if (!game.revealed.has(neighborKey) && !game.flags.has(neighborKey)) {
        return [neighborRow, neighborCol];
      }
    }
  }

  return null;
}

function findExploratoryMove() {
  const moves = availableMoves();

  if (moves.length === 0) {
    return null;
  }

  return moves[Math.floor(Math.random() * moves.length)];
}

function makeHelperMove() {
  if (isGameOver()) {
    return;
  }

  const safeStyleMove = findSafeStyleMove();

  if (safeStyleMove !== null) {
    const [row, col] = safeStyleMove;
    game.trace.unshift(`Helper selected safe-style move ${cellLabel(row, col)}.`);
    revealCell(row, col);
    return;
  }

  const exploratoryMove = findExploratoryMove();

  if (exploratoryMove === null) {
    game.trace.unshift("Helper found no available moves.");
    render();
    return;
  }

  const [row, col] = exploratoryMove;
  game.trace.unshift(`Helper selected exploratory move ${cellLabel(row, col)}.`);
  revealCell(row, col);
}

function suggestedMove() {
  if (isGameOver()) {
    return "Restart to play again.";
  }

  for (const key of game.revealed) {
    if (nearbyMineCount(...parseCellKey(key)) === 0) {
      for (const [row, col] of neighbors(...parseCellKey(key))) {
        const neighborKey = cellKey(row, col);

        if (!game.revealed.has(neighborKey) && !game.flags.has(neighborKey)) {
          return `Try ${cellLabel(row, col)} near an empty revealed cell.`;
        }
      }
    }
  }

  return "Choose an unrevealed cell, or right-click to flag a suspected mine.";
}

function renderBoard() {
  boardElement.innerHTML = "";

  for (let row = 0; row < height; row += 1) {
    for (let col = 0; col < width; col += 1) {
      const key = cellKey(row, col);
      const button = document.createElement("button");
      const isRevealed = game.revealed.has(key);
      const isFlagged = game.flags.has(key);
      const isMine = game.mines.has(key);
      const count = nearbyMineCount(row, col);

      button.className = "cell";
      button.type = "button";
      button.dataset.row = row;
      button.dataset.col = col;

      if (isFlagged && !isRevealed) {
        button.dataset.state = "flagged";
        button.textContent = "⚑";
        button.setAttribute("aria-label", `Flagged cell ${cellLabel(row, col)}`);
      } else if (isRevealed && isMine) {
        button.dataset.state = "mine";
        button.textContent = "✹";
        button.setAttribute("aria-label", `Mine at ${cellLabel(row, col)}`);
      } else if (isRevealed) {
        button.dataset.state = "revealed";
        button.textContent = count > 0 ? String(count) : "";
        button.setAttribute(
          "aria-label",
          `Revealed safe cell ${cellLabel(row, col)} with ${count} nearby mine(s)`,
        );
      } else {
        button.dataset.state = "hidden";
        button.textContent = "";
        button.setAttribute("aria-label", `Hidden cell ${cellLabel(row, col)}`);
      }

      button.addEventListener("click", () => revealCell(row, col));

      button.addEventListener("contextmenu", (event) => {
        event.preventDefault();
        toggleFlag(row, col);
      });

      boardElement.append(button);
    }
  }
}

function renderStatus() {
  if (hasWon()) {
    statusElement.textContent = "Game won. All mines have been flagged.";
    return;
  }

  if (game.lost) {
    statusElement.textContent = "Game over. A mine was revealed.";
    return;
  }

  statusElement.textContent = "Game in progress. Click to reveal. Right-click to flag.";
}

function renderKnowledgePanel() {
  const safes = safeCells();
  const mines = suspectedMineCells();

  knownSafesElement.textContent = safes.size > 0 ? formatCells(safes) : "None yet";
  knownMinesElement.textContent = mines.size > 0 ? formatCells(mines) : "None yet";
  suggestedMoveElement.textContent = suggestedMove();
}

function renderTrace() {
  traceListElement.innerHTML = "";

  for (const message of game.trace.slice(0, 6)) {
    const item = document.createElement("li");
    item.textContent = message;
    traceListElement.append(item);
  }
}

function render() {
  renderBoard();
  renderStatus();
  renderKnowledgePanel();
  renderTrace();
}

helperButton.addEventListener("click", makeHelperMove);

restartButton.addEventListener("click", () => {
  game = createGame();
  render();
});

render();
