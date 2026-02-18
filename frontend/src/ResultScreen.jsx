// src/ResultScreen.jsx
import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./App.css";

function ResultScreen() {
  const { state } = useLocation();
  const navigate = useNavigate();

  if (!state || !state.result) {
    navigate("/");
    return null;
  }

  const {
    match_percentage,
    match_level,
    matched_skills,
    missing_skills,
    improvement_suggestions,
  } = state.result;

  const handleDownload = () => {
    const content = `
Match Percentage: ${match_percentage.toFixed(2)}%
Level: ${match_level}
Matched Skills: ${matched_skills.join(", ")}
Missing Skills: ${missing_skills.join(", ")}
Suggestions: ${improvement_suggestions.join(", ")}
    `;
    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "resume_analysis.txt";
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="result-container">
      <h1 style={{ color: "#00FF7F" }}>Analysis Result</h1>
      <p>
        <strong>Match Percentage:</strong> {match_percentage.toFixed(2)}%
      </p>
      <p>
        <strong>Match Level:</strong> {match_level}
      </p>
      <p>
        <strong>Matched Skills:</strong> {matched_skills.join(", ")}
      </p>
      <p>
        <strong>Missing Skills:</strong> {missing_skills.join(", ")}
      </p>
      <p>
        <strong>Suggestions:</strong> {improvement_suggestions.join(", ")}
      </p>
      <button onClick={handleDownload} className="download-btn">
        Download Result
      </button>
      <button onClick={() => navigate("/")} className="back-btn">
        Back
      </button>
    </div>
  );
}

export default ResultScreen;
