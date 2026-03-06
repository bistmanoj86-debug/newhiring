from extensions import db
from datetime import datetime


class Application(db.Model):

    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)

    job_id = db.Column(
        db.Integer,
        db.ForeignKey("jobs.id"),
        nullable=False
    )

    candidate_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    resume = db.Column(db.String(255), nullable=True)

    match_score = db.Column(db.Float, default=0)

    status = db.Column(db.String(50), default="Applied")

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    job = db.relationship("Job", backref="applications")
    candidate = db.relationship("User", backref="applications")

    def __repr__(self):
        return f"<Application {self.id}>"