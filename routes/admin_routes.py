from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from werkzeug.security import generate_password_hash
from models import db, User
from validation import is_strong_password

admin = Blueprint('admin', __name__)

@admin.route('/controlpanel')
def controlpanel():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    user = User.query.get(session['user_id'])
    return render_template('pages/controlpanel.html', users=User.query.all(), current_user_id=user.id, current_user_is_admin=user.is_admin)

@admin.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    current_user = User.query.get(session['user_id'])
    user = User.query.get_or_404(user_id)
    if current_user.name.lower() != 'admin':
        flash('Permission denied.', 'error')
        return redirect(url_for('admin.controlpanel'))

    if request.method == 'POST':
        user.name = request.form['name'].strip()
        user.email = request.form['email'].strip()
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

@admin.route('/user/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    current_user = User.query.get(session['user_id'])
    if not current_user.is_admin or current_user.id == user_id:
        flash('Permission denied.', 'error')
        return redirect(url_for('admin.controlpanel'))
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted.', 'success')
    return redirect(url_for('admin.controlpanel'))

@admin.route('/make_admin/<int:user_id>', methods=['POST'])
def make_admin(user_id):
    if session['user_id'] == user_id:
        flash('Cannot modify your own role.', 'error')
        return redirect(url_for('admin.controlpanel'))
    user = User.query.get(user_id)
    if user:
        user.is_admin = True
        db.session.commit()
        flash('User promoted to admin.', 'success')
    return redirect(url_for('admin.controlpanel'))

@admin.route('/revoke_admin/<int:user_id>', methods=['POST'])
def revoke_admin(user_id):
    current_user = User.query.get(session['user_id'])
    if not current_user.is_admin or current_user.id == user_id:
        flash('Permission denied.', 'error')
        return redirect(url_for('admin.controlpanel'))
    user = User.query.get(user_id)
    if user:
        user.is_admin = False
        db.session.commit()
        flash('Admin rights revoked.', 'success')
    return redirect(url_for('admin.controlpanel'))
