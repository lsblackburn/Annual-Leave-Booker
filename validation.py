from models import User
import re

def validate_registration_form(name, email, password, confirm_password):
    if name.strip().lower() == 'admin': # Stops users registering as 'admin'
        return False, "The name Admin is reserved and cannot be used."

    if password != confirm_password: # Check if passwords match, if not, return error message
        return False, "Passwords do not match."
    
    is_valid, message = is_strong_password(password) # Check if password is strong (calls is_strong_password function), if not, return error message
    if not is_valid:
        return False, message

    if User.query.filter_by(email=email).first(): # Check if email is already registered, if so, return error message
        return False, "Email is already registered."

    return True, None # If all checks pass, return True

def is_strong_password(password): # Function to check if the password is strong
    if len(password) < 8: # Check if password is at least 8 characters long, if not, return error message
        return False, "Password must be at least 8 characters long."
    if not re.search(r'[A-Z]', password): # Check if password contains at least one uppercase letter, if not, return error message
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', password): # Check if password contains at least one lowercase letter, if not, return error message
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r'\d', password): # Check if password contains at least one digit, if not, return error message
        return False, "Password must contain at least one digit."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password): # Check if password contains at least one special character, if not, return error message
        return False, "Password must contain at least one special character."

    return True, None # If all checks pass, return True


def validate_login_form(email, password): # Function to validate login form
    user = User.query.filter_by(email=email, password=password).first() # Check if user exists with the provided email and password
    if user: # If user exists, return True and the user object
        return True, user
    return False, None
