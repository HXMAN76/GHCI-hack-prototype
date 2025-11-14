# VoiceBanker Rasa Custom Actions

This directory contains all custom actions for the VoiceBanker voice banking assistant. Actions handle backend logic, database operations, and complex banking workflows.

## Overview

Custom actions in Rasa are Python functions that execute when triggered by intents. In VoiceBanker, they handle:
- Banking operations (balance checks, transfers, loan inquiries)
- User authentication (voice biometric, OTP verification)
- Data retrieval and transaction logging
- User confirmations and help

## Project Structure

```
actions/
├── __init__.py                      # Module initialization
├── banking_db.py                    # Database models and operations
├── check_balance.py                 # Balance inquiry action
├── transfer_money.py                # Money transfer action
├── view_transactions.py             # Transaction history action
├── view_loan_info.py                # Loan details action
├── check_alerts.py                  # Billing alerts action
├── account_info.py                  # Account information action
├── voice_biometric.py               # Voice authentication actions
├── otp_auth.py                      # OTP authentication actions
├── help_actions.py                  # Help and confirmation actions
├── db/                              # Database files (JSON)
│   ├── accounts.json
│   ├── transactions.json
│   ├── loans.json
│   ├── alerts.json
│   └── biometrics.json
└── README.md                        # This file
```

## Available Actions

### Banking Operations

#### 1. **action_check_balance**
**File:** `check_balance.py`  
**Triggers:** `check_balance` intent  
**Purpose:** Retrieve and display current account balance

**Input Slots:**
- None (uses session ID for user identification)

**Output Slots:**
- `balance`: Current balance amount
- `account_number`: User's account number
- `return_value`: "success" or "error"

**Example Flow:**
```
User: "What's my balance?"
→ Intent: check_balance
→ Action: action_check_balance
→ Response: "Your current account balance is ₹50,000.00"
```

---

#### 2. **action_transfer_money**
**File:** `transfer_money.py`  
**Triggers:** `transfer_money` intent  
**Purpose:** Transfer funds to a recipient with balance validation

**Input Slots:**
- `amount`: Transfer amount (required)
- `recipient`: Recipient name or account number (required)

**Output Slots:**
- `transfer_amount`: Amount transferred
- `transfer_recipient`: Recipient name
- `new_balance`: Balance after transfer
- `transaction_id`: Transaction reference ID
- `return_value`: "success", "insufficient_balance", "missing_data", or "error"

**Example Flow:**
```
User: "Transfer 5000 rupees to Raj"
→ Intent: transfer_money (with amount=5000, recipient=Raj)
→ Action: action_transfer_money
1. Validates amount and recipient
2. Checks balance sufficiency (₹50,000 >= ₹5,000 ✓)
3. Creates transaction record
4. Updates balance (₹50,000 - ₹5,000 = ₹45,000)
→ Response: "Transfer successful! ₹5,000.00 sent to Raj. 
           Your new balance is ₹45,000.00. TXN ID: TXN123456"
```

---

#### 3. **action_view_transaction_history**
**File:** `view_transactions.py`  
**Triggers:** `transaction_history` intent  
**Purpose:** Display recent transactions (last 5 by default)

**Input Slots:**
- None

**Output Slots:**
- `transaction_history`: Formatted history text
- `transaction_count`: Number of transactions
- `return_value`: "success" or "error"

**Example Response:**
```
Here are your recent transactions:

1. 2025-11-14 - Transfer to Raj
   Amount: ₹5,000.00 (DEBIT)
   Status: completed

2. 2025-11-13 - Salary Credit
   Amount: ₹50,000.00 (CREDIT)
   Status: completed
```

---

#### 4. **action_view_loan_info**
**File:** `view_loan_info.py`  
**Triggers:** `loan_inquiry` intent  
**Purpose:** Display loan details and status

**Input Slots:**
- `loan_type`: (Optional) Specific loan type (home, personal, auto, etc.)

**Output Slots:**
- `loan_id`: Loan identifier
- `loan_type`: Type of loan
- `loan_balance`: Outstanding amount
- `loan_emi`: Monthly EMI
- `loan_status`: Current status (active, closed, etc.)
- `return_value`: "success", "no_loans", or "error"

**Example Response:**
```
Here are your Personal Loan details:

Loan ID: LN00123456
Principal Amount: ₹5,00,000.00
Current Outstanding: ₹3,50,000.00
Interest Rate: 8.5% per annum
Monthly EMI: ₹10,500.00
Months Remaining: 24
Status: ACTIVE
```

---

#### 5. **action_check_billing_alerts**
**File:** `check_alerts.py`  
**Triggers:** `check_alerts` intent  
**Purpose:** Display pending bills and payment reminders

**Input Slots:**
- None

**Output Slots:**
- `pending_bills`: Count of pending bills
- `total_bill_amount`: Sum of all pending bills
- `alerts_list`: Formatted alert text
- `return_value`: "success", "no_alerts", or "error"

**Example Response:**
```
You have 3 pending payment(s):

1. ELECTRICITY
   Amount: ₹1,200.00
   Due Date: 2025-11-20

2. PHONE
   Amount: ₹599.00
   Due Date: 2025-11-22

3. BROADBAND
   Amount: ₹999.00
   Due Date: 2025-11-25

Total Amount Due: ₹2,798.00
```

---

#### 6. **action_view_account_info**
**File:** `account_info.py`  
**Triggers:** `account_info` intent  
**Purpose:** Display detailed account information

**Input Slots:**
- None

**Output Slots:**
- `account_number`: Account number
- `account_holder`: Account holder name
- `account_type`: Account type (savings, current, etc.)
- `ifsc_code`: IFSC code
- `branch`: Branch name
- `balance`: Current balance
- `return_value`: "success" or "error"

---

### Authentication & Security

#### 7. **action_enroll_voice_biometric**
**File:** `voice_biometric.py`  
**Triggers:** Voice enrollment request  
**Purpose:** Enroll user's voice for biometric authentication

**Security Features:**
- Uses hashed/obfuscated embeddings
- Never stores raw voice data
- Secure enrollment process

**Output Slots:**
- `voice_enrolled`: Boolean flag
- `biometric_id`: User ID for biometric
- `return_value`: "success" or "error"

**Note:** In production, this receives voice embedding from ASR module

---

#### 8. **action_verify_voice_biometric**
**File:** `voice_biometric.py`  
**Triggers:** Voice verification request  
**Purpose:** Authenticate user via voice biometric

**Input Slots:**
- `voice_confidence`: Confidence score from ASR (0-1)

**Output Slots:**
- `voice_verified`: Boolean authentication result
- `confidence_score`: Verification confidence
- `return_value`: "authenticated", "verification_failed", or "error"

**Security:**
- Compares against hashed embedding
- Requires confidence threshold (default: 0.75)
- No raw voice data processed

---

#### 9. **action_generate_otp**
**File:** `otp_auth.py`  
**Triggers:** OTP request for sensitive operations  
**Purpose:** Generate and send one-time password

**Security Features:**
- Rate limiting: Max 3 OTP requests per 10 minutes
- 10-minute expiry
- Cryptographically secure random generation

**Output Slots:**
- `otp_sent`: Boolean flag
- `otp_expiry`: Expiry time in seconds (600)
- `return_value`: "otp_generated", "rate_limited", or "error"

**Production Implementation:**
- Send via SMS using Twilio
- Or via Email for alternative verification

**Demo Mode:**
- OTP displayed in log (for testing)

---

#### 10. **action_verify_otp**
**File:** `otp_auth.py`  
**Triggers:** OTP verification  
**Purpose:** Verify OTP provided by user

**Input Slots:**
- `otp`: OTP code provided by user (extracted via NLU)

**Output Slots:**
- `otp_verified`: Boolean verification result
- `return_value`: "otp_verified", "otp_incorrect", "otp_expired", or "error"

**Validation:**
- Checks OTP matches stored value
- Validates expiry (must be within 10 minutes)
- Returns specific error for user guidance

---

### User Assistance

#### 11. **action_provide_help**
**File:** `help_actions.py`  
**Triggers:** `help` intent  
**Purpose:** Display available features and services

**Output Slots:**
- `return_value`: "success" or "error"

**Response Includes:**
- Account services (balance, details, transactions)
- Transfers & payments (money transfers, bill payments)
- Loan information
- Alerts & reminders
- Security features (voice auth, OTP)

---

#### 12. **action_confirm_action**
**File:** `help_actions.py`  
**Triggers:** Before executing high-risk operations  
**Purpose:** Confirm user action before proceeding

**Input Slots:**
- `action_type`: Type of action (transfer, payment, etc.)
- `action_amount`: Amount involved (optional)
- `action_recipient`: Recipient/destination (optional)

**Output Slots:**
- `action_awaiting_confirmation`: Boolean flag
- `return_value`: "awaiting_confirmation"

**Example:**
```
User: "Transfer 10,000 to Priya"
→ Action: action_confirm_action
→ Response: "Please confirm: TRANSFER of ₹10,000.00 to Priya.
            Say YES to confirm or NO to cancel."
```

---

## Database Models (banking_db.py)

### BankingAccount
```python
account_number: str
account_holder: str
account_type: str          # savings, current, etc.
balance: float
ifsc_code: str
branch: str
```

### Transaction
```python
transaction_id: str
date: str (ISO format)
type: str                  # debit, credit
amount: float
recipient: Optional[str]
description: str
status: str                # completed, pending, failed
```

### Loan
```python
loan_id: str
loan_type: str             # home, personal, auto, etc.
principal_amount: float
current_balance: float
interest_rate: float
tenure_months: int
emi: float
status: str                # active, closed, defaulted
```

### BillingAlert
```python
alert_id: str
bill_type: str
amount: float
due_date: str
status: str                # pending, paid
```

### VoiceBiometric
```python
user_id: str
embedding_hash: str        # Hashed/obfuscated
enrollment_date: str
last_verified: str
confidence_threshold: float  # Default: 0.75
```

---

## Development Workflow

### 1. **Running Rasa Actions Server**

```bash
cd backend/temp_learn

# Terminal 1: Start Rasa NLU/Dialog server
rasa run

# Terminal 2: Start custom actions server
rasa run actions
```

### 2. **Testing Actions**

```bash
# Interactive shell
rasa shell

# Example interaction:
> Hey, what's my balance?
> What's my balance?
> Show account balance
```

### 3. **Adding New Actions**

1. Create action file: `actions/new_action.py`
2. Define action class inheriting from `Action`
3. Implement `name()` and `run()` methods
4. Update `endpoints.yml` if needed
5. Add intents to `nlu.yml` to trigger action
6. Add action to domain `domain.yml`
7. Create dialogue stories for action flow

**Template:**
```python
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionNewAction(Action):
    def name(self) -> str:
        return "action_new_action"
    
    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        # Your action logic here
        dispatcher.utter_message(text="Response")
        return [SlotSet("slot_name", value)]
```

---

## Error Handling

All actions include try-catch blocks and return meaningful error messages:

```python
try:
    # Action logic
except Exception as e:
    dispatcher.utter_message(text=f"Error: {str(e)}")
    return [SlotSet("return_value", "error")]
```

---

## Security Considerations

### ✅ Implemented
- Hashed voice biometric storage (never raw embeddings)
- OTP rate limiting (3 attempts per 10 minutes)
- Transaction audit logging
- Session-based user isolation
- Error messages without sensitive data leakage

### ⚠️ To Implement (Production)
- Real ASR/voice embedding integration
- Database encryption for biometric data
- HTTPS/TLS for all communications
- Multi-factor authentication for high-value transfers
- Fraud detection algorithms
- Compliance with RBI/banking regulations

---

## Testing

### Unit Tests
```bash
pytest tests/test_actions.py -v
```

### Integration Tests
```bash
# Test with Rasa interactive shell
rasa shell

# Test specific flow
rasa test
```

---

## References

- [Rasa Custom Actions Documentation](https://rasa.com/docs/rasa-pro/concepts/custom-actions)
- [Rasa SDK API](https://rasa.com/docs/rasa-sdk)
- [VoiceBanker Project Documentation](../../PROJECT_DOCS.md)

---

## Contributing

When adding new actions:
1. Follow existing code style and documentation
2. Include docstrings for all methods
3. Handle errors gracefully
4. Update this README
5. Add corresponding intents to NLU
6. Add dialogue stories for new flows
7. Include unit tests

---

**Last Updated:** November 2025
