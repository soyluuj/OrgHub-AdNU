from extensions import db

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(150), nullable=False)

    email = db.Column(db.String(150), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    id_number = db.Column(db.String(50))

    role = db.Column(
        db.Enum("student", "faculty", "admin"),
        nullable=False,
        default="student"
    )

    account_status = db.Column(
        db.Enum("pending", "verified", "suspended", "banned"),
        nullable=False,
        default="pending"
    )
    
    bids = db.relationship(
        "Bid",
        back_populates = "bidder",
        cascade= "all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.email}>"
    