from functools import wraps
from flask import session, redirect, url_for, flash
from models import User

def admin_required(f):
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

def is_main_admin(user):
    return user.name.lower() == 'admin'

def get_user_or_redirect(user_id, redirect_endpoint='admin.controlpanel'):
    user = User.query.get(user_id)
    if not user:
        flash("User not found", "error")
        return None, redirect(url_for(redirect_endpoint))
    return user, None

