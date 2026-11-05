from extensions import db
from models import Order, OrderItem, Product

class OrderService:
    @staticmethod
    def create_order(student_id, product_id, quantity=1):
        product = Product.query.get(product_id)
        if not product or product.stock < quantity:
            return False, "Item is out of stock or unavailable."

        # 1. Create the Order
        new_order = Order(
            student_id=student_id,
            org_id=product.org_id,
            status="Pending"
        )
        db.session.add(new_order)
        db.session.flush() # Flush to get the order.id before committing

        # 2. Create the Order Item
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=product.id,
            quantity=quantity,
            price_at_time=product.price
        )
        db.session.add(order_item)

        # 3. Deduct Stock
        product.stock -= quantity

        db.session.commit()
        return True, new_order

    @staticmethod
    def update_order_status(order_id, org_id, new_status, instructions=None):
        order = Order.query.filter_by(id=order_id, org_id=org_id).first()
        if order:
            order.status = new_status
            if instructions is not None:
                order.pickup_instructions = instructions
            db.session.commit()
            return True
        return False