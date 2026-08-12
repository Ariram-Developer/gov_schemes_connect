import os
from flask import Flask, flash, redirect, request, url_for, render_template, session
import mysql.connector
from config import Config
from app import db
from app.db import get_db

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
        if 'user_id' in session:
            if session.get('role') == 'admin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('user.schemes'))
        return render_template('index.html')

    @app.route('/profile', methods=['GET', 'POST'])
    def profile():
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
            
        user_id = session['user_id']
        
        # Use the pooled database connection instead of manual connection
        connection = get_db()
        cursor = connection.cursor(dictionary=True)
        
        if request.method == 'POST':
            new_username = request.form.get('username')
            new_email = request.form.get('email')
            new_fullname = request.form.get('full_name')
            new_phone = request.form.get('phone_number')
            
            cursor.execute("SELECT id FROM users WHERE (username = %s OR email = %s) AND id != %s", (new_username, new_email, user_id))
            
            if cursor.fetchone():
                flash("That Username or Email is already taken by another account.", "error")
            else:
                cursor.execute("""
                    UPDATE users SET username = %s, email = %s, full_name = %s, phone_number = %s WHERE id = %s
                """, (new_username, new_email, new_fullname, new_phone, user_id))
                connection.commit()
                
                session['full_name'] = new_fullname 
                flash("Profile vault updated successfully.", "success")
                
        cursor.execute("SELECT username, email, full_name, phone_number, role, created_at FROM users WHERE id = %s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        
        return render_template('profile.html', user=user_data)

    if not app.debug:
        @app.errorhandler(Exception)
        def handle_exception(e):
            import traceback
            return f"<h1>CRITICAL ERROR:</h1><pre>{traceback.format_exc()}</pre>", 500

    return app