import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, redirect, url_for, session, flash, request, current_app

from extensions import db
from app.models.job import Job
from app.models.application import Application
from app.models.user import User

from app.services.resume_parser import parse_resume
from app.services.ai_matcher import compare_skills


# ---------------- BLUEPRINT ----------------
candidate_bp = Blueprint("candidate_bp", __name__, url_prefix="/candidate")

ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}


# ---------------- FILE CHECK ----------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ================= DASHBOARD =================
@candidate_bp.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    jobs = Job.query.filter_by(status="Approved").all()

    return render_template("candidate/dashboard.html", jobs=jobs)


# ================= JOB LIST WITH SEARCH =================
@candidate_bp.route("/jobs")
def job_list():

    title = request.args.get("title")
    location = request.args.get("location")
    skill = request.args.get("skill")

    jobs = Job.query.filter_by(status="Approved")

    if title:
        jobs = jobs.filter(Job.title.ilike(f"%{title}%"))

    if location:
        jobs = jobs.filter(Job.location.ilike(f"%{location}%"))

    if skill:
        jobs = jobs.filter(Job.skills.ilike(f"%{skill}%"))

    jobs = jobs.all()

    return render_template("candidate/job_list.html", jobs=jobs)


# ================= JOB DETAIL =================
@candidate_bp.route("/job/<int:job_id>")
def job_detail(job_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    job = Job.query.get_or_404(job_id)

    return render_template("candidate/job_detail.html", job=job)


# ================= APPLY JOB =================
@candidate_bp.route("/apply/<int:job_id>", methods=["POST"])
def apply_job(job_id):

    if "user_id" not in session:
        flash("Please login first")
        return redirect(url_for("auth.login"))

    job = Job.query.get_or_404(job_id)

    resume_file = request.files.get("resume")

    if not resume_file or resume_file.filename == "":
        flash("Resume is required!")
        return redirect(url_for("candidate_bp.job_list"))

    if not allowed_file(resume_file.filename):
        flash("Only PDF, DOC, DOCX allowed!")
        return redirect(url_for("candidate_bp.job_list"))

    filename = secure_filename(resume_file.filename)

    upload_folder = os.path.join(
        current_app.root_path,
        "static",
        "uploads",
        "resumes"
    )

    os.makedirs(upload_folder, exist_ok=True)

    filepath = os.path.join(upload_folder, filename)
    resume_file.save(filepath)

    result = parse_resume(filepath)
    resume_skills = result["skills"]

    job_skills = job.skills.split(",")

    compare_result = compare_skills(resume_skills, job_skills)
    match_percent = compare_result["match_percent"]

    application = Application(
        job_id=job_id,
        candidate_id=session["user_id"],
        resume=filename,
        status="Applied",
        match_score=match_percent
    )

    db.session.add(application)
    db.session.commit()

    flash(f"Application Submitted! Match Score: {match_percent}%")

    return redirect(url_for("candidate_bp.my_applications"))


# ================= MY APPLICATIONS =================
@candidate_bp.route("/applications")
def my_applications():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    applications = Application.query.filter_by(
        candidate_id=session["user_id"]
    ).all()

    return render_template("candidate/applications.html", applications=applications)


# ================= PROFILE =================
@candidate_bp.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = db.session.get(User, session["user_id"])

    if not user:
        flash("User not found")
        return redirect(url_for("auth.login"))

    return render_template("candidate/profile.html", user=user)


# ================= REQUEST VERIFICATION =================
@candidate_bp.route("/request-verification")
def request_verification():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = db.session.get(User, session["user_id"])

    if not user:
        flash("User not found")
        return redirect(url_for("candidate_bp.profile"))

    user.verification_requested = True
    db.session.commit()

    flash("Verification request sent to admin")

    return redirect(url_for("candidate_bp.profile"))


# ================= RECOMMENDED JOBS =================
@candidate_bp.route("/recommended-jobs")
def recommended_jobs():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    application = Application.query.filter_by(
        candidate_id=session["user_id"]
    ).order_by(Application.id.desc()).first()

    if not application:
        flash("Apply at least one job to generate recommendations.")
        return redirect(url_for("candidate_bp.job_list"))

    resume_path = os.path.join(
        current_app.root_path,
        "static",
        "uploads",
        "resumes",
        application.resume
    )

    result = parse_resume(resume_path)
    candidate_skills = result["skills"]

    jobs = Job.query.filter_by(status="Approved").all()

    recommended = []

    for job in jobs:

        job_skills = job.skills.split(",")

        compare_result = compare_skills(candidate_skills, job_skills)

        recommended.append({
            "job": job,
            "match_percent": compare_result["match_percent"]
        })

    recommended.sort(key=lambda x: x["match_percent"], reverse=True)

    return render_template("candidate/recommended_jobs.html", recommended=recommended)


# ================= SETTINGS =================
@candidate_bp.route("/settings")
def settings():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return render_template("candidate/settings.html")


# ================= CHANGE PASSWORD =================
@candidate_bp.route("/change-password")
def change_password():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return render_template("candidate/change_password.html")


# ================= UPDATE RESUME =================
@candidate_bp.route("/update-resume", methods=["GET", "POST"])
def update_resume():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        resume_file = request.files.get("resume")

        if resume_file and allowed_file(resume_file.filename):

            filename = secure_filename(resume_file.filename)

            upload_folder = os.path.join(
                current_app.root_path,
                "static",
                "uploads",
                "resumes"
            )

            os.makedirs(upload_folder, exist_ok=True)

            filepath = os.path.join(upload_folder, filename)
            resume_file.save(filepath)

            flash("Resume updated successfully")

    return render_template("candidate/update_resume.html")


# ================= NOTIFICATION SETTINGS =================
@candidate_bp.route("/notifications", methods=["GET", "POST"])
def notification_settings():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        flash("Notification settings saved")

    return render_template("candidate/notifications.html")


# ================= ACCOUNT SECURITY =================
@candidate_bp.route("/security")
def account_security():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return render_template("candidate/security.html")


# ================= DELETE ACCOUNT =================
@candidate_bp.route("/delete-account")
def delete_account():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return render_template("candidate/delete_account.html")