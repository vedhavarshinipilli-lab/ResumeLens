from fastapi import APIRouter, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.resume_analysis import analyze_resume
import logging
logger = logging.getLogger("uvicorn.error")
logging.basicConfig(level=logging.INFO)                                                                                                                         

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/resume")
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse(
        "upload.html",
        {"request": request}
    )


@router.post("/upload")
async def upload_resume(
    request: Request,
    file: UploadFile = File(...),
    job_description: str = Form(""),
    target_role: str = Form("")
):
    logger.info("UPLOAD ENDPOINT HIT")

    content = await file.read()
    resume_text = content.decode(errors="ignore")

    result = await analyze_resume(
        resume_text=resume_text,
        job_description=job_description,
        target_role=target_role
    )

    return result