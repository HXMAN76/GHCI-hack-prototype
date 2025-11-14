Mock DB initialization for VoiceBanker (development)

Location: `backend/temp_learn/db/`

Purpose
-------
These JSON files are lightweight mock data stores used by the Rasa custom actions during local development and tests. They allow actions to read/write simple records without a real PostgreSQL instance.

Files
-----
- `accounts.json`
  - Contains a single `account` object with fields matching the `BankingAccount` model: `account_number`, `account_holder`, `account_type`, `balance`, `ifsc_code`, `branch`, `currency`, `created_at`.

- `transactions.json`
  - Contains `transactions` array. Each transaction object includes `transaction_id`, `date`, `type` (`debit`/`credit`), `amount`, `recipient`, `description`, `status`.

- `loans.json`
  - Contains `loans` array. Each loan includes `loan_id`, `loan_type`, `principal`, `current_balance`, `interest_rate`, `tenure_months`, `emi`, `status`.

- `alerts.json`
  - Contains `alerts` array. Each alert includes `alert_id`, `bill_type`, `amount`, `due_date`, `status`.

- `biometrics.json`
  - Contains enrollment data for voice biometrics: `user_id` or `biometric_id`, `embedding_hash`, `enrollment_date`, `confidence_threshold`.

Notes and Usage
---------------
- These files are read/written by `banking_db.py` helper functions. The module will create a file with example data on first run if missing.
- To reset mock data, replace files with new JSON or delete them — the actions will regenerate baseline mock records on next run.
- For integration tests, you can copy these files into test fixtures and modify values as needed.

Extending Mock Data
-------------------
- Add more user accounts by adding objects under `accounts.json` keyed by user/session.
- Add more transactions into `transactions.json` to test pagination and filtering.
- Add multiple loans and alerts to test edge cases like zero balance, overdue bills, or multiple concurrent loans.

Security
--------
- The biometrics file stores only hashed embeddings (`embedding_hash`). Do not store raw audio or un-hashed embeddings here.
- Treat these mock files as non-sensitive for local dev. For any CI or shared runner, remove or obfuscate real PII.

Examples
--------
See `accounts.json`, `transactions.json`, `loans.json`, `alerts.json`, `biometrics.json` in the same directory for sample structures.
