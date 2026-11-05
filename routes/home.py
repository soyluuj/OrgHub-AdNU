import json
from flask import Blueprint, render_template
from models import Organization, Announcement, PageView
from extensions import db
from sqlalchemy import desc

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def index():
    # Get latest 5 announcements for the feed
    recent_announcements = Announcement.query.order_by(desc(Announcement.created_at)).limit(5).all()
    
    # Get all orgs
    orgs = Organization.query.all()

    # Group orgs by category
    categorized_orgs = {
        "curricular": [],
        "extra-curricular": [],
        "department": []
    }
    for org in orgs:
        if org.category in categorized_orgs:
            categorized_orgs[org.category].append(org)

    return render_template(
        "home.html", 
        recent_announcements=recent_announcements,
        categorized_orgs=categorized_orgs
    )

@home_bp.route("/org/<slug>")
def public_org_page(slug):
    org = Organization.query.filter_by(slug=slug).first_or_404()
    
    new_view = PageView(org_id=org.id)
    db.session.add(new_view)
    db.session.commit()

    org_links = []
    if org.links:
        try:
            org_links = json.loads(org.links)
        except:
            pass
    
    return render_template("public/org_page.html", org=org, org_links=org_links)