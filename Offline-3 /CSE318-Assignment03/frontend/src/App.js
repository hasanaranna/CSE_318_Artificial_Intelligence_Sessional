import React, { useEffect, useState } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";

const ROWS = 9,
  COLS = 6;

function App() {
  const [board, setBoard] = useState([]);
  const [header, setHeader] = useState("");
  const [winner, setWinner] = useState(null);
  const [loading, setLoading] = useState(true);
  const [whoseTurn, setWhoseTurn] = useState("Red");
  const [invalidMove, setInvalidMove] = useState(false);

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
    if (winner || whoseTurn === "AI") return;

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

  const handleRefreshBoard = async () => {
    setLoading(true);
    const response = await axios.get("http://localhost:4000/refresh");
    if (response.data.status === "success") {
      console.log("Board refreshed");
      fetchBoard();
    }
    setLoading(false);
  }

  useEffect(() => {
    fetchBoard();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="container mt-5">
      {winner && (
        <div className="alert alert-success">
          🎉 Game Over! <strong>{winner}</strong> wins!
        </div>
      )}

      <h2 className="mb-3">Chain Reaction Game (Red vs AI)</h2>
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
    </div>
  );
}

export default App;
