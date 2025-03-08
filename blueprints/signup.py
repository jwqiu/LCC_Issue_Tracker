from flask import Blueprint, render_template, Flask
import mysql.connector
from flask import request
import connect 
from flask import session,redirect,url_for
from extensions import bcrypt
import re

def db_connection():
    conn=mysql.connector.connect(
        host=connect.dbhost,
        user=connect.dbuser,
        password=connect.dbpassword,
        database=connect.dbname
    )
    return conn


signup = Blueprint('signup',__name__)


@signup.route('/signup_1')
def signup_1():
    return render_template("signup_1.html")

@signup.route('/signup_1_submit', methods=["POST"])
def signup_1_submit():
    username=request.form.get("username")
    password1=request.form.get("password1")
    password2=request.form.get("password2")


    conn = db_connection() 
    cursor=conn.cursor()      
    cursor.execute('SELECT username FROM LCC.users WHERE username = %s;',(username,))
    result=cursor.fetchone()

    cursor.close()
    conn.close()

    if result is not None:
        return render_template('signup_1.html',error_message="An account already exists with this username")
    elif len(username) > 20:
        return render_template('signup_1.html',error_message="Your username cannot exceed 20 characters.")
    elif password1!=password2:
        return render_template('signup_1.html',error_message="The two new passwords you entered do not match.")
    
    elif not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z0-9]+$', password1): 
        return render_template('signup_1.html',username=username,error_message="Your password should contain at least one letter and one number")
    elif len(password1) < 8:
        return render_template('signup_1.html',username=username,error_message="Passwords should be at least 8 characters long")


    else:
        password_hash = bcrypt.generate_password_hash(password1).decode('utf-8')
        session['username'] = username
        session['password_hash'] = password_hash
        return render_template('signup_2.html',username=username,password_hash=password_hash)

@signup.route('/signup_2')
def signup_2():
    print(session['username'])
    return render_template("signup_2.html")

@signup.route('/signup_2_submit',methods=["POST"])
def signup_2_submit():
    email=request.form.get("email")
    first_name=request.form.get("first_name")
    last_name=request.form.get("last_name")
    location=request.form.get("home_city")
    username = session.get("username")
    password_hash = session.get("password_hash") 

    if len(email) > 320:
        return render_template('signup_2.html',error_message="Your email address cannot exceed 320 characters!")

    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        return render_template('signup_2.html',error_message="Invalid email address!")

    conn = db_connection() 
    cursor=conn.cursor()     
    cursor.execute("""
            INSERT INTO users (username, password_hash, email, first_name,last_name,location,role) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (username, password_hash, email, first_name,last_name,location,'visitor'))

    conn.commit()

    session['loggedin'] = True
    session['role'] = 'visitor'
    user_id = cursor.lastrowid
    session['user_id'] = user_id


    return render_template('signup_2.html', show_alert=True, next_page=url_for('issues.issues'))