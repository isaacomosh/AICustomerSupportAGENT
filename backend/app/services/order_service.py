from ..extensions import db
from ..models import CartItem, Order, OrderItem, Product
from ..rag import vector_store
from . import cart_service

def _place(uid, lines):  # lines: [(Product, qty)]
    for p, q in lines:
        if p.stock < q: return None, f"{p.name} is out of stock"
    order = Order(user_id=uid, total=sum(p.price * q for p, q in lines))
    for p, q in lines:
        p.stock -= q
        order.items.append(OrderItem(name=p.name, quantity=q, price=p.price))
    db.session.add(order); db.session.commit()
    vector_store.state["stale"] = True  # stock changed: re-sync product chunks on next question
    return order, None

def place_order(uid):
    items = CartItem.query.filter_by(user_id=uid).all()
    if not items: return None, "Cart is empty"
    order, err = _place(uid, [(i.product, i.quantity) for i in items])
    if order: cart_service.clear(uid)
    return order, err

def place_from_draft(uid, draft):
    lines = [(db.session.get(Product, d["product_id"]), d["qty"]) for d in draft]
    lines = [l for l in lines if l[0]]
    return _place(uid, lines) if lines else (None, "Nothing to order")

def user_orders(uid):
    return [o.to_dict() for o in Order.query.filter_by(user_id=uid).order_by(Order.id.desc())]
