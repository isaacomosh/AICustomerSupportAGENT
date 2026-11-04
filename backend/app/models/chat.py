from datetime import datetime
from ..extensions import db

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(64), index=True)
    role = db.Column(db.String(10))  # user | model
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
