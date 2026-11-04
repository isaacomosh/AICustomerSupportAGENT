import os, hashlib
from ..models import Product
from .embeddings import embed
from . import vector_store as vs

KB_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "knowledge_base")

def _item(text, source):
    return hashlib.sha1(text.encode()).hexdigest(), text, {"source": source}

def load_chunks():
    items = {}
    for folder in ("products", "faqs", "policies", "delivery", "payments"):
        d = os.path.join(KB_DIR, folder)
        for f in sorted(os.listdir(d)):
            if f.endswith((".md", ".txt")):
                for para in open(os.path.join(d, f), encoding="utf-8").read().split("\n\n"):
                    if para.strip():
                        i = _item(f"[{folder}] {para.strip()}", folder); items[i[0]] = i
    for p in Product.query.all():  # live product data straight from the database
        stock = f"{p.stock} in stock" if p.stock else "out of stock"
        i = _item(f"[product] {p.name} ({p.category.name}) - ${p.price:.2f}, {stock}. {p.description}", "product")
        items[i[0]] = i
    return list(items.values())

def build_index():
    """Incremental sync: embeds only new/changed chunks, removes chunks that no longer exist."""
    items = load_chunks()
    have = vs.existing_ids()
    new = [i for i in items if i[0] not in have]
    if new:
        vs.upsert([i[0] for i in new], [i[1] for i in new], embed([i[1] for i in new]), [i[2] for i in new])
    vs.prune([i[0] for i in items])
    vs.state["stale"] = False
    return len(items)
