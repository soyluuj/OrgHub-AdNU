from extensions import db
from datetime import datetime

class PageView(db.Model):
    __tablename__ = 'page_views'
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow)