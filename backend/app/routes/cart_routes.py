from flask import Blueprint, request, session, jsonify
from ..services import cart_service
from ..utils.helpers import login_required

bp = Blueprint("cart", __name__, url_prefix="/api/cart")

@bp.get("")
@login_required
def get(): return jsonify(cart_service.get_cart(session["user_id"]))

@bp.post("")
@login_required
def add():
    d = request.get_json() or {}
    cart = cart_service.add_item(session["user_id"], d.get("product_id"), int(d.get("quantity", 1)))
    return (jsonify(cart), 200) if cart else (jsonify(error="Product not found"), 404)

@bp.delete("/<int:pid>")
@login_required
def remove(pid): return jsonify(cart_service.remove_item(session["user_id"], pid))
