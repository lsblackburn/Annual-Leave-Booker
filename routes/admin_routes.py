from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from werkzeug.security import generate_password_hash
from models import db, User
from validation import is_strong_password

# Create a Blueprint named 'admin' to encapsulate all admin-related routes
admin = Blueprint('admin', __name__)

@admin.route('/controlpanel') # Route for the admin control panel
def controlpanel():
    # Check if the user is logged in
    if 'user_id' not in session:
        return redirect(url_for('auth.login')) # Redirect to login page if not logged in

    # Retrieve the current user from the database
    user = User.query.get(session['user_id'])

    # Render the control panel template with necessary context
    return render_template(
        'pages/controlpanel.html',
        users=User.query.all(),  # Pass all users to the template
        current_user_id=user.id,  # Pass current user's ID
        current_user_is_admin=user.is_admin  # Pass current user's admin status
    )

@admin.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])  # Route to edit a user's details
def edit_user(user_id):
    # Retrieve the current user from the database
    current_user = User.query.get(session['user_id'])

    # Retrieve the user to be edited or return 404 if not found
    user = User.query.get_or_404(user_id)

    # Check if the current user has permission to edit users
    if current_user.name.lower() != 'admin':
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

        # Commit the changes to the database
        db.session.commit()
        flash('User updated.', 'success')
        return redirect(url_for('admin.controlpanel'))

    # Render the edit user template with the user's current data
    return render_template('pages/edit_user.html', user=user)


@admin.route('/user/delete/<int:user_id>', methods=['POST'])  # Route to delete a user
def delete_user(user_id):
    # Retrieve the current user from the database
    current_user = User.query.get(session['user_id'])

    # Check if the current user is an admin and not trying to delete themselves
    if not current_user.is_admin or current_user.id == user_id:
        flash('Permission denied.', 'error')
        return redirect(url_for('admin.controlpanel'))

    # Retrieve the user to be deleted
    user = User.query.get(user_id)
    
    if user.name.lower() == 'admin':
        flash('Cannot delete the main admin.', 'error')
        return redirect(url_for('admin.controlpanel'))
    
    if user:
        # Delete the user from the database
        db.session.delete(user)
        db.session.commit()
        flash('User deleted.', 'success')

    return redirect(url_for('admin.controlpanel'))


@admin.route('/make_admin/<int:user_id>', methods=['POST'])  # Route to promote a user to admin
def make_admin(user_id):
    # Prevent users from modifying their own role
    if session['user_id'] == user_id:
        flash('Cannot modify your own role.', 'error')
        return redirect(url_for('admin.controlpanel'))

    # Retrieve the user to be promoted
    user = User.query.get(user_id)
    
    if user.name.lower() == 'admin':
        flash('Cannot promote the main admin.', 'error')
        return redirect(url_for('admin.controlpanel'))
    
    if user:
        # Set the user's admin status to True
        user.is_admin = True
        db.session.commit()
        flash('User promoted to admin.', 'success')

    return redirect(url_for('admin.controlpanel'))



@admin.route('/revoke_admin/<int:user_id>', methods=['POST'])  # Route to revoke a user's admin rights
def revoke_admin(user_id):
    # Retrieve the current user from the database
    current_user = User.query.get(session['user_id'])

    # Check if the current user is an admin and not trying to revoke their own admin rights
    if not current_user.is_admin or current_user.id == user_id:
        flash('Permission denied.', 'error')
        return redirect(url_for('admin.controlpanel'))

    # Retrieve the user whose admin rights are to be revoked
    user = User.query.get(user_id)
    
    if user.name.lower() == 'admin':
        flash('Cannot revoke admin rights from the main admin.', 'error')
        return redirect(url_for('admin.controlpanel'))
    
    if user:
        # Set the user's admin status to False
        user.is_admin = False
        db.session.commit()
        flash('Admin rights revoked.', 'success')

    return redirect(url_for('admin.controlpanel'))
