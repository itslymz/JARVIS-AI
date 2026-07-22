"""Text-to-speech synthesis module."""

import pyttsx3
from typing import Optional
from app.config import settings


class TextToSpeech:
    """Text-to-speech handler.
    
    Converts text to natural speech using pyttsx3 or cloud providers.
    """

    def __init__(self, voice_provider: str = "pyttsx3"):
        """Initialize text-to-speech.
        
        Args:
            voice_provider: Provider name (pyttsx3, google, azure, etc.)
        """
        self.voice_provider = voice_provider
        
        if voice_provider == "pyttsx3":
            self.engine = pyttsx3.init()
            # Configure voice properties
            self.engine.setProperty('rate', 150)  # Speed
            self.engine.setProperty('volume', 0.9)  # Volume
            
            # Set voice (prefer female)
            voices = self.engine.getProperty('voices')
            if len(voices) > 1:
                self.engine.setProperty('voice', voices[1].id)

    def speak(self, text: str, save_to_file: Optional[str] = None) -> bool:
        """Speak text.
        
        Args:
            text: Text to speak
            save_to_file: Optional file path to save audio
            
        Returns:
            True if successful
        """
        try:
            if self.voice_provider == "pyttsx3":
                if save_to_file:
                    self.engine.save_to_file(text, save_to_file)
                self.engine.say(text)
                self.engine.runAndWait()
                return True
        except Exception as e:
            print(f"Text-to-speech error: {e}")
            return False

    def set_rate(self, rate: int) -> None:
        """Set speech rate.
        
        Args:
            rate: Speech rate (50-300)
        """
        if self.voice_provider == "pyttsx3":
            self.engine.setProperty('rate', max(50, min(300, rate)))

    def set_volume(self, volume: float) -> None:
        """Set volume.
        
        Args:
            volume: Volume level (0.0-1.0)
        """
        if self.voice_provider == "pyttsx3":
            self.engine.setProperty('volume', max(0.0, min(1.0, volume)))
