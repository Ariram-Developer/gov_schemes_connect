from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import mysql
from app.db import get_db
from app.utils import admin_required, login_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # 1. Command Center Real-Time Metrics
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
    
    # Capture status from URL for the dashboard quick-filter
    status_filter = request.args.get('status', 'All')
    
    # 2. Recent Activity Feed (Clean Top 5 Global Submissions, Filterable)
    query = """
        SELECT a.*, u.full_name as applicant_name, s.title AS scheme_title 
        FROM applications a
        JOIN users u ON a.user_id = u.id
        JOIN schemes s ON a.scheme_id = s.id
    """
    
    if status_filter in ['Pending', 'Accepted', 'Rejected', 'Approved']:
        db_status = 'Accepted' if status_filter == 'Approved' else status_filter
        query += f" WHERE a.status = '{db_status}'"
        
    query += " ORDER BY a.applied_at DESC LIMIT 5"
    
    cursor.execute(query)
    recent_applications = cursor.fetchall()
    cursor.close()
    
    return render_template('admin/dashboard.html', metrics=metrics, applications=recent_applications, current_filter=status_filter)


@admin_bp.route('/users')
@login_required
def manage_users():
    if session.get('role') != 'admin':
        flash('Unauthorized access.', 'error')
        return redirect(url_for('user.schemes'))
        
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # 1. Real-Time Security Metrics
    cursor.execute("SELECT COUNT(id) as count FROM users WHERE role = 'citizen' AND is_active = 1")
    active_count = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(id) as count FROM users WHERE role = 'citizen' AND is_active = 0")
    suspended_count = cursor.fetchone()['count']
    
    metrics = {
        'active_users': active_count,
        'suspended_users': suspended_count,
        'total_users': active_count + suspended_count
    }
    
    # Capture status selection from the URL argument (?status=All/Active/Suspended)
    status_filter = request.args.get('status', 'All')
    
    # 2. Filtered Database Target Query
    query = """
        SELECT u.id, u.full_name, u.email, u.phone_number, u.created_at, u.is_active,
               COUNT(a.id) as total_applications
        FROM users u
        LEFT JOIN applications a ON u.id = a.user_id
        WHERE u.role = 'citizen'
    """
    
    if status_filter == 'Active':
        query += " AND u.is_active = 1"
    elif status_filter == 'Suspended':
        query += " AND u.is_active = 0"
        
    query += """
        GROUP BY u.id
        ORDER BY u.id DESC
    """
    
    cursor.execute(query)
    users = cursor.fetchall()
    cursor.close()
    
    return render_template('admin/users_manage.html', users=users, metrics=metrics, current_filter=status_filter)


@admin_bp.route('/users/<int:user_id>/toggle', methods=['POST'])
@login_required
def toggle_user_status(user_id):
    if session.get('role') != 'admin':
        flash('Unauthorized access.', 'error')
        return redirect(url_for('user.schemes'))
        
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    try:
        # Check current status to determine the action taken
        cursor.execute("SELECT is_active FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        if user:
            new_status = 0 if user['is_active'] else 1
            cursor.execute("UPDATE users SET is_active = %s WHERE id = %s", (new_status, user_id))
            db.commit()
            
            action = "restored" if new_status == 1 else "suspended"
            flash(f'Account access has been successfully {action}.', 'success')
        else:
            flash('User record not found.', 'error')
            
    except mysql.connector.Error as err:
        flash('A database error occurred while updating the account.', 'error')
    finally:
        cursor.close()
        
    return redirect(url_for('admin.manage_users'))


# Functional placeholder for modules we will build next
@admin_bp.route('/module/<module_name>')
@admin_required
def placeholder(module_name):
    clean_name = module_name.replace("_", " ").title()
    flash(f'The {clean_name} module is active and will be fully built in the next step!', 'success')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/schemes')
@login_required
def manage_schemes():
    if session.get('role') != 'admin':
        flash('Unauthorized access.', 'error')
        return redirect(url_for('user.schemes'))
        
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM schemes ORDER BY created_at DESC")
    schemes = cursor.fetchall()
    cursor.close()
    return render_template('admin/schemes_manage.html', schemes=schemes)


@admin_bp.route('/schemes/new', methods=['GET', 'POST'])
@login_required
def add_scheme():
    if session.get('role') != 'admin':
        flash('Unauthorized access.', 'error')
        return redirect(url_for('user.schemes'))
        
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '').strip()
        description = request.form.get('description', '').strip()
        eligibility = request.form.get('eligibility_criteria', '').strip()
        required_docs = request.form.get('required_documents', '').strip()
        
        # Validation: Check for empty fields
        if not title or not category or not description or not eligibility or not required_docs:
            flash('All fields are mandatory.', 'error')
            cursor.close()
            return redirect(request.url)
            
        try:
            cursor.execute("""
                INSERT INTO schemes (title, category, description, eligibility_criteria, required_documents, created_by)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (title, category, description, eligibility, required_docs, session['user_id']))
            db.commit()
            flash('Scheme successfully created and published.', 'success')
            cursor.close()
            return redirect(url_for('admin.manage_schemes'))
        except mysql.connector.IntegrityError:
            flash('A scheme with this title already exists. Please choose a unique title.', 'error')
        finally:
            cursor.close()
            
    # Fetch existing categories for the dropdown suggestion list
    cursor.execute("SELECT DISTINCT category FROM schemes")
    categories = [row['category'] for row in cursor.fetchall()]
    cursor.close()
    
    return render_template('admin/scheme_add.html', categories=categories)


@admin_bp.route('/schemes/<int:scheme_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_scheme(scheme_id):
    if session.get('role') != 'admin':
        flash('Unauthorized access.', 'error')
        return redirect(url_for('user.schemes'))
        
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '').strip()
        description = request.form.get('description', '').strip()
        eligibility = request.form.get('eligibility_criteria', '').strip()
        required_docs = request.form.get('required_documents', '').strip()
        
        if not title or not category or not description or not eligibility or not required_docs:
            flash('All fields are mandatory.', 'error')
            return redirect(request.url)
            
        try:
            cursor.execute("""
                UPDATE schemes 
                SET title = %s, category = %s, description = %s, 
                    eligibility_criteria = %s, required_documents = %s
                WHERE id = %s
            """, (title, category, description, eligibility, required_docs, scheme_id))
            db.commit()
            flash('Scheme successfully updated.', 'success')
            return redirect(url_for('admin.manage_schemes'))
        except mysql.connector.IntegrityError:
            flash('A scheme with this title already exists.', 'error')
        finally:
            cursor.close()
            
    # GET Request: Fetch existing scheme data to pre-fill the form
    cursor.execute("SELECT * FROM schemes WHERE id = %s", (scheme_id,))
    scheme = cursor.fetchone()
    
    if not scheme:
        flash('Scheme not found.', 'error')
        cursor.close()
        return redirect(url_for('admin.manage_schemes'))
        
    # Fetch unique categories for the dropdown list
    cursor.execute("SELECT DISTINCT category FROM schemes")
    categories = [row['category'] for row in cursor.fetchall()]
    cursor.close()
    
    return render_template('admin/scheme_edit.html', scheme=scheme, categories=categories)


@admin_bp.route('/schemes/<int:scheme_id>/archive', methods=['POST'])
@login_required
def archive_scheme(scheme_id):
    if session.get('role') != 'admin':
        flash('Unauthorized access.', 'error')
        return redirect(url_for('user.schemes'))
        
    db = get_db()
    cursor = db.cursor()
    
    try:
        # Toggle the is_active status (Allows Archiving and Restoring)
        cursor.execute("UPDATE schemes SET is_active = NOT is_active WHERE id = %s", (scheme_id,))
        db.commit()
        flash('Scheme status successfully updated.', 'success')
    except mysql.connector.Error as err:
        flash('A database error occurred.', 'error')
    finally:
        cursor.close()
        
    return redirect(url_for('admin.manage_schemes'))


@admin_bp.route('/applications')
@login_required
def manage_applications():
    if session.get('role') != 'admin':
        flash('Unauthorized access.', 'error')
        return redirect(url_for('user.schemes'))
        
    status_filter = request.args.get('status', 'All')
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    query = """
        SELECT a.*, u.full_name as applicant_name, s.title as scheme_title 
        FROM applications a
        JOIN users u ON a.user_id = u.id
        JOIN schemes s ON a.scheme_id = s.id
    """
    
    if status_filter in ['Pending', 'Accepted', 'Rejected', 'Approved']:
        db_status = 'Accepted' if status_filter == 'Approved' else status_filter
        query += f" WHERE a.status = '{db_status}'"
        
    query += " ORDER BY a.applied_at DESC"
    
    cursor.execute(query)
    applications = cursor.fetchall()
    cursor.close()
    
    return render_template('admin/applications_list.html', applications=applications, current_filter=status_filter)


@admin_bp.route('/applications/<int:app_id>/review', methods=['GET', 'POST'])
@login_required
def review_application(app_id):
    if session.get('role') != 'admin':
        flash('Unauthorized access.', 'error')
        return redirect(url_for('user.schemes'))
        
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # Capture Context Variables
    return_status = request.args.get('status', 'All')
    source = request.args.get('source', 'manage_applications')
    
    if request.method == 'POST':
        action = request.form.get('action') 
        remarks = request.form.get('remarks', '').strip()
        
        new_status = 'Accepted' if action == 'Approve' else 'Rejected'
        
        try:
            cursor.execute("""
                UPDATE applications 
                SET status = %s, admin_remarks = %s 
                WHERE id = %s
            """, (new_status, remarks, app_id))
            db.commit()
            
            ui_status = 'approved' if new_status == 'Accepted' else 'rejected'
            flash(f'Application successfully {ui_status}.', 'success')
            
            # Intelligently route back to origin
            if source == 'dashboard':
                return redirect(url_for('admin.dashboard', status=return_status) + '#recent-table')
            else:
                return redirect(url_for('admin.manage_applications', status=return_status))
            
        except mysql.connector.Error as err:
            flash('Database error occurred.', 'error')
            return redirect(request.url)
            
    cursor.execute("""
        SELECT a.*, u.full_name, u.email, s.title, s.category 
        FROM applications a
        JOIN users u ON a.user_id = u.id
        JOIN schemes s ON a.scheme_id = s.id
        WHERE a.id = %s
    """, (app_id,))
    application = cursor.fetchone()
    cursor.close()
    
    if not application:
        flash('Application not found.', 'error')
        if source == 'dashboard':
            return redirect(url_for('admin.dashboard', status=return_status) + '#recent-table')
        return redirect(url_for('admin.manage_applications', status=return_status))
        
    document_list = [doc.strip() for doc in application['document_url'].split(',')] if application['document_url'] else []
    
    # Pass 'source' to the template so the Back Button knows where to go
    return render_template('admin/application_review.html', application=application, documents=document_list, return_status=return_status, source=source)