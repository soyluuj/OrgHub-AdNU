from functools import wraps
from flask import session, flash, redirect, url_for
from models import User

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

def org_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in.")
            return redirect(url_for("auth.login"))
        
        user = User.query.get(session["user_id"])
        if not user or user.role != 'org_admin':
            flash("You do not have permission to access this page.")
            return redirect(url_for("home.index")) # Assuming home blueprint has 'index'
            
        return f(*args, **kwargs)
    return decorated_function