# app/auth/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from argon2 import PasswordHasher
from app.models import User
from app import db
from .decorators import admin_required

# Create a Blueprint for authentication routes
auth_bp = Blueprint('auth_bp', __name__)

# Initialize the PasswordHasher
ph = PasswordHasher()


@auth_bp.route('/')
def index():
    """Redirects the base URL to the registration page."""
    return redirect(url_for('auth_bp.login'))


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


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Find the user by their email
        user = User.query.filter_by(email=email).first()

        # Check if the user exists and the password is correct
        if user and user.check_password(password):
            # Log the user in and create a session
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('auth_bp.dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'warning')
            return redirect(url_for('auth_bp.login'))

    return render_template('login.html')


@auth_bp.route('/dashboard')
@login_required
def dashboard():
    """A protected route that only logged-in users can see."""
    return "<h1>Welcome to your Dashboard!</h1>"


@auth_bp.route('/logout')
@login_required
def logout():
    """Logs the current user out."""
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth_bp.login'))

@auth_bp.route('/admin-dashboard')
@login_required
@admin_required
def admin_dashboard():
    """Displays a list of all users for admins."""
    try:
        # Query the database to get all users
        users = User.query.all()
    except Exception as e:
        flash('Could not retrieve users from the database.', 'danger')
        users = []

    return render_template('admin_dashboard.html', users=users)
