"""
Custom Actions Integration Guide

This file documents how to integrate all custom actions into Rasa domain configuration.
Add these action definitions to your domain.yml file.
"""

# ==================== ACTIONS CONFIGURATION ====================
# Add to domain.yml:

actions:
  # ========== BANKING OPERATIONS ==========
  - action_check_balance
  - action_transfer_money
  - action_view_transaction_history
  - action_view_loan_info
  - action_check_billing_alerts
  - action_view_account_info
  
  # ========== AUTHENTICATION ==========
  - action_enroll_voice_biometric
  - action_verify_voice_biometric
  - action_generate_otp
  - action_verify_otp
  
  # ========== USER ASSISTANCE ==========
  - action_provide_help
  - action_confirm_action

# ==================== SLOTS CONFIGURATION ====================
# Add to domain.yml:

slots:
  # ===== Account Information =====
  account_number:
    type: text
    mappings:
      - type: controlled
  
  account_holder:
    type: text
    mappings:
      - type: controlled
  
  account_type:
    type: text
    mappings:
      - type: controlled
  
  ifsc_code:
    type: text
    mappings:
      - type: controlled
  
  branch:
    type: text
    mappings:
      - type: controlled
  
  balance:
    type: float
    mappings:
      - type: controlled
  
  # ===== Transfer Slots =====
  amount:
    type: float
    mappings:
      - type: from_entity
        entity: amount
  
  recipient:
    type: text
    mappings:
      - type: from_entity
        entity: recipient
      - type: from_text
  
  transfer_amount:
    type: float
    mappings:
      - type: controlled
  
  transfer_recipient:
    type: text
    mappings:
      - type: controlled
  
  new_balance:
    type: float
    mappings:
      - type: controlled
  
  transaction_id:
    type: text
    mappings:
      - type: controlled
  
  # ===== Loan Slots =====
  loan_type:
    type: text
    mappings:
      - type: from_entity
        entity: loan_type
  
  loan_id:
    type: text
    mappings:
      - type: controlled
  
  loan_balance:
    type: float
    mappings:
      - type: controlled
  
  loan_emi:
    type: float
    mappings:
      - type: controlled
  
  loan_status:
    type: text
    mappings:
      - type: controlled
  
  # ===== Transaction History Slots =====
  transaction_history:
    type: text
    mappings:
      - type: controlled
  
  transaction_count:
    type: int
    mappings:
      - type: controlled
  
  # ===== Alert Slots =====
  pending_bills:
    type: int
    mappings:
      - type: controlled
  
  total_bill_amount:
    type: float
    mappings:
      - type: controlled
  
  alerts_list:
    type: text
    mappings:
      - type: controlled
  
  # ===== Authentication Slots =====
  voice_enrolled:
    type: bool
    mappings:
      - type: controlled
  
  voice_verified:
    type: bool
    mappings:
      - type: controlled
  
  biometric_id:
    type: text
    mappings:
      - type: controlled
  
  confidence_score:
    type: float
    mappings:
      - type: controlled
  
  voice_confidence:
    type: float
    mappings:
      - type: controlled
  
  otp_sent:
    type: bool
    mappings:
      - type: controlled
  
  otp_verified:
    type: bool
    mappings:
      - type: controlled
  
  otp:
    type: text
    mappings:
      - type: from_entity
        entity: otp
      - type: from_text
  
  otp_expiry:
    type: int
    mappings:
      - type: controlled
  
  # ===== Confirmation Slots =====
  action_type:
    type: text
    mappings:
      - type: controlled
  
  action_amount:
    type: float
    mappings:
      - type: controlled
  
  action_recipient:
    type: text
    mappings:
      - type: controlled
  
  action_awaiting_confirmation:
    type: bool
    mappings:
      - type: controlled
  
  # ===== Return Value Slot (Generic status) =====
  return_value:
    type: text
    mappings:
      - type: controlled

# ==================== EXAMPLE DIALOGUE FLOWS ====================

# Flow 1: Check Balance
# User: "What's my balance?"
# → Intent: check_balance
# → Action: action_check_balance
# → Response: "Your balance is ₹50,000"

# Flow 2: Transfer Money
# User: "Transfer 5000 to Raj"
# → Intent: transfer_money (amount=5000, recipient=Raj)
# → Action: action_confirm_action
#   → Response: "Confirm transfer ₹5000 to Raj? Say YES/NO"
# User: "Yes"
# → Intent: affirm
# → Action: action_transfer_money
# → Action: action_generate_otp
#   → Response: "OTP sent. Say the code."
# User: "123456"
# → Intent: verify_otp (otp=123456)
# → Action: action_verify_otp
# → Response: "Transfer successful!"

# Flow 3: View Loan Info
# User: "What's my loan status?"
# → Intent: loan_inquiry
# → Action: action_view_loan_info
# → Response: "Loan details: balance ₹3,50,000, EMI ₹10,500..."

# Flow 4: Check Bills
# User: "Do I have any pending bills?"
# → Intent: check_alerts
# → Action: action_check_billing_alerts
# → Response: "3 pending bills totaling ₹2,798"

# ==================== RESPONSES CONFIGURATION ====================
# Add to domain.yml if using response templates:

responses:
  utter_balance_confirmation:
    - text: "Your balance is ₹{balance}"
  
  utter_transfer_success:
    - text: "Transfer of ₹{transfer_amount} to {transfer_recipient} successful! 
             New balance: ₹{new_balance}"
  
  utter_insufficient_balance:
    - text: "Insufficient balance. Available: ₹{balance}, 
             Requested: ₹{amount}"
  
  utter_otp_sent:
    - text: "OTP sent to your registered phone. Valid for 10 minutes."
  
  utter_otp_verified:
    - text: "OTP verification successful!"
  
  utter_ask_confirm:
    - text: "Please confirm: {action_type} of ₹{action_amount} 
             to {action_recipient}. Say YES or NO."

# ==================== ENTITY EXTRACTION SETUP ====================
# Add to nlu.yml for better entity recognition:

- regex: amount
  examples: |
    - \d+(?:\.\d{1,2})?

- regex: account_number
  examples: |
    - \d{10,16}

- regex: otp
  examples: |
    - \d{4,6}

- lookup: recipient
  examples: |
    - Raj
    - Priya
    - Amit
    - Suresh
    - Neha
    - Ramesh

- lookup: loan_type
  examples: |
    - home loan
    - personal loan
    - auto loan
    - student loan

- lookup: bill_type
  examples: |
    - electricity
    - phone
    - water
    - gas
    - broadband

# ==================== ENDPOINTS CONFIGURATION ====================
# Ensure actions server is configured in endpoints.yml:

action_endpoint:
  url: "http://localhost:5055/webhook"

# Or if using named actions module:
action_endpoint:
  actions_module: "actions"
