import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User
from flask_migrate import upgrade

app = create_app()
app.app_context().push()

upgrade()  

admin = User(
    username='admin',
    email='admin@quizmaster.com',
    is_admin=True
)
admin.set_password('admin123')

existing_admin = User.query.filter_by(email='admin@quizmaster.com').first()
if not existing_admin:
    db.session.add(admin)
    db.session.commit()
    print("Admin user created successfull!")
else:
    print("Admin user already exists!")
