# Mock Database Summary

Created: November 14, 2025

## Files Overview

### ✅ **accounts.json** (3 accounts)
Sample customer accounts with realistic banking profiles:
- **Arjun Kumar** (9876543210): Savings, ₹50,000 balance
- **Priya Sharma** (9876543211): Current, ₹150,000 balance  
- **Rajesh Patel** (9876543212): Savings, ₹75,000.50 balance

### ✅ **transactions.json** (10 transactions)
Mixed transaction history across all accounts:
- Credits: Salary deposits, interest, freelance income
- Debits: Bills, transfers, shopping, insurance
- Date range: Oct 31 - Nov 10, 2025
- Status: All completed

### ✅ **loans.json** (4 active loans)
Diverse loan portfolio across different account holders:
- **Personal Loan**: ₹200K principal → ₹150K balance, ₹4,244 EMI
- **Home Loan**: ₹2M principal → ₹1.8M balance, ₹14,500 EMI
- **Business Loan**: ₹500K principal → ₹300K balance, ₹7,500 EMI
- **Auto Loan**: ₹600K principal → ₹450K balance, ₹11,250 EMI

### ✅ **alerts.json** (8 billing alerts)
Real-world bills with varying due dates:
- **Utilities**: Electricity, water, broadband
- **Subscriptions**: Mobile (Vodafone), credit card
- **Taxes**: Business tax, vehicle registration
- **Due dates**: Nov 15 - Dec 15, 2025
- **Amounts**: ₹499 - ₹25,000

### ✅ **biometrics.json** (3 voice profiles)
Enrolled voice biometric records:
- All users: Fully enrolled and verified
- Confidence threshold: 0.75 (75%)
- Success/failure counts: Realistic tracking
- Hash format: SHA256 (never raw embeddings)

### ✅ **contacts.json** (from template)
Pre-existing contact list (2 contacts):
- Joe (@JoeMyers)
- Mary (@MaryLu)

### ✅ **README.md** (800+ lines)
Comprehensive documentation covering:
- Schema definitions for each database file
- Field descriptions and valid values
- Usage in banking_db.py
- Development workflow (reset, add data, test, clear)
- Data characteristics and patterns
- Production migration guide
- Security considerations
- Schema versioning

---

## Quick Stats

| Database | Records | Size | Purpose |
|----------|---------|------|---------|
| accounts.json | 3 | ~600 bytes | Customer account data |
| transactions.json | 10 | ~2.5 KB | Transaction history |
| loans.json | 4 | ~1.5 KB | Active loan portfolio |
| alerts.json | 8 | ~2.0 KB | Billing alerts |
| biometrics.json | 3 | ~1.2 KB | Voice auth enrollment |
| contacts.json | 2 | ~100 bytes | Contact directory |
| **Total** | **30** | **~8 KB** | **Mock database** |

---

## Test Scenarios Supported

### ✅ Balance Inquiry
- Query account balance
- Test with multiple accounts
- Fallback to mock data creation

### ✅ Money Transfer
- Transfer from high balance account (Priya: ₹150K)
- Transfer to recipient "Rajesh Patel"
- Validation: Check for insufficient balance (Arjun: ₹50K)

### ✅ Transaction History
- View last 5 transactions
- Mixed credit/debit patterns
- Real merchant names and categories

### ✅ Loan Inquiry
- Check multiple loan types
- Display EMI and tenure information
- Filter by loan type (Personal, Home, Business, Auto)

### ✅ Billing Alerts
- View pending bills
- Check overdue status (bills < 5 days)
- Prioritize by due date
- Calculate total amount due (example: ₹50,298 total)

### ✅ Voice Biometric
- Enrollment verification (all 3 users enrolled)
- Confidence threshold testing (0.75)
- Success/fail rate tracking
- Multi-attempt handling

### ✅ OTP Verification
- Rate limiting test (max 3 attempts per 10 min)
- Expiry handling (10 minute window)
- Error scenarios (expired, incorrect)

### ✅ Account Information
- Retrieve full account profile
- Branch and IFSC code verification
- Account type display

### ✅ Help & Confirmation
- Display all available features
- Confirmation for high-value transfers
- Action detail formatting

---

## Integration Points

### With banking_db.py
```python
# All these functions now have data to work with:
get_account("9876543210")  # Returns Arjun's account
get_transactions(limit=5)   # Returns last 5 transactions
get_loans()                 # Returns all 4 loans
get_alerts()                # Returns all 8 pending bills
enroll_voice_biometric()    # Stores hashed embedding
verify_voice_biometric()    # Matches against hash
```

### With Rasa Actions
```python
# action_check_balance: Reads from accounts.json
# action_transfer_money: Reads/writes accounts.json + transactions.json
# action_view_transactions: Reads from transactions.json
# action_view_loan_info: Reads from loans.json
# action_check_alerts: Reads from alerts.json
# action_enroll_voice_biometric: Writes to biometrics.json
# action_verify_voice_biometric: Reads from biometrics.json
```

### With FastAPI
```python
# POST /api/account/balance - reads accounts.json
# POST /api/account/transfer - reads/writes transactions.json
# POST /api/account/history - reads transactions.json
# GET /api/account/{id}/loans - reads loans.json
```

---

## Development Workflow

### 1. Fresh Start
```bash
cd backend/temp_learn
# Delete session data (Rasa creates session files)
rm -rf /tmp/voicebanker_session_*

# Start Rasa action server (loads mock databases automatically)
rasa run actions
```

### 2. Test Specific Scenario
```bash
# Example: Test low balance rejection
nano db/accounts.json
# Change Arjun's balance to 2000.00
# Try transfer of 5000 → should fail

# Reset:
git checkout db/accounts.json
```

### 3. Add Production Data
```bash
# When ready for real data:
# 1. Create PostgreSQL container
# 2. Modify banking_db.py to use SQLAlchemy
# 3. Migrate mock data to database
# 4. Update connection string in .env
```

### 4. Clear Everything
```bash
# Reset mock databases to initial state
rm db/*.json
# Rasa will regenerate with defaults on next startup

# Or restore from git
git checkout db/
```

---

## Edge Cases Covered

| Edge Case | Database Record | Test Method |
|-----------|-----------------|-------------|
| Empty balance | Can modify Arjun's balance to 0 | Try transfer > 0 |
| Overdue bill | Change alert due_date to past | Run check_alerts |
| No transactions | Remove all from transactions.json | View history |
| No loans | Delete loans.json contents | Query loan_inquiry |
| Low confidence match | Adjust verification_fail_count | Test voice verify |
| OTP expiry | Generate, wait 10+ min, verify | Integration test |
| Multiple accounts | All 3 accounts available | Account selection |

---

## Data Quality Checklist

✅ **Consistency**
- All account_number references match across files
- Transaction amounts are reasonable (₹499-₹25,000)
- EMI amounts match loan calculations
- Balance >= 0 for all accounts

✅ **Realism**
- Transaction dates span 10 days (realistic frequency)
- Bill types match real-world payments
- EMI values match tenure and principal
- Interest rates within industry standards (7-10%)

✅ **Completeness**
- All required fields present in each record
- No null/undefined values (except optional fields)
- Dates in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
- IDs follow consistent naming (TXN*, ALT*, LN*, etc.)

✅ **Security**
- Biometric embeddings stored as SHA256 hashes
- No raw passwords or PINs
- No hardcoded secrets
- Test data clearly marked as mock

---

## Next Steps

1. **Rasa Integration**
   - Load mock databases when Rasa action server starts
   - Verify with: `rasa run actions` → check logs for successful JSON loading

2. **Unit Tests**
   - Create `tests/test_banking_db.py` to validate:
     - Account retrieval and updates
     - Transaction creation and filtering
     - Loan calculations
     - Alert prioritization
     - Biometric verification

3. **Dialogue Stories**
   - Create `data/flows/` with multi-turn flows using mock data
   - Example: "Check balance" → reads accounts.json

4. **Frontend Integration**
   - Build React components to display accounts, transactions, loans, alerts
   - Fetch from FastAPI endpoints powered by banking_db.py

5. **Production Migration**
   - Export mock data to PostgreSQL schema
   - Update banking_db.py to use SQLAlchemy ORM
   - Test with real database under load

---

**Status**: ✅ **Ready for Development**

All mock databases are populated with realistic test data covering:
- ✅ 3 diverse customer accounts
- ✅ 10 realistic transactions
- ✅ 4 active loans with varying tenures
- ✅ 8 pending bills with real providers
- ✅ 3 enrolled voice biometric profiles

**See Also:**
- `ACTIONS_README.md` - Action implementations
- `ACTIONS_INTEGRATION.md` - Rasa integration guide
- `banking_db.py` - Database operations code
- `README.md` - Comprehensive documentation

---

Generated: November 14, 2025  
For VoiceBanker Custom Actions Development
