import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.decorators import org_admin_required
from services.org_service import OrgService
from models import User, Product

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/")
@org_admin_required
def index():
    user = User.query.get(session["user_id"])
    if not user.organization:
        return redirect(url_for('dashboard.setup_org'))
    
    # Sort announcements newest first for the dashboard
    announcements = sorted(user.organization.announcements, key=lambda x: x.created_at, reverse=True)
    return render_template("dashboard/index.html", org=user.organization, announcements=announcements)

@dashboard_bp.route("/setup", methods=["GET", "POST"])
@org_admin_required
def setup_org():
    user = User.query.get(session["user_id"])
    if user.organization:
        return redirect(url_for('dashboard.index'))

    if request.method == "POST":
        OrgService.create_profile(user.user_id, request.form.get("name"), request.form.get("category"))
        flash("Organization profile created!")
        return redirect(url_for('dashboard.index'))

    return render_template("dashboard/setup.html")

# --- NEW ROUTES BELOW ---

@dashboard_bp.route("/settings", methods=["GET", "POST"])
@org_admin_required
def settings():
    user = User.query.get(session["user_id"])
    org = user.organization

    if request.method == "POST":
        OrgService.update_profile(
            org, 
            request.form, 
            request.files.get("logo"), 
            request.files.get("cover")
        )
        flash("Profile updated successfully!")
        return redirect(url_for('dashboard.settings'))

    org_links = []
    if org.links:
        try:
            org_links = json.loads(org.links)
        except:
            pass

    return render_template("dashboard/settings.html", org=org, org_links=org_links)

@dashboard_bp.route("/announcements/create", methods=["POST"])
@org_admin_required
def create_announcement():
    user = User.query.get(session["user_id"])
    title = request.form.get("title")
    content = request.form.get("content")
    
    if title and content:
        OrgService.create_announcement(
            user.organization.id, 
            request.form, 
            request.files.get("image") # <--- Pass the uploaded image
        )
        flash("Announcement posted!")
    else:
        flash("Title and content are required.")
        
    return redirect(url_for('dashboard.index'))

@dashboard_bp.route("/announcements/<int:announcement_id>/delete", methods=["POST"])
@org_admin_required
def delete_announcement(announcement_id):
    user = User.query.get(session["user_id"])
    if OrgService.delete_announcement(announcement_id, user.organization.id):
        flash("Announcement deleted.")
    else:
        flash("Announcement not found.")
        
    return redirect(url_for('dashboard.index'))

@dashboard_bp.route("/merch")
@org_admin_required
def merch():
    user = User.query.get(session["user_id"])
    products = user.organization.products
    return render_template("dashboard/merch.html", org=user.organization, products=products)

@dashboard_bp.route("/merch/add", methods=["GET", "POST"])
@org_admin_required
def add_merch():
    user = User.query.get(session["user_id"])
    
    if request.method == "POST":
        OrgService.create_product(
            user.organization.id, 
            request.form, 
            request.files.get("image")
        )
        flash("Merch added successfully!")
        return redirect(url_for('dashboard.merch'))
        
    return render_template("dashboard/merch_form.html", org=user.organization, product=None)

@dashboard_bp.route("/merch/<int:product_id>/edit", methods=["GET", "POST"])
@org_admin_required
def edit_merch(product_id):
    user = User.query.get(session["user_id"])
    product = Product.query.filter_by(id=product_id, org_id=user.organization.id).first_or_404()
    
    if request.method == "POST":
        success = OrgService.update_product(
            product_id, 
            user.organization.id, 
            request.form, 
            request.files.get("image")
        )
        if success:
            flash("Merch updated successfully!")
            return redirect(url_for('dashboard.merch'))
            
    return render_template("dashboard/merch_form.html", org=user.organization, product=product)

@dashboard_bp.route("/merch/<int:product_id>/delete", methods=["POST"])
@org_admin_required
def delete_merch(product_id):
    user = User.query.get(session["user_id"])
    if OrgService.delete_product(product_id, user.organization.id):
        flash("Merch deleted.")
    return redirect(url_for('dashboard.merch'))