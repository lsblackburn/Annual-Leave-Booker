from app import app, db
from models import User, AnnualLeave
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from faker import Faker
import random

fake = Faker()

def seed_users():
    with app.app_context():
        now = datetime.utcnow()
        user_ids = []

        for _ in range(10):
            email = fake.unique.email()
            if not User.query.filter_by(email=email).first():
                user = User(
                    name=fake.name(),
                    email=email,
                    password=generate_password_hash('Password123!'),
                    is_admin=False,
                    created_at=now,
                    updated_at=now
                )
                db.session.add(user)
                db.session.flush()  # Get the user's ID without committing yet
                user_ids.append(user.id)

        db.session.commit()
        print("10 test users created.")
        return user_ids


def seed_annual_leave(user_ids, num_leaves=20):
    with app.app_context():
        statuses = ['pending', 'approved', 'rejected']

        for _ in range(num_leaves):
            user_id = random.choice(user_ids)
            start_date = fake.date_time_between(start_date='-30d', end_date='+30d')
            end_date = start_date + timedelta(days=random.randint(1, 10))

            leave = AnnualLeave(
                user_id=user_id,
                start_date=start_date,
                end_date=end_date,
                status=random.choice(statuses),
                created_at=start_date,
                updated_at=start_date
            )
            db.session.add(leave)

        db.session.commit()
        print(f"{num_leaves} annual leave entries created for random users.")


if __name__ == '__main__':
    user_ids = seed_users()
    seed_annual_leave(user_ids)
