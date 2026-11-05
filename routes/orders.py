from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.decorators import login_required
from services.order_service import OrderService
from models import Order

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")

@orders_bp.route("/checkout/<int:product_id>", methods=["POST"])
@login_required
def checkout(product_id):
    # If an org admin tries to order, you can block it here if you want.
    success, result = OrderService.create_order(
        student_id=session["user_id"],
        product_id=product_id,
        quantity=int(request.form.get("quantity", 1))
    )
    
    if success:
        flash("Order placed successfully! The org has been notified.")
        return redirect(url_for('orders.my_orders'))
    else:
        flash(result)
        return redirect(url_for('home.index'))

@orders_bp.route("/my-orders")
@login_required
def my_orders():
    # Fetch orders for the logged-in student
    student_orders = Order.query.filter_by(student_id=session["user_id"]).order_by(Order.created_at.desc()).all()
    return render_template("orders/my_orders.html", orders=student_orders)

