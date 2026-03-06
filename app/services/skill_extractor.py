# ================= GLOBAL SKILL LIST =================

SKILL_LIST = [
    "python",
    "flask",
    "django",
    "fastapi",
    "java",
    "spring",
    "html",
    "css",
    "javascript",
    "react",
    "node",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "machine learning",
    "data analysis",
    "pandas",
    "numpy",
    "git",
    "docker"
]


# ================= SKILL EXTRACTION FUNCTION =================

def extract_skills(text):

    found_skills = []

    if not text:
        return found_skills

    text = text.lower()

    for skill in SKILL_LIST:
        if skill in text:
            found_skills.append(skill)

    return found_skills