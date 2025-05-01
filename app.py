from flask import Flask, render_template, flash, session, redirect, url_for
from models import db, User
from routes.auth_routes import auth
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False
app.secret_key = secrets.token_hex(16) # Generate a random secret key

db.init_app(app)
app.register_blueprint(auth)

@app.route('/')
def dashboard(): # This is the main dashboard route
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'error')
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    return render_template('pages/dashboard.html', is_admin=user.is_admin)

@app.route('/controlpanel')
def controlpanel():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'error')
        return redirect(url_for('auth.login'))

    current_user = User.query.get(session['user_id'])
    users = User.query.all()
    return render_template('pages/controlpanel.html', users=users, current_user_id=current_user.id)


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



if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Create the database tables if they don't exist
    app.run(debug=True)
