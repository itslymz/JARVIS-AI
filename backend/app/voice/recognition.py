"""Speech recognition module."""

from typing import Optional
import speech_recognition as sr
from app.config import settings


class SpeechRecognizer:
    """Speech recognition handler.
    
    Converts audio input to text using Google Speech Recognition API.
    """

    def __init__(self, language: str = "en-US"):
        """Initialize speech recognizer.
        
        Args:
            language: Language code (e.g., 'en-US', 'es-ES')
        """
        self.recognizer = sr.Recognizer()
        self.language = language
        self.microphone = sr.Microphone()

    def recognize_from_audio(self, audio_file_path: str) -> Optional[str]:
        """Recognize speech from audio file.
        
        Args:
            audio_file_path: Path to audio file
            
        Returns:
            Recognized text or None
        """
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio, language=self.language)
                return text
        except sr.UnknownValueError:
            print("Audio not understood")
            return None
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            return None

    def recognize_from_microphone(self) -> Optional[str]:
        """Recognize speech from microphone.
        
        Returns:
            Recognized text or None
        """
        try:
            with self.microphone as source:
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=10)
                text = self.recognizer.recognize_google(audio, language=self.language)
                print(f"Heard: {text}")
                return text
        except sr.UnknownValueError:
            print("Audio not understood")
            return None
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            return None
        except sr.WaitTimeoutError:
            print("Timeout waiting for audio")
            return None
