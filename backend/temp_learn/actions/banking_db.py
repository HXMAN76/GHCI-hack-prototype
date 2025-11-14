"""
Banking Database and Models for VoiceBanker

Manages user data, transactions, and banking information.
Session-based storage for development/testing.
"""

import os
import shutil
import tempfile
import json
from typing import Any, List, Optional
from datetime import datetime
from pydantic import BaseModel

from rasa.nlu.utils import write_json_to_file
from rasa.shared.utils.io import read_json_file


# ==================== DATA MODELS ====================

class BankingAccount(BaseModel):
    """User banking account information"""
    account_number: str
    account_holder: str
    account_type: str  # savings, current, etc.
    balance: float
    ifsc_code: str
    branch: str


class Transaction(BaseModel):
    """Financial transaction record"""
    transaction_id: str
    date: str
    type: str  # debit, credit
    amount: float
    recipient: Optional[str] = None
    description: str
    status: str  # completed, pending, failed


class Loan(BaseModel):
    """Loan information"""
    loan_id: str
    loan_type: str  # home, personal, auto, etc.
    principal_amount: float
    current_balance: float
    interest_rate: float
    tenure_months: int
    emi: float
    status: str  # active, closed, defaulted


class BillingAlert(BaseModel):
    """Billing alerts and reminders"""
    alert_id: str
    bill_type: str
    amount: float
    due_date: str
    status: str  # pending, paid


class VoiceBiometric(BaseModel):
    """Stored voice biometric data"""
    user_id: str
    embedding_hash: str  # Hashed/obfuscated embedding
    enrollment_date: str
    last_verified: str
    confidence_threshold: float


# ==================== DATABASE PATH MANAGEMENT ====================

ORIGIN_DB_PATH = "db"
ACCOUNTS_DB = "accounts.json"
TRANSACTIONS_DB = "transactions.json"
LOANS_DB = "loans.json"
ALERTS_DB = "alerts.json"
BIOMETRICS_DB = "biometrics.json"


def get_session_db_path(session_id: str) -> str:
    """Get session-specific database directory"""
    tempdir = tempfile.gettempdir()
    project_name = "voicebanker"
    return os.path.join(tempdir, project_name, session_id)


def prepare_db_file(session_id: str, db: str) -> str:
    """Prepare database file for a session"""
    session_db_path = get_session_db_path(session_id)
    os.makedirs(session_db_path, exist_ok=True)
    destination_file = os.path.join(session_db_path, db)
    
    if not os.path.exists(destination_file):
        origin_file = os.path.join(ORIGIN_DB_PATH, db)
        if os.path.exists(origin_file):
            shutil.copy(origin_file, destination_file)
        else:
            # Create empty database
            write_json_to_file(destination_file, {})
    
    return destination_file


def read_db(session_id: str, db: str) -> Any:
    """Read database file"""
    db_file = prepare_db_file(session_id, db)
    try:
        return read_json_file(db_file)
    except:
        return {}


def write_db(session_id: str, db: str, data: Any) -> None:
    """Write to database file"""
    db_file = prepare_db_file(session_id, db)
    write_json_to_file(db_file, data)


# ==================== ACCOUNT OPERATIONS ====================

def get_account(session_id: str) -> Optional[BankingAccount]:
    """Retrieve user's banking account"""
    data = read_db(session_id, ACCOUNTS_DB)
    if isinstance(data, dict) and "account" in data:
        return BankingAccount(**data["account"])
    return None


def create_mock_account(session_id: str, account_holder: str = "User") -> BankingAccount:
    """Create a mock account for testing"""
    account = BankingAccount(
        account_number="9876543210",
        account_holder=account_holder,
        account_type="savings",
        balance=50000.00,
        ifsc_code="DEMO0000001",
        branch="Main Branch"
    )
    write_db(session_id, ACCOUNTS_DB, {"account": account.dict()})
    return account


def update_balance(session_id: str, amount: float, transaction_type: str) -> Optional[float]:
    """Update account balance"""
    account = get_account(session_id)
    if not account:
        account = create_mock_account(session_id)
    
    if transaction_type == "debit":
        if account.balance >= amount:
            account.balance -= amount
        else:
            return None  # Insufficient balance
    elif transaction_type == "credit":
        account.balance += amount
    
    write_db(session_id, ACCOUNTS_DB, {"account": account.dict()})
    return account.balance


# ==================== TRANSACTION OPERATIONS ====================

def get_transactions(session_id: str, limit: int = 10) -> List[Transaction]:
    """Get recent transactions"""
    data = read_db(session_id, TRANSACTIONS_DB)
    transactions = data.get("transactions", [])
    return [Transaction(**t) for t in transactions[-limit:]]


def add_transaction(session_id: str, transaction: Transaction) -> None:
    """Add new transaction"""
    data = read_db(session_id, TRANSACTIONS_DB)
    if "transactions" not in data:
        data["transactions"] = []
    data["transactions"].append(transaction.dict())
    write_db(session_id, TRANSACTIONS_DB, data)


def create_transaction(
    session_id: str,
    amount: float,
    recipient: str,
    transaction_type: str = "transfer"
) -> Transaction:
    """Create a new transaction record"""
    transaction = Transaction(
        transaction_id=f"TXN{int(datetime.now().timestamp())}",
        date=datetime.now().isoformat(),
        type="debit",
        amount=amount,
        recipient=recipient,
        description=f"{transaction_type.capitalize()} to {recipient}",
        status="completed"
    )
    add_transaction(session_id, transaction)
    return transaction


# ==================== LOAN OPERATIONS ====================

def get_loans(session_id: str) -> List[Loan]:
    """Get user's active loans"""
    data = read_db(session_id, LOANS_DB)
    loans = data.get("loans", [])
    return [Loan(**l) for l in loans]


def get_loan_info(session_id: str, loan_type: str = None) -> Optional[Loan]:
    """Get loan information"""
    loans = get_loans(session_id)
    
    if loan_type:
        for loan in loans:
            if loan.loan_type.lower() == loan_type.lower():
                return loan
    
    # Return first active loan
    for loan in loans:
        if loan.status == "active":
            return loan
    
    return loans[0] if loans else None


def create_mock_loan(session_id: str) -> Loan:
    """Create mock loan data"""
    loan = Loan(
        loan_id="LN00123456",
        loan_type="personal",
        principal_amount=500000.00,
        current_balance=350000.00,
        interest_rate=8.5,
        tenure_months=60,
        emi=10500.00,
        status="active"
    )
    data = read_db(session_id, LOANS_DB)
    data["loans"] = [loan.dict()]
    write_db(session_id, LOANS_DB, data)
    return loan


# ==================== BILLING OPERATIONS ====================

def get_alerts(session_id: str) -> List[BillingAlert]:
    """Get pending billing alerts"""
    data = read_db(session_id, ALERTS_DB)
    alerts = data.get("alerts", [])
    return [BillingAlert(**a) for a in alerts if a.get("status") == "pending"]


def create_mock_alerts(session_id: str) -> List[BillingAlert]:
    """Create mock billing alerts"""
    alerts = [
        BillingAlert(
            alert_id="ALT001",
            bill_type="electricity",
            amount=1200.00,
            due_date="2025-11-20",
            status="pending"
        ),
        BillingAlert(
            alert_id="ALT002",
            bill_type="phone",
            amount=599.00,
            due_date="2025-11-22",
            status="pending"
        ),
        BillingAlert(
            alert_id="ALT003",
            bill_type="broadband",
            amount=999.00,
            due_date="2025-11-25",
            status="pending"
        ),
    ]
    data = read_db(session_id, ALERTS_DB)
    data["alerts"] = [a.dict() for a in alerts]
    write_db(session_id, ALERTS_DB, data)
    return alerts


# ==================== VOICE BIOMETRIC OPERATIONS ====================

def get_biometric(session_id: str) -> Optional[VoiceBiometric]:
    """Get stored voice biometric"""
    data = read_db(session_id, BIOMETRICS_DB)
    if "biometric" in data:
        return VoiceBiometric(**data["biometric"])
    return None


def enroll_voice_biometric(session_id: str, embedding_hash: str) -> VoiceBiometric:
    """Enroll user's voice biometric"""
    biometric = VoiceBiometric(
        user_id=session_id,
        embedding_hash=embedding_hash,
        enrollment_date=datetime.now().isoformat(),
        last_verified=datetime.now().isoformat(),
        confidence_threshold=0.75
    )
    write_db(session_id, BIOMETRICS_DB, {"biometric": biometric.dict()})
    return biometric


def verify_voice_biometric(
    session_id: str,
    embedding_hash: str,
    confidence: float
) -> bool:
    """Verify voice biometric"""
    biometric = get_biometric(session_id)
    if not biometric:
        return False
    return confidence >= biometric.confidence_threshold
