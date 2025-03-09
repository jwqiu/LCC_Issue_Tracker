from flask import Blueprint,request,session,flash,redirect,url_for
from database import db_connection
from datetime import datetime


comment = Blueprint('comment',__name__)

@comment.route('/comment',methods=['POST'])
def comment_submit():
    
    conn = db_connection() 
    cursor=conn.cursor()
    """
    Store the comments submitted by users by retrieving the hidden variables issue_id from the issue detail form
    """
    issue_id=request.form.get('issue_id')
    content=request.form.get("comment")
    issue_status=request.form.get("issue_status")
    current_time = datetime.now() 
    user_id=session.get('user_id')
    cursor.execute("INSERT INTO comments (issue_id,user_id,content,created_at) VALUES (%s, %s, %s, %s)",(issue_id,user_id,content,current_time))
    conn.commit()

    """
    Display a success notification, The frontend will get this information and show a notification
    """
    flash("✅ Comment added successfully", "success")
    


    """
    If the user is a visitor, nothing happens and redirect to the issue detail page. 
    Otherwise, we will check the issue's status and the commenter's role to decide whether to update the issue status to 'open' 
    and update the database accordingly

    """
    role=session.get('role')
    if role == 'visitor':
        cursor.close()
        conn.close()
        return redirect(url_for('issues.issue_detail',issue_id=issue_id))
    else:
        if issue_status != 'open' :
            cursor.execute("UPDATE issues SET status = %s WHERE issue_id = %s", ('open', issue_id))
            conn.commit()
            return redirect(url_for('issues.issue_detail',issue_id=issue_id))
        else:
            return redirect(url_for('issues.issue_detail',issue_id=issue_id))







