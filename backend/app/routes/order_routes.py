from flask import Blueprint, session, jsonify
from ..services import order_service
from ..utils.helpers import login_required

bp = Blueprint("orders", __name__, url_prefix="/api/orders")

@bp.post("")
@login_required
def place():
    order, err = order_service.place_order(session["user_id"])
    return (jsonify(order.to_dict()), 201) if order else (jsonify(error=err), 400)

@bp.get("")
@login_required
def mine(): return jsonify(order_service.user_orders(session["user_id"]))
