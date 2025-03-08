from flask import Blueprint, render_template
import mysql.connector
from flask import request, session, redirect,url_for
from database import db_connection

logout_bp = Blueprint('logout',__name__)

@logout_bp.route("/logout")
def logout():
    session.clear()  
    return redirect(url_for("login.welcome"))  