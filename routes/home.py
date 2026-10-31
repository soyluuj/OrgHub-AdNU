from flask import Blueprint, render_template
from models import Organization

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def index():
    orgs = Organization.query.all()
    # For now, just show all orgs on the home page
    return render_template("home.html", orgs=orgs)