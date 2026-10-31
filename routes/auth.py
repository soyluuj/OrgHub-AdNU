from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        success, message = AuthService.register(
            request.form["fullname"],
            request.form["email"],
            request.form["password"],
            request.form.get("role", "student")
        )
        flash(message)
        if success:
            return redirect(url_for("auth.login"))
    return render_template("auth/register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = AuthService.login(request.form["email"], request.form["password"])
        if user:
            session["user_id"] = user.user_id
            session["user_name"] = user.full_name
            session["role"] = user.role
            return redirect(url_for("home.index"))
        flash("Invalid email or password.")
    return render_template("auth/login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home.index"))