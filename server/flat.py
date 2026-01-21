@flat_bp.route("/create", methods=["POST"])
def create_flat():
    data = request.json

    token = secrets.token_hex(4).upper()

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO flats (flat_number, token, token_used)
        VALUES (?, ?, ?)
    """, (data["flat_number"], token, 0))

    conn.commit()
    conn.close()

    return {
        "message": "Flat created successfully 🔥",
        "token": token
    }
