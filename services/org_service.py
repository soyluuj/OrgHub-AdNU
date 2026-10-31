from extensions import db
from models import Organization
import re

class OrgService:
    @staticmethod
    def create_profile(user_id, name, category):
        # Create a URL slug (e.g., "Computer Society" -> "computer-society")
        slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
        
        if Organization.query.filter_by(slug=slug).first():
            slug = f"{slug}-{user_id}"

        org = Organization(user_id=user_id, name=name, slug=slug, category=category)
        db.session.add(org)
        db.session.commit()
        return org