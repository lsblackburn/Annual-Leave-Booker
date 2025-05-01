from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from models import db, User
from validation import validate_registration_form, validate_login_form
from werkzeug.security import generate_password_hash, check_password_hash

# Define the authentication blueprint
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])  # Route for user login
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Attempt to find the user by email
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):  # Verify password
            session['user_id'] = user.id  # Store user ID in session
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard.dashboard_view'))  # Redirect to dashboard
        else:
            flash('Invalid email or password.', 'error')
            return render_template('pages/login.html')
    
    return render_template('pages/login.html')  # Render the login template

@auth.route('/register', methods=['GET', 'POST'])  # Route for user registration
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validate the registration form
        valid, message = validate_registration_form(name, email, password, confirm_password)
        if not valid:
            flash(message, 'error')
            return render_template('pages/register.html')

        hashed_password = generate_password_hash(password)  # Hash the password

        # Create a new user and add to the database
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return render_template('pages/login.html')

    return render_template('pages/register.html')  # Render the registration template

@auth.route('/logout', methods=['GET', 'POST'])  # Route for user logout
def logout():
    session.clear()  # Clear all session data
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))  # Redirect to login page
