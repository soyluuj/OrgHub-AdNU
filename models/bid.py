from extensions import db

class Bid(db.Model):

    __tablename__ = "bids"

    bid_id = db.Column(
        db.Integer,
        primary_key=True
    )

    item_id = db.Column(
        db.Integer,
        db.ForeignKey("items.item_id"),
        nullable=False
    )

    bidder_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable=False
    )

    bid_amount = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    bid_time = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    item = db.relationship(
        "Item",
        back_populates="bids"
    )

    bidder = db.relationship(
        "User",
        back_populates="bids"
    )

    def __repr__(self):

        return f"<Bid {self.bid_amount}>"