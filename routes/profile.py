from flask import Blueprint, render_template, session, redirect, url_for
from utils.decorators import login_required
from models import User, Order

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")

@profile_bp.route("/")
@login_required
def index():
    user = User.query.get(session["user_id"])
    
    # If an Org Admin somehow lands here, send them to their dashboard
    if user.role == 'org_admin':
        return redirect(url_for('dashboard.index'))
        
    # Get order stats for the student
    orders = Order.query.filter_by(student_id=user.user_id).order_by(Order.created_at.desc()).all()
    total_orders = len(orders)
    pending_orders = len([o for o in orders if o.status in ['Pending', 'Ready for Pickup']])
    
    return render_template(
        "profile/index.html", 
        user=user, 
        total_orders=total_orders, 
        pending_orders=pending_orders
    )