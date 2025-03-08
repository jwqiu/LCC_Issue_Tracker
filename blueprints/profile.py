from flask import Blueprint, render_template,session,request,redirect,url_for
from database import db_connection
from werkzeug.utils import secure_filename
import os



profile = Blueprint('profile',__name__)

UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@profile.route('/profile_submit', methods=['POST'])
def profile_submit():

    filename = None
    user_id = session.get('user_id')
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    location = request.form['location']

    file = request.files.get('file')  
    if file and file.filename:
        filename = secure_filename(file.filename)  
        file_path = os.path.join(UPLOAD_FOLDER, filename)  
        file.save(file_path)  
        profile_image_path = f"static/uploads/{filename}"

    conn = db_connection()
    cursor = conn.cursor()

    if filename is None:

        cursor.execute("""
            UPDATE users 
            SET first_name = %s, last_name = %s, email = %s, location = %s
            WHERE user_id = %s
        """, (first_name, last_name, email, location, user_id))
    else:
        cursor.execute("""
            UPDATE users 
            SET first_name = %s, last_name = %s, email = %s, location = %s, profile_image = %s
            WHERE user_id = %s
        """, (first_name, last_name, email, location, profile_image_path, user_id))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('profile.profile_home'))


@profile.route('/profile_edit')
def profile_edit():
    
    user_id = session.get('user_id')

    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = %s",(user_id,))
    profile_detail=cursor.fetchone()

    first_name=profile_detail[4]
    last_name=profile_detail[5]
    email=profile_detail[3]
    location=profile_detail[6]
    username=session.get('username')
    role=session.get('role')
    profile_image=profile_detail[7]


    cursor.close()
    conn.close()
    
    return render_template('profile_edit.html',
    first_name=first_name,
    last_name=last_name,
    email=email,
    location=location,
    username=username,
    role=role,
    profile_image=profile_image)

@profile.route('/profile')
def profile_home():

    user_id=session.get('user_id')

    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = %s",(user_id,))
    profile_detail=cursor.fetchone()
    profile_image=profile_detail[7]

    return render_template('profile.html',profile_detail=profile_detail,profile_image=profile_image)