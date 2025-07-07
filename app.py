from flask import Flask, session, g, render_template
from models import db, User, AnnualLeave
from routes.auth_routes import auth
from routes.leave_routes import leave
from routes.dashboard_routes import dashboard
from routes.admin_routes import admin
from config import SECRET_KEY


# Initialize the Flask application
app = Flask(__name__)

# Configure the mySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/annual_leave_db'

# Enhance session security
app.config['SESSION_COOKIE_HTTPONLY'] = True # Prevent JavaScript access to session cookie
app.config['SESSION_COOKIE_SECURE'] = False # Set to True in production to use HTTPS

app.config['SECRET_KEY'] = SECRET_KEY

# Initialize the mySQL database instance with the Flask app
db.init_app(app)

# Register blueprints for route management
app.register_blueprint(auth)     
app.register_blueprint(dashboard)
app.register_blueprint(leave)
app.register_blueprint(admin)

@app.before_request
def before_every_request():
    # Load the current user before each request and store in the global object
    g.user = User.query.get(session['user_id']) if 'user_id' in session else None
    
    # Load the pending leave count for admin users before each request
    if hasattr(g, 'user') and g.user and g.user.is_admin:
        g.pending_leave_count = AnnualLeave.query.filter_by(status='pending').count()
    else:
        g.pending_leave_count = 0

# Context processor to inject the current user into templates
@app.context_processor
def inject_user():
    return dict(current_user=g.user)

# Error handler for 404 Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('pages/404.html'), 404

# Entry point for running the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)
