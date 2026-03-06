from flask import Blueprint, jsonify
from app.models.job import Job
from app.models.application import Application

api = Blueprint("api", __name__, url_prefix="/api")


# ---------------- GET ALL JOBS ----------------
@api.route("/jobs")
def get_jobs():

    jobs = Job.query.all()

    job_list = []

    for job in jobs:
        job_list.append({
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "location": job.location,
            "skills": job.skills,
            "status": job.status
        })

    return jsonify(job_list)


# ---------------- GET SINGLE JOB ----------------
@api.route("/jobs/<int:job_id>")
def get_job(job_id):

    job = Job.query.get_or_404(job_id)

    return jsonify({
        "id": job.id,
        "title": job.title,
        "description": job.description,
        "location": job.location,
        "skills": job.skills,
        "status": job.status
    })


# ---------------- GET APPLICATIONS ----------------
@api.route("/applications")
def get_applications():

    applications = Application.query.all()

    data = []

    for app in applications:
        data.append({
            "id": app.id,
            "job_id": app.job_id,
            "candidate_id": app.candidate_id,
            "resume": app.resume,
            "status": app.status,
            "match_score": app.match_score
        })

    return jsonify(data)