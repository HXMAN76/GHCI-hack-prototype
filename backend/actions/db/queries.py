# actions/db/queries.py
# SQLite-safe banking queries for Rasa actions

from .connection import get_conn, release_conn
from datetime import datetime


# --------------------------------------------------------
# Get account balance
# --------------------------------------------------------
def get_balance(user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT balance FROM accounts WHERE user_id=?", (user_id,))
    row = cur.fetchone()

    release_conn(conn)
    return row["balance"] if row else None


# --------------------------------------------------------
# Get last 5 transactions
# --------------------------------------------------------
def get_transactions(user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT tx_date, tx_type, amount, description
        FROM transactions
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT 5
    """, (user_id,))

    rows = cur.fetchall()
    release_conn(conn)

    return rows


# --------------------------------------------------------
# Transfer money securely (sender → recipient)
# --------------------------------------------------------
def transfer_money(sender_id, recipient_account, amount, recipient_ifsc=None):
    conn = get_conn()
    if conn is None:
        return False, "Database connection error."

    cur = conn.cursor()

    # Debug
    print("\n--- DEBUG TRANSFER ---")
    print("sender:", sender_id)
    print("recipient_account:", recipient_account)
    print("amount:", amount)
    print("------------------------\n")

    # 1️⃣ Validate sender
    cur.execute("SELECT balance FROM accounts WHERE user_id=?", (sender_id,))
    row_sender = cur.fetchone()

    if not row_sender:
        release_conn(conn)
        return False, "Your account was not found."

    sender_balance = row_sender["balance"]

    if sender_balance < amount:
        release_conn(conn)
        return False, "You do not have enough balance."

    # 2️⃣ Validate recipient by account number and IFSC (if provided)
    if recipient_ifsc:
        # Compare IFSC case-insensitively by uppercasing stored value
        cur.execute("""
            SELECT user_id, account_number, ifsc_code
            FROM accounts
            WHERE account_number=? AND UPPER(ifsc_code)=?
        """, (str(recipient_account), str(recipient_ifsc).upper()))
    else:
        cur.execute("""
            SELECT user_id, account_number, ifsc_code
            FROM accounts
            WHERE account_number=?
        """, (str(recipient_account),))
    row_rec = cur.fetchone()

    if not row_rec:
        release_conn(conn)
        return False, "Recipient account does not exist."

    receiver_id = row_rec["user_id"]

    # 3️⃣ Perform transfer
    try:
        cur.execute("UPDATE accounts SET balance = balance - ? WHERE user_id=?", (amount, sender_id))
        cur.execute("UPDATE accounts SET balance = balance + ? WHERE account_number=?", (amount, recipient_account))

        # 4️⃣ Add transaction logs
        now = datetime.now().isoformat()

        cur.execute("""
            INSERT INTO transactions (user_id, tx_date, tx_type, amount, description)
            VALUES (?, ?, ?, ?, ?)
        """, (sender_id, now, "debit", amount, f"Transferred to {recipient_account} / IFSC: {recipient_ifsc or 'N/A'}"))

        cur.execute("""
            INSERT INTO transactions (user_id, tx_date, tx_type, amount, description)
            VALUES (?, ?, ?, ?, ?)
        """, (receiver_id, now, "credit", amount, f"Received from {sender_id} / Acc: {recipient_account}"))

        conn.commit()
    except Exception as e:
        # Ensure connection is released on error and return a friendly message
        try:
            conn.rollback()
        except Exception:
            pass
        release_conn(conn)
        return False, f"Transfer failed: {str(e)}"

    release_conn(conn)
    return True, "Transfer successful."


# --------------------------------------------------------
# Block card
# --------------------------------------------------------
def block_card(user_id, card_type):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE accounts
        SET card_status='blocked'
        WHERE user_id=? AND card_type=?
    """, (user_id, card_type))

    conn.commit()
    release_conn(conn)
    return True


# --------------------------------------------------------
# Report fraud
# --------------------------------------------------------
def report_fraud(user_id, description):
    conn = get_conn()
    cur = conn.cursor()

    now = datetime.now().isoformat()

    cur.execute("""
        INSERT INTO fraud_reports (user_id, description, created_at)
        VALUES (?, ?, ?)
    """, (user_id, description, now))

    conn.commit()
    release_conn(conn)
    return True
