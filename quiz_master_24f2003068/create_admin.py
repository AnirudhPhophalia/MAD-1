import sys
import os
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__)) # for adding the python directory
sys.path.append(current_dir)

from app import create_app, db
from app.models import User

app = create_app()
app.app_context().push()

db.create_all() #It cretes table 

admin = User(
    username='admin',
    email='admin@quizmaster.com',
    full_name='Administrator',
    qualification='System Admin',
    date_of_birth=datetime.now(),
    is_admin=True
)
admin.set_password('admin123')

existing_admin = User.query.filter_by(email='admin@quizmaster.com').first() #for checking teh admin existance
if not existing_admin:
    db.session.add(admin)
    db.session.commit()
    print("Admin user created successfully!")
else:
    print("Admin user already exists!")
