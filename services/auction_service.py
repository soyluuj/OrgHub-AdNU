from datetime import datetime
import os, uuid
from extensions import db
from models import Item, ItemImage
from services.upload_service import UploadService

class AuctionService:

    @staticmethod
    def create_listing(form, files, seller_id):

        item = Item(

            seller_id=seller_id,
            category_id=int(form["category"]),
            title=form["title"],
            description=form["description"],
            item_condition=form["condition"],
            starting_price=float(form["price"]),
            auction_start=datetime.now(),
            auction_end=datetime.fromisoformat
            (
                form["auction_end"]
            ),
            donate_to_nstp=("donate" in form)
        )

        db.session.add(item)
        db.session.commit()
        
        saved_images = UploadService.save_images(files)
   
        for path in saved_images:

            image = ItemImage(
                item_id=item.item_id,  
                image_path=path
            )
                #i suspect that item_id is the problem, since that shit is shown as the pic
                
            db.session.add(image)
            db.session.commit()

        return item
    
    @staticmethod
    def update_expired_auctions():

        expired = Item.query.filter(

            Item.auction_end <= datetime.now(),
            Item.status != "sold"

        ).all()

        for item in expired:

            if item.bids:

                item.status = "sold"

            else:

                item.status = "cancelled"

        db.session.commit()        
        
    @staticmethod
    def delete_listing(item):

        db.session.delete(item)
        db.session.commit()
    
    @staticmethod
    def update_listing(item, form):

        item.category_id = int(form["category"])

        item.title = form["title"]

        item.description = form["description"]

        item.item_condition = form["condition"]

        item.starting_price = float(form["price"])

        item.auction_end = datetime.fromisoformat(
            form["auction_end"]
        )

        item.donate_to_nstp = (
            "donate" in form
        )

        db.session.commit()