async def parse_resume(text: str):
    """
    Extract raw information from resume text.
    """

    print("SERVICE HIT",flush=True)

    return {
        "name": "Unknown",
        "email": "unknown@example.com",
        "phone": "N/A",
        "skills": ["Python", "FastAPI", "Git"],  # temporary extraction
        "characters": len(text),
        "preview": text[:200],
    }