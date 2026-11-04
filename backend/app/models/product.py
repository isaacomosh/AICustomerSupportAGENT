from ..extensions import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, default="")
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    emoji = db.Column(db.String(8), default="")
    image = db.Column(db.String(200), default="")
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description, "price": self.price,
                "stock": self.stock, "image": self.image or "", "emoji": self.emoji, "category": self.category.slug}
