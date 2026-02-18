from app.services.ai_service import calculate_match
from app.services.resume_analysis import extract_skills
from app.services.skill_normalizer import normalize_skills

def run_prediction(resume_text: str, job_description: str):

    match_result = calculate_match(resume_text, job_description)

    score = match_result["match_percentage"]
    resume_skills = normalize_skills(extract_skills(resume_text))
    job_skills = normalize_skills(extract_skills(job_description))

    matched = list(set(resume_skills) & set(job_skills))
    missing = list(set(job_skills) - set(resume_skills))

    if score >= 75:
        level = "High"
    elif score >= 50:
        level = "Medium"
    else:
        level = "Low"

    suggestions = []
    if missing:
        suggestions.append(f"Consider adding these skills: {', '.join(missing[:5])}")

    return {
        "match_percentage": score,
        "match_level": level,
        "matched_skills": matched,
        "missing_skills": missing,
        "improvement_suggestions": suggestions
    }