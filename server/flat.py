from flask import Blueprint, request
from database import get_db
import secrets

flat_bp = Blueprint("flat", __name__)

# ---------------- CREATE FLAT (ADMIN) ----------------
@flat_bp.route("/create", methods=["POST"])
def create_flat():
    data = request.json

    # 🔑 Generate random token
    token = secrets.token_hex(4).upper()   # Example: A9F3K2XQ

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO flats (flat_number, tenant_name, meter_number, token)
        VALUES (?, ?, ?, ?)
    """, (data["flat_number"], data["tenant_name"], data["meter_number"], token))

    conn.commit()
    conn.close()

    return {
        "message": "Flat created successfully 🔥",
        "token": token
    }


# ---------------- LIST FLATS ----------------
@flat_bp.route("/", methods=["GET"])
def list_flats():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM flats")
    flats = cur.fetchall()

    conn.close()

    result = []

    for f in flats:
        result.append({
            "flat_number": f["flat_number"],
            "tenant_name": f["tenant_name"],
            "meter_number": f["meter_number"],
            "token": f["token"],
            "token_used": bool(f["token_used"])
        })

    return result
