from functools import wraps
from flask import session, jsonify

def login_required(f):
    @wraps(f)
    def wrapper(*a, **k):
        if "user_id" not in session:
            return jsonify(error="Log in to continue"), 401
        return f(*a, **k)
    return wrapper

IMG = "assets/images/products/"
IMAGES = {"PulseFit S2": "pulsefit-s2.jpg", "Orbit GPS Pro": "orbit-gps-pro.jpg", "Horizon VR One": "horizon-vr-one.jpg",
          "Horizon VR Air": "horizon-vr-air.jpg", "Grip Pro Controller": "grip-pro-controller.jpg",
          "Aurora Pad Controller": "aurora-pad-controller.jpg"}

def seed():
    from ..extensions import db
    from ..models import Category, Product
    if not Category.query.first():
        cats = {s: Category(slug=s, name=n) for s, n in
                [("smart-watch", "Smart-Watch"), ("vr-headsets", "VR-Headsets"), ("controllers", "Controllers")]}
        db.session.add_all(cats.values())
        rows = [
            ("PulseFit S2", "smart-watch", 199, 25, "", "AMOLED smartwatch, heart-rate and sleep tracking, 7-day battery, 5ATM water resistance."),
            ("Orbit GPS Pro", "smart-watch", 329, 12, "", "Rugged GPS watch with offline maps, 14-day battery and multi-sport modes."),
            ("Horizon VR One", "vr-headsets", 449, 8, "", "Standalone VR headset, 2K per eye, 120Hz, inside-out tracking, 128GB storage."),
            ("Horizon VR Air", "vr-headsets", 299, 0, "", "Lightweight PC-tethered VR headset with 90Hz display. Currently out of stock."),
            ("Grip Pro Controller", "controllers", 69, 40, "", "Ergonomic wireless gamepad with haptic triggers, 30-hour battery, works with PC and mobile."),
            ("Aurora Pad Controller", "controllers", 99, 15, "", "Wireless gamepad with a neon gradient shell, haptic triggers and 30-hour battery. Works with PC and mobile."),
        ]
        for n, c, p, s, e, d in rows:
            db.session.add(Product(name=n, price=p, stock=s, emoji=e, description=d, category=cats[c]))
        db.session.commit()
    _ensure_images()

def _ensure_images():
    """Upgrades older databases in place: adds the image column, renames the old demo controller, fills in photos."""
    from sqlalchemy import inspect, text
    from ..extensions import db
    from ..models import Product
    if "image" not in [c["name"] for c in inspect(db.engine).get_columns("product")]:
        db.session.execute(text("ALTER TABLE product ADD COLUMN image VARCHAR(200) DEFAULT ''")); db.session.commit()
    old = Product.query.filter_by(name="VR Motion Pair").first()
    if old:
        old.name = "Aurora Pad Controller"
        old.description = "Wireless gamepad with a neon gradient shell, haptic triggers and 30-hour battery. Works with PC and mobile."
    for p in Product.query.all():
        if not p.image and p.name in IMAGES: p.image = IMG + IMAGES[p.name]
    db.session.commit()
