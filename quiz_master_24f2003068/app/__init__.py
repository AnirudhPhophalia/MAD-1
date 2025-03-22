from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate 
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()#migration ke liye database ko
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):#app create karne ke liye
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)  
    login_manager.init_app(app)

    from app.routes import admin, user, auth #routes import karne ke liye
    app.register_blueprint(admin.anirudh_bp)
    app.register_blueprint(user.anirudh_bp)
    app.register_blueprint(auth.anirudh_bp)

    return app



