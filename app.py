from flask import Flask,session, redirect, url_for, request
from extensions import bcrypt  
from blueprints.issues import issues_bp
from blueprints.login import login_bp
from blueprints.password import password
from blueprints.profile import profile
from blueprints.users import users
from blueprints.signup import signup
from blueprints.logout import logout_bp
from blueprints.comment import comment




app = Flask(__name__)
app.secret_key = "key_for_assessment_course_639"

bcrypt.init_app(app) 

@app.before_request
def require_login():
    allowed_routes = [
        "login.login", 
        "login.welcome", 
        "login.login_submit", 
        "signup.signup_1",  
        "signup.signup_1_submit",  
        "signup.signup_2",
        "signup.signup_2_submit",
        "static"
    ]
    if request.endpoint is None: 
        return

    if request.endpoint not in allowed_routes and not session.get("loggedin"):
        session["login_required"] = True
        return redirect(url_for("login.login"))

app.register_blueprint(issues_bp)
app.register_blueprint(login_bp)
app.register_blueprint(signup)
app.register_blueprint(password)
app.register_blueprint(profile)
app.register_blueprint(users)
app.register_blueprint(logout_bp)
app.register_blueprint(comment)


if __name__ == '__main__':
    app.run(debug=True)



