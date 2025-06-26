const express = require("express");
const fs = require("fs");
const path = require("path");
const cors = require("cors");
const { exec } = require("child_process");
const { execSync } = require("child_process");
const app = express();
const PORT = 4000;

const FILE_PATH = path.join(__dirname, "..", "gamestate.txt");
const ENGINE_PATH = path.join(__dirname, "..", "engine", "engine.py");
const GLOBAL_TXT_PATH = path.join(__dirname, "..", "global.txt");
const FIRST_MOVE_DONE_PATH = path.join(__dirname, "..", "first_move_done.txt");
// const CSV = path.join(__dirname, "..", "result.csv");
const CSV = path.join(__dirname, "..", "result_random.csv");

app.use(cors());
app.use(express.json());

app.get("/state", (req, res) => {
  const content = fs.readFileSync(FILE_PATH, "utf-8");
  const lines = content.trim().split("\n");
  const header = lines[0];
  const board = lines.slice(1).map((line) => line.trim().split(" "));
  let winner = null;

  if (header.startsWith("Winner:")) {
    winner = header.split(":")[1].trim();
  }

  res.json({ board, header, winner });
});

app.post("/move", (req, res) => {
  const { row, col, color } = req.body;

  try {
    const cmd = `python3 ../engine/humanMoveSimulator.py ${row} ${col} ${color}`;
    execSync(cmd);
    // send success after executing the command
    res.send({ status: "success" });
  } catch (e) {
    return res.status(400).send({ error: "Invalid or exploding move" });
  }
});

app.get("/ai-move", (req, res) => {
  // console.log("Blue AI move requested");
  who = "BlueAI";
  const cmd = `python3 "${ENGINE_PATH}" ${who}`;
  exec(cmd, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error running engine: ${error.message}`);
      return res.status(500).send({ error: "AI failed to move." });
    }
    if (stderr) {
      console.error(`Engine stderr: ${stderr}`);
    }
    return res.send({ status: "success" });
  });
});

app.get("/my-ai-move", (req, res) => {
  // console.log("Red AI move requested");
  who = "RedAI";
  const cmd = `python3 "${ENGINE_PATH}" ${who}`;
  exec(cmd, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error running engine: ${error.message}`);
      return res.status(500).send({ error: "AI failed to move." });
    }
    if (stderr) {
      console.error(`Engine stderr: ${stderr}`);
    }
    return res.send({ status: "success" });
  });
}
);

app.get("/refresh", (req, res) => {
  try {
    const fs = require("fs");
    const path = require("path");

    fs.writeFileSync(GLOBAL_TXT_PATH, "");

    fs.writeFileSync(FIRST_MOVE_DONE_PATH, "False");

    const initialBoard =
      "Human Move:\n" + Array(9).fill("0 0 0 0 0 0").join("\n");
    fs.writeFileSync(FILE_PATH, initialBoard);

    return res.send({ status: "success" });
  } catch (error) {
    console.error("Error refreshing board:", error);
    return res.status(500).send({ error: "Failed to refresh board." });
  }
});

app.get("/start", (req, res) => {
  try {
    const fs = require("fs");
    const path = require("path");

    fs.writeFileSync(GLOBAL_TXT_PATH, "");

    fs.writeFileSync(FIRST_MOVE_DONE_PATH, "False");

    const initialBoard =
      "Red AI Move:\n" + Array(9).fill("0 0 0 0 0 0").join("\n");
    fs.writeFileSync(FILE_PATH, initialBoard);

    return res.send({ status: "success" });

  } catch (error) {
    console.error("Error starting game:", error);
    return res.status(500).send({ error: "Failed to start game." });
  }
}
);

app.post("/save", (req, res) => {
  try {
    const { heuristic1, heuristic2, duration, who_won } = req.body;
    if (
      heuristic1 === undefined ||
      heuristic2 === undefined ||
      duration === undefined ||
      !who_won
    ) {
      return res.status(400).send({ error: "Missing required fields." });
    }

    const row = `${heuristic1},${heuristic2},${duration},${who_won}\n`;

    // If file does not exist, write header first
    if (!fs.existsSync(CSV)) {
      fs.writeFileSync(CSV, "heuristicA,heuristicB,time,winner\n");
    }

    // Append the row
    fs.appendFileSync(CSV, row);

    return res.send({ status: "success" });
  } catch (error) {
    console.error("Error saving game data:", error);
    return res.status(500).send({ error: "Failed to save game data." });
  }
});


app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
