def normalize_skills(skills: list[str]) -> list[str]:
    """
    Normalize skill names for consistent comparison.
    """

    normalization_map = {
        "python": "python",
        "fastapi": "fastapi",
        "git": "git",
        "sql": "sql",
        "postgresql": "sql",
        "mysql": "sql",
    }

    normalized = set()

    for skill in skills:
        key = skill.strip().lower()
        normalized.add(normalization_map.get(key, key))

    return list(normalized)