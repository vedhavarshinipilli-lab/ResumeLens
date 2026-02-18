from fastapi import APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.services.predict_service import run_prediction

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

import os

router = APIRouter(prefix="/predict", tags=["Prediction"])


class PredictRequest(BaseModel):
    resume_text: str
    job_description: str


# 🔹 Normal Prediction Endpoint (unchanged logic)
@router.post("/")
def predict(data: PredictRequest):
    result = run_prediction(
        resume_text=data.resume_text,
        job_description=data.job_description
    )
    return result


# 🔹 Download Professional PDF Report
@router.post("/download")
def download_report(data: PredictRequest):

    result = run_prediction(
        resume_text=data.resume_text,
        job_description=data.job_description
    )

    file_path = "ResumeLens_Report.pdf"
    doc = SimpleDocTemplate(file_path)
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    normal_style = styles["Normal"]

    # Title
    elements.append(Paragraph("ResumeLens - Resume Analysis Report", title_style))
    elements.append(Spacer(1, 0.3 * inch))

    # Match Score
    elements.append(
        Paragraph(
            f"<b>Match Percentage:</b> {round(result['match_percentage'], 1)}%",
            normal_style
        )
    )
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(
        Paragraph(
            f"<b>Match Level:</b> {result['match_level']}",
            normal_style
        )
    )
    elements.append(Spacer(1, 0.3 * inch))

    # Matched Skills
    elements.append(Paragraph("<b>Matched Skills:</b>", normal_style))
    elements.append(Spacer(1, 0.1 * inch))

    if result["matched_skills"]:
        matched = [
            ListItem(Paragraph(skill, normal_style))
            for skill in result["matched_skills"]
        ]
        elements.append(ListFlowable(matched))
    else:
        elements.append(Paragraph("No matched skills found.", normal_style))

    elements.append(Spacer(1, 0.3 * inch))

    # Missing Skills
    elements.append(Paragraph("<b>Missing Skills:</b>", normal_style))
    elements.append(Spacer(1, 0.1 * inch))

    missing = [
        ListItem(Paragraph(skill, normal_style))
        for skill in result["missing_skills"]
    ]
    elements.append(ListFlowable(missing))

    elements.append(Spacer(1, 0.3 * inch))

    # Suggestions
    elements.append(Paragraph("<b>Improvement Suggestions:</b>", normal_style))
    elements.append(Spacer(1, 0.1 * inch))

    suggestions = [
        ListItem(Paragraph(tip, normal_style))
        for tip in result["improvement_suggestions"]
    ]
    elements.append(ListFlowable(suggestions))

    # Build PDF
    doc.build(elements)

    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename="ResumeLens_Report.pdf"
    )