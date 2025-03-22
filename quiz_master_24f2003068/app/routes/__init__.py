from .admin import anirudh_bp as admin_bp
from .user import anirudh_bp as user_bp
from .auth import anirudh_bp as auth_bp

def init_app(app):
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
