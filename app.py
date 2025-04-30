from flask import Flask, render_template, flash, session, redirect, url_for
from models import db
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
    return render_template('pages/dashboard.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Create the database tables if they don't exist
    app.run(debug=True)
