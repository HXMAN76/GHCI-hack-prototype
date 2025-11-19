from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from .db.queries import (
    get_balance,
    get_transactions,
    transfer_money,
    block_card,
    report_fraud
)
import re

def safe_amount(val):
    try:
        return float(str(val).replace("rupees", "").replace("₹", "").strip())
    except:
        return None


class ActionCheckBalance(Action):
    def name(self):
        return "action_check_balance"

    def run(self, dispatcher, tracker, domain):
        user_id = tracker.sender_id
        bal = get_balance(user_id)

        if bal is None:
            dispatcher.utter_message(text="Could not fetch balance.")
            return []

        dispatcher.utter_message(text=f"Your current balance is ₹{bal:.2f}.")
        return []


class ActionTransactionHistory(Action):
    def name(self):
        return "action_transaction_history"

    def run(self, dispatcher, tracker, domain):
        user_id = tracker.sender_id
        rows = get_transactions(user_id)

        if not rows:
            dispatcher.utter_message(text="No recent transactions.")
            return []

        msg = "Here are your last 5 transactions:\n"
        for r in rows:
            msg += f"- {r['tx_date']} | {r['tx_type']} | ₹{r['amount']} | {r['description']}\n"

        dispatcher.utter_message(text=msg)
        return []


class ActionTransferMoney(Action):
    def name(self):
        return "action_transfer_money"

    def run(self, dispatcher, tracker, domain):

        name = tracker.get_slot("name")
        acc = tracker.get_slot("account_number")
        ifsc = tracker.get_slot("ifsc")
        amt_raw = tracker.get_slot("amount")

        amt = safe_amount(amt_raw)
        if amt is None:
            dispatcher.utter_message(text="Invalid amount. Please type again.")
            return []

        user_id = tracker.sender_id

        # Sanitize account number: extract digits
        if isinstance(acc, str):
            m = re.search(r"(\d+)", acc)
            if m:
                acc_clean = m.group(1)
            else:
                acc_clean = acc.strip()
        else:
            acc_clean = acc

        # Sanitize IFSC: pick the first alphanumeric token and uppercase it
        if ifsc:
            m2 = re.search(r"([A-Za-z0-9]+)", str(ifsc))
            if m2:
                ifsc_clean = m2.group(1).upper()
            else:
                ifsc_clean = str(ifsc).strip().upper()
        else:
            ifsc_clean = None

        ok, msg = transfer_money(user_id, acc_clean, amt, recipient_ifsc=ifsc_clean)

        if not ok:
            dispatcher.utter_message(text=msg)
            return []

        dispatcher.utter_message(
            text=f"₹{amt:.2f} has been transferred to {name} (Acc: {acc})."
        )

        return [
            SlotSet("name", None),
            SlotSet("account_number", None),
            SlotSet("ifsc", None),
            SlotSet("amount", None)
        ]


class ActionBlockCard(Action):
    def name(self):
        return "action_block_card"

    def run(self, dispatcher, tracker, domain):
        user_id = tracker.sender_id
        ctype = tracker.get_slot("card_type")
        block_card(user_id, ctype)

        return [SlotSet("card_type", None)]


class ActionReportFraud(Action):
    def name(self):
        return "action_report_fraud"

    def run(self, dispatcher, tracker, domain):
        user_id = tracker.sender_id
        details = tracker.get_slot("fraud_details") or "User suspected fraud"
        report_fraud(user_id, details)

        dispatcher.utter_message(
            text="Fraud report submitted. Our team will contact you."
        )

        return [SlotSet("fraud_details", None)]


class ActionLoanRates(Action):
    def name(self):
        return "action_loan_rates"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Loan rates:\n- Home: 8.3%\n- Personal: 12.5%\n- Education: 10.2%")
        return []


class ActionFDRates(Action):
    def name(self):
        return "action_fd_rates"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="FD rates:\n- 6 months: 5.5%\n- 1 year: 6.2%\n- 5 years: 7.75%")
        return []


class ActionBranchLocator(Action):
    def name(self):
        return "action_branch_locator"

    def run(self, dispatcher, tracker, domain):
        city = tracker.get_slot("location")

        branches = {
            "Delhi": "Connaught Place Branch",
            "Mumbai": "Bandra West Branch",
            "Kochi": "MG Road Branch",
            "Bengaluru": "Indiranagar Branch"
        }

        if city in branches:
            dispatcher.utter_message(text=f"Nearest branch in {city}: {branches[city]}")
        else:
            dispatcher.utter_message(text="Please specify a valid city.")

        return []


# --------------------------------------------------------
# Confirmation helper actions (no-op placeholders)
# These are lightweight actions used in stories/rules to mark
# that the system has set up a confirmation step. They don't
# perform heavy logic but must be registered so Rasa doesn't
# complain about missing actions or contradictory rules.
# --------------------------------------------------------


class ActionSetConfirmTransfer(Action):
    def name(self):
        return "action_set_confirm_transfer"

    def run(self, dispatcher, tracker, domain):
        # Placeholder: in future, could set a slot like 'confirm_transfer'
        return []


class ActionResetConfirmTransfer(Action):
    def name(self):
        return "action_reset_confirm_transfer"

    def run(self, dispatcher, tracker, domain):
        return []


class ActionSetConfirmCardBlock(Action):
    def name(self):
        return "action_set_confirm_card_block"

    def run(self, dispatcher, tracker, domain):
        return []


class ActionResetConfirmCardBlock(Action):
    def name(self):
        return "action_reset_confirm_card_block"

    def run(self, dispatcher, tracker, domain):
        return []


class ActionSetConfirmFraud(Action):
    def name(self):
        return "action_set_confirm_fraud"

    def run(self, dispatcher, tracker, domain):
        return []


class ActionResetConfirmFraud(Action):
    def name(self):
        return "action_reset_confirm_fraud"

    def run(self, dispatcher, tracker, domain):
        return []
