from flask import Flask, redirect, url_for
from config import Config
from app import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Database teardown
    db.init_app(app)

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.user import user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)

    # Base route redirects to login
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app