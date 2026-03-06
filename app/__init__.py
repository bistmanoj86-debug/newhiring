from flask import Flask, session, redirect, url_for, render_template
from config import Config
from extensions import db

# Import models
from app.models import User, Job, Application, Notification, Chat


def create_app():

    app = Flask(__name__)

    # ---------------- LOAD CONFIG ----------------
    app.config.from_object(Config)

    # ---------------- INIT DATABASE ----------------
    db.init_app(app)

    # ---------------- REGISTER BLUEPRINTS ----------------
    from app.routes.auth_routes import auth
    from app.routes.recruiter_routes import recruiter
    from app.routes.candidate_routes import candidate_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.notification_routes import notification_bp
    from app.routes.chat_routes import chat_bp
    from app.routes.api_routes import api   # ⭐ ADD THIS

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(recruiter)
    app.register_blueprint(candidate_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(api)   # ⭐ API REGISTER

    # ---------------- CREATE DATABASE TABLES ----------------
    with app.app_context():
        db.create_all()

    # ---------------- CONTEXT PROCESSOR ----------------
    @app.context_processor
    def inject_user():

        if "user_id" in session:

            user = db.session.get(User, session["user_id"])

            unread_count = Notification.query.filter_by(
                user_id=session["user_id"],
                is_read=False
            ).count()

            return dict(
                current_user=user,
                unread_count=unread_count
            )

        return dict(current_user=None, unread_count=0)

    # ---------------- HOME PAGE ----------------
    @app.route("/")
    def home():

        if "user_id" in session:

            role = session.get("role")

            if role == "recruiter":
                return redirect(url_for("recruiter.dashboard"))

            elif role == "candidate":
                return redirect(url_for("candidate_bp.dashboard"))

            elif role == "admin":
                return redirect(url_for("admin.dashboard"))

        return render_template("auth/login.html")

    # ---------------- DASHBOARD TEST ----------------
    @app.route("/dashboard")
    def dashboard():

        if "user_id" not in session:
            return redirect(url_for("auth.login"))

        return f"Welcome {session.get('user_email')}"

    return app