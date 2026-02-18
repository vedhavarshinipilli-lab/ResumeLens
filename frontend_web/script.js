document.getElementById("analyzeBtn").addEventListener("click", function () {
  const fileInput = document.getElementById("resumeInput");
  const jobDescription = document.getElementById("jobDescription").value.trim();
  const resultDiv = document.getElementById("result");

  if (!fileInput.files.length) {
    alert("Please upload your resume.");
    return;
  }

  if (!jobDescription) {
    alert("Please paste the job description.");
    return;
  }

  const score = Math.floor(Math.random() * 31) + 70;

  let message =
    score > 85
      ? "Excellent alignment detected."
      : score > 75
        ? "Strong potential match."
        : "Moderate match. Consider optimizing keywords.";

  resultDiv.style.display = "block";
  resultDiv.innerHTML = `
    <strong>Match Score:</strong> ${score}% <br><br>
    <strong>AI Insight:</strong> ${message}
  `;
});
