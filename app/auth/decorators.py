# app/auth/decorators.py

from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def admin_required(f):
    """
    A custom decorator to ensure the user is an admin.
    If they are not, it flashes an error and redirects them.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated and has the 'Admin' role
        if not current_user.is_authenticated or current_user.role != 'Admin':
            flash('This area is for admins only.', 'danger')
            # Redirect to a safe page, like the main dashboard or login
            return redirect(url_for('auth_bp.login')) 
        return f(*args, **kwargs)
    return decorated_function