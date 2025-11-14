"""
Action: View Loan Information

Retrieves and displays loan details including balance, EMI, and status.
"""

from typing import Any, Dict, List, Text, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.banking_db import get_loan_info, get_loans, create_mock_loan


class ActionViewLoanInfo(Action):
    """View loan information and status"""
    
    def name(self) -> str:
        return "action_view_loan_info"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        """
        Retrieve and display loan information.
        
        Optional slots:
            - loan_type: Specific loan type to query (home, personal, auto, etc.)
        
        Returns:
            Loan details or no loans message
        """
        try:
            loan_type = tracker.get_slot("loan_type")
            
            # Get loans
            loans = get_loans(tracker.sender_id)
            
            # Create mock loan if none exist
            if not loans:
                loan = create_mock_loan(tracker.sender_id)
                loans = [loan]
            
            # Find specific loan or first active one
            if loan_type:
                loan = get_loan_info(tracker.sender_id, loan_type)
            else:
                loan = get_loan_info(tracker.sender_id)
            
            if not loan:
                dispatcher.utter_message(
                    text="You don't have any active loans."
                )
                return [SlotSet("return_value", "no_loans")]
            
            # Format loan information
            months_remaining = loan.tenure_months - int(
                (loan.principal_amount - loan.current_balance) / loan.emi
            )
            
            message = (
                f"Here are your {loan.loan_type.capitalize()} Loan details:\n\n"
                f"Loan ID: {loan.loan_id}\n"
                f"Principal Amount: ₹{loan.principal_amount:,.2f}\n"
                f"Current Outstanding: ₹{loan.current_balance:,.2f}\n"
                f"Interest Rate: {loan.interest_rate}% per annum\n"
                f"Monthly EMI: ₹{loan.emi:,.2f}\n"
                f"Months Remaining: {max(0, months_remaining)}\n"
                f"Status: {loan.status.upper()}"
            )
            
            dispatcher.utter_message(text=message)
            
            return [
                SlotSet("loan_id", loan.loan_id),
                SlotSet("loan_type", loan.loan_type),
                SlotSet("loan_balance", loan.current_balance),
                SlotSet("loan_emi", loan.emi),
                SlotSet("loan_status", loan.status),
                SlotSet("return_value", "success")
            ]
            
        except Exception as e:
            error_message = f"Couldn't retrieve loan information. Error: {str(e)}"
            dispatcher.utter_message(text=error_message)
            return [SlotSet("return_value", "error")]
