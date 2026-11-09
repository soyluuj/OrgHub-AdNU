import json
from flask import Blueprint, render_template, request, session, redirect, url_for
from models import Organization, Announcement, PageView
from extensions import db
from sqlalchemy import desc, or_

home_bp = Blueprint("home", __name__)

# NEW: Landing Page Route
@home_bp.route("/landing")
def landing():
    # If they are already logged in, send them straight to the hub
    if session.get("user_id"):
        return redirect(url_for("home.index"))
    return render_template("landing.html")

@home_bp.route("/")
def index():
    if not session.get("user_id"):
        return redirect(url_for("home.landing"))

    search_query = request.args.get("search", "").strip()
    category_filter = request.args.get("category", "").strip()

    # Base Queries
    orgs_query = Organization.query
    announcements_query = Announcement.query

    # Apply Search Filter
    if search_query:
        # Search Orgs by Name
        orgs_query = orgs_query.filter(Organization.name.ilike(f"%{search_query}%"))
        
        # Search Announcements by Title, Content, OR Org Name
        announcements_query = announcements_query.filter(
            or_(
                Announcement.title.ilike(f"%{search_query}%"),
                Announcement.content.ilike(f"%{search_query}%"),
                Announcement.organization.has(Organization.name.ilike(f"%{search_query}%")) # <-- NEW: Search by Org Name
            )
        )

    # Apply Category Filter
    if category_filter and category_filter in ['curricular', 'extra-curricular', 'department']:
        orgs_query = orgs_query.filter_by(category=category_filter)
        # If filtering by category, hide announcements from other categories
        announcements_query = announcements_query.join(Organization).filter(Organization.category == category_filter)

    # Fetch Results
    recent_announcements = announcements_query.order_by(desc(Announcement.created_at)).limit(10).all()
    filtered_orgs = orgs_query.all()

    # Group orgs by category for the template
    categorized_orgs = {
        "curricular": [],
        "extra-curricular": [],
        "department": []
    }
    for org in filtered_orgs:
        if org.category in categorized_orgs:
            categorized_orgs[org.category].append(org)

    return render_template(
        "home.html", 
        recent_announcements=recent_announcements,
        categorized_orgs=categorized_orgs,
        search_query=search_query,
        category_filter=category_filter
    )

@home_bp.route("/org/<slug>")
def public_org_page(slug):
    org = Organization.query.filter_by(slug=slug).first_or_404()
    
    # 1. Parse the links JSON safely
    org_links = []
    if org.links:
        try:
            org_links = json.loads(org.links)
        except:
            pass

    # 2. Handle merch search
    merch_search = request.args.get("merch_search", "").strip()
    
    if merch_search:
        filtered_products = [p for p in org.products if merch_search.lower() in p.name.lower() or (p.description and merch_search.lower() in p.description.lower())]
    else:
        filtered_products = org.products

    # 3. Track view
    new_view = PageView(org_id=org.id)
    db.session.add(new_view)
    db.session.commit()
    
    # 4. Pass BOTH org_links and filtered_products to the template
    return render_template(
        "public/org_page.html", 
        org=org, 
        org_links=org_links, 
        products=filtered_products, 
        merch_search=merch_search
    )