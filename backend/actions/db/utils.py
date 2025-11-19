# actions/db/utils.py

import re
from datetime import datetime


# ============================================================
# 1. FORMAT CURRENCY
# ============================================================
def format_inr(amount):
    """
    Format number into INR format.
    Example: 25000.5 → ₹25,000.50
    """
    try:
        return f"₹{float(amount):,.2f}"
    except:
        return str(amount)


# ============================================================
# 2. ACCOUNT NUMBER VALIDATION
# ============================================================
def is_valid_account_number(acc):
    """
    Checks if account number is:
    - numeric
    - 6 to 20 digits
    """
    if not acc:
        return False
    return bool(re.fullmatch(r"[0-9]{6,20}", acc))


# ============================================================
# 3. IFSC VALIDATION
# ============================================================
def is_valid_ifsc(ifsc):
    """
    Valid IFSC format:
    - 4 letters + 0 + 6 digits
    Example: HDFC0001234
    """
    if not ifsc:
        return False
    return bool(re.fullmatch(r"[A-Za-z]{4}0[0-9]{6}", ifsc))


# ============================================================
# 4. SAFE AMOUNT PARSING
# ============================================================
def safe_amount(value):
    """
    Convert amount to float safely.
    Return None if invalid.
    """
    try:
        amt = float(value)
        if amt > 0:
            return amt
        return None
    except:
        return None


# ============================================================
# 5. CLEAN USER INPUT
# ============================================================
def clean_text(text):
    """
    Remove unwanted characters, trim spaces.
    """
    if not text:
        return ""
    return text.strip().replace("\n", " ").replace("\t", " ")


# ============================================================
# 6. FORMAT TRANSACTION DATE
# ============================================================
def format_tx_date(dt):
    """
    Convert Postgres timestamp to a readable format.
    Example: 2025-01-22 14:55:31 → 22 Jan 2025, 2:55 PM
    """
    try:
        if isinstance(dt, datetime):
            return dt.strftime("%d %b %Y, %I:%M %p")
        return str(dt)
    except:
        return str(dt)


# ============================================================
# 7. STANDARDIZED ERROR MESSAGES
# ============================================================
def error_invalid_account():
    return "The provided account number seems incorrect. Please recheck."

def error_invalid_ifsc():
    return "The IFSC code entered is not valid."

def error_invalid_amount():
    return "Please provide a valid amount greater than zero."

def error_missing_info():
    return "Some required information is missing. Please provide the details again."


# ============================================================
# 8. USER FRIENDLY TRANSACTION FORMATTER
# ============================================================
def format_transaction_row(row):
    """
    Convert a transaction row into readable string.
    row expected format: (tx_date, type, amount, description)
    """
    try:
        date, tx_type, amount, desc = row
        return f"{format_tx_date(date)} | {tx_type} | {format_inr(amount)} | {desc}"
    except:
        return str(row)