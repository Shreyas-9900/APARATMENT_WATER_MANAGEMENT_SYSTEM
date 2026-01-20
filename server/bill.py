from flask import Blueprint, request
from database import get_db

bill_bp = Blueprint("bill", __name__)

RATE_PER_UNIT = 10   # ₹10 per unit (you can change later)


# ---------------- CREATE BILL (ADMIN ENTERS READING) ----------------
@bill_bp.route("/create", methods=["POST"])
def create_bill():
    data = request.json

    flat_id = data["flat_id"]
    month = data["month"]
    prev = int(data["prev_reading"])
    curr = int(data["curr_reading"])

    if curr < prev:
        return {"error": "Current reading cannot be less than previous ❌"}, 400

    # 🔥 AUTO CALCULATION
    units = curr - prev
    amount = units * RATE_PER_UNIT

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO bills (flat_id, month, prev_reading, curr_reading, units, amount)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (flat_id, month, prev, curr, units, amount))

    conn.commit()
    conn.close()

    return {
        "message": "Bill generated successfully 🔥",
        "units": units,
        "amount": amount
    }


# ---------------- VIEW ALL BILLS (ADMIN) ----------------
@bill_bp.route("/", methods=["GET"])
def all_bills():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT bills.*, flats.flat_number 
        FROM bills 
        JOIN flats ON bills.flat_id = flats.id
    """)

    rows = cur.fetchall()
    conn.close()

    result = []

    for b in rows:
        result.append({
            "bill_id": b["id"],
            "flat_number": b["flat_number"],
            "month": b["month"],
            "prev": b["prev_reading"],
            "curr": b["curr_reading"],
            "units": b["units"],
            "amount": b["amount"],
            "paid": bool(b["paid"])
        })

    return result


# ---------------- TENANT: VIEW MY BILLS ONLY ----------------
@bill_bp.route("/my/<int:flat_id>", methods=["GET"])
def my_bills(flat_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM bills WHERE flat_id = ?
    """, (flat_id,))

    rows = cur.fetchall()
    conn.close()

    result = []

    for b in rows:
        result.append({
            "bill_id": b["id"],
            "month": b["month"],
            "units": b["units"],
            "amount": b["amount"],
            "paid": bool(b["paid"])
        })

    return result


# ---------------- MARK BILL AS PAID (ADMIN) ----------------
@bill_bp.route("/pay/<int:bill_id>", methods=["POST"])
def mark_paid(bill_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE bills SET paid = 1 WHERE id = ?
    """, (bill_id,))

    conn.commit()
    conn.close()

    return {"message": "Bill marked as PAID ✅"}
