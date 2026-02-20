import React, { useState } from "react";

export default function Home() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showResult, setShowResult] = useState(false);

  // Read text from .txt quickly; try to extract PDF text (best-effort)
  const getResumeTextFromFile = async (file) => {
    if (!file) return null;
    const ext = (file.name.split(".").pop() || "").toLowerCase();
    if (ext === "txt") {
      return await file.text();
    }
    if (ext === "pdf") {
      try {
        const pdfjsLib = await import("pdfjs-dist/build/pdf");
        pdfjsLib.GlobalWorkerOptions.workerSrc = new URL(
          "pdfjs-dist/build/pdf.worker.min.js",
          import.meta.url,
        ).toString();

        const arrayBuffer = await file.arrayBuffer();
        const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
        let text = "";
        for (let i = 1; i <= pdf.numPages; i++) {
          const page = await pdf.getPage(i);
          const content = await page.getTextContent();
          const strings = content.items.map((item) => item.str || "");
          text += strings.join(" ") + "\n";
        }
        return text || null;
      } catch (err) {
        console.warn("PDF text extraction failed:", err);
        return null;
      }
    }
    return null;
  };

  const handleAnalyze = async () => {
    if (!jobDescription || jobDescription.trim().length === 0) {
      alert("Please paste the job description before analyzing.");
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      let resume_text = "Sample resume text for now";
      const extracted = await getResumeTextFromFile(selectedFile);
      if (extracted && extracted.trim().length > 30) {
        resume_text = extracted;
      }

      const response = await fetch(
        `${import.meta.env.VITE_BACKEND_URL}/predict/`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            resume_text,
            job_description: jobDescription,
          }),
        },
      );

      if (!response.ok) {
        const errBody = await response.json().catch(() => null);
        throw new Error(
          `Server responded ${response.status}${
            errBody?.detail ? ": " + errBody.detail : ""
          }`,
        );
      }

      const data = await response.json();
      setResult(data);
      setShowResult(true);
    } catch (err) {
      console.error("Analyze error:", err);
      alert("Analysis failed. Check backend or the console for details.");
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async () => {
    if (!jobDescription || jobDescription.trim().length === 0) {
      alert("Please paste the job description first.");
      return;
    }

    setLoading(true);
    try {
      let resume_text = "Sample resume text for now";
      const extracted = await getResumeTextFromFile(selectedFile);
      if (extracted && extracted.trim().length > 30) resume_text = extracted;

      const response = await fetch(
        `${import.meta.env.VITE_BACKEND_URL}/predict/`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            resume_text,
            job_description: jobDescription,
          }),
        },
      );

      if (!response.ok) throw new Error("Failed to generate PDF on server.");

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "ResumeLens_Report.pdf";
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Download error:", err);
      alert("Failed to download report. Check backend logs.");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setShowResult(false);
    setResult(null);
  };

  // ----- Render Structured Result Screen -----
  if (showResult && result) {
    return (
      <div className="page">
        <div className="card result-screen">
          <div className="top-row">
            <div>
              <h1 className="title">Resume Analysis Report</h1>
              <p className="subtitle">
                Professional summary — actionable and clear
              </p>
            </div>
            <div style={{ textAlign: "right" }}>
              <button className="ghost-btn" onClick={handleReset}>
                ← Back
              </button>
            </div>
          </div>

          <div className="report-grid">
            <div className="score-card">
              <div className="score-value">
                {Math.round(result.match_percentage)}%
              </div>
              <div className="score-label">Match Score</div>
              <div className="level-badge">{result.match_level}</div>
            </div>

            <div className="lists">
              <div className="list-block">
                <h4>Matched Skills</h4>
                {result.matched_skills && result.matched_skills.length > 0 ? (
                  <div className="chips">
                    {result.matched_skills.map((s, i) => (
                      <span key={i} className="chip good">
                        {s}
                      </span>
                    ))}
                  </div>
                ) : (
                  <div className="empty-note">No matched skills found.</div>
                )}
              </div>

              <div className="list-block">
                <h4>Missing Skills</h4>
                {result.missing_skills && result.missing_skills.length > 0 ? (
                  <div className="chips">
                    {result.missing_skills.map((s, i) => (
                      <span key={i} className="chip bad">
                        {s}
                      </span>
                    ))}
                  </div>
                ) : (
                  <div className="empty-note">None — good job!</div>
                )}
              </div>
            </div>
          </div>

          <div className="section">
            <h4>Improvement Suggestions</h4>
            <ul className="suggestions">
              {result.improvement_suggestions &&
              result.improvement_suggestions.length > 0 ? (
                result.improvement_suggestions.map((tip, idx) => (
                  <li key={idx}>{tip}</li>
                ))
              ) : (
                <li>No suggestions — excellent!</li>
              )}
            </ul>
          </div>

          <div className="result-actions">
            <button className="download-btn" onClick={handleDownload}>
              {loading ? "Preparing PDF..." : "Download Full Report (PDF)"}
            </button>
            <button className="secondary-btn" onClick={handleReset}>
              Analyze Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ----- Upload / Analyze Screen -----
  return (
    <div className="page">
      <div className="card">
        <h1 className="title">ResumeLens</h1>
        <p className="subtitle">
          AI-powered resume analysis — paste job description and analyze
        </p>

        <div className="section">
          <label className="label">Upload Resume (optional)</label>
          <input
            type="file"
            accept=".pdf,.txt"
            onChange={(e) => setSelectedFile(e.target.files[0] || null)}
            className="file-input"
          />
          {selectedFile && <div className="file-name">{selectedFile.name}</div>}
        </div>

        <div className="section">
          <label className="label">Job Description</label>
          <textarea
            placeholder="Paste job description here..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            rows={6}
          />
        </div>

        <button onClick={handleAnalyze} className="analyze-btn">
          {loading ? "Analyzing..." : "Analyze Resume"}
        </button>
      </div>
    </div>
  );
}
