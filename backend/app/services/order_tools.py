"""Tools the LLM may call. Nothing here places an order: draft_order only prepares one,
and the customer must press Confirm in the UI (POST /api/chat/confirm-order)."""
from difflib import get_close_matches
from flask import session
from google.genai import types
from ..models import Product, Order

S = types.Schema
DECLARATIONS = [
    types.FunctionDeclaration(
        name="draft_order",
        description=("Prepare an order when the customer explicitly asks to buy or order products. It does NOT place the order: "
                     "the customer must press the Confirm button. Use product names from the catalog."),
        parameters=S(type="OBJECT", required=["items"], properties={"items": S(type="ARRAY", items=S(
            type="OBJECT", required=["product_name"],
            properties={"product_name": S(type="STRING"), "quantity": S(type="INTEGER")}))})),
    types.FunctionDeclaration(name="cancel_order_draft", description="Discard the pending order draft if the customer changes their mind."),
    types.FunctionDeclaration(name="my_orders", description="List the logged-in customer's recent orders and their status."),
]

class Toolbox:
    declarations = DECLARATIONS
    def __init__(self, uid):
        self.uid, self.action = uid, None   
    def run(self, name, args):
        fns = {"draft_order": self.draft_order, "cancel_order_draft": self.cancel_order_draft, "my_orders": self.my_orders}
        if name not in fns: return {"error": "Unknown tool"}
        if not self.uid:
            self.action = {"type": "login"}
            return {"error": "Customer is not logged in. Tell them to log in first, then ask again."}
        try: return fns[name](**args)
        except Exception as e: return {"error": f"Tool failed: {e}"}

    def draft_order(self, items=()):
        catalog = {p.name.lower(): p for p in Product.query.all()}
        lines, problems = [], []
        for it in list(items)[:10]:
            asked = str(it.get("product_name", ""))
            qty = max(1, min(int(it.get("quantity") or 1), 10))
            m = get_close_matches(asked.lower(), catalog, n=1, cutoff=0.6)
            if not m: problems.append(f"No product matching '{asked}'"); continue
            p = catalog[m[0]]
            if p.stock < qty: problems.append(f"{p.name}: only {p.stock} in stock"); continue
            lines.append({"product_id": p.id, "name": p.name, "qty": qty, "price": p.price, "image": p.image or ""})
        if not lines: return {"error": "; ".join(problems) or "No items given"}
        session["draft"] = [{"product_id": l["product_id"], "qty": l["qty"]} for l in lines]
        total = sum(l["qty"] * l["price"] for l in lines)
        self.action = {"type": "confirm_order", "items": lines, "total": total}
        return {"status": "awaiting_customer_confirmation_button", "items": lines, "total": total, "problems": problems}

    def cancel_order_draft(self):
        session.pop("draft", None); self.action = None
        return {"status": "draft_discarded"}

    def my_orders(self):
        rows = Order.query.filter_by(user_id=self.uid).order_by(Order.id.desc()).limit(5).all()
        return {"orders": [o.to_dict() for o in rows]}
