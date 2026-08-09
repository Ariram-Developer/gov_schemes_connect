import os
import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
import mysql
from werkzeug.utils import secure_filename
from app.db import get_db
from app.utils import login_required

user_bp = Blueprint('user', __name__, url_prefix='/user')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'png', 'jpg', 'jpeg'}

@user_bp.route('/schemes')
@login_required
def schemes():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM schemes ORDER BY created_at DESC")
    schemes = cursor.fetchall()
    cursor.close()
    return render_template('user/schemes.html', schemes=schemes)

@user_bp.route('/apply/<int:scheme_id>', methods=['GET', 'POST'])
@login_required
def apply(scheme_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # 1. Fetch the specific scheme details
    cursor.execute("SELECT * FROM schemes WHERE id = %s", (scheme_id,))
    scheme = cursor.fetchone()
    
    if not scheme:
        flash('Scheme not found.', 'error')
        cursor.close()
        return redirect(url_for('user.schemes'))
        
    # 2. Dynamically build a list of required documents with clean ID "slugs" for HTML inputs
    required_docs_raw = [doc.strip() for doc in scheme['required_documents'].split(',')]
    doc_fields = []
    for doc in required_docs_raw:
        # Converts "Aadhaar Card" into "aadhaar_card"
        slug = re.sub(r'[^a-zA-Z0-9]', '_', doc.lower())
        doc_fields.append({'name': doc, 'slug': slug})

    # 3. Handle the Submission
    if request.method == 'POST':
        uploaded_paths = []
        
        # STRICT VALIDATION: Check every dynamically generated field
        for doc_obj in doc_fields:
            slug = doc_obj['slug']
            doc_name = doc_obj['name']
            
            if slug not in request.files:
                flash(f'Validation Error: Missing upload field for {doc_name}', 'error')
                return redirect(request.url)
                
            file = request.files[slug]
            if file.filename == '':
                flash(f'Validation Error: You forgot to upload your {doc_name}.', 'error')
                return redirect(request.url)
                
            if not allowed_file(file.filename):
                flash(f'Validation Error: Invalid file format for {doc_name}. Use PDF, JPG, or PNG.', 'error')
                return redirect(request.url)

            # Securely save each verified file
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = secure_filename(f"u{session['user_id']}_s{scheme_id}_{slug[:15]}.{ext}")
            file_path = os.path.join(current_app.root_path, 'static', 'uploads', filename)
            file.save(file_path)
            
            uploaded_paths.append(f"/static/uploads/{filename}")
        
        # Combine all safe file paths into a single comma-separated string
        all_documents_str = ",".join(uploaded_paths)
        
        try:
            cursor.execute(
                "INSERT INTO applications (user_id, scheme_id, document_url) VALUES (%s, %s, %s)",
                (session['user_id'], scheme_id, all_documents_str)
            )
            db.commit()
            flash('Application submitted successfully! All documents securely uploaded.', 'success')
        except mysql.connector.IntegrityError:
            flash('You have already applied for this scheme.', 'error')
        finally:
            cursor.close()
            
        return redirect(url_for('user.track'))

    cursor.close()
    return render_template('user/apply.html', scheme=scheme, doc_fields=doc_fields)

@user_bp.route('/track')
@login_required
def track():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.*, s.title AS scheme_title, s.category 
        FROM applications a
        JOIN schemes s ON a.scheme_id = s.id
        WHERE a.user_id = %s
        ORDER BY a.applied_at DESC
    """, (session['user_id'],))
    applications = cursor.fetchall()
    cursor.close()
    return render_template('user/track.html', applications=applications)