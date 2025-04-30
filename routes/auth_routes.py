from flask import Blueprint, render_template, request, flash
from models import db, User
from validation import validate_registration_form, validate_login_form

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        valid, user = validate_login_form(email, password)
        if valid:
            flash('Login successful!', 'success')
            return render_template('pages/dashboard.html')
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('pages/login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        valid, message = validate_registration_form(name, email, password, confirm_password)
        if not valid:
            flash(message, 'error')
            return render_template('pages/register.html')

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return render_template('pages/login.html')

    return render_template('pages/register.html')
