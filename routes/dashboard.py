from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.decorators import org_admin_required
from services.org_service import OrgService
from models import Organization, User

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/")
@org_admin_required
def index():
    user = User.query.get(session["user_id"])
    
    # Check if they have created their org profile yet
    if not user.organization:
        return redirect(url_for('dashboard.setup_org'))
        
    return render_template("dashboard/index.html", org=user.organization)

@dashboard_bp.route("/setup", methods=["GET", "POST"])
@org_admin_required
def setup_org():
    user = User.query.get(session["user_id"])
    
    # If they already have an org, redirect to dashboard
    if user.organization:
        return redirect(url_for('dashboard.index'))

    if request.method == "POST":
        org_name = request.form.get("name")
        org_category = request.form.get("category")
        
        OrgService.create_profile(user.user_id, org_name, org_category)
        flash("Organization profile created!")
        return redirect(url_for('dashboard.index'))

    return render_template("dashboard/setup.html")