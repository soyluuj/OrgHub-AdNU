from extensions import db
from models import Bid, Item
from datetime import datetime

class BidService:

    @staticmethod
    def place_bid(item_id, bidder_id, amount):

        item = Item.query.get_or_404(item_id)
        
        if datetime.now() >= item.auction_end:
            return False, "This auction has already ended." 

        highest_bid = max(
            [bid.bid_amount for bid in item.bids],
            default=item.starting_price
        )

        if bidder_id == item.seller_id:

            return False, "You cannot bid on your own listing."

        if amount <= highest_bid:

            return False, (
                f"Your bid must be higher than ₱{highest_bid:.2f}"
            )

        bid = Bid(

            item_id=item_id,
            bidder_id=bidder_id,
            bid_amount=amount

        )

        db.session.add(bid)
        db.session.commit()

        return True, "Bid placed successfully!"
