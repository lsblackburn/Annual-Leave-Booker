from flask import Flask, session, g
from models import db, User
from routes.auth_routes import auth
from routes.leave_routes import leave
from routes.dashboard_routes import dashboard
from routes.admin_routes import admin
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False
app.secret_key = secrets.token_hex(16)

db.init_app(app)

# Register route blueprints
app.register_blueprint(auth)
app.register_blueprint(dashboard)
app.register_blueprint(leave)
app.register_blueprint(admin)

@app.before_request
def load_user():
    g.user = User.query.get(session['user_id']) if 'user_id' in session else None

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
