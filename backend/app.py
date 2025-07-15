from flask import Flask
from flask_cors import CORS
from db import create_table
from routes import register_routes  
# ✅ import your API routes
from auth import auth_bp

app = Flask(__name__)
CORS(app)

create_table()            # ✅ create DB table on startup
register_routes(app)      # ✅ register all API endpoints
app.register_blueprint(auth_bp)
@app.route("/")
def home():
    return "Inventory API is running!"

if __name__ == "__main__":
    app.run(debug=True)
