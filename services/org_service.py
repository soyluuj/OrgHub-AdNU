from extensions import db
from models import Organization, Announcement
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