from flask import request, jsonify
from db import connect_db
import datetime
import jwt

# 🔐 Use the same secret key as in auth.py
SECRET_KEY = "your_secret_key"

# ✅ Token verification function
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def register_routes(app):

    # 🔓 Public route: Get inventory (optional to protect)
    @app.route("/inventory", methods=["GET"])
    def get_inventory():
        token = request.headers.get("Authorization")
        if not token or not verify_token(token):
            return jsonify({"error": "Unauthorized"}), 401

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory")
        items = cursor.fetchall()
        conn.close()
        return jsonify(items)

    # 🔒 Protected route: Add item
    @app.route("/inventory", methods=["POST"])
    def add_item():
        token = request.headers.get("Authorization")
        if not token or not verify_token(token):
            return jsonify({"error": "Unauthorized"}), 401

        data = request.get_json()
        item_name = data.get("item_name")
        quantity = data.get("quantity")

        if not item_name or not isinstance(quantity, int):
            return jsonify({"error": "Invalid input"}), 400

        last_updated = datetime.datetime.now().strftime("%Y-%m-%d")

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO inventory (item_name, quantity, last_updated) VALUES (?, ?, ?)",
            (item_name, quantity, last_updated)
        )
        conn.commit()
        conn.close()

        return jsonify({"message": "Item added successfully"})
