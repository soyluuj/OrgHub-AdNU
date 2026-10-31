from extensions import db


class Item(db.Model):

    __tablename__ = "items"

    item_id = db.Column(
        db.Integer,
        primary_key=True
    )

    seller_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.category_id"),
        nullable=False
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    item_condition = db.Column(
        db.Enum(
            "new",
            "like_new",
            "used"
        ),
        nullable=False
    )

    starting_price = db.Column(
        db.Numeric(10,2),
        nullable=False
    )

    status = db.Column(
        db.Enum(
            "available",
            "bidding",
            "sold",
            "cancelled"
        ),
        default="available"
    )

    auction_start = db.Column(
        db.DateTime
    )

    auction_end = db.Column(
        db.DateTime
    )

    donate_to_nstp = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    seller = db.relationship(
        "User",
        backref="items"
    )

    category = db.relationship(
        "Category",
        back_populates="items"
    )

    images = db.relationship(
        "ItemImage",
        back_populates="item",
        cascade="all, delete-orphan"
    )
    bids = db.relationship(
    "Bid",
    back_populates="item",
    cascade="all, delete-orphan",
    order_by="Bid.bid_amount.desc()"
    )

    def __repr__(self):
        return f"<Item {self.title}>"
    