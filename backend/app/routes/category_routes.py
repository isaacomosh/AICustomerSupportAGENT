from flask import Blueprint, jsonify
from ..models import Category

bp = Blueprint("categories", __name__, url_prefix="/api/categories")

@bp.get("")
def categories():
    return jsonify([c.to_dict() for c in Category.query.all()])
