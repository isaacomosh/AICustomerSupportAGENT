from flask import Blueprint, request, session, jsonify
from ..extensions import db
from ..models import User
from ..utils.validators import valid_email, valid_password

bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@bp.post("/register")
def register():
    d = request.get_json() or {}
    if not valid_email(d.get("email")) or not valid_password(d.get("password")):
        return jsonify(error="Valid email and a password of 6+ characters required"), 400
    if User.query.filter_by(email=d["email"]).first():
        return jsonify(error="Email already registered"), 409
    u = User(name=d.get("name", ""), email=d["email"]); u.set_password(d["password"])
    db.session.add(u); db.session.commit()
    session["user_id"] = u.id
    return jsonify(id=u.id, name=u.name), 201

@bp.post("/login")
def login():
    d = request.get_json() or {}
    u = User.query.filter_by(email=d.get("email")).first()
    if not u or not u.check_password(d.get("password", "")):
        return jsonify(error="Wrong email or password"), 401
    session["user_id"] = u.id
    return jsonify(id=u.id, name=u.name)

@bp.post("/logout")
def logout():
    session.clear(); return jsonify(ok=True)

@bp.get("/me")
def me():
    from ..models import User
    u = db.session.get(User, session.get("user_id")) if "user_id" in session else None
    return jsonify(user={"id": u.id, "name": u.name or u.email} if u else None)
