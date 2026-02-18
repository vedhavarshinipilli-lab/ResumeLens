// src/App.jsx
import React, { useState } from "react";
import { Routes, Route } from "react-router-dom";
import Home from "./Home";
import ResultScreen from "./ResultScreen";

function App() {
  const [resumeData, setResumeData] = useState(null);

  return (
    <Routes>
      <Route path="/" element={<Home setResumeData={setResumeData} />} />
      <Route
        path="/results"
        element={<ResultScreen resumeData={resumeData} />}
      />
    </Routes>
  );
}

export default App;
