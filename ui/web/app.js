const boardElement = document.querySelector("#board");
const statusElement = document.querySelector("#status");
const restartButton = document.querySelector("#restart-button");
const knownSafesElement = document.querySelector("#known-safes");
const knownMinesElement = document.querySelector("#known-mines");
const suggestedMoveElement = document.querySelector("#suggested-move");
const traceListElement = document.querySelector("#trace-list");

const height = 8;
const width = 8;

function cellLabel(row, col) {
  return `(${row}, ${col})`;
}

function renderBoard() {
  boardElement.innerHTML = "";

  for (let row = 0; row < height; row += 1) {
    for (let col = 0; col < width; col += 1) {
      const button = document.createElement("button");

      button.className = "cell";
      button.type = "button";
      button.dataset.row = row;
      button.dataset.col = col;
      button.dataset.state = "hidden";
      button.setAttribute("aria-label", `Hidden cell ${cellLabel(row, col)}`);

      button.addEventListener("click", () => {
        button.dataset.state = "revealed";
        button.textContent = "";
        button.setAttribute("aria-label", `Revealed cell ${cellLabel(row, col)}`);
        statusElement.textContent = `Revealed cell ${cellLabel(row, col)}. AI integration comes next.`;
        knownSafesElement.textContent = cellLabel(row, col);
        suggestedMoveElement.textContent = "Waiting for Python AI integration.";
        renderTrace(`Cell ${cellLabel(row, col)} was revealed in the UI prototype.`);
      });

      boardElement.append(button);
    }
  }
}

function renderTrace(message) {
  traceListElement.innerHTML = "";

  const item = document.createElement("li");
  item.textContent = message;
  traceListElement.append(item);
}

restartButton.addEventListener("click", () => {
  statusElement.textContent = "Choose a cell to begin.";
  knownSafesElement.textContent = "None yet";
  knownMinesElement.textContent = "None yet";
  suggestedMoveElement.textContent = "Not available yet";
  renderTrace("No reasoning events yet.");
  renderBoard();
});

renderBoard();