from flask import Blueprint, request
from flask_login import login_user, UserMixin
import bcrypt
from database import get_db

auth_bp = Blueprint("auth", __name__)

# Simple user class for flask-login
class User(UserMixin):
    def __init__(self, id, role):
        self.id = id
        self.role = role


# ---------------- CREATE ADMIN (ONE TIME) ----------------
@auth_bp.route("/create-admin", methods=["POST"])
def create_admin():
    data = request.json

    hashed = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        (data["username"], hashed.decode(), "admin")
    )

    conn.commit()
    conn.close()

    return {"message": "Admin created successfully 🔥"}


# ---------------- LOGIN (ADMIN + TENANT) ----------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username = ?", (data["username"],))
    user = cur.fetchone()

    conn.close()

    if not user:
        return {"error": "User not found"}, 404

    if not bcrypt.checkpw(data["password"].encode(), user["password"].encode()):
        return {"error": "Wrong password"}, 401

    login_user(User(user["id"], user["role"]))

    return {
        "message": "Login successful 🔥",
        "role": user["role"]
    }


# ---------------- TENANT REGISTER WITH TOKEN 🔑 ----------------
@auth_bp.route("/tenant-register", methods=["POST"])
def tenant_register():
    data = request.json

    conn = get_db()
    cur = conn.cursor()

    # Check token
    cur.execute(
        "SELECT * FROM flats WHERE token = ? AND token_used = 0",
        (data["token"],)
    )
    flat = cur.fetchone()

    if not flat:
        return {"error": "Invalid or already used token ❌"}, 400

    hashed = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())

    # Create tenant
    cur.execute(
        "INSERT INTO users (username, password, role, flat_id) VALUES (?, ?, ?, ?)",
        (data["username"], hashed.decode(), "tenant", flat["id"])
    )

    # Mark token as used 🔒
    cur.execute(
        "UPDATE flats SET token_used = 1 WHERE id = ?",
        (flat["id"],)
    )

    conn.commit()
    conn.close()

    return {"message": "Tenant registered & linked to flat 🔥"}
