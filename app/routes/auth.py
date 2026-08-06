import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        full_name = request.form['full_name'].strip()
        phone_number = request.form['phone_number'].strip()
        
        # Validation 1: Passwords Match
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'error')
            return redirect(url_for('auth.register'))
            
        # Validation 2: Password Strength (8 chars, 1 uppercase, 1 lowercase, 1 number)
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', password):
            flash('Password must be at least 8 characters and include uppercase, lowercase, and a number.', 'error')
            return redirect(url_for('auth.register'))

        # Validation 3: Phone Number Format (10 digits, starts with 6, 7, 8, or 9)
        if not re.match(r'^[6-9]\d{9}$', phone_number):
            flash('Phone number must be exactly 10 digits and start with 6, 7, 8, or 9.', 'error')
            return redirect(url_for('auth.register'))
            
        # Validation 4: Basic Email Format
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            flash('Please enter a valid email address.', 'error')
            return redirect(url_for('auth.register'))
        
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE email = %s OR username = %s", (email, username))
        if cursor.fetchone():
            flash('Email or Username already exists.', 'error')
            cursor.close()
            return redirect(url_for('auth.register'))
            
        # Hash password and insert including phone_number
        hashed_pw = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, full_name, phone_number) VALUES (%s, %s, %s, %s, %s)",
            (username, email, hashed_pw, full_name, phone_number)
        )
        db.commit()
        cursor.close()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/login.html', is_register=True)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password']
        
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session.clear()
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['full_name'] = user['full_name']
            
            if user['role'] == 'admin':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('user.schemes'))
            
        flash('Invalid email or password.', 'error')
        
    return render_template('auth/login.html', is_register=False)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))