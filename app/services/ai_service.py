def calculate_match(resume_text: str, job_description: str):
    """
    Lightweight keyword-based matching.
    Works on Render free tier (no heavy ML models).
    """

    # Convert text to lowercase and split into words
    resume_words = set(resume_text.lower().split())
    job_words = set(job_description.lower().split())

    # If job description is empty
    if not job_words:
        return {
            "match_percentage": 0,
            "match_level": "Low"
        }

    # Find common words
    common_words = resume_words.intersection(job_words)

    # Calculate score
    score = len(common_words) / len(job_words)
    percentage = round(score * 100, 2)

    # Determine match level
    if percentage > 75:
        level = "High"
    elif percentage > 50:
        level = "Medium"
    else:
        level = "Low"

    return {
        "match_percentage": percentage,
        "match_level": level
    }