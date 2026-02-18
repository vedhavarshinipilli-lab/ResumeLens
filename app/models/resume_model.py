from pydantic import BaseModel
from typing import List


class ResumeAnalysis(BaseModel):
    characters: int
    skills: List[str]
    preview: str