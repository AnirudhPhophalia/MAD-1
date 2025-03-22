import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '24f2003068'
    SQLALCHEMY_DATABASE_URI = os.environ.get('quiz_master.db') or 'sqlite:///../quiz_master.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
