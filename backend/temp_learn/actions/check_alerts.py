"""
Action: Check Billing Alerts

Retrieves and displays pending bills and payment reminders.
"""

from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.banking_db import get_alerts, create_mock_alerts


class ActionCheckBillingAlerts(Action):
    """Check pending bills and alerts"""
    
    def name(self) -> str:
        return "action_check_billing_alerts"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        """
        Retrieve and display pending billing alerts.
        
        Returns:
            List of pending bills or no alerts message
        """
        try:
            # Get alerts
            alerts = get_alerts(tracker.sender_id)
            
            # Create mock alerts if none exist
            if not alerts:
                all_alerts = create_mock_alerts(tracker.sender_id)
                alerts = [a for a in all_alerts if a.status == "pending"]
            
            if not alerts:
                dispatcher.utter_message(
                    text="You don't have any pending bills or payment reminders."
                )
                return [SlotSet("return_value", "no_alerts")]
            
            # Format alerts
            total_amount = sum(a.amount for a in alerts)
            message = f"You have {len(alerts)} pending payment(s):\n\n"
            
            for idx, alert in enumerate(alerts, 1):
                message += (
                    f"{idx}. {alert.bill_type.upper()}\n"
                    f"   Amount: ₹{alert.amount:,.2f}\n"
                    f"   Due Date: {alert.due_date}\n\n"
                )
            
            message += f"Total Amount Due: ₹{total_amount:,.2f}"
            dispatcher.utter_message(text=message)
            
            return [
                SlotSet("pending_bills", len(alerts)),
                SlotSet("total_bill_amount", total_amount),
                SlotSet("alerts_list", message),
                SlotSet("return_value", "success")
            ]
            
        except Exception as e:
            error_message = f"Couldn't retrieve billing alerts. Error: {str(e)}"
            dispatcher.utter_message(text=error_message)
            return [SlotSet("return_value", "error")]
