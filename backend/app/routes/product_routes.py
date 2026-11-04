from flask import Blueprint, request, jsonify
from ..services import product_service

bp = Blueprint("products", __name__, url_prefix="/api/products")

@bp.get("")
def products():
    return jsonify(product_service.list_products(request.args.get("category")))

@bp.get("/<int:pid>")
def one(pid):
    from ..extensions import db
    from ..models import Product
    p = db.session.get(Product, pid)
    return (jsonify(p.to_dict()), 200) if p else (jsonify(error="Product not found"), 404)
