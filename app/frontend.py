import streamlit as st
import requests
import PyPDF2
import tempfile

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

st.set_page_config(page_title="ResumeLens AI", layout="centered")

st.title("🚀 ResumeLens AI")
st.write("Upload Resume (PDF) or Paste Text")

# -----------------------
# Resume Upload Section
# -----------------------
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

resume_text = ""

if uploaded_file is not None:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            resume_text += text

# Manual Paste Option
resume_text_manual = st.text_area("Or Paste Resume Text", height=200)

if resume_text_manual:
    resume_text = resume_text_manual

# -----------------------
# Job Description
# -----------------------
job_description = st.text_area("Paste Job Description", height=200)

# -----------------------
# Analyze Button
# -----------------------
if st.button("Analyze Match"):

    if not resume_text or not job_description:
        st.warning("Please provide resume and job description.")
    else:
        try:
            response = requests.post(
                "http://127.0.0.1:8000/predict/",
                json={
                    "resume_text": resume_text,
                    "job_description": job_description
                }
            )

            if response.status_code == 200:
                result = response.json()

                percentage = result["match_percentage"]

                st.markdown(f"## 🎯 Match Score: {percentage}%")
                st.progress(int(percentage))
                st.write(f"*Level:* {result['match_level']}")

                st.subheader("✅ Matched Skills")
                if result["matched_skills"]:
                    st.write(", ".join(result["matched_skills"]))
                else:
                    st.write("None")

                st.subheader("❌ Missing Skills")
                if result["missing_skills"]:
                    st.write(", ".join(result["missing_skills"]))
                else:
                    st.write("None")

                st.subheader("💡 Suggestions")
                if result["improvement_suggestions"]:
                    for suggestion in result["improvement_suggestions"]:
                        st.write(f"- {suggestion}")
                else:
                    st.write("Resume looks well aligned.")

                # -----------------------
                # Generate PDF Report
                # -----------------------
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                doc = SimpleDocTemplate(temp_file.name)
                elements = []

                styles = getSampleStyleSheet()

                elements.append(Paragraph("ResumeLens AI Match Report", styles["Title"]))
                elements.append(Spacer(1, 0.3 * inch))

                elements.append(Paragraph(f"Match Score: {percentage}%", styles["Normal"]))
                elements.append(Paragraph(f"Match Level: {result['match_level']}", styles["Normal"]))
                elements.append(Spacer(1, 0.3 * inch))

                elements.append(Paragraph("Matched Skills:", styles["Heading2"]))
                for skill in result["matched_skills"]:
                    elements.append(Paragraph(f"- {skill}", styles["Normal"]))

                elements.append(Spacer(1, 0.2 * inch))
                elements.append(Paragraph("Missing Skills:", styles["Heading2"]))
                for skill in result["missing_skills"]:
                    elements.append(Paragraph(f"- {skill}", styles["Normal"]))

                elements.append(Spacer(1, 0.2 * inch))
                elements.append(Paragraph("Suggestions:", styles["Heading2"]))
                for suggestion in result["improvement_suggestions"]:
                    elements.append(Paragraph(f"- {suggestion}", styles["Normal"]))

                doc.build(elements)

                with open(temp_file.name, "rb") as f:
                    st.download_button(
                        label="📄 Download Match Report",
                        data=f,
                        file_name="ResumeLens_Report.pdf",
                        mime="application/pdf"
                    )

            else:
                st.error("Backend error. Check FastAPI server.")

        except Exception as e:
            st.error(f"Connection error: {e}")