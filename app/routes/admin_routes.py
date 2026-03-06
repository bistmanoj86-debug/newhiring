from flask import Blueprint, render_template, redirect, url_for, flash, session
from extensions import db

from app.models.user import User
from app.models.job import Job


# ---------------- BLUEPRINT ----------------
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# ================= ADMIN DASHBOARD =================
@admin_bp.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    users = User.query.all()

    return render_template(
        "admin/dashboard.html",
        users=users
    )


# ================= ALL USERS =================
@admin_bp.route("/all-users")
def all_users():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    users = User.query.all()

    return render_template(
        "admin/all_users.html",
        users=users
    )


# ================= VERIFY USER =================
@admin_bp.route("/verify/<int:user_id>")
def verify_user(user_id):

    user = db.session.get(User, user_id)

    if user:
        user.is_verified = True
        user.verification_requested = False

        db.session.commit()

        flash("User verified successfully")

    return redirect(url_for("admin.verification_requests"))


# ================= UNVERIFY USER =================
@admin_bp.route("/unverify/<int:user_id>")
def unverify_user(user_id):

    user = db.session.get(User, user_id)

    if user:
        user.is_verified = False

        db.session.commit()

        flash("User verification removed")

    return redirect(url_for("admin.dashboard"))


# ================= VERIFICATION REQUESTS =================
@admin_bp.route("/verification-requests")
def verification_requests():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    users = User.query.filter_by(
        verification_requested=True
    ).all()

    return render_template(
        "admin/verification_requests.html",
        users=users
    )


# ================= JOB APPROVAL PAGE =================
@admin_bp.route("/approve-jobs")
def approve_jobs():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    jobs = Job.query.filter_by(status="Pending").all()

    return render_template(
        "admin/approve_jobs.html",
        jobs=jobs
    )


# ================= APPROVE JOB =================
@admin_bp.route("/approve-job/<int:job_id>")
def approve_job(job_id):

    job = Job.query.get_or_404(job_id)

    job.status = "Approved"

    db.session.commit()

    flash("Job approved successfully")

    return redirect(url_for("admin.approve_jobs"))


# ================= REJECT JOB =================
@admin_bp.route("/reject-job/<int:job_id>")
def reject_job(job_id):

    job = Job.query.get_or_404(job_id)

    db.session.delete(job)

    db.session.commit()

    flash("Job rejected and removed")

    return redirect(url_for("admin.approve_jobs"))


# ================= ALL JOBS =================
@admin_bp.route("/all-jobs")
def all_jobs():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    jobs = Job.query.all()

    return render_template(
        "admin/all_jobs.html",
        jobs=jobs
    )


# ================= DELETE JOB =================
@admin_bp.route("/delete-job/<int:job_id>")
def delete_job(job_id):

    job = Job.query.get_or_404(job_id)

    db.session.delete(job)

    db.session.commit()

    flash("Job deleted successfully")

    return redirect(url_for("admin.all_jobs"))


# ================= VERIFY RECRUITERS =================
@admin_bp.route("/verify-recruiters")
def verify_recruiters():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    recruiters = User.query.filter_by(role="recruiter").all()

    return render_template(
        "admin/verify_recruiters.html",
        recruiters=recruiters
    )