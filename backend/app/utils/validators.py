import re
def valid_email(e): return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", e or ""))
def valid_password(p): return bool(p) and len(p) >= 6
