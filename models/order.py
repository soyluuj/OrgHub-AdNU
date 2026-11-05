from extensions import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    org_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    
    status = db.Column(db.String(50), default='Pending') # 'Pending', 'Ready for Pickup', 'Completed', 'Cancelled'
    pickup_instructions = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    student = db.relationship('User', backref='orders')
    organization = db.relationship('Organization', backref='orders')
    items = db.relationship('OrderItem', backref='order', cascade="all, delete-orphan")

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price_at_time = db.Column(db.Numeric(10, 2), nullable=False) # Save price in case it changes later
    
    # Relationships
    product = db.relationship('Product', backref='order_items')