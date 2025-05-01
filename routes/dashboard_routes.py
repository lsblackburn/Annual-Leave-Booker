from flask import Blueprint, render_template, redirect, url_for, session, flash
from models import User, AnnualLeave

# Define the 'dashboard' blueprint
dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
def dashboard_view():
    # Redirect to login if user is not authenticated
    if 'user_id' not in session:
        flash('Please log in.', 'error')
        return redirect(url_for('auth.login'))

    # Retrieve the current user from the database
    user = User.query.get(session['user_id'])

    # Fetch all leave records, ordered by start date descending
    leaves = AnnualLeave.query.order_by(AnnualLeave.start_date.desc()).all()

    # Render the dashboard template with user role and leave data
    return render_template('pages/dashboard.html', is_admin=user.is_admin, leaves=leaves)
