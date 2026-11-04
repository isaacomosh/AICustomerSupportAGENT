from ..models import Product, Category

def list_products(slug=None):
    q = Product.query
    if slug and slug != "all":
        q = q.join(Category).filter(Category.slug == slug)
    return [p.to_dict() for p in q.all()]

def mentioned(text, limit=3):
    """Products whose names appear in `text`, in order of appearance (used for chat product cards)."""
    low, hits = (text or "").lower(), []
    for p in Product.query.all():
        i = low.find(p.name.lower())
        if i >= 0: hits.append((i, p))
    return [p.to_dict() for _, p in sorted(hits, key=lambda h: h[0])[:limit]]
