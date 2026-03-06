import PyPDF2
import re


# ---------------- EXTRACT TEXT FROM PDF ----------------
def extract_text_from_pdf(filepath):

    text = ""

    try:
        with open(filepath, "rb") as file:
            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

    except Exception as e:
        print("Resume parsing error:", e)

    return text


# ---------------- EXTRACT SKILLS ----------------
def extract_skills(text):

    skills_list = [
        "python", "flask", "django", "java",
        "html", "css", "javascript",
        "sql", "mysql", "mongodb",
        "machine learning", "data analysis",
        "react", "node"
    ]

    found_skills = []

    if not text:
        return found_skills

    text = text.lower()

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return found_skills


# ---------------- CALCULATE MATCH SCORE ----------------
def calculate_match_score(resume_text, job_description):

    if not resume_text or not job_description:
        return 0

    resume_text = resume_text.lower()
    job_description = job_description.lower()

    resume_words = set(re.findall(r'\w+', resume_text))
    job_words = set(re.findall(r'\w+', job_description))

    if not job_words:
        return 0

    match = resume_words.intersection(job_words)

    score = (len(match) / len(job_words)) * 100

    return round(score, 2)


# ---------------- MAIN FUNCTION ----------------
def parse_resume(filepath, job_description=""):

    text = extract_text_from_pdf(filepath)

    skills = extract_skills(text)

    score = calculate_match_score(text, job_description)

    return {
        "text": text,
        "skills": skills,
        "match_score": score
    }