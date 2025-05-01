from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from datetime import datetime
from models import db, AnnualLeave, User

leave = Blueprint('leave', __name__, url_prefix='/leave')

@leave.route('/create', methods=['GET', 'POST'])
def create_leave():
    if 'user_id' not in session:
        flash('Please log in.', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        try:
            start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format.', 'error')
            return render_template('pages/create_leave.html')

        if end_date < start_date:
            flash('End date cannot be before start date.', 'error')
            return render_template('pages/create_leave.html')

        leave = AnnualLeave(user_id=session['user_id'], start_date=start_date, end_date=end_date, status='pending')
        db.session.add(leave)
        db.session.commit()
        flash('Leave request submitted.', 'success')
        return redirect(url_for('dashboard.dashboard_view'))

    return render_template('pages/create_leave.html')


@leave.route('/<int:leave_id>/approve', methods=['POST'])
def approve_leave(leave_id):
    user = User.query.get(session['user_id'])
    if not user.is_admin:
        flash('Permission denied.', 'error')
        return redirect(url_for('dashboard.dashboard_view'))

    leave = AnnualLeave.query.get_or_404(leave_id)
    leave.status = 'approved'
    db.session.commit()
    flash('Leave approved.', 'success')
    return redirect(url_for('dashboard.dashboard_view'))


@leave.route('/<int:leave_id>/reject', methods=['POST'])
def reject_leave(leave_id):
    user = User.query.get(session['user_id'])
    if not user.is_admin:
        flash('Permission denied.', 'error')
        return redirect(url_for('dashboard.dashboard_view'))

    leave = AnnualLeave.query.get_or_404(leave_id)
    leave.status = 'rejected'
    db.session.commit()
    flash('Leave rejected.', 'success')
    return redirect(url_for('dashboard.dashboard_view'))
