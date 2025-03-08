from flask import Blueprint, render_template,request,session,redirect,url_for
from database import db_connection
from extensions import bcrypt
import re



password = Blueprint('password',__name__)

@password.route('/password')
def password_home():
    return render_template('password.html')


@password.route('/password_submit',methods=['POST'])
def password_submit():

    currentpassword = request.form['currentpassword']
    newPassword = request.form['newPassword']
    confirmPassword = request.form['confirmPassword']
    user_id=session.get('user_id')

    conn = db_connection() 
    cursor=conn.cursor(buffered=True)    

    cursor.execute("SELECT password_hash FROM LCC.users WHERE user_id=%s;",(user_id,))
    password_hash=cursor.fetchone()

    if bcrypt.check_password_hash(password_hash[0], currentpassword):
        if confirmPassword==newPassword:
            if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z0-9]+$', newPassword): 
                return render_template("password.html",error_message="Your new password should contain at least one letter and one number")
            elif newPassword == currentpassword:
                return render_template("password.html",error_message="New password cannot be the same as the current password.")
            elif len(newPassword) < 8:
                return render_template("password.html",error_message="Passwords should be at least 8 characters long")
            else:
                new_password_hash = bcrypt.generate_password_hash(newPassword).decode('utf-8')
                cursor.execute("""
                UPDATE users 
                SET password_hash=%s
                WHERE user_id = %s
                """ , (new_password_hash,user_id))
                conn.commit()
                success_message="Password updated successfully"

                return render_template("password.html",success_message=success_message)
        else:
            return render_template("password.html",error_message='The two new passwords you entered do not match')
    else:
        error_message='Password is incorrect'
        return render_template("password.html",error_message=error_message)
