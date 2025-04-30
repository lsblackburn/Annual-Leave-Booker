from models import User

def validate_registration_form(name, email, password, confirm_password):
    if password != confirm_password:
        return False, "Passwords do not match."

    if User.query.filter_by(email=email).first():
        return False, "Email is already registered."

    return True, None

def validate_login_form(email, password):
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        return True, user
    return False, None
