# app/auth/routes.py
from .decorators import admin_required
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from argon2 import PasswordHasher
from app.models import User
from app import db
from .forms import LoginForm, RegistrationForm
from datetime import datetime, timedelta 

# Create a Blueprint for authentication routes
auth_bp = Blueprint('auth_bp', __name__)

# Initialize the PasswordHasher
ph = PasswordHasher()


@auth_bp.route('/')
def index():
    """Redirects the base URL to the login page."""
    return redirect(url_for('auth_bp.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration with WTForms."""
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        # --- Validation for existing user ---
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
            role='User'  # Default role for registration
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth_bp.login'))

    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login with account lockout logic."""
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        # Check if the account is currently locked
        if user and user.locked_until and user.locked_until > datetime.utcnow():
            flash(f"Your account is locked. Please try again after {user.locked_until.strftime('%Y-%m-%d %H:%M:%S')} UTC.", 'danger')
            return redirect(url_for('auth_bp.login'))

        # Check if user exists and password is correct
        if user and user.check_password(password):
            # --- Successful Login ---
            # Reset failed attempts and unlock account on successful login
            user.failed_login_attempts = 0
            user.locked_until = None
            db.session.commit()

            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('auth_bp.dashboard'))
        else:
            # --- Failed Login ---
            if user:
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= 5: # Lock after 5 failed attempts
                    user.locked_until = datetime.utcnow() + timedelta(minutes=15) # Lock for 15 minutes
                    flash('Your account has been locked for 15 minutes due to too many failed login attempts.', 'danger')
                db.session.commit()
            
            flash('Invalid email or password. Please try again.', 'warning')
            return redirect(url_for('auth_bp.login'))

    return render_template('login.html', form=form)


@auth_bp.route('/dashboard')
@login_required
def dashboard():
    """A protected route that only logged-in users can see."""
    # We will expand this on Day 6
    return "<h1>Welcome to your Dashboard!</h1>"

# at the end of app/auth/routes.py, after the dashboard() function

@auth_bp.route('/admin-dashboard')
@login_required
@admin_required
def admin_dashboard():
    """Displays a list of all users for admins."""
    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)


@auth_bp.route('/logout')
@login_required
def logout():
    """Logs the current user out."""
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth_bp.login'))