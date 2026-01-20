from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from database import init_db

app = Flask(__name__)
app.secret_key = "very-simple-secret-key"

CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)

# Import routes
from auth import auth_bp
from flat import flat_bp
from bill import bill_bp


app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(flat_bp, url_prefix="/api/flats")
app.register_blueprint(bill_bp, url_prefix="/api/bills")

# Init DB
init_db()

@app.route("/")
def home():
    return {"message": "Smart Water Billing Backend Running 🔥"}

if __name__ == "__main__":
    app.run(debug=True)
