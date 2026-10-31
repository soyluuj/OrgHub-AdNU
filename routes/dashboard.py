from flask import (
    Blueprint,
    render_template,
    session
)
from utils.auth     import login_required
from sqlalchemy     import func
from models         import Bid, Item


dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@dashboard_bp.route("/my-listings")
@login_required
def my_listings():

    items = (
        Item.query
        .filter_by(seller_id=session["user_id"])
        .order_by(Item.created_at.desc())
        .all()
    )

    return render_template(
        "my-listings.html",
        items=items
    )

@dashboard_bp.route("/my-bids")
@login_required
def my_bids():

    items = (
        Item.query
        .join(Bid)
        .filter(
            Bid.bidder_id == session["user_id"])
        .distinct()
        .all()
    )
    my_highest = {}

    for item in items:

        highest = (
            Bid.query
            .filter_by(
                item_id=item.item_id,
                bidder_id=session["user_id"]
            )
            .order_by(Bid.bid_amount.desc())
            .first()
        )

        my_highest[item.item_id] = highest

    return render_template(
        "my-bids.html",
        items=items,
        my_highest=my_highest
    )