from app.services.skill_data import SKILL_ALIASES


def normalize_skills(skills: list[str]) -> list[str]:
    """
    Normalize skill names for consistent comparison using alias mapping.
    """

    normalized = set()

    for skill in skills:
        skill_lower = skill.strip().lower()

        matched = False

        for canonical, aliases in SKILL_ALIASES.items():
            if skill_lower in aliases:
                normalized.add(canonical)
                matched = True
                break

        if not matched:
            normalized.add(skill_lower)

    return list(normalized)