# app/models.py
from app import db
from flask_login import UserMixin      # <--- IMPORT UserMixin
from argon2 import PasswordHasher

ph = PasswordHasher()

# The User class now inherits from UserMixin
class User(db.Model, UserMixin):       # <--- ADD UserMixin HERE
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(80), nullable=False, default='User')

    def check_password(self, password):
        """Verify password against the stored hash."""
        try:
            return ph.verify(self.password_hash, password)
        except Exception:
            return False

    def __repr__(self):
        return f'<User {self.username}>'

# ADD THIS FUNCTION vvvv
