from extensions import db

class ItemImage(db.Model):

    __tablename__ = "item_images"

    image_id = db.Column(
        db.Integer,
        primary_key=True
    )

    item_id = db.Column(
        db.Integer,
        db.ForeignKey("items.item_id"),
        nullable=False
    )

    image_path = db.Column(
        db.String(255),
        nullable=False
    )

    item = db.relationship(
        "Item",
        back_populates="images"
    )

    def __repr__(self):
        return f"<ItemImage {self.image_path}>"