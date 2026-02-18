import re

def extract_skills(text: str):

    # simple skill keyword list (you can expand later)
    skill_keywords = [
        "python", "java", "c++", "machine learning", "deep learning",
        "sql", "excel", "tensorflow", "pytorch",
        "communication", "leadership", "data analysis",
        "aws", "docker", "kubernetes", "react", "node"
    ]

    text = text.lower()

    found_skills = []

    for skill in skill_keywords:
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            found_skills.append(skill)

    return found_skills

