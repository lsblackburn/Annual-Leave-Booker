from models import User
from datetime import datetime
from flask import flash
from werkzeug.security import check_password_hash
import re

def validate_registration_form(name, email, password, confirm_password):
    # Validates the registration form.
    # - Name cannot be 'admin'
    # - Email must be unique
    # - Passwords must match
    # - Password must be strong
    if name.strip().lower() == 'admin':
        return False, "The name Admin is reserved and cannot be used."
    
    if not name or not email or not password:
        return False, "All fields are required."
    
    if password != confirm_password:
        return False, "Passwords do not match."
    
    is_valid, message = is_strong_password(password)
    
    if not is_valid:
        return False, message
    
    if User.query.filter_by(email=email).first():
        return False, "Email is already registered."

    return True, None

def is_strong_password(password):
    # Ensures password meets security standards:
    # At least 8 characters
    # Includes uppercase, lowercase, digit, special character
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character."
    
    return True, None

def validate_login_form(email, password):
    # Validates login credentials.
    # - Email must exist
    # - Password must match stored hash
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return True, user
    return False, None

def parse_dates(start_str, end_str):
    #Parses date strings into datetime objects. Returns (start, end) or (None, None) if invalid.
    try:
        start_date = datetime.strptime(start_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_str, '%Y-%m-%d')
        return start_date, end_date
    except ValueError:
        flash('Invalid date format.', 'error')
        return None, None

def validate_date_order(start_date, end_date):
    # Validates that end date is after start date.
    if end_date < start_date:
        flash('End date cannot be before start date.', 'error')
        return False
    return True

def validate_future_start(start_date):
    # Validates that the start date is not in the past.
    if start_date < datetime.now():
        flash('Start date cannot be in the past.', 'error')
        return False
    return True

def validate_user_owns_leave(leave, session_user_id):
    # Checks if the user owns the leave request.
    if leave.user_id != session_user_id:
        flash('You can only edit your own leave.', 'error')
        return False
    return True