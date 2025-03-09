from flask import Blueprint, render_template,flash
import mysql.connector
from flask import request, session, redirect,url_for
from database import db_connection
from blueprints.login import login_bp
from datetime import datetime



issues_bp = Blueprint('issues',__name__)

@issues_bp.route('/issues')
def issues():

    conn = db_connection() 
    cursor=conn.cursor()         


    """
    Calculate the number of issues reported by the user
    Calculate the number of existing issues by type 
    Retrieve the user's profile image URL from the database and other user information
    adjust the frontend display accordingly based on the above information
    """
    user_id=session.get('user_id')
    cursor.execute("SELECT COUNT(*) FROM issues WHERE user_id = %s",(user_id,))
    num_reported = cursor.fetchone()[0]

    cursor.execute("""
        SELECT status, COUNT(*) AS count
        FROM issues
        GROUP BY status
        ORDER BY FIELD(status, 'new', 'open', 'stalled', 'resolved');
    """
    )
    issues_type_num=cursor.fetchall()

    cursor.execute("SELECT * FROM users WHERE user_id = %s",(user_id,))
    profile_detail=cursor.fetchone()
    profile_image=profile_detail[7]

    username=session.get("username")
    role=session.get("role")



    """
    Query the issues reported by the user and display it in a seperate module
    """
    cursor.execute("SELECT * FROM issues WHERE user_id = %s",(user_id,))
    your_issues=cursor.fetchall()


    """
    Add simple pagination to the issue list
    """
    cursor.execute("SELECT * FROM issues;")
    issues_data = cursor.fetchall()
    status_order = {"new": 1, "open": 2, "stalled": 3, "resolved": 4}
    issues_data.sort(key=lambda issue: status_order.get(issue[5].lower(), 5))

    cursor.close()
    conn.close()

    filter_status = request.args.get('filter', 'all')  
    if filter_status != 'all':
        filtered_issues = [issue for issue in issues_data if issue[5] == filter_status]
    else:
        filtered_issues = issues_data

    per_page = 10
    page = request.args.get('page', 1, type=int)

    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_data = filtered_issues[start_idx:end_idx]

    total_pages = (len(filtered_issues) + per_page - 1) // per_page 


    return render_template('issues.html',paginated_data=paginated_data,
        page=page,
        total_pages=total_pages,
        filter_status=filter_status,
        username=username,
        num_reported=num_reported,
        issues_type_num=issues_type_num,
        your_issues=your_issues,
        role=role,
        profile_image=profile_image)        

@issues_bp.route('/issue/<int:issue_id>')
def issue_detail(issue_id):
    
    
    """
    Retrieve issue details by joining the `users` and `issues` tables based on `user_id`, filtering by `issue_id`.  
    If the issue does not exist, render the `permission.html` template with a redirect link to the issues page.  
    """
    conn = db_connection() 
    cursor=conn.cursor()
    cursor.execute("""
    SELECT issues.*,users.*
    FROM users 
    LEFT JOIN issues ON users.user_id=issues.user_id
    WHERE issue_id = %s;
    """
    ,(issue_id,))
    issue = cursor.fetchone()
    if not issue:
        return render_template('permission.html',next_page=url_for('issues.issues'))
    
    issue_status=issue[5]       


    """
    Query and display the comments related to the issue
    """
    cursor.execute("""

    SELECT comments.*,users.*
    FROM comments
    LEFT JOIN users ON comments.user_id = users.user_id
    WHERE issue_id = %s
    """
    ,(issue_id,)
    )
    comments=cursor.fetchall()
    cursor.close()
    conn.close()


    """
    Check whether the user has permission to access this issue
    """
    role=session.get('role')
    user_id=session.get('user_id')
    if role == 'visitor':
        if user_id==issue[1]:
            return render_template('issue_detail.html',issue_id=issue_id,issue=issue,comments=comments,issue_status=issue_status,role=role)
        else:
            return render_template('permission.html',next_page=url_for('issues.issues'))
    else:
        return render_template('issue_detail.html',issue_id=issue_id,issue=issue,comments=comments,issue_status=issue_status,role=role)



"""
Render the report issue page
"""
@issues_bp.route('/report')
def report():
    return render_template('report_issue.html')


"""
We have a separate route to handle the submission of a new issue
"""
@issues_bp.route('/report_submit',methods=['POST'])
def report_submit():
    conn = db_connection() 
    cursor=conn.cursor()
    summary=request.form.get("summary")
    description=request.form.get("description")
    user_id=session.get('user_id')
    status='new'
    current_time = datetime.now() 
    cursor.execute("INSERT INTO issues (user_id,summary,description,status,created_at) VALUES (%s, %s, %s, %s, %s)",(user_id,summary,description,status,current_time))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("issues.issues"))


@issues_bp.route('/issue/issue_update')
def issue_update():
    
    """
    The user can update the issue status and manage changes here    
    Since the frontend only displays the issue status change button for admins and helpers, there is no need to distinguish user roles here
    """
    conn = db_connection() 
    cursor=conn.cursor()
    issue_id = request.args.get('issue_id')  
    status=request.args.get('status')   
    cursor.execute("UPDATE issues SET status = %s WHERE issue_id = %s", (status, issue_id))
    conn.commit()

    cursor.close()
    conn.close()

    flash("✅ Updated successfully", "success")
    return redirect(url_for('issues.issue_detail',issue_id=issue_id))



