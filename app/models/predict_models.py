from pydantic import BaseModel
from typing import List

class PredictRequest(BaseModel):
    resume_text: str
    job_description: str

class PredictResponse(BaseModel):
    matching_skills: List[str]
    missing_skills: List[str]
    score: float