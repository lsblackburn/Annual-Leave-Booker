from flask import Flask, render_template, flash, session, redirect, url_for, request, g
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from routes.auth_routes import auth
import secrets
from validation import is_strong_password

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False
app.secret_key = secrets.token_hex(16) # Generate a random secret key

db.init_app(app)
app.register_blueprint(auth)

@app.before_request
def load_user(): # Load the user from the session before each request
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])
    else:
        g.user = None

@app.route('/')
def dashboard(): # This is the main dashboard route
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'error')
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    return render_template('pages/dashboard.html')

@app.route('/controlpanel')
def controlpanel():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'error')
        return redirect(url_for('auth.login'))

    current_user = User.query.get(session['user_id'])
    users = User.query.all()
    return render_template(
        'pages/controlpanel.html',
        users=users,
        current_user_id=current_user.id,
        current_user_is_admin=current_user.is_admin
    )
    
    
@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('auth.login'))

    current_user = User.query.get(session['user_id'])
    user_to_edit = User.query.get_or_404(user_id)

    if current_user.name.lower() != 'admin':
        flash('You do not have permission to edit users.', 'error')
        return redirect(url_for('controlpanel'))

    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        if not name or not email:
            flash('Name and email cannot be empty.', 'error')
            return render_template('pages/edit_user.html', user=user_to_edit)

        existing_user = User.query.filter_by(email=email).first()
        if existing_user and existing_user.id != user_to_edit.id:
            flash('Email is already registered to another user.', 'error')
            return render_template('pages/edit_user.html', user=user_to_edit)

        user_to_edit.name = name
        user_to_edit.email = email

        if password:
            is_valid, message = is_strong_password(password)
            if not is_valid:
                flash(message, 'error')
                return render_template('pages/edit_user.html', user=user_to_edit)
            user_to_edit.password = generate_password_hash(password)

        db.session.commit()
        flash('User updated successfully.', 'success')
        return redirect(url_for('controlpanel'))

    return render_template('pages/edit_user.html', user=user_to_edit)
    
    

@app.route('/user/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'user_id' not in session:
        flash('You must be logged in to perform this action.', 'error')
        return redirect(url_for('auth.login'))

    current_user = User.query.get(session['user_id'])

    if not current_user or not current_user.is_admin:
        flash('You are not authorized to delete users.', 'error')
        return redirect(url_for('controlpanel'))

    user_to_delete = User.query.get(user_id)

    if not user_to_delete:
        flash('User not found.', 'error')
        return redirect(url_for('controlpanel'))

    if user_to_delete.id == current_user.id:
        flash('You cannot delete your own account.', 'error')
        return redirect(url_for('controlpanel'))

    db.session.delete(user_to_delete)
    db.session.commit()
    flash('User deleted successfully.', 'success')
    
    
@app.route('/make_admin/<int:user_id>', methods=['POST'])
def make_admin(user_id):
    if 'user_id' not in session:
        flash('You must be logged in to perform this action.', 'error')
        return redirect(url_for('auth.login'))

    current_user = User.query.get(session['user_id'])
    if current_user.id == user_id:
        flash('You cannot modify your own role.', 'error')
        return redirect(url_for('controlpanel'))

    user_to_promote = User.query.get(user_id)
    if user_to_promote:
        user_to_promote.is_admin = True
        db.session.commit()
        flash(f'User {user_to_promote.name} is now an admin.', 'success')
    else:
        flash('User not found.', 'error')

    return redirect(url_for('controlpanel'))


@app.route('/revoke_admin/<int:user_id>', methods=['POST'])
def revoke_admin(user_id):
    if 'user_id' not in session:
        flash('You must be logged in to perform this action.', 'error')
        return redirect(url_for('auth.login'))

    current_user = User.query.get(session['user_id'])
    if not current_user.is_admin:
        flash('Only admins can revoke admin rights.', 'error')
        return redirect(url_for('controlpanel'))

    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot revoke your own admin rights.', 'error')
        return redirect(url_for('controlpanel'))

    user.is_admin = False
    db.session.commit()
    flash(f'{user.name} is no longer an admin.', 'success')
    return redirect(url_for('controlpanel'))




if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Create the database tables if they don't exist
    app.run(debug=True)
