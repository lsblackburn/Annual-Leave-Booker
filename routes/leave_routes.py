from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from datetime import datetime
from models import db, AnnualLeave, User

# Define the 'leave' blueprint with a URL prefix
leave = Blueprint('leave', __name__, url_prefix='/leave')

@leave.route('/create', methods=['GET', 'POST'])  # Route for creating a new leave request
def create_leave():
    # Check if the user is logged in
    if 'user_id' not in session:
        flash('Please log in.', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        try:
            # Parse start and end dates from the form
            start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format.', 'error')
            return render_template('pages/create_leave.html')

        # Validate that the end date is not before the start date
        if end_date < start_date:
            flash('End date cannot be before start date.', 'error')
            return render_template('pages/create_leave.html')

        # Create a new leave request with 'pending' status
        leave = AnnualLeave(
            user_id=session['user_id'],
            start_date=start_date,
            end_date=end_date,
            status='pending'
        )
        db.session.add(leave)  # Add the new leave request to the session
        db.session.commit()    # Commit the session to save changes
        flash('Leave request submitted.', 'success')
        return redirect(url_for('dashboard.dashboard_view'))

    # Render the leave creation form for GET requests
    return render_template('pages/create_leave.html')

@leave.route('/<int:leave_id>/edit', methods=['GET', 'POST'])
def edit_leave(leave_id):
    leave = AnnualLeave.query.get_or_404(leave_id)
    
    # Check if the current user is the one who booked the leave
    if leave.user_id != session['user_id']:
        flash('You can only edit your own leave.', 'error')
        return redirect(url_for('dashboard.dashboard_view'))

    if request.method == 'POST':
        try:
            start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format.', 'error')
            return render_template('pages/edit_leave.html', leave=leave)

        if end_date < start_date:
            flash('End date cannot be before start date.', 'error')
            return render_template('pages/edit_leave.html', leave=leave)

        # Update the leave dates and set status to 'pending' for reapproval
        leave.start_date = start_date
        leave.end_date = end_date
        leave.status = 'pending'
        db.session.commit()

        flash('Leave updated. Awaiting admin approval.', 'success')
        return redirect(url_for('dashboard.dashboard_view'))

    return render_template('pages/edit_leave.html', leave=leave)

@leave.route('/<int:leave_id>/approve', methods=['POST'])  # Route for approving a leave request
def approve_leave(leave_id):
    # Retrieve the current user from the session
    user = User.query.get(session['user_id'])
    # Check if the user has admin privileges
    if not user.is_admin:
        flash('Permission denied.', 'error')
        return redirect(url_for('dashboard.dashboard_view'))

    # Retrieve the leave request by ID or return 404 if not found
    leave = AnnualLeave.query.get_or_404(leave_id)
    leave.status = 'approved'  # Update the status to 'approved'
    db.session.commit()        # Commit the change to the database
    flash('Leave approved.', 'success')
    return redirect(url_for('dashboard.dashboard_view'))

@leave.route('/<int:leave_id>/reject', methods=['POST'])  # Route for rejecting a leave request
def reject_leave(leave_id):
    # Retrieve the current user from the session
    user = User.query.get(session['user_id'])
    # Check if the user has admin privileges
    if not user.is_admin:
        flash('Permission denied.', 'error')
        return redirect(url_for('dashboard.dashboard_view'))

    # Retrieve the leave request by ID or return 404 if not found
    leave = AnnualLeave.query.get_or_404(leave_id)
    leave.status = 'rejected'  # Update the status to 'rejected'
    db.session.commit()        # Commit the change to the database
    flash('Leave rejected.', 'success')
    return redirect(url_for('dashboard.dashboard_view'))
