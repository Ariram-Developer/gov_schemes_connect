from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.db import get_db
from app.utils import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # 1. Real-Time Dynamic Metrics
    cursor.execute("SELECT COUNT(id) as count FROM users WHERE role = 'citizen'")
    total_users = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(id) as count FROM schemes")
    total_schemes = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(id) as count FROM applications WHERE status = 'Pending'")
    pending_apps = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(id) as count FROM applications WHERE status = 'Accepted'")
    approved_apps = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(id) as count FROM applications WHERE status = 'Rejected'")
    rejected_apps = cursor.fetchone()['count']
    
    metrics = {
        'total_users': total_users,
        'total_schemes': total_schemes,
        'pending_apps': pending_apps,
        'approved_apps': approved_apps,
        'rejected_apps': rejected_apps
    }
    
    # 2. Dynamic Filtering Logic for the Ledger
    status_filter = request.args.get('status')
    
    if status_filter in ['Pending', 'Accepted', 'Rejected']:
        cursor.execute("""
            SELECT a.*, u.full_name, s.title AS scheme_title 
            FROM applications a
            JOIN users u ON a.user_id = u.id
            JOIN schemes s ON a.scheme_id = s.id
            WHERE a.status = %s
            ORDER BY a.applied_at DESC
        """, (status_filter,))
    else:
        cursor.execute("""
            SELECT a.*, u.full_name, s.title AS scheme_title 
            FROM applications a
            JOIN users u ON a.user_id = u.id
            JOIN schemes s ON a.scheme_id = s.id
            ORDER BY a.applied_at DESC
        """)
        
    applications = cursor.fetchall()
    cursor.close()
    
    return render_template('admin/dashboard.html', metrics=metrics, applications=applications, current_filter=status_filter)

# Functional placeholder for modules we will build next
@admin_bp.route('/module/<module_name>')
@admin_required
def placeholder(module_name):
    clean_name = module_name.replace("_", " ").title()
    flash(f'The {clean_name} module is active and will be fully built in the next step!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/application/<int:app_id>', methods=['GET', 'POST'])
@admin_required
def review_application(app_id):
    # We will build this HTML view in the next phase!
    flash(f'Fetching data for Application #{app_id}... Interface coming next.', 'success')
    return redirect(url_for('admin.dashboard'))