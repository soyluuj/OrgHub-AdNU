from models import Category, Item, Bid
from services.bid_service import BidService
from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
)

from utils.auth import login_required
from models import Category
from services.auction_service import AuctionService

auction_bp = Blueprint("auction", __name__)


@auction_bp.route("/create-listing", methods=["GET", "POST"])
@login_required
def create_listing():

    if request.method == "POST":
        

        AuctionService.create_listing(
            request.form,
            request.files.getlist("images"),
            session["user_id"]
        )

        flash("Auction created successfully!")

        return redirect(url_for("dashboard.dashboard"))

    categories = Category.query.order_by(
        Category.category_name
    ).all()

    return render_template(
        "create-listing.html",
        categories=categories
    )
    
@auction_bp.route("/auction/<int:item_id>")
def auction_detail(item_id):

    AuctionService.update_expired_auctions()
    item = Item.query.get_or_404(item_id)

    bids = (
        Bid.query
        .filter_by  (item_id = item.item_id)
        .order_by   (Bid.bid_amount.desc ())
        .all        ()
        )

    for bid in bids:
        print(
            bid.bid_id,
            bid.item_id,
            bid.bidder_id,
            bid.bid_amount
        )

    return render_template(
        "auction-detail.html",
        item    =item,
        bids    =bids,
        now     =datetime.now()
    )

    
@auction_bp.route(
    "/auction/<int:item_id>/bid",
    methods=["POST"]
    )

@login_required
def place_bid(item_id):

    amount = float(request.form["bid"])

    success, message = BidService.place_bid(

        item_id,
        session["user_id"],
        amount

    )

    flash(message)

    return redirect(
        url_for(
            "auction.auction_detail",
            item_id=item_id
        )
    )
    
@auction_bp.route(
    "/listing/<int:item_id>/delete",
    methods=["POST"]
)
@login_required
def delete_listing(item_id):

    item = Item.query.get_or_404(item_id)

    if item.seller_id != session["user_id"]:

        flash("You cannot delete another user's listing.")

        return redirect(
            url_for(
                "auction.auction_detail",
                item_id=item_id
            )
        )

    AuctionService.delete_listing(item)

    flash("Listing deleted successfully.")

    return redirect(
        url_for("dashboard.my_listings")
    )
    
@auction_bp.route(
    "/listing/<int:item_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def edit_listing(item_id):

    item = Item.query.get_or_404(item_id)

    if item.seller_id != session["user_id"]:

        flash("You cannot edit another user's listing.")

        return redirect(
            url_for(
                "auction.auction_detail",
                item_id=item_id
            )
        )

    categories = Category.query.order_by(
        Category.category_name
    ).all()

    if request.method == "POST":

        AuctionService.update_listing(
            item,
            request.form
        )

        flash("Listing updated successfully.")

        return redirect(
            url_for("dashboard.my_listings")
        )

    return render_template(
        "create-listing.html",
        item=item,
        categories=categories,
        editing=True
    )