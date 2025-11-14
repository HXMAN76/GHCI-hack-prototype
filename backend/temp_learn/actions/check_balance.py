"""
Action: Check Account Balance

Retrieves the user's current account balance from the database.
Supports banking context for VoiceBanker project.
"""

from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.banking_db import get_account, create_mock_account


class ActionCheckBalance(Action):
    """Check and retrieve account balance"""
    
    def name(self) -> str:
        return "action_check_balance"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        """
        Execute balance check action.
        
        Returns:
            Balance amount or error status via slot
        """
        try:
            # Get user's account
            account = get_account(tracker.sender_id)
            
            # Create mock account if not exists
            if not account:
                account = create_mock_account(tracker.sender_id, "Customer")
            
            # Format response
            balance = account.balance
            account_number = account.account_number
            
            message = f"Your current account balance is ₹{balance:,.2f}"
            dispatcher.utter_message(text=message)
            
            return [
                SlotSet("balance", balance),
                SlotSet("account_number", account_number),
                SlotSet("return_value", "success")
            ]
            
        except Exception as e:
            error_message = f"Sorry, I couldn't retrieve your balance. Error: {str(e)}"
            dispatcher.utter_message(text=error_message)
            return [SlotSet("return_value", "error")]
