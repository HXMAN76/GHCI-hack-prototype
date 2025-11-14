"""
VoiceBanker Custom Actions Module

Contains all Rasa custom actions for banking operations, authentication,
and user assistance features.

Actions Available:
- Banking Operations:
  * action_check_balance: View account balance
  * action_transfer_money: Transfer funds to recipient
  * action_view_transaction_history: View recent transactions
  * action_view_loan_info: View loan details
  * action_check_billing_alerts: View pending bills
  * action_view_account_info: View account information

- Authentication & Security:
  * action_enroll_voice_biometric: Enroll voice biometric
  * action_verify_voice_biometric: Verify voice authentication
  * action_generate_otp: Generate OTP
  * action_verify_otp: Verify OTP

- User Assistance:
  * action_provide_help: Show available features
  * action_confirm_action: Confirm important actions

Database:
- banking_db.py: Data models and database operations
- Supports: Accounts, Transactions, Loans, Alerts, Voice Biometrics
"""

from actions.banking_db import (
    BankingAccount,
    Transaction,
    Loan,
    BillingAlert,
    VoiceBiometric,
    get_account,
    get_transactions,
    get_loans,
    get_alerts,
    update_balance,
    create_transaction,
)

__all__ = [
    "BankingAccount",
    "Transaction",
    "Loan",
    "BillingAlert",
    "VoiceBiometric",
    "get_account",
    "get_transactions",
    "get_loans",
    "get_alerts",
    "update_balance",
    "create_transaction",
]
