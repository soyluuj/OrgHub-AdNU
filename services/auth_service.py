from extensions import db, bcrypt
from models import User

class AuthService:
    @staticmethod
    def register(full_name, email, password, role):
        if User.query.filter_by(email=email).first():
            return False, "Email already exists."
        
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(full_name=full_name, email=email, password_hash=hashed_password, role=role)
        db.session.add(user)
        db.session.commit()
        return True, "Account created successfully."

    @staticmethod
    def login(email, password):
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            return user
        return None