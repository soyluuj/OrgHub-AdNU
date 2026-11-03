from extensions import db
from models import Organization, Announcement, Product
import re

class OrgService:
    @staticmethod
    def create_profile(user_id, name, category):
        slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
        if Organization.query.filter_by(slug=slug).first():
            slug = f"{slug}-{user_id}"

        org = Organization(user_id=user_id, name=name, slug=slug, category=category)
        db.session.add(org)
        db.session.commit()
        return org

    @staticmethod
    def update_profile(org, form, logo_file, cover_file):
        from services.upload_service import UploadService
        
        org.name = form.get("name")
        org.bio = form.get("bio")
        
        # Update images if new ones were uploaded
        if logo_file:
            new_logo = UploadService.save_image(logo_file)
            if new_logo: org.logo_url = new_logo
            
        if cover_file:
            new_cover = UploadService.save_image(cover_file)
            if new_cover: org.cover_image_url = new_cover
            
        db.session.commit()
        return org

    @staticmethod
    def create_announcement(org_id, title, content):
        announcement = Announcement(org_id=org_id, title=title, content=content)
        db.session.add(announcement)
        db.session.commit()
        return announcement

    @staticmethod
    def delete_announcement(announcement_id, org_id):
        # Ensure the announcement belongs to this org before deleting
        announcement = Announcement.query.filter_by(id=announcement_id, org_id=org_id).first()
        if announcement:
            db.session.delete(announcement)
            db.session.commit()
            return True
        return False

    @staticmethod
    def create_product(org_id, form, image_file):
        from services.upload_service import UploadService
        
        image_url = UploadService.save_image(image_file)
        
        product = Product(
            org_id=org_id,
            name=form.get("name"),
            description=form.get("description"),
            price=float(form.get("price")),
            stock=int(form.get("stock")),
            image_url=image_url
        )
        db.session.add(product)
        db.session.commit()
        return product

    @staticmethod
    def update_product(product_id, org_id, form, image_file):
        from services.upload_service import UploadService
        
        # Security: Ensure the product belongs to this org
        product = Product.query.filter_by(id=product_id, org_id=org_id).first()
        if not product:
            return False
            
        product.name = form.get("name")
        product.description = form.get("description")
        product.price = float(form.get("price"))
        product.stock = int(form.get("stock"))
        
        if image_file and image_file.filename != "":
            new_image = UploadService.save_image(image_file)
            if new_image:
                product.image_url = new_image
                
        db.session.commit()
        return True

    @staticmethod
    def delete_product(product_id, org_id):
        product = Product.query.filter_by(id=product_id, org_id=org_id).first()
        if product:
            db.session.delete(product)
            db.session.commit()
            return True
        return False