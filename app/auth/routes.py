# app/auth/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from argon2 import PasswordHasher
from app.models import User
from app import db

# Create a Blueprint for authentication routes
auth_bp = Blueprint('auth_bp', __name__)

# Initialize the PasswordHasher
ph = PasswordHasher()


@auth_bp.route('/')
def index():
    """Redirects the base URL to the registration page."""
    return redirect(url_for('auth_bp.register'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration."""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        # --- Validation ---
        user_by_email = User.query.filter_by(email=email).first()
        if user_by_email:
            flash('Email address already exists. Please log in.', 'warning')
            return redirect(url_for('auth_bp.login'))
        
        user_by_username = User.query.filter_by(username=username).first()
        if user_by_username:
            flash('Username is already taken. Please choose a different one.', 'warning')
            return redirect(url_for('auth_bp.register'))

        # --- Create New User ---
        password_hash = ph.hash(password)
        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            role=role
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth_bp.login'))

    return render_template('register.html')


@auth_bp.route('/login')
def login():
    """Renders the login page."""
    return render_template('login.html')