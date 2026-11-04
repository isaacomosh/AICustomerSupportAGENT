from ..extensions import db
from ..models import CartItem, Product

def get_cart(uid):
    items = CartItem.query.filter_by(user_id=uid).all()
    return {"items": [{"product_id": i.product_id, "name": i.product.name, "qty": i.quantity,
                       "price": i.product.price, "image": i.product.image or ""} for i in items],
            "total": sum(i.quantity * i.product.price for i in items)}

def add_item(uid, pid, qty=1):
    if not db.session.get(Product, pid): return None
    it = CartItem.query.filter_by(user_id=uid, product_id=pid).first()
    if it: it.quantity += qty
    else: db.session.add(CartItem(user_id=uid, product_id=pid, quantity=qty))
    db.session.commit()
    return get_cart(uid)

def clear(uid):
    CartItem.query.filter_by(user_id=uid).delete(); db.session.commit()

def remove_item(uid, pid):
    CartItem.query.filter_by(user_id=uid, product_id=pid).delete(); db.session.commit()
    return get_cart(uid)
