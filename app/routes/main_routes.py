from flask import Blueprint, render_template, session, redirect, url_for

main = Blueprint("main", __name__)

@main.route("/")
def home():

    if "user_id" in session:

        if session.get("role") == "recruiter":
            return redirect(url_for("recruiter.dashboard"))

        elif session.get("role") == "candidate":
            return redirect(url_for("candidate.dashboard"))

    return render_template("home.html")