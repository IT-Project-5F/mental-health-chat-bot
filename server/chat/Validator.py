import json
import os
import re
import logging
from typing import Optional, Dict, List, Tuple
from datetime import datetime
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of mental health validation"""

    is_trigger: bool
    category: Optional[str] = None
    matched_word: Optional[str] = None
    response: Optional[str] = None
    confidence: float = 0.0
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class MentalHealthModel:
    """
    Complete mental health validation model that loads trigger words from JSON
    and provides appropriate responses for different categories of mental health triggers.
    """
    def __init__(self):
        self.word_list = self._load_trigger_words()
        self.validation_history = []
        self.emergency_contacts = self._load_emergency_contacts()
        logger.info(
            f"MentalHealthModel initialized with {len(self.word_list)} categories"
        )

    def _load_trigger_words(self) -> Dict[str, List[str]]:
        try:
            current_dir = os.path.dirname(__file__)
            json_path = os.path.join(current_dir, "Trigger_Words.json")

            with open(json_path, "r", encoding="utf-8") as file:
                word_list = json.load(file)

            # Validate the structure
            if not isinstance(word_list, dict):
                raise ValueError("Trigger words JSON must be a dictionary")

            # Normalize all words to lowercase for consistent matching
            normalized_list = {}
            for category, words in word_list.items():
                if isinstance(words, list):
                    normalized_list[category] = [
                        word.lower().strip() for word in words if word.strip()
                    ]
                else:
                    logger.warning(
                        f"Category '{category}' does not contain a list. Skipping."
                    )

            logger.info(f"Successfully loaded trigger words from: {json_path}")
            logger.info(f"Categories loaded: {list(normalized_list.keys())}")

            return normalized_list

        except FileNotFoundError:
            logger.error(
                f"Trigger_words.json not found in {os.path.dirname(__file__)}"
            )
            return self._get_default_trigger_words()
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing Trigger_words.json: {e}")
            return self._get_default_trigger_words()
        except Exception as e:
            logger.error(f"Unexpected error loading trigger words: {e}")
            return self._get_default_trigger_words()

    def _load_emergency_contacts(self) -> Dict[str, Dict[str, str]]:
        """Load emergency contacts for different regions"""
        return {
            "australia": {
                "lifeline": "13 11 14",
                "crisis_text": "Text HELLO to 741741",
                "emergency": "000",
                "beyond_blue": "1300 22 4636",
                "kids_helpline": "1800 55 1800",
            },
            "usa": {
                "suicide_prevention": "988",
                "crisis_text": "Text HOME to 741741",
                "emergency": "911",
            },
            "uk": {"samaritans": "116 123", "emergency": "999"},
        }

    def validate_input(self, user_input: str, region: str = "australia") -> ValidationResult:
        """
        Validate user input for mental health triggers using regex for all matches.
        """
        if not user_input or not isinstance(user_input, str):
            return ValidationResult(is_trigger=False)

        text = user_input.lower().strip()

        for category, words in self.word_list.items():
            # Join words into a single regex pattern (word boundaries for single words)
            # Escape special characters and handle multi-word phrases
            pattern = r"|".join(
                [r"\b" + re.escape(word) + r"\b" if " " not in word else re.escape(word) for word in words]
            )

            match = re.search(pattern, text)
            if match:
                matched_word = match.group(0)
                confidence = self._calculate_confidence(matched_word, text)
                result = ValidationResult(
                    is_trigger=True,
                    category=category,
                    matched_word=matched_word,
                    response=self._get_response_for_category(category, region),
                    confidence=confidence,
                )
                self._log_validation(result, user_input)
                return result

        # No triggers found
        result = ValidationResult(is_trigger=False)
        self._log_validation(result, user_input)
        return result


    def _calculate_confidence(self, matched_word: str, text: str) -> float:
        """Calculate confidence score for trigger detection"""
        word_length = len(matched_word)
        text_length = len(text)

        # Base confidence on word length relative to text length
        base_confidence = min(word_length / max(text_length, 1), 1.0)

        # Boost confidence for exact matches
        if matched_word == text.strip():
            return 1.0

        # Boost confidence for multi-word phrases
        if len(matched_word.split()) > 1:
            base_confidence *= 1.2

        return min(base_confidence, 1.0)

    def _log_validation(self, result: ValidationResult, original_input: str):
        """Log validation results for monitoring and debugging"""
        self.validation_history.append(
            {
                "timestamp": result.timestamp,
                "input_length": len(original_input),
                "is_trigger": result.is_trigger,
                "category": result.category,
                "matched_word": result.matched_word,
                "confidence": result.confidence,
            }
        )

        # Keep only last 100 validations
        if len(self.validation_history) > 100:
            self.validation_history = self.validation_history[-100:]

        if result.is_trigger:
            logger.warning(
                f"Mental health trigger detected - Category: {result.category}, Word: {result.matched_word}, Confidence: {result.confidence:.2f}"
            )
        else:
            logger.debug("No mental health triggers detected")

    def _get_response_for_category(
        self, category: str, region: str = "australia"
    ) -> str:
        """Get appropriate response based on trigger category and region"""
        response_map = {
            "suicide_self_harm": self._suicide_response,
            "violence_harm_others": self._violence_response,
            "profanity_harmful": self._profanity_response,
            "substance_triggers": self._substance_response,
            "crisis_immediate": self._crisis_response,
        }

        response_func = response_map.get(category, self._default_response)
        return response_func(region)

    def _suicide_response(self, region: str = "australia") -> str:
        """Response for suicide/self-harm triggers"""
        contacts = self.emergency_contacts.get(
            region, self.emergency_contacts["australia"]
        )

        return f"""I'm concerned about what you've shared. You don't have to face this alone.

IMMEDIATE HELP AVAILABLE:

Crisis Line: {contacts.get('lifeline', contacts.get('suicide_prevention', 'Contact local emergency services'))}
Text Support: {contacts.get('crisis_text', 'Available in your region')}
Emergency: {contacts.get('emergency', '911/999/000')}

REMEMBER:

These feelings can change. Help is available 24/7. You matter and your life has value. Speaking to a counselor can provide immediate relief.

Please reach out to a trusted friend, family member, or healthcare provider right now. If you're in immediate danger, please contact emergency services."""

    def _violence_response(self, region: str = "australia") -> str:
        """Response for violence/harm to others triggers"""
        contacts = self.emergency_contacts.get(
            region, self.emergency_contacts["australia"]
        )

        return f"""I understand you might be feeling angry or frustrated, but I cannot provide guidance on harmful actions toward others.

IF YOU'RE HAVING THOUGHTS OF HARMING OTHERS:

Contact a mental health professional immediately
Call crisis support: {contacts.get('lifeline', 'local crisis line')}
Emergency services: {contacts.get('emergency', 'local emergency number')}

HEALTHY WAYS TO MANAGE ANGER:

Take deep breaths or count to ten
Physical exercise or go for a walk
Talk to a trusted friend or counselor
Write down your feelings

Professional support can help you work through these feelings constructively."""

    def _profanity_response(self, region: str = "australia") -> str:
        """Response for profanity/harmful language triggers"""
        return """I understand you might be frustrated or upset. It's okay to feel this way, and I'm here to help.

Let's focus on what's bothering you and how we can work through it together. Sometimes talking about difficult feelings can help us understand them better.

Would you like to share what's on your mind? I'm here to listen and support you."""

    def _substance_response(self, region: str = "australia") -> str:
        """Response for substance abuse triggers"""
        contacts = self.emergency_contacts.get(
            region, self.emergency_contacts["australia"]
        )

        aus_specific = (
            """Alcohol & Drug Information Service: 1800 250 015
DirectLine: 1800 888 236 (24/7)"""
            if region == "australia"
            else "Contact your local substance abuse helpline"
        )

        return f"""Substance use can significantly impact mental health and wellbeing. You don't have to handle this alone.

SUPPORT RESOURCES:

{aus_specific}
Crisis Support: {contacts.get('lifeline', 'local crisis line')}

CONSIDER:

Speaking with a healthcare provider about treatment options
Joining a support group
Talking to a counselor who specializes in addiction

Recovery is possible, and seeking help is a sign of strength. Many people have successfully overcome substance challenges with proper support."""

    def _crisis_response(self, region: str = "australia") -> str:
        """Response for immediate crisis situations"""
        contacts = self.emergency_contacts.get(
            region, self.emergency_contacts["australia"]
        )

        return f"""I can see you're in crisis right now. Please get immediate help:

CONTACT NOW:

Crisis Line: {contacts.get('lifeline', 'local crisis line')} (24/7)
Emergency: {contacts.get('emergency', 'local emergency number')}
Text Crisis Support: {contacts.get('crisis_text', 'available in your region')}

If you're in immediate physical danger, call emergency services right away.

You don't have to go through this alone. Crisis counselors are trained to help people in exactly your situation. Please reach out to one of these services right now."""

    def _default_response(self, region: str = "australia") -> str:
        """Default response for unrecognized categories"""
        contacts = self.emergency_contacts.get(
            region, self.emergency_contacts["australia"]
        )

        return f"""I understand you're going through something difficult right now.

SUPPORT IS AVAILABLE:

Talk to someone: {contacts.get('lifeline', 'local crisis line')}
Professional help: Consider speaking with a counselor or therapist
Trusted support: Reach out to friends, family, or community

Remember that seeking help is a positive step, and you don't have to face challenges alone."""