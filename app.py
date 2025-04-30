#imports
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = secrets.token_hex(16) # Generate a random secret key

# Create a database model for the user
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    def __repr__(self) -> str:
        return f'<User {self.name}>'

# Routes to webpages
@app.route('/')
def dashboard():
    return render_template('pages/dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email, password=password).first()
        if user: # Check if the user exists in the database
            flash('Login successful!', 'success')
            return render_template('pages/dashboard.html')
        else: # If user does not exist, show error message
            flash('Invalid email or password.', 'error')
            return render_template('pages/login.html')
    
    return render_template('pages/login.html')
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password: # Check if passwords match
            flash('Passwords do not match.', 'error')
            return render_template('pages/register.html')
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user: # Check if email is already registered
            flash('Email is already registered.', 'error')
            return render_template('pages/register.html')
        
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful. Please log in.', 'success')
        return render_template('pages/login.html')
    
    return render_template('pages/register.html')
   



if __name__ == '__main__':
    
    with app.app_context():
        db.create_all()  # Create the database tables if they don't exist
    
    app.run(debug=True)