from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from models import db, User
from validation import validate_registration_form, validate_login_form
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login(): # User login route
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Validate login form
        user = User.query.filter_by(email=email).first() # Check if user exists by checking only the email
        if user and check_password_hash(user.password, password): # Check password hash
            session['user_id'] = user.id  # Store user in session
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard.dashboard_view'))  # Redirect to dashboard
        else:
            flash('Invalid email or password.', 'error')
            return render_template('pages/login.html')
    
    return render_template('pages/login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register(): # User registration route
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validate registration form
        valid, message = validate_registration_form(name, email, password, confirm_password)
        if not valid:
            flash(message, 'error')
            return render_template('pages/register.html')

        hashed_password = generate_password_hash(password) # Hash the password

        # Check if email already exists
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return render_template('pages/login.html')

    return render_template('pages/register.html')


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    # Handle user logout logic here
    session.clear()  # Destroy all session data
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))  # Redirect to login page