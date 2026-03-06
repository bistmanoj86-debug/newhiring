from flask import Blueprint, render_template, session, redirect, url_for
from extensions import db
from app.models.notification import Notification

notification_bp = Blueprint(
    "notification",
    __name__,
    url_prefix="/notifications"
)

# ---------------- VIEW NOTIFICATIONS ----------------
@notification_bp.route("/")
def view_notifications():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    notifications = Notification.query.filter_by(
        user_id=session["user_id"]
    ).order_by(Notification.created_at.desc()).all()

    return render_template(
        "notifications.html",
        notifications=notifications
    )


# ---------------- MARK AS READ ----------------
@notification_bp.route("/read/<int:id>")
def mark_as_read(id):

    notification = Notification.query.get_or_404(id)
    notification.is_read = True
    db.session.commit()

    return redirect(url_for("notification.view_notifications"))


# ---------------- TEST NOTIFICATION (FOR NAVBAR COUNT) ----------------
@notification_bp.route("/add-test")
def add_test_notification():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    n = Notification(
        user_id=session["user_id"],
        message="Test notification 🔔"
    )

    db.session.add(n)
    db.session.commit()

    return "Notification Added Successfully ✅"