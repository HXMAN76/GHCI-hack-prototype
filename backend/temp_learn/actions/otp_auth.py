"""
Action: OTP (One-Time Password) Authentication

Handles OTP generation, sending, and verification for secure transactions.
Implements rate limiting for security.
"""

from typing import Any, Dict, List, Text
import random
import time

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


# Simple in-memory OTP store (in production, use database)
otp_storage = {}


class ActionGenerateOTP(Action):
    """Generate and send OTP to user"""
    
    def name(self) -> str:
        return "action_generate_otp"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        """
        Generate OTP for authentication.
        
        In production:
        - Use cryptographically secure random generation
        - Send via SMS/Email
        - Store in secure database
        - Implement expiry mechanism
        
        Returns:
            OTP generation status
        """
        try:
            session_id = tracker.sender_id
            
            # Check rate limiting (max 3 attempts per 10 minutes)
            if session_id in otp_storage:
                attempts = otp_storage[session_id].get("attempts", 0)
                last_attempt = otp_storage[session_id].get("last_attempt", 0)
                time_elapsed = time.time() - last_attempt
                
                if attempts >= 3 and time_elapsed < 600:  # 600 seconds = 10 minutes
                    dispatcher.utter_message(
                        text="You've exceeded the maximum OTP attempts. "
                        "Please try again in 10 minutes."
                    )
                    return [SlotSet("return_value", "rate_limited")]
            
            # Generate 6-digit OTP
            otp = str(random.randint(100000, 999999))
            
            # Store OTP with metadata
            if session_id not in otp_storage:
                otp_storage[session_id] = {}
            
            otp_storage[session_id]["otp"] = otp
            otp_storage[session_id]["timestamp"] = time.time()
            otp_storage[session_id]["attempts"] = otp_storage[session_id].get("attempts", 0) + 1
            otp_storage[session_id]["last_attempt"] = time.time()
            otp_storage[session_id]["verified"] = False
            
            # In production, send via SMS/Email
            # twilio_client.messages.create(
            #     to=user_phone,
            #     from_="VOICEBANKER",
            #     body=f"Your VoiceBanker OTP is: {otp}. Valid for 10 minutes."
            # )
            
            message = (
                f"One-time password has been sent to your registered phone. "
                f"OTP: {otp} (Valid for 10 minutes). "
                f"Please say the OTP to verify."
            )
            dispatcher.utter_message(text=message)
            
            return [
                SlotSet("otp_sent", True),
                SlotSet("otp_expiry", 600),  # 10 minutes
                SlotSet("return_value", "otp_generated")
            ]
            
        except Exception as e:
            error_message = f"OTP generation failed. Error: {str(e)}"
            dispatcher.utter_message(text=error_message)
            return [SlotSet("return_value", "error")]


class ActionVerifyOTP(Action):
    """Verify OTP provided by user"""
    
    def name(self) -> str:
        return "action_verify_otp"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        """
        Verify OTP provided by user.
        
        Requires slots:
            - otp: OTP code provided by user (extracted from speech)
        
        Returns:
            OTP verification success or failure
        """
        try:
            session_id = tracker.sender_id
            user_otp = tracker.get_slot("otp")
            
            if not user_otp:
                dispatcher.utter_message(
                    text="I didn't catch the OTP. Please say it again."
                )
                return [SlotSet("return_value", "otp_missing")]
            
            # Check if OTP exists
            if session_id not in otp_storage:
                dispatcher.utter_message(
                    text="No OTP request found. Please request a new OTP."
                )
                return [SlotSet("return_value", "no_otp_requested")]
            
            stored_otp_data = otp_storage[session_id]
            stored_otp = stored_otp_data.get("otp")
            timestamp = stored_otp_data.get("timestamp", 0)
            
            # Check OTP expiry (10 minutes)
            if time.time() - timestamp > 600:
                dispatcher.utter_message(
                    text="The OTP has expired. Please request a new one."
                )
                return [SlotSet("return_value", "otp_expired")]
            
            # Convert to string for comparison
            user_otp_str = str(user_otp).strip()
            
            # Verify OTP
            if user_otp_str == stored_otp:
                otp_storage[session_id]["verified"] = True
                
                message = (
                    "OTP verification successful! "
                    "Your transaction has been authenticated."
                )
                dispatcher.utter_message(text=message)
                
                return [
                    SlotSet("otp_verified", True),
                    SlotSet("return_value", "otp_verified")
                ]
            else:
                message = (
                    "OTP verification failed. "
                    "The code you provided doesn't match. Please try again."
                )
                dispatcher.utter_message(text=message)
                
                return [
                    SlotSet("otp_verified", False),
                    SlotSet("return_value", "otp_incorrect")
                ]
            
        except Exception as e:
            error_message = f"OTP verification error. Error: {str(e)}"
            dispatcher.utter_message(text=error_message)
            return [SlotSet("return_value", "error")]
