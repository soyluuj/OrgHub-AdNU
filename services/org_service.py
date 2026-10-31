from extensions import db
from models import Organization
import re

class OrgService:
    @staticmethod
    def create_profile(user_id, name, category):
        # Create a URL-friendly slug (e.g., "Chess Club" -> "chess-club")
        slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
        
        # Ensure slug is unique
        existing_org = Organization.query.filter_by(slug=slug).first()
        if existing_org:
            slug = f"{slug}-{user_id}"

        new_org = Organization(
            user_id=user_id,
            name=name,
            slug=slug,
            category=category
        )
        db.session.add(new_org)
        db.session.commit()
        return new_org