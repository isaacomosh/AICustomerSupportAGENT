from ..extensions import db
from ..models import ChatMessage
from ..rag.retriever import retrieve
from ..rag.generator import generate
from ..rag import language
from .order_tools import Toolbox
from . import product_service

def reply(session_id, message, lang="en", uid=None):
    """Returns (answer, action, product_cards). action is None, a confirm_order card, or a login prompt."""
    past = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.id.desc()).limit(6).all()
    history = [(m.role, m.content) for m in reversed(past)]
    toolbox = Toolbox(uid)
    try:
        contexts = retrieve(language.to_english(message, lang))
        answer = generate(message, contexts, history, lang, toolbox)
    except Exception as e:
        print("chatbot error:", e)
        return "Sorry, I can't reach the assistant right now. Please try again shortly.", None, []
    db.session.add_all([ChatMessage(session_id=session_id, role="user", content=message),
                        ChatMessage(session_id=session_id, role="model", content=answer)])
    db.session.commit()
    cards = [] if toolbox.action else product_service.mentioned(answer)  # the order card replaces product cards
    return answer, toolbox.action, cards
