from models import User

def validate_registration_form(name, email, password, confirm_password):
    if password != confirm_password:
        return False, "Passwords do not match."
    
    is_valid, message = is_strong_password(password)
    if not is_valid:
        return False, message

    if User.query.filter_by(email=email).first():
        return False, "Email is already registered."

    return True, None

import re

def is_strong_password(password):
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
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        return True, user
    return False, None
