"""
Action: View Transaction History

Retrieves and displays recent transactions in a user-friendly format.
"""

from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.banking_db import get_transactions


class ActionViewTransactionHistory(Action):
    """View recent transactions"""
    
    def name(self) -> str:
        return "action_view_transaction_history"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        """
        Retrieve and display transaction history.
        
        Returns:
            Formatted transaction list or empty state message
        """
        try:
            # Get recent transactions (last 5)
            transactions = get_transactions(tracker.sender_id, limit=5)
            
            if not transactions:
                dispatcher.utter_message(
                    text="You don't have any transaction history yet."
                )
                return [SlotSet("transaction_history", None)]
            
            # Format transactions for display
            history_text = "Here are your recent transactions:\n\n"
            
            for idx, txn in enumerate(transactions, 1):
                date_str = txn.date.split('T')[0]  # Extract just the date
                history_text += (
                    f"{idx}. {date_str} - {txn.description}\n"
                    f"   Amount: ₹{txn.amount:,.2f} ({txn.type.upper()})\n"
                    f"   Status: {txn.status}\n\n"
                )
            
            dispatcher.utter_message(text=history_text)
            
            return [
                SlotSet("transaction_history", history_text),
                SlotSet("transaction_count", len(transactions)),
                SlotSet("return_value", "success")
            ]
            
        except Exception as e:
            error_message = f"Couldn't retrieve transaction history. Error: {str(e)}"
            dispatcher.utter_message(text=error_message)
            return [SlotSet("return_value", "error")]
