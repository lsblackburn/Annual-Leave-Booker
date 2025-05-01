from flask import Flask, session, g
from models import db, User
from routes.auth_routes import auth
from routes.leave_routes import leave
from routes.dashboard_routes import dashboard
from routes.admin_routes import admin
import secrets

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Enhance session security
app.config['SESSION_COOKIE_HTTPONLY'] = True # Prevent JavaScript access to session cookie
app.config['SESSION_COOKIE_SECURE'] = False # Set to True in production to use HTTPS

# Generate a random secret key for securely signing the session cookie
app.secret_key = secrets.token_hex(16)

# Initialize the SQLAlchemy database instance with the Flask app
db.init_app(app)

# Register blueprints for route management
app.register_blueprint(auth)     
app.register_blueprint(dashboard)
app.register_blueprint(leave)
app.register_blueprint(admin)

# Load the current user before each request and store in the global object
@app.before_request
def load_user():
    g.user = User.query.get(session['user_id']) if 'user_id' in session else None

# Entry point for running the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)
