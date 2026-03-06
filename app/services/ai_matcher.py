# ---------------- COMPARE SKILLS ----------------
def compare_skills(resume_skills, job_skills):

    if not resume_skills or not job_skills:
        return {
            "matched_skills": [],
            "match_percent": 0
        }

    resume_set = set(skill.lower() for skill in resume_skills)
    job_set = set(skill.lower() for skill in job_skills)

    # ✅ Common Skills
    matched = list(resume_set.intersection(job_set))

    # ✅ Match %
    match_percent = (len(matched) / len(job_set)) * 100

    return {
        "matched_skills": matched,
        "match_percent": round(match_percent, 2)
    }