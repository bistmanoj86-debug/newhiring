from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db
from app.models.application import Application
from app.models.job import Job


# ---------------- BLUEPRINT ----------------
recruiter = Blueprint("recruiter", __name__, url_prefix="/recruiter")


# ---------------- DASHBOARD ----------------
@recruiter.route("/dashboard")
def dashboard():

    if "user_id" not in session or session.get("role") != "recruiter":
        return redirect(url_for("auth.login"))

    # Recruiter ke jobs
    jobs = Job.query.filter_by(
        recruiter_id=session["user_id"]
    ).all()

    # Sirf recruiter ke jobs ke applicants
    applications = Application.query.join(Job).filter(
        Job.recruiter_id == session["user_id"]
    ).all()

    return render_template(
        "recruiter/dashboard.html",
        jobs=jobs,
        applications=applications
    )


# ---------------- MY JOBS ----------------
@recruiter.route("/my-jobs")
def my_jobs():

    if "user_id" not in session or session.get("role") != "recruiter":
        return redirect(url_for("auth.login"))

    jobs = Job.query.filter_by(
        recruiter_id=session["user_id"]
    ).all()

    return render_template(
        "recruiter/my_jobs.html",
        jobs=jobs
    )


# ---------------- VIEW ALL APPLICATIONS ----------------
@recruiter.route("/applications")
def view_applications():

    if "user_id" not in session or session.get("role") != "recruiter":
        return redirect(url_for("auth.login"))

    applications = Application.query.join(Job).filter(
        Job.recruiter_id == session["user_id"]
    ).all()

    return render_template(
        "recruiter/applications.html",
        applications=applications
    )


# ---------------- VIEW APPLICATIONS FOR A JOB ----------------
@recruiter.route("/job/<int:job_id>/applications")
def job_applications(job_id):

    if "user_id" not in session or session.get("role") != "recruiter":
        return redirect(url_for("auth.login"))

    applications = Application.query.filter_by(job_id=job_id).all()

    return render_template(
        "recruiter/applications.html",
        applications=applications
    )


# ---------------- UPDATE APPLICATION STATUS ----------------
@recruiter.route("/update-status/<int:app_id>", methods=["POST"])
def update_status(app_id):

    if "user_id" not in session or session.get("role") != "recruiter":
        return redirect(url_for("auth.login"))

    application = Application.query.get_or_404(app_id)

    new_status = request.form.get("status")

    valid_status = [
        "Applied",
        "Viewed",
        "Shortlisted",
        "Interview",
        "Hired"
    ]

    if new_status in valid_status:

        application.status = new_status
        db.session.commit()

        flash("Status Updated Successfully")

    else:
        flash("Invalid Status")

    return redirect(url_for("recruiter.view_applications"))


# ---------------- POST JOB ----------------
@recruiter.route("/post-job", methods=["GET", "POST"])
def post_job():

    if "user_id" not in session or session.get("role") != "recruiter":
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        title = request.form.get("title")
        description = request.form.get("description")
        location = request.form.get("location")
        skills = request.form.get("skills")

        new_job = Job(
            title=title,
            description=description,
            location=location,
            skills=skills,
            recruiter_id=session["user_id"],
            status="Approved"
        )

        db.session.add(new_job)
        db.session.commit()

        flash("Job Posted Successfully!")

        return redirect(url_for("recruiter.dashboard"))

    return render_template("recruiter/post_job.html")


# ---------------- EDIT JOB ----------------
@recruiter.route("/job/<int:job_id>/edit", methods=["GET", "POST"])
def edit_job(job_id):

    if "user_id" not in session or session.get("role") != "recruiter":
        return redirect(url_for("auth.login"))

    job = Job.query.get_or_404(job_id)

    if request.method == "POST":

        job.title = request.form["title"]
        job.location = request.form["location"]
        job.skills = request.form["skills"]

        db.session.commit()

        flash("Job updated successfully")

        return redirect(url_for("recruiter.my_jobs"))

    return render_template(
        "recruiter/edit_job.html",
        job=job
    )


# ---------------- DELETE JOB ----------------
@recruiter.route("/job/<int:job_id>/delete")
def delete_job(job_id):

    if "user_id" not in session or session.get("role") != "recruiter":
        return redirect(url_for("auth.login"))

    job = Job.query.get_or_404(job_id)

    db.session.delete(job)
    db.session.commit()

    flash("Job deleted successfully")

    return redirect(url_for("recruiter.my_jobs"))


# ---------------- VIEW CANDIDATES ----------------
@recruiter.route("/candidates")
def candidates():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    applications = Application.query.join(Job).filter(
        Job.recruiter_id == session["user_id"]
    ).all()

    return render_template(
        "recruiter/candidates.html",
        applications=applications
    )