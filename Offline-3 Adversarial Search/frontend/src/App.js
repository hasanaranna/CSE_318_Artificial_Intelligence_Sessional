import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";

const ROWS = 9,
  COLS = 6;

function App() {
  const [board, setBoard] = useState([]);
  const [header, setHeader] = useState("");
  const [winner, setWinner] = useState(null);
  const winnerRef = useRef(winner);
  useEffect(() => {
    winnerRef.current = winner;
  }, [winner]);
  const [loading, setLoading] = useState(true);
  const [whoseTurn, setWhoseTurn] = useState("Red");
  const whoseTurnRef = useRef(whoseTurn);
  useEffect(() => {
    whoseTurnRef.current = whoseTurn;
  }, [whoseTurn]);

  const [invalidMove, setInvalidMove] = useState(false);
  const [first_player, setFirstPlayer] = useState("self");
  const [duration, setDuration] = useState(null);
  console.log("Duration:", duration);
  const startTimeRef = useRef(null);

  const fetchBoard = async () => {
    const res = await axios.get("http://localhost:4000/state");
    // const lines = res.data.trim().split("\n");
    //const boardLines = lines.slice(1).map((row) => row.trim().split(" "));
    const data = res.data;
    setHeader(data.header);
    setWinner(data.winner);
    setBoard(data.board);
    setLoading(false);
    // console.log("Board fetched:", boardLines);
  };

  const handleClick = async (r, c) => {
    if (winner || whoseTurnRef.current === "Blue" || first_player === "ai") return;

    const response = await axios.post("http://localhost:4000/move", {
      row: r,
      col: c,
      color: "R",
    });
    setTimeout(() => fetchBoard(), 1000);
    if (response.data.status === "success") {
      setWhoseTurn("AI");
      console.log(`Human moved at (${r}, ${c})`);
      // Trigger AI move after a short delay
      setTimeout(() => aiMove(), 1000);
    } else if (response.data.status === "invalidMove") {
      setInvalidMove(true);
      setTimeout(() => setInvalidMove(false), 2000);
      // console.error("Invalid move:", response.data.error);
    }
  };

  const aiMove = async () => {
    const response = await axios.get("http://localhost:4000/ai-move");
    if (response.data.status === "success") {
      setWhoseTurn("Red");
      console.log("AI moved:", response.data.move);
      fetchBoard();
    } else {
      console.error("AI move failed:", response.data.error);
    }
  };

  const myAIMove = async () => {
    if (whoseTurn === "Blue") return;
    const response = await axios.get("http://localhost:4000/my-ai-move");
    if (response.data.status === "success") {
      setWhoseTurn("Blue");
      console.log("My AI moved:", response.data.move);
      fetchBoard();
    } else {
      console.error("My AI move failed:", response.data.error);
    }
  };

  const handleRefreshBoard = async () => {
    setLoading(true);
    const response = await axios.get("http://localhost:4000/refresh");
    if (response.data.status === "success") {
      console.log("Board refreshed");
      fetchBoard();
      setWhoseTurn("Red");
    }
    setLoading(false);
  };

  const handleStart = async () => {
    const response = await axios.get("http://localhost:4000/start");
    if (response.data.status === "success") {
      console.log("AI vs AI game started");
      setWhoseTurn("Red");

      setDuration(null);
      startTimeRef.current = Date.now();

      fetchBoard();
      runAIBattle();

      // setTimeout(runAIBattle, 1000);
    } else {
      console.error("Failed to start AI vs AI game:", response.data.error);
    }
  };

  const runAIBattle = async () => {
    if (winnerRef.current) {
      if (startTimeRef.current) {
        const duration = (Date.now() - startTimeRef.current) / 1000;
        setDuration(duration);
        startTimeRef.current = null;
      }
      return;
    }

    try {
      if (whoseTurnRef.current === "Red") {
        await myAIMove();
        setWhoseTurn("Blue");
      } else {
        await aiMove();
        setWhoseTurn("Red");
      }

      await fetchBoard();
      if (!winnerRef.current) {
        setTimeout(runAIBattle, 1000);
      } else {
        const duration = (Date.now() - startTimeRef.current) / 1000;
        setDuration(duration);
        startTimeRef.current = null;
      }
    } catch (error) {
      console.error("Error in AI battle:", error);
    }
  };

  const handleSave = async () => {
    if (!duration) {
      console.error("No game duration to save.");
      return;
    }
    try {
      let heuristic1 = 1;
      let heuristic2 = 0;
      let who_won;
      if (winner === "Red") {
        who_won = heuristic1;
      } else if (winner === "Blue") {
        who_won = heuristic2;
      }


      const response = await axios.post("http://localhost:4000/save", {
        heuristic1,
        heuristic2,
        duration,
        who_won,
      });
      if (response.data.status === "success") {
        console.log("Game data saved successfully:", response.data);
      } else {
        console.error("Failed to save game data:", response.data.error);
      }
    } catch (error) {
      console.error("Error saving game data:", error);
    }
  };

  useEffect(() => {
    fetchBoard();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div
      className="container mt-5"
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "100vh",
      }}
    >
      {winner && (
        <div className="alert alert-success">
          Game Over! <strong>{winner}</strong> wins!
        </div>
      )}

      <div className="mb-3">
        <label htmlFor="first-player-select" className="form-label">
          First Player:
        </label>
        <select
          id="first-player-select"
          className="form-select"
          value={first_player}
          onChange={(e) => setFirstPlayer(e.target.value)}
          style={{
            maxWidth: "200px",
            display: "inline-block",
            marginLeft: "10px",
          }}
        >
          <option value="self">Self</option>
          <option value="ai">My AI</option>
        </select>
      </div>

      <h1 className="text-center">Chain Reaction</h1>
      <h2 className="text-center">"{first_player}/Red" vs "AI/Blue"</h2>
      <p>
        Current Turn: <strong>{whoseTurn}</strong>
      </p>
      {invalidMove && (
        <div
          style={{
            color: "white",
            backgroundColor: "#d9534f",
            padding: "8px",
            borderRadius: "4px",
            marginBottom: "10px",
            textAlign: "center",
            maxWidth: "300px",
          }}
        >
          Invalid move! Please try again.
        </div>
      )}
      <div className="table table-bordered text-center">
        {board.map((row, r) => (
          <div key={r} className="d-flex">
            {row.map((cell, c) => (
              <div
                key={c}
                onClick={() => handleClick(r, c)}
                style={{
                  width: "50px",
                  height: "50px",
                  lineHeight: "50px",
                  cursor: "pointer",
                  backgroundColor: cell.endsWith("R")
                    ? "#f88"
                    : cell.endsWith("B")
                    ? "#88f"
                    : "#eee",
                  border: "1px solid #aaa",
                }}
              >
                {cell !== "0" ? cell[0] : ""}
              </div>
            ))}
          </div>
        ))}
      </div>
      <div className="mt-3">
        <button
          className="btn btn-primary"
          onClick={() => {
            setLoading(true);
            handleRefreshBoard();
          }}
        >
          Refresh Board
        </button>
      </div>
      {first_player === "ai" && (
        <div className="mt-3">
          <button className="btn btn-secondary" onClick={handleStart}>
            Start AI vs AI
          </button>
        </div>
      )}
      {duration !== null && (
        <div className="mt-3">
          <p>
            Game Duration: <strong>{duration.toFixed(2)} seconds</strong>
          </p>
          <button
            className="btn btn-secondary"
            onClick={() => {
              handleSave();
            }}
          >
            Save Data
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
