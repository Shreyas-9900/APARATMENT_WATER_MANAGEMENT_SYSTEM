import sqlite3

def get_db():
    conn = sqlite3.connect("billing.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    # USERS TABLE (ADMIN + TENANT)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT,
        flat_id INTEGER
    )
    """)

    # FLATS TABLE (WITH TOKEN 🔑)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS flats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flat_number TEXT,
        tenant_name TEXT,
        meter_number TEXT,
        token TEXT UNIQUE,
        token_used INTEGER DEFAULT 0
    )
    """)

    # BILLS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS bills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flat_id INTEGER,
        month TEXT,
        prev_reading INTEGER,
        curr_reading INTEGER,
        units INTEGER,
        amount INTEGER,
        paid INTEGER DEFAULT 0
    )
    """)


    conn.commit()
    conn.close()
