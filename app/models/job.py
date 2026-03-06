from extensions import db


class Job(db.Model):

    __tablename__ = "jobs"

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Job title
    title = db.Column(
        db.String(200),
        nullable=False
    )

    # Job description
    description = db.Column(
        db.Text,
        nullable=False
    )

    # Job location
    location = db.Column(
        db.String(100),
        nullable=False
    )

    # Required skills
    skills = db.Column(
        db.String(200),
        nullable=False
    )

    # Recruiter who created the job
    recruiter_id = db.Column(
        db.Integer,
        nullable=False
    )

    # Admin approval status
    status = db.Column(
        db.String(50),
        default="Pending"
    )

    # Optional: created time
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # Optional: readable output
    def __repr__(self):
        return f"<Job {self.title}>"