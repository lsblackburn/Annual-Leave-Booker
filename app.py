from flask import Flask, render_template
from models import db
from routes.auth_routes import auth
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = secrets.token_hex(16)

db.init_app(app)
app.register_blueprint(auth)

@app.route('/')
def dashboard():
    return render_template('pages/dashboard.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
