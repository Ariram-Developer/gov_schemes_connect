import os
from flask import Flask, flash, redirect, request, url_for, render_template, session
import mysql.connector
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

    @app.route('/profile', methods=['GET', 'POST'])
    def profile():
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
            
        user_id = session['user_id']
        
        # Now securely reading from your .env file
        conn = mysql.connector.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            user=os.environ.get('DB_USER', 'root'),
            password=os.environ.get('DB_PASSWORD', ''),
            database=os.environ.get('DB_NAME', 'gov_scheme_connect')
        )
        cursor = conn.cursor(dictionary=True)
        
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
                conn.commit()
                
                # Update the session name in case they changed their full name
                session['full_name'] = new_fullname 
                flash("Profile vault updated successfully.", "success")
                
        cursor.execute("SELECT username, email, full_name, phone_number, role, created_at FROM users WHERE id = %s", (user_id,))
        user_data = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return render_template('profile.html', user=user_data)

    return app