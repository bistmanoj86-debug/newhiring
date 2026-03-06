from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
import random


# ---------------- BLUEPRINT ----------------
auth = Blueprint("auth", __name__)


# ---------------- REGISTER ----------------
@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        if role not in ["candidate", "recruiter"]:
            role = "candidate"

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("User already exists!")
            return redirect(url_for("auth.register"))

        hashed_password = generate_password_hash(password)

        new_user = User(
            email=email,
            password=hashed_password,
            role=role
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration Successful! Please login.")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


# ---------------- LOGIN ----------------
@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("User not found!")
            return redirect(url_for("auth.login"))

        if not check_password_hash(user.password, password):
            flash("Incorrect password!")
            return redirect(url_for("auth.login"))

        session["user_id"] = user.id
        session["user_email"] = user.email
        session["role"] = user.role

        flash("Login Successful!")

        if user.role == "admin":
            return redirect(url_for("admin.dashboard"))

        elif user.role == "recruiter":
            return redirect(url_for("recruiter.dashboard"))

        else:
            return redirect(url_for("candidate_bp.dashboard"))

    return render_template("auth/login.html")


# ---------------- SEND OTP ----------------
@auth.route("/send-otp", methods=["POST"])
def send_otp():

    phone = request.form.get("phone")

    if not phone:
        flash("Enter phone number")
        return redirect(url_for("auth.login"))

    otp = random.randint(100000, 999999)

    session["otp"] = otp
    session["phone"] = phone

    print("OTP:", otp)  # terminal me dikhega

    flash("OTP sent!")

    return redirect(url_for("auth.verify_otp"))


# ---------------- VERIFY OTP ----------------
@auth.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():

    if request.method == "POST":

        user_otp = request.form.get("otp")

        if not user_otp:
            flash("Enter OTP")
            return redirect(url_for("auth.verify_otp"))

        if int(user_otp) == session.get("otp"):

            # ✅ IMPORTANT: session set karo
            session["user_id"] = session.get("phone")
            session["role"] = "candidate"

            flash("Login successful via OTP")

            return redirect(url_for("candidate_bp.dashboard"))

        else:
            flash("Invalid OTP")

    return render_template("auth/verify_otp.html")


# ---------------- FORGOT PASSWORD ----------------
@auth.route("/forgot-password")
def forgot_password():
    return render_template("auth/forgot_password.html")


# ---------------- LOGOUT ----------------
@auth.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully!")

    return redirect(url_for("auth.login"))