# seed.py — Create DB tables + Insert 5 demo users
# Run ONCE before starting Rasa:
#   python3 seed.py

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "database.sqlite3")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

def run_schema():
    """Creates all required tables from schema.sql"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print("📌 Loading schema.sql ...")
    with open(SCHEMA_PATH, "r") as f:
        schema_sql = f.read()
        cur.executescript(schema_sql)

    conn.commit()
    conn.close()
    print("✅ Tables created / verified successfully!\n")


def seed_data():
    """Insert 5 test users + accounts + sample transactions"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print("📌 Seeding demo users...")

    # ------------------------------------------------------------
    # 5 DEMO USERS (username + password + name)
    # ------------------------------------------------------------
    users = [
        ("demo",     "1234", "Demo User"),
        ("rahul",    "1111", "Rahul Mehta"),
        ("priya",    "2222", "Priya Sharma"),
        ("arjun",    "3333", "Arjun Verma"),
        ("sneha",    "4444", "Sneha Nair"),
    ]

    for username, password, name in users:
        cur.execute("""
            INSERT OR IGNORE INTO users (username, password, name)
            VALUES (?, ?, ?)
        """, (username, password, name))

    conn.commit()

    # ------------------------------------------------------------
    # FETCH user IDs (auto increment)
    # ------------------------------------------------------------
    cur.execute("SELECT id, username FROM users")
    user_map = {u[1]: u[0] for u in cur.fetchall()}

    print("   ➤ Users inserted:", user_map)

    # ------------------------------------------------------------
    # Insert accounts for each user
    # ------------------------------------------------------------
    accounts = [
        (user_map["demo"],  "100001", "IFSC0001", 25000, "debit"),
        (user_map["rahul"], "100002", "IFSC0002", 32000, "debit"),
        (user_map["priya"], "100003", "IFSC0003", 41000, "credit"),
        (user_map["arjun"], "100004", "IFSC0004", 50000, "debit"),
        (user_map["sneha"], "100005", "IFSC0005", 28000, "credit"),
    ]

    print("\n📌 Seeding accounts...")

    for user_id, acc_no, ifsc, balance, card in accounts:
        cur.execute("""
            INSERT OR IGNORE INTO accounts (user_id, account_number, ifsc_code, balance, card_type)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, acc_no, ifsc, balance, card))

    conn.commit()

    # ------------------------------------------------------------
    # OPTIONAL: Insert sample transactions for 'demo' user
    # ------------------------------------------------------------
    print("\n📌 Inserting sample transactions for 'demo'...")

    demo_uid = user_map["demo"]

    sample_txn = [
        (demo_uid, "2025-01-01", "debit",   500,  "Grocery purchase"),
        (demo_uid, "2025-01-05", "credit", 2000, "Salary credit"),
        (demo_uid, "2025-01-07", "debit",   800, "Mobile recharge"),
        (demo_uid, "2025-01-10", "debit",  1500, "Online shopping"),
        (demo_uid, "2025-01-12", "credit",  500, "Refund received"),
    ]

    for u, date, tx_type, amt, desc in sample_txn:
        cur.execute("""
            INSERT INTO transactions (user_id, tx_date, tx_type, amount, description)
            VALUES (?, ?, ?, ?, ?)
        """, (u, date, tx_type, amt, desc))

    conn.commit()
    conn.close()

    print("\n✅ Seeding completed successfully!\n")


if __name__ == "__main__":
    print("=======================================")
    print("   RASA VOICEBANKER DB INITIALIZATION  ")
    print("=======================================\n")

    # 1. Create tables
    run_schema()

    # 2. Insert demo data
    seed_data()

    print("🎉 Database is ready to use!")
