from app.services.skill_data import SKILL_ALIASES
import re

def extract_skills(text: str):

    text = text.lower()
    found_skills = []

    for canonical, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            if re.search(r"\b" + re.escape(alias) + r"\b", text):
                found_skills.append(canonical)
                break

    return found_skills