"""
Action: Help and Feature Discovery

Provides help information and available banking features.
"""

from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class ActionProvideHelp(Action):
    """Provide help information"""
    
    def name(self) -> str:
        return "action_provide_help"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        """
        Display available features and banking services.
        
        Returns:
            Help message with available operations
        """
        try:
            help_message = (
                "I'm VoiceBanker, your AI assistant for voice-based banking. "
                "Here's what I can help you with:\n\n"
                "💰 **ACCOUNT SERVICES**\n"
                "- Check your account balance\n"
                "- View account details\n"
                "- See transaction history\n\n"
                "💸 **TRANSFERS & PAYMENTS**\n"
                "- Transfer money to contacts\n"
                "- Pay bills (electricity, phone, water, etc.)\n"
                "- Send funds to bank accounts\n\n"
                "📊 **LOAN INFORMATION**\n"
                "- Check loan details\n"
                "- View EMI and payment schedule\n"
                "- Get loan status\n\n"
                "🔔 **ALERTS & REMINDERS**\n"
                "- View pending bills\n"
                "- Get payment reminders\n"
                "- Check due dates\n\n"
                "🔐 **SECURITY**\n"
                "- Voice authentication\n"
                "- One-time password (OTP) verification\n\n"
                "What would you like to do?"
            )
            
            dispatcher.utter_message(text=help_message)
            
            return [SlotSet("return_value", "success")]
            
        except Exception as e:
            error_message = f"Error retrieving help. Error: {str(e)}"
            dispatcher.utter_message(text=error_message)
            return [SlotSet("return_value", "error")]


class ActionConfirmAction(Action):
    """Confirm user action before proceeding"""
    
    def name(self) -> str:
        return "action_confirm_action"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        """
        Ask user for confirmation on important actions.
        
        Slots used:
            - action_type: Type of action (transfer, payment, etc.)
            - action_amount: Amount involved
            - action_recipient: Recipient/destination
        
        Returns:
            Confirmation message
        """
        try:
            action_type = tracker.get_slot("action_type")
            action_amount = tracker.get_slot("action_amount")
            action_recipient = tracker.get_slot("action_recipient")
            
            if not action_type:
                dispatcher.utter_message(
                    text="I need more details to confirm your action."
                )
                return [SlotSet("return_value", "incomplete_data")]
            
            # Build confirmation message
            message = f"Please confirm: {action_type.upper()}"
            
            if action_amount:
                message += f" of ₹{action_amount:,.2f}"
            if action_recipient:
                message += f" to {action_recipient}"
            
            message += "\n\nSay YES to confirm or NO to cancel."
            
            dispatcher.utter_message(text=message)
            
            return [
                SlotSet("action_awaiting_confirmation", True),
                SlotSet("return_value", "awaiting_confirmation")
            ]
            
        except Exception as e:
            error_message = f"Error in confirmation. Error: {str(e)}"
            dispatcher.utter_message(text=error_message)
            return [SlotSet("return_value", "error")]
