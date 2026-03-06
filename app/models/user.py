from extensions import db


class User(db.Model):

    __tablename__ = "users"

    # ---------------- PRIMARY KEY ----------------
    id = db.Column(db.Integer, primary_key=True)

    # ---------------- LOGIN INFO ----------------
    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    # ---------------- USER ROLE ----------------
    role = db.Column(
        db.String(50),
        nullable=False,
        default="candidate"
    )
    # candidate / recruiter / admin

    # ---------------- VERIFICATION SYSTEM ----------------
    is_verified = db.Column(
        db.Boolean,
        default=False
    )

    verification_requested = db.Column(
        db.Boolean,
        default=False
    )

    verification_type = db.Column(
        db.String(50)
    )
    # celebrity / company / public_figure / official_brand

    # ---------------- STRING REPRESENTATION ----------------
    def __repr__(self):
        return f"<User {self.email}>"