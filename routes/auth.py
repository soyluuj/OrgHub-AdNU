from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)

from services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        success, message = AuthService.register(
            request.form["fullname"],
            request.form["email"],
            request.form["password"],
            request.form.get("id_number", ""),
        )
        # temp
        print ("REGISTER", success, message)

        flash(message)

        if success:
            return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        user = AuthService.login(
            request.form["email"],
            request.form["password"],
        )

        if user:

            session["user_id"] = user.user_id
            session["user_name"] = user.full_name
            session["user_email"] = user.email

            return redirect(url_for("home.home"))

        flash("Invalid email or password.")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home.home"))