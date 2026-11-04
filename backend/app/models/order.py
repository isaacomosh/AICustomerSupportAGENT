from datetime import datetime
from ..extensions import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    total = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default="processing")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship("OrderItem", backref="order")
    def to_dict(self):
        return {"id": self.id, "total": self.total, "status": self.status,
                "items": [{"name": i.name, "qty": i.quantity, "price": i.price} for i in self.items]}

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    name = db.Column(db.String(120))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
