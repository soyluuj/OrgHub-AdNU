import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.decorators import org_admin_required
from services.org_service import OrgService
from services.order_service import OrderService
from models import User, Product, Announcement, PageView, Order

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/")
@org_admin_required
def index():
    user = User.query.get(session["user_id"])
    if not user.organization:
        return redirect(url_for('dashboard.setup_org'))

    org = user.organization
    # Get some quick stats for the overview
    total_announcements = len(org.announcements)
    total_merch = len(org.products)
    total_views = PageView.query.filter_by(org_id=org.id).count()

    return render_template(
        "dashboard/index.html", 
        org=org, 
        total_announcements=total_announcements,
        total_merch=total_merch,
        total_views=total_views
    )

@dashboard_bp.route("/announcements")
@org_admin_required
def announcements():
    user = User.query.get(session["user_id"])
    org = user.organization
    
    # Sort announcements newest first
    posts = sorted(org.announcements, key=lambda x: x.created_at, reverse=True)
    return render_template("dashboard/announcements.html", org=org, announcements=posts)

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
            request.files.get("image")
        )
        flash("Announcement posted!")
    else:
        flash("Title and content are required.")
        
    return redirect(url_for('dashboard.announcements')) # Redirect to the new page

@dashboard_bp.route("/announcements/<int:announcement_id>/delete", methods=["POST"])
@org_admin_required
def delete_announcement(announcement_id):
    user = User.query.get(session["user_id"])
    if OrgService.delete_announcement(announcement_id, user.organization.id):
        flash("Announcement deleted.")
    else:
        flash("Announcement not found.")
        
    return redirect(url_for('dashboard.announcements'))

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

@dashboard_bp.route("/orders")
@org_admin_required
def orders():
    user = User.query.get(session["user_id"])
    
    # Safety check in case the org profile isn't set up yet
    if not user.organization:
        return redirect(url_for('dashboard.setup_org'))
        
    current_org_id = user.organization.id
    
    # Active orders (anything not completed)
    active_orders = Order.query.filter(
        Order.org_id == current_org_id, 
        Order.status != 'Completed'
    ).order_by(Order.created_at.desc()).all()
    
    # Completed orders (History)
    completed_orders = Order.query.filter(
        Order.org_id == current_org_id, 
        Order.status == 'Completed'
    ).order_by(Order.created_at.desc()).all()
    
    return render_template(
        "dashboard/orders.html", 
        org=user.organization, 
        active_orders=active_orders, 
        completed_orders=completed_orders
    )

@dashboard_bp.route("/orders/<int:order_id>/update", methods=["POST"])
@org_admin_required
def update_order(order_id):
    user = User.query.get(session["user_id"])
    new_status = request.form.get("status")
    instructions = request.form.get("instructions")
    
    OrderService.update_order_status(order_id, user.organization.id, new_status, instructions)
    flash("Order updated!")
    return redirect(url_for('dashboard.orders'))

@dashboard_bp.route("/merch/<int:product_id>/delete", methods=["POST"])
@org_admin_required
def delete_merch(product_id):
    user = User.query.get(session["user_id"])
    if OrgService.delete_product(product_id, user.organization.id):
        flash("Merch deleted.")
    return redirect(url_for('dashboard.merch'))

@dashboard_bp.app_context_processor
def inject_pending_orders():
    if session.get('role') == 'org_admin' and 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user and user.organization:
            count = Order.query.filter_by(org_id=user.organization.id, status='Pending').count()
            return dict(pending_orders_count=count)
    return dict(pending_orders_count=0)