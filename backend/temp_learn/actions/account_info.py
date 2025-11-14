"""
Action: Account Information

Retrieves account details including account number, type, IFSC code, etc.
"""

from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.banking_db import get_account, create_mock_account


class ActionViewAccountInfo(Action):
    """View account details"""
    
    def name(self) -> str:
        return "action_view_account_info"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        """
        Retrieve and display account information.
        
        Returns:
            Account details or error status
        """
        try:
            # Get account
            account = get_account(tracker.sender_id)
            if not account:
                account = create_mock_account(tracker.sender_id, "Customer")
            
            # Format account info
            message = (
                f"Here are your account details:\n\n"
                f"Account Holder: {account.account_holder}\n"
                f"Account Number: {account.account_number}\n"
                f"Account Type: {account.account_type.capitalize()}\n"
                f"IFSC Code: {account.ifsc_code}\n"
                f"Branch: {account.branch}\n"
                f"Current Balance: ₹{account.balance:,.2f}"
            )
            
            dispatcher.utter_message(text=message)
            
            return [
                SlotSet("account_number", account.account_number),
                SlotSet("account_holder", account.account_holder),
                SlotSet("account_type", account.account_type),
                SlotSet("ifsc_code", account.ifsc_code),
                SlotSet("branch", account.branch),
                SlotSet("balance", account.balance),
                SlotSet("return_value", "success")
            ]
            
        except Exception as e:
            error_message = f"Couldn't retrieve account information. Error: {str(e)}"
            dispatcher.utter_message(text=error_message)
            return [SlotSet("return_value", "error")]
