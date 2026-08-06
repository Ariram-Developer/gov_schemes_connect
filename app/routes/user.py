from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.db import get_db
from app.utils import login_required

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/schemes')
@login_required
def schemes():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # Fetch all active welfare schemes from the database
    cursor.execute("SELECT * FROM schemes ORDER BY id DESC")
    all_schemes = cursor.fetchall()
    cursor.close()
    
    return render_template('user/schemes.html', schemes=all_schemes)

@user_bp.route('/track')
@login_required
def track():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # Fetch only the applications belonging to the logged-in citizen
    cursor.execute("""
        SELECT a.*, s.title AS scheme_title, s.category 
        FROM applications a
        JOIN schemes s ON a.scheme_id = s.id
        WHERE a.user_id = %s
        ORDER BY a.applied_at DESC
    """, (session['user_id'],))
    
    user_applications = cursor.fetchall()
    cursor.close()
    
    return render_template('user/track.html', applications=user_applications)