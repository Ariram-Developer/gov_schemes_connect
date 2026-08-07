from flask import Flask, redirect, url_for, render_template, session
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
    # 1. Check if the user is already logged in
        if 'user_id' in session:
            # 2. If they are an Admin, send them to the Admin Workspace
            if session.get('role') == 'admin':
                return redirect(url_for('admin.dashboard'))
            # 3. If they are a Citizen, send them to the Schemes grid
            else:
                return redirect(url_for('user.schemes'))
                
        # 4. If they are NOT logged in, show the Landing Page!
        return render_template('index.html')

    return app