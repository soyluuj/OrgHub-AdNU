from extensions import db, bcrypt
from models import User


class AuthService:

    @staticmethod
    def register(full_name, email, password, id_number, role="student"):

        # Check if email already exists
        existing = User.query.filter_by(email=email).first()

        if existing:
            return False, "Email already exists."

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        user = User(
            full_name=full_name,
            email=email,
            password=hashed_password,
            id_number=id_number,
            role=role
        )

        db.session.add(user)
        db.session.commit()

        return True, "Account created successfully."


    @staticmethod
    def login(email, password):

        user = User.query.filter_by(email=email).first()

        if not user:
            return None

        if bcrypt.check_password_hash(user.password, password):
            return user

        return None