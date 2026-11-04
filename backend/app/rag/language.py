
from flask import current_app
from .embeddings import client, with_retry

LANGUAGES = {"en": "English", "sw": "Kiswahili", "luo": "Dholuo", "ki": "Gĩkũyũ"}
LOW_RESOURCE = {"luo", "ki"} 

def rule(lang):
    if lang == "en":
        return "Reply in English."
    name = LANGUAGES[lang]
    r = f"The customer writes in {name}. Reply in {name}."
    if lang in LOW_RESOURCE:
        r += (" Use short, simple sentences. Keep product names, prices, numbers and order numbers exactly as given. "
              "If you are not sure of a word, use the English or Kiswahili word instead of inventing one. "
              "The customer may mix in English or Kiswahili; that is fine.")
    return r

def to_english(text, lang):
    """English rendering of the question, used only for knowledge-base retrieval."""
    if lang not in LOW_RESOURCE:
        return text
    try:
        r = with_retry(lambda: client().models.generate_content(
            model=current_app.config["GEN_MODEL"],
            contents=f"Translate this {LANGUAGES[lang]} customer message into English. Output only the translation:\n{text}"))
        return (r.text or text).strip()
    except Exception:
        return text
