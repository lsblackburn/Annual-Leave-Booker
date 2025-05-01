from flask import Blueprint, render_template, redirect, url_for, session, flash
from models import User, AnnualLeave

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
def dashboard_view():
    if 'user_id' not in session:
        flash('Please log in.', 'error')
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    leaves = AnnualLeave.query.filter_by(user_id=user.id).order_by(AnnualLeave.start_date.desc()).all()
    return render_template('pages/dashboard.html', is_admin=user.is_admin, leaves=leaves)
