# VoiceBanker Mock Database

This directory contains JSON mock databases for local development and testing. These files are loaded and managed by `backend/temp_learn/actions/banking_db.py`.

## Database Files

### 1. **accounts.json**
Stores customer account information.

```json
{
  "accounts": [
    {
      "account_number": "9876543210",
      "account_holder": "Arjun Kumar",
      "account_type": "Savings|Current",
      "balance": 50000.00,
      "ifsc_code": "SBIN0001234",
      "branch": "Mumbai Main Branch",
      "created_at": "2023-05-15T10:30:00Z",
      "status": "active"
    }
  ]
}
```

**Fields:**
- `account_number` - Unique 10-digit account identifier
- `account_holder` - Full name of account owner
- `account_type` - Type of account (Savings/Current/Business)
- `balance` - Current account balance in INR
- `ifsc_code` - Indian Financial System Code
- `branch` - Bank branch name
- `created_at` - Account creation timestamp
- `status` - Account status (active/inactive/suspended)

**Current Data:** 3 sample accounts with varying balances

---

### 2. **transactions.json**
Stores all account transactions (credits/debits).

```json
{
  "transactions": [
    {
      "transaction_id": "TXN20251101001",
      "account_number": "9876543210",
      "date": "2025-11-10T14:30:00Z",
      "type": "credit|debit",
      "amount": 5000.00,
      "recipient": "Salary Deposit",
      "description": "Monthly salary credit",
      "status": "completed|pending|failed"
    }
  ]
}
```

**Fields:**
- `transaction_id` - Unique transaction identifier (format: TXNYYYYMMDDnnn)
- `account_number` - Associated account
- `date` - Transaction timestamp
- `type` - credit (incoming) or debit (outgoing)
- `amount` - Transaction amount in INR
- `recipient` - Recipient name or business
- `description` - Transaction description (salary, bill payment, transfer, etc.)
- `status` - Transaction status

**Current Data:** 10 sample transactions across 3 accounts

---

### 3. **loans.json**
Stores active loan information.

```json
{
  "loans": [
    {
      "loan_id": "LN00001234",
      "account_number": "9876543210",
      "loan_type": "Personal Loan|Home Loan|Business Loan|Auto Loan",
      "principal": 200000.00,
      "current_balance": 150000.00,
      "interest_rate": 10.5,
      "tenure": 60,
      "emi": 4244.00,
      "start_date": "2023-06-01T00:00:00Z",
      "next_emi_date": "2025-12-01T00:00:00Z",
      "status": "active|closed|defaulted",
      "emi_paid": 18
    }
  ]
}
```

**Fields:**
- `loan_id` - Unique loan identifier
- `account_number` - Associated account
- `loan_type` - Type of loan
- `principal` - Original loan amount
- `current_balance` - Remaining balance
- `interest_rate` - Annual interest rate (%)
- `tenure` - Loan tenure in months
- `emi` - Equated Monthly Installment amount
- `start_date` - Loan start date
- `next_emi_date` - Next EMI due date
- `status` - Loan status
- `emi_paid` - Number of EMIs paid

**Current Data:** 4 sample loans with different types and EMI amounts

---

### 4. **alerts.json**
Stores billing alerts and reminders.

```json
{
  "alerts": [
    {
      "alert_id": "ALT0001",
      "account_number": "9876543210",
      "bill_type": "electricity|water|mobile|credit_card|business_tax|vehicle_tax|broadband",
      "amount": 2500.00,
      "due_date": "2025-11-20T23:59:59Z",
      "issued_date": "2025-11-01T00:00:00Z",
      "provider": "Mumbai Electricity Board",
      "status": "pending|paid|overdue",
      "days_to_due": 6
    }
  ]
}
```

**Fields:**
- `alert_id` - Unique alert identifier
- `account_number` - Associated account
- `bill_type` - Type of bill (utility, tax, subscription, etc.)
- `amount` - Bill amount in INR
- `due_date` - Payment due date
- `issued_date` - Bill issued date
- `provider` - Service provider name
- `status` - Payment status
- `days_to_due` - Days remaining until due date

**Current Data:** 8 sample bills with different due dates and providers

---

### 5. **biometrics.json**
Stores voice biometric data for authentication.

```json
{
  "biometrics": [
    {
      "account_number": "9876543210",
      "user_id": "user_arjun_001",
      "embedding_hash": "sha256_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1",
      "enrollment_date": "2023-06-01T10:30:00Z",
      "confidence_threshold": 0.75,
      "is_enrolled": true,
      "enrollment_samples": 5,
      "last_verification": "2025-11-14T09:15:00Z",
      "verification_success_count": 42,
      "verification_fail_count": 2
    }
  ]
}
```

**Fields:**
- `account_number` - Associated account
- `user_id` - Unique user identifier
- `embedding_hash` - SHA256 hash of voice embedding (never raw audio)
- `enrollment_date` - When voice was enrolled
- `confidence_threshold` - Minimum confidence for verification (0.75 = 75%)
- `is_enrolled` - Whether user has completed voice enrollment
- `enrollment_samples` - Number of samples used for enrollment
- `last_verification` - Timestamp of last successful verification
- `verification_success_count` - Total successful verifications
- `verification_fail_count` - Total failed verification attempts

**Current Data:** 3 sample users with complete voice biometric enrollment

**Security Note:** Embeddings are stored as SHA256 hashes. Raw audio embeddings are never stored, transmitted, or logged.

---

## Usage in Code

### Automatic Loading
When the Rasa action server starts, `banking_db.py` automatically:
1. Checks if mock database files exist in `db/`
2. Loads them into session-based JSON storage
3. Initializes missing accounts with mock data
4. Returns data for Rasa action queries

### Example from banking_db.py
```python
def get_account(account_number: str = None) -> dict:
    """Get account by account_number or create mock if not found."""
    db_file = ORIGIN_DB_PATH / "accounts.json"
    
    if not db_file.exists():
        prepare_db_file(db_file)
    
    with open(db_file, 'r') as f:
        data = json.load(f)
    
    # Find account or create mock
    for account in data.get('accounts', []):
        if account['account_number'] == account_number:
            return account
    
    # Create mock account if not found
    return create_mock_account(account_number)
```

---

## Development Workflow

### 1. Reset Database to Initial State
```bash
cd backend/temp_learn
# Copy from original files (if using git)
git checkout db/*.json

# Or manually delete and let banking_db.py regenerate:
rm db/*.json
# Next action call will regenerate with mock data
```

### 2. Add Sample Data
Edit any JSON file directly to add accounts, transactions, loans, or alerts:
```bash
nano db/accounts.json
# Add new account object to "accounts" array
```

### 3. Test with Specific Scenarios
Modify database to create test cases:
- **Low balance**: Set balance < 10000 to test transfer rejection
- **Overdue bills**: Set past due_date to test alert prioritization
- **No loans**: Remove all loan entries to test "no loans found" flow
- **Multiple accounts**: Add more accounts to test account selection

### 4. Clear Session Data
```bash
# Session data is stored in /tmp/ by default
# Clear before testing fresh scenarios:
rm -rf /tmp/voicebanker_session_*
```

---

## Data Characteristics

### Accounts
- **Account Numbers**: 9876543210-9876543212 (ICICI format)
- **Balance Range**: ₹50,000 - ₹150,000
- **Branches**: Mumbai, Delhi, Bangalore

### Transactions
- **Recent**: Last 10 days (Nov 1-10, 2025)
- **Mix**: Credits (salary, interest) and debits (bills, transfers, shopping)
- **Pattern**: Realistic spending (bills, transfers, salary)

### Loans
- **Types**: Personal, Home, Business, Auto
- **Amount Range**: ₹200,000 - ₹2,000,000
- **EMI Range**: ₹4,244 - ₹14,500
- **Status**: All active with varying payment history

### Bills
- **Types**: Utilities (electricity, water), subscriptions (mobile, broadband), taxes, credit card
- **Amount Range**: ₹499 - ₹25,000
- **Due Dates**: Spread across Nov 15 - Dec 15, 2025

### Voice Biometrics
- **Enrollment Status**: All 3 users enrolled and verified
- **Confidence Threshold**: 0.75 (75%)
- **Verification History**: 31-87 successful verifications per user

---

## For Production Use

**Do NOT use these files in production.** Instead:

1. **Replace with PostgreSQL**
   ```bash
   # Modify banking_db.py to use SQLAlchemy + PostgreSQL
   from sqlalchemy import create_engine
   engine = create_engine(os.getenv('DATABASE_URL'))
   ```

2. **Migrate to Real Database**
   - Use `alembic` for schema migrations
   - Seed production data from migration scripts
   - Implement proper backup/restore procedures

3. **Security Hardening**
   - Never store raw biometric embeddings
   - Encrypt sensitive data at rest
   - Use parametrized queries to prevent SQL injection
   - Implement row-level security for multi-tenancy

4. **Compliance**
   - Implement audit logging for all transactions
   - GDPR: Add data retention policies
   - PCI-DSS: For credit card data handling
   - RBI: Account reconciliation and reporting

---

## Testing Integration

### With Rasa NLU
```bash
# Terminal 1: Start Rasa action server
rasa run actions

# Terminal 2: Test with Rasa shell
rasa shell
# Say: "What's my balance?"
# Will call action_check_balance → reads accounts.json
```

### With FastAPI
```bash
# Terminal 1: Start FastAPI backend
cd backend
uvicorn main:app --reload

# Terminal 2: Test endpoint
curl -X POST http://localhost:8000/api/account/9876543210/balance
```

### With pytest
```bash
# Run unit tests
pytest tests/test_actions.py -v

# Test specific action
pytest tests/test_actions.py::test_check_balance -v
```

---

## Schema Versioning

Current Database Schema Version: **1.0**

**Fields Added in Future Versions:**
- Account: `overdraft_limit`, `credit_score`, `credit_limit`
- Transactions: `category`, `merchant_id`, `receipt_url`
- Loans: `foreclosure_charge`, `prepayment_penalty`
- Alerts: `notification_sent_date`, `reminder_count`, `auto_pay_enabled`
- Biometrics: `liveness_score`, `speech_quality`, `microphone_quality`

---

**Last Updated:** November 14, 2025

**Maintained By:** VoiceBanker Development Team

See `ACTIONS_README.md` and `banking_db.py` for implementation details.
