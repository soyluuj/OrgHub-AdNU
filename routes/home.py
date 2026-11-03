from flask import Blueprint, render_template, abort
from models import Organization, PageView
from extensions import db

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def index():
    orgs = Organization.query.all()
    return render_template("home.html", orgs=orgs)

@home_bp.route("/org/<slug>")
def public_org_page(slug):
    org = Organization.query.filter_by(slug=slug).first_or_404()
    
    # Optional: Track a page view for analytics!
    new_view = PageView(org_id=org.id)
    db.session.add(new_view)
    db.session.commit()
    
    return render_template("public/org_page.html", org=org)