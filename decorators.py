from functools import wraps
from flask import session, redirect, url_for, flash, g
from models import User

def admin_required(f): # Decorator to check if the user is an admin
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            flash('Access denied: Administrator privileges are required.', 'error')
            return redirect(url_for('dashboard.dashboard_view'))

        return f(user, *args, **kwargs)  # Pass current_user to route
    return decorated_function

def login_required(view): # Decorator to ensure the user is logged in
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        user_id = session.get('user_id')
        if user_id is None:
            flash('Please log in.', 'error')
            return redirect(url_for('auth.login'))

        g.user = User.query.get(user_id)
        return view(*args, **kwargs)
    return wrapped_view