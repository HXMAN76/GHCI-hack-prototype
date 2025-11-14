"""
Action: Voice Biometric Authentication

Handles voice-based authentication and enrollment for VoiceBanker.
Uses hashed embeddings for security.
"""

from typing import Any, Dict, List, Text
import hashlib

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.banking_db import enroll_voice_biometric, verify_voice_biometric


class ActionEnrollVoiceBiometric(Action):
    """Enroll user's voice for biometric authentication"""
    
    def name(self) -> str:
        return "action_enroll_voice_biometric"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        """
        Enroll voice biometric for first-time setup.
        In production, this would capture real voice embedding.
        
        Returns:
            Enrollment success or error status
        """
        try:
            # In production, audio would be captured and processed by ASR module
            # For demo, create a mock embedding hash
            mock_embedding = f"embedding_{tracker.sender_id}"
            embedding_hash = hashlib.sha256(
                mock_embedding.encode()
            ).hexdigest()
            
            biometric = enroll_voice_biometric(tracker.sender_id, embedding_hash)
            
            message = (
                "Voice biometric enrollment successful! "
                "Your voice profile has been created and saved securely. "
                "You can now use voice authentication to access your account."
            )
            dispatcher.utter_message(text=message)
            
            return [
                SlotSet("voice_enrolled", True),
                SlotSet("biometric_id", biometric.user_id),
                SlotSet("return_value", "success")
            ]
            
        except Exception as e:
            error_message = f"Voice enrollment failed. Error: {str(e)}"
            dispatcher.utter_message(text=error_message)
            return [SlotSet("return_value", "error")]


class ActionVerifyVoiceBiometric(Action):
    """Verify user's voice against stored biometric"""
    
    def name(self) -> str:
        return "action_verify_voice_biometric"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        """
        Verify voice biometric for authentication.
        
        Optional slots:
            - voice_confidence: Confidence score from ASR module (0-1)
        
        Returns:
            Authentication success or failure
        """
        try:
            voice_confidence = tracker.get_slot("voice_confidence")
            
            if voice_confidence is None:
                # Mock confidence for demo
                voice_confidence = 0.82
            else:
                try:
                    voice_confidence = float(voice_confidence)
                except (ValueError, TypeError):
                    voice_confidence = 0.82
            
            # Create embedding hash
            mock_embedding = f"embedding_{tracker.sender_id}"
            embedding_hash = hashlib.sha256(
                mock_embedding.encode()
            ).hexdigest()
            
            # Verify against stored biometric
            is_verified = verify_voice_biometric(
                tracker.sender_id,
                embedding_hash,
                voice_confidence
            )
            
            if is_verified:
                message = (
                    "Voice verification successful! "
                    "You've been authenticated. Proceeding with your request."
                )
                dispatcher.utter_message(text=message)
                
                return [
                    SlotSet("voice_verified", True),
                    SlotSet("confidence_score", voice_confidence),
                    SlotSet("return_value", "authenticated")
                ]
            else:
                message = (
                    "Sorry, voice verification failed. "
                    f"Confidence score: {voice_confidence:.1%}. "
                    "Please try again or use OTP authentication."
                )
                dispatcher.utter_message(text=message)
                
                return [
                    SlotSet("voice_verified", False),
                    SlotSet("return_value", "verification_failed")
                ]
            
        except Exception as e:
            error_message = f"Voice verification error. Error: {str(e)}"
            dispatcher.utter_message(text=error_message)
            return [SlotSet("return_value", "error")]
