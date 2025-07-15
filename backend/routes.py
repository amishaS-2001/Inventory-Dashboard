import sqlite3
from flask import request, jsonify

USERS = {
    "admin": "admin123"
}

def register_routes(app):

    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json()
        if USERS.get(data["username"]) == data["password"]:
            return jsonify({"message": "success"})
        return jsonify({"error": "Invalid credentials"}), 401

    @app.route("/inventory", methods=["GET", "POST", "DELETE"])
    def inventory():
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                quantity INTEGER NOT NULL
            );
        ''')

        if request.method == "POST":
            data = request.get_json()
            cursor.execute("INSERT INTO inventory (item_name, quantity) VALUES (?, ?)",
                           (data["item_name"], data["quantity"]))
            conn.commit()
            conn.close()
            return jsonify({"message": "Item added"}), 201

        elif request.method == "DELETE":
            data = request.get_json()
            cursor.execute("DELETE FROM inventory WHERE id = ?", (data["id"],))
            conn.commit()
            conn.close()
            return jsonify({"message": "Item deleted"}), 200

        else:  # GET
            cursor.execute("SELECT * FROM inventory")
            items = cursor.fetchall()
            conn.close()
            return jsonify(items)
