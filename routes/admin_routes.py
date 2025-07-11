from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from werkzeug.security import generate_password_hash
from models import db, User, AnnualLeave
from validation import is_strong_password
from decorators import admin_required

# Create a Blueprint named 'admin' to encapsulate all admin-related routes
admin = Blueprint('admin', __name__)

def is_main_admin(user): # Check if the user is the main admin
    return user.name.lower() == 'admin'

def get_user_or_redirect(user_id, redirect_endpoint='admin.controlpanel'): # Retrieve a user by ID or redirect if not found
    user = User.query.get(user_id)
    if not user:
        flash("User not found", "error")
        return None, redirect(url_for(redirect_endpoint))
    return user, None


@admin.route('/controlpanel') # Route for the admin control panel
@admin_required  # Decorator to ensure the user is an admin
def controlpanel(current_user):
    # Render the control panel template with necessary context
    return render_template(
        'pages/controlpanel.html',
        users=User.query.all(),  # Pass all users to the template
        current_user_id=current_user.id,  # Pass current user's ID
        current_user_is_admin=current_user.is_admin  # Pass current user's admin status
    )
    
    
@admin.route('/pending-leave')  # Route for pending leave requests
@admin_required
def pending_leave(current_user):
    # Retrieve all pending leave requests from the database
    pending_leaves = AnnualLeave.query.filter_by(status='pending').all()
    # Render the pending leave template with necessary context
    return render_template(
        'pages/pending_leave.html',
        leaves=pending_leaves,  # Pass all pending leave requests to the template
        current_user_id=current_user.id,  # Pass current user's ID
        current_user_is_admin=current_user.is_admin  # Pass current user's admin status
    )
    
@admin.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(current_user, user_id):
    
    # Retrieve the user to be edited or return 404 if not found
    user, response = get_user_or_redirect(user_id)
    if response:
        return response

    # Check if the user being edited is the main admin
    if is_main_admin(user):
        flash('Permission denied, you cannot edit the main admin.', 'error')
        return redirect(url_for('admin.controlpanel'))

    if request.method == 'POST':
        # Update user's name and email from the form data
        user.name = request.form['name'].strip()
        user.email = request.form['email'].strip()

        # If a new password is provided, validate and update it
        if request.form['password']:
            valid, msg = is_strong_password(request.form['password'])
            if not valid:
                flash(msg, 'error')
                return render_template('pages/edit_user.html', user=user)
            user.password = generate_password_hash(request.form['password'])

        db.session.commit()
        flash('User updated.', 'success')
        return redirect(url_for('admin.controlpanel'))

    return render_template('pages/edit_user.html', user=user)


@admin.route('/user/delete/<int:user_id>', methods=['POST'])  # Route to delete a user
@admin_required
def delete_user(current_user, user_id):
    # Retrieve the current user from the database
    current_user = User.query.get(session['user_id'])

    # Check if the current user is an admin and not trying to delete themselves
    if not current_user.is_admin or current_user.id == user_id:
        flash('Permission denied.', 'error')
        return redirect(url_for('admin.controlpanel'))

    # Retrieve the user to be deleted
    user, response = get_user_or_redirect(user_id)
    if response:
        return response
    
    if is_main_admin(user):
        flash('Cannot delete the main admin.', 'error')
        return redirect(url_for('admin.controlpanel'))
    
    if user:
        # Delete the user from the database
        db.session.delete(user)
        db.session.commit()
        flash('User deleted.', 'success')

    return redirect(url_for('admin.controlpanel'))


# Route to toggle admin status of a user
@admin.route('/toggle_admin/<int:user_id>/<action>', methods=['POST'])
@admin_required
def toggle_admin(current_user, user_id, action):
    if current_user.id == user_id:
        flash("Cannot modify your own role.", "error")
        return redirect(url_for('admin.controlpanel'))

    user, response = get_user_or_redirect(user_id)
    if response:
        return response

    if is_main_admin(user): # Check if the user is the main admin
        flash("Cannot modify main admin.", "error")
        return redirect(url_for('admin.controlpanel'))

    user.is_admin = True if action == 'promote' else False # Toggle admin status
    db.session.commit()
    flash(f"User {'promoted to' if user.is_admin else 'demoted from'} admin.", "success")
    return redirect(url_for('admin.controlpanel'))
