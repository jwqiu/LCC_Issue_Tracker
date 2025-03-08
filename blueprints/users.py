from flask import Blueprint, render_template,request,redirect,url_for,session,flash
from database import db_connection

users = Blueprint('users',__name__)

@users.before_request
def restrict_to_admin():
    if  session['role'] != 'admin':
        return render_template('permission.html',next_page=url_for('issues.issues'))

@users.route('/user_detail/<int:user_id>')
def user_detail(user_id):
    conn = db_connection() 
    cursor=conn.cursor()  

    cursor.execute("SELECT * FROM users WHERE user_id=%s;",(user_id,))
    profile_detail=cursor.fetchone()

    username=profile_detail[1]
    role=profile_detail[8]
    first_name=profile_detail[4]
    last_name=profile_detail[5]
    email=profile_detail[3]
    location=profile_detail[6]
    profile_image=profile_detail[7]


    return render_template('user_detail.html',
    username=username,
    role=role,
    first_name=first_name,
    last_name=last_name,
    email=email,
    location=location,
    profile_image=profile_image)

@users.route('/users')
def users_list():

    conn = db_connection() 
    cursor=conn.cursor()    
    cursor.execute("SELECT * FROM users;")
    users=cursor.fetchall()

    cursor.execute("""
        SELECT role, COUNT(*) AS count
        FROM users
        GROUP BY role
        ORDER BY FIELD(role, 'admin', 'helper', 'visitor');
    """
    )
    user_type_num=cursor.fetchall()
    
    filter_status = request.args.get('filter', 'all')

    if filter_status == 'all':
        cursor.execute("SELECT * FROM users;")
    else:
        cursor.execute("SELECT * FROM users WHERE role = %s;", (filter_status,))

    users_filtered = cursor.fetchall()


    return render_template('users.html',users=users,user_type_num=user_type_num,users_filtered=users_filtered,filter_status=filter_status)

@users.route('/update_user')
def update_user():
    user_id = request.args.get('user_id')  

    conn = db_connection()
    cursor = conn.cursor()
    status=request.args.get('status')   
    new_role = request.args.get('role')

    if new_role:   
        cursor.execute("UPDATE users SET role = %s WHERE user_id = %s", (new_role, user_id))
        conn.commit()
    elif status:
        cursor.execute("UPDATE users SET status = %s WHERE user_id = %s", (status, user_id))
        conn.commit()

    cursor.close()
    conn.close()
    
    flash("✅ Updated successfully", "success")

    return redirect(url_for('users.users_list'))  

@users.route('/search')
def search_users():
    query = request.args.get('query', '').strip() 

    conn = db_connection()
    cursor = conn.cursor()
    no_results = False

    if query:
        cursor.execute("""
            SELECT * 
            FROM users 
            WHERE username=%s OR first_name=%s OR last_name=%s
        """, (query, query, query))
        search_results = cursor.fetchall()
    else:
        search_results = []  

    cursor.execute("""
        SELECT role, COUNT(*) AS count
        FROM users
        GROUP BY role
        ORDER BY FIELD(role, 'admin', 'helper', 'visitor');
    """
    )
    user_type_num=cursor.fetchall()

    users_filtered = []
    if not search_results:
        cursor.execute("SELECT * FROM users")  
        users_filtered = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('search_results.html', search_results=search_results, query=query,user_type_num=user_type_num,users_filtered=users_filtered,no_results=no_results)
