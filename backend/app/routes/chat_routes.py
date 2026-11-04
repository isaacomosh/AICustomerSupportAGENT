import uuid
from flask import Blueprint, request, session, jsonify
from ..services import chatbot_service, order_service
from ..rag import knowledge_base
from ..rag.language import LANGUAGES
from ..utils.helpers import login_required

bp = Blueprint("chat", __name__, url_prefix="/api/chat")

@bp.post("")
def chat():
    d = request.get_json() or {}
    msg = (d.get("message") or "").strip()
    if not msg: return jsonify(error="Message required"), 400
    lang = d.get("lang") if d.get("lang") in LANGUAGES else "en"
    sid = session.setdefault("chat_id", uuid.uuid4().hex)
    answer, action, cards = chatbot_service.reply(sid, msg[:1000], lang, session.get("user_id"))
    return jsonify(reply=answer, action=action, products=cards)

@bp.post("/confirm-order")  # the only place a chat-drafted order becomes a real order
@login_required
def confirm_order():
    draft = session.pop("draft", None)
    if not draft: return jsonify(error="No pending order"), 400
    order, err = order_service.place_from_draft(session["user_id"], draft)
    return (jsonify(order.to_dict()), 201) if order else (jsonify(error=err), 400)

@bp.post("/cancel-order")
def cancel_order():
    session.pop("draft", None); return jsonify(ok=True)

@bp.post("/reindex")  # call after editing knowledge_base/ files or products
def reindex():
    return jsonify(chunks=knowledge_base.build_index())
