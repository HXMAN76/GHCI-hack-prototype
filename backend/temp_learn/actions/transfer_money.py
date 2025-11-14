"""
Action: Transfer Money

Handles fund transfers to recipients with amount verification.
Includes transaction logging and balance updates.
"""

from typing import Any, Dict, List, Text, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.banking_db import (
    get_account,
    create_mock_account,
    update_balance,
    create_transaction,
)


class ActionTransferMoney(Action):
    """Transfer money to a recipient"""
    
    def name(self) -> str:
        return "action_transfer_money"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        """
        Execute money transfer action.
        
        Requires slots:
            - amount: Transfer amount
            - recipient: Recipient name or account number
        
        Returns:
            Transaction confirmation or error status
        """
        try:
            # Get transfer details from slots
            amount = tracker.get_slot("amount")
            recipient = tracker.get_slot("recipient")
            
            if not amount or not recipient:
                dispatcher.utter_message(
                    text="I need both amount and recipient details to proceed. "
                    "Please provide the amount and who you want to transfer to."
                )
                return [SlotSet("return_value", "missing_data")]
            
            # Convert amount to float if string
            try:
                amount = float(str(amount).replace(",", ""))
            except (ValueError, AttributeError):
                dispatcher.utter_message(
                    text=f"I couldn't understand the amount '{amount}'. "
                    "Please provide a valid amount in rupees."
                )
                return [SlotSet("return_value", "invalid_amount")]
            
            # Get user account
            account = get_account(tracker.sender_id)
            if not account:
                account = create_mock_account(tracker.sender_id, "Customer")
            
            # Check sufficient balance
            if account.balance < amount:
                dispatcher.utter_message(
                    text=f"Sorry, you don't have sufficient balance. "
                    f"Your current balance is ₹{account.balance:,.2f} "
                    f"and you're trying to transfer ₹{amount:,.2f}."
                )
                return [SlotSet("return_value", "insufficient_balance")]
            
            # Create transaction
            transaction = create_transaction(
                tracker.sender_id,
                amount,
                recipient,
                "transfer"
            )
            
            # Update balance
            new_balance = update_balance(
                tracker.sender_id,
                amount,
                "debit"
            )
            
            # Confirmation message
            message = (
                f"Transfer successful! ₹{amount:,.2f} has been sent to {recipient}. "
                f"Your new balance is ₹{new_balance:,.2f}. "
                f"Transaction ID: {transaction.transaction_id}"
            )
            dispatcher.utter_message(text=message)
            
            return [
                SlotSet("transfer_amount", amount),
                SlotSet("transfer_recipient", recipient),
                SlotSet("new_balance", new_balance),
                SlotSet("transaction_id", transaction.transaction_id),
                SlotSet("return_value", "success")
            ]
            
        except Exception as e:
            error_message = f"Transfer failed. Error: {str(e)}"
            dispatcher.utter_message(text=error_message)
            return [SlotSet("return_value", "error")]
