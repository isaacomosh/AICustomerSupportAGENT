from ..extensions import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(40), unique=True, nullable=False)
    name = db.Column(db.String(60), nullable=False)
    products = db.relationship("Product", backref="category")
    def to_dict(self): return {"id": self.id, "slug": self.slug, "name": self.name}
