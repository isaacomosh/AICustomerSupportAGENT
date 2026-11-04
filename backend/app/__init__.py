import os
from flask import Flask
from config import Config
from .extensions import db

def create_app(config=Config):
    app = Flask(__name__, static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend")), static_url_path="")
    app.config.from_object(config)
    db.init_app(app)
    from .routes import auth_routes, product_routes, category_routes, cart_routes, order_routes, chat_routes
    for m in (auth_routes, product_routes, category_routes, cart_routes, order_routes, chat_routes):
        app.register_blueprint(m.bp)
    with app.app_context():
        from . import models  # noqa: F401
        db.create_all()
        from .utils.helpers import seed
        seed()
    @app.get("/")
    def index():
        return app.send_static_file("index.html")
    return app
