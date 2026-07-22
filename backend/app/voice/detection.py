"""Voice activity detection module."""

from typing import Optional
import numpy as np


class VoiceActivityDetector:
    """Detects voice activity in audio streams.
    
    Identifies whether audio contains speech or is silence.
    """

    def __init__(self, energy_threshold: float = 300.0):
        """Initialize voice activity detector.
        
        Args:
            energy_threshold: Energy threshold for voice detection
        """
        self.energy_threshold = energy_threshold

    def detect(self, audio_chunk: bytes) -> bool:
        """Detect voice activity in audio chunk.
        
        Args:
            audio_chunk: Audio data
            
        Returns:
            True if voice detected
        """
        try:
            # Convert audio bytes to numpy array
            audio_array = np.frombuffer(audio_chunk, dtype=np.int16)
            # Calculate energy
            energy = np.sqrt(np.mean(np.square(audio_array)))
            # Check if energy exceeds threshold
            return energy > self.energy_threshold
        except Exception as e:
            print(f"Voice activity detection error: {e}")
            return False
