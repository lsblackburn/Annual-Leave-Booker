from app import app, db
from models import User
from werkzeug.security import generate_password_hash
from datetime import datetime

def seed_admin_user(): # Function to seed the admin user
    with app.app_context():
        # Check if the admin already exists
        if not User.query.filter_by(email='admin@admin.com').first():
            now = datetime.utcnow()
            admin_user = User(
                name='Admin',
                email='admin@admin.com',
                password=generate_password_hash('Password123!'),
                is_admin=True,
                created_at=now,
                updated_at=now
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created.")
        else:
            print("Admin user already exists.")


if __name__ == '__main__':
    seed_admin_user()
