from flask import Blueprint, render_template, Flask, flash
import mysql.connector
from flask import request
import connect 
from flask import session,redirect,url_for
from extensions import bcrypt

def db_connection():
    conn=mysql.connector.connect(
        host=connect.dbhost,
        user=connect.dbuser,
        password=connect.dbpassword,
        database=connect.dbname
    )
    return conn

login_bp = Blueprint('login',__name__)


@login_bp.route('/')
def welcome():
    return render_template('welcome.html')

@login_bp.route('/login_submit', methods=["POST"])
def login_submit():
    username=request.form.get("username")
    password=request.form.get("password")

    conn = db_connection() 
    cursor=conn.cursor(buffered=True)         

    cursor.execute("SELECT email,password_hash,username,role,user_id,status FROM users WHERE username=%s;",(username,))
    account=cursor.fetchone()

    cursor.close()
    conn.close()

    if account is None:

        return render_template("login.html", error_type="not_registered") 
    
    elif account[5]=='inactive':

        return render_template("login.html", error_type="inactive") 

    else:
        password_hash = account[1]

        if bcrypt.check_password_hash(password_hash, password):
            session['loggedin'] = True
            session['username'] = account[2]
            session['role'] = account[3]
            session['user_id']=account[4]

            return redirect(url_for("issues.issues"))

        else:
            username=account[2]
            error_type='wrong_password'
            return render_template("login.html",error_type=error_type,username=username)

@login_bp.route('/login')
def login():
    login_required = session.pop("login_required", False)
    check_login=session.get('loggedin')
    if check_login:
        return render_template('login.html',show_alert=True, next_page=url_for('issues.issues'))
    else:
        return render_template('login.html',login_required=login_required)


        
