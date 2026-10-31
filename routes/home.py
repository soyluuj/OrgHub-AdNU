from flask                      import Blueprint, render_template
from models                     import Item
from datetime                   import datetime, timedelta
from services.auction_service   import AuctionService
from flask                      import request

home_bp = Blueprint(
    "home",
    __name__
)


@home_bp.route("/")
def home():

    now = datetime.now()

    AuctionService.update_expired_auctions()

    ending_soon = (
        Item.query
        .filter(
            Item.status.in_(["available", "bidding"]),
            Item.auction_end >= now,
            Item.auction_end <= now + timedelta(hours=24)
        )
        .order_by(Item.auction_end.asc())
        .limit(5)
        .all()
    )
    search = request.args.get("search", "")

    query = Item.query.filter(
        Item.status != "cancelled"
    )

    if search:

        query = query.filter(
            Item.title.ilike(f"%{search}%")
        )

    items = (
        query
        .order_by(Item.created_at.desc())
        .all()
    )

    latest = (
        Item.query
        .filter(
            Item.status.in_(["available", "bidding"]),
            Item.auction_end > now
        )
        .order_by(Item.created_at.desc())
        .all()
    )

    
    
    return render_template(
        "home.html",
        items=latest,
        ending_soon=ending_soon,
        search=search
    )



