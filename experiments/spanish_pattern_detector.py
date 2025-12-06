"""
Spanish Pattern Detector
For Romance language (Spanish) theological translation
"""

import sys
sys.path.append('experiments')

from enhanced_pattern_detector import EnhancedPatternDetector
import numpy as np


class SpanishPatternDetector(EnhancedPatternDetector):
    """
    Spanish (Romance language) pattern detector.
    
    Predictions based on pattern analysis:
    - Moderate Love increase (+0.10-0.15)
    - Good English alignment
    - Consistent theological terms
    """
    
    def __init__(self):
        super().__init__()
        
        # Spanish theological terms with LJPW coordinates
        self.spanish_theological = {
            # God/Divine
            'Dios': [0.88, 0.90, 0.75, 0.98],  # God
            'Señor': [0.85, 0.90, 0.80, 0.95],  # Lord
            'Padre': [0.90, 0.85, 0.70, 0.92],  # Father
            'Hijo': [0.85, 0.88, 0.72, 0.90],  # Son
            
            # Kingdom/Reign
            'reino': [0.75, 0.90, 0.85, 0.88],  # kingdom
            'rey': [0.70, 0.88, 0.90, 0.85],  # king
            
            # Spirit
            'Espíritu': [0.90, 0.70, 0.60, 0.95],  # Spirit
            'Santo': [0.88, 0.88, 0.48, 0.95],  # Holy
            
            # Gospel/Message
            'evangelio': [0.90, 0.85, 0.70, 0.95],  # gospel
            'palabra': [0.75, 0.85, 0.70, 0.92],  # word
            
            # Faith/Belief
            'fe': [0.82, 0.75, 0.55, 0.88],  # faith
            'creer': [0.80, 0.73, 0.58, 0.85],  # believe
            
            # Baptism
            'bautismo': [0.70, 0.80, 0.60, 0.75],  # baptism
            'bautizar': [0.68, 0.78, 0.62, 0.73],  # baptize
            
            # Love/Mercy
            'amor': [0.95, 0.50, 0.30, 0.60],  # love
            'misericordia': [0.92, 0.70, 0.35, 0.85],  # mercy
            
            # Repentance
            'arrepentimiento': [0.75, 0.88, 0.50, 0.85],  # repentance
            'arrepentirse': [0.73, 0.86, 0.52, 0.83],  # repent
        }
        
        # Spanish phonetic characteristics
        self.spanish_phonetic_boost = {
            'vowels': 0.08,  # Romance languages have clear vowels
            'liquids': 0.06,  # l, r sounds
        }
        
        # Spanish grammatical markers
        self.spanish_particles = {
            'de': {'J': 0.08},  # of/from (genitive)
            'del': {'J': 0.08},  # of the
            'en': {'J': 0.05},  # in/on
            'con': {'L': 0.08},  # with (relational)
            'para': {'W': 0.08},  # for (purpose)
        }
    
    def calculate_field_signature(self, text: str, context=None):
        """
        Calculate LJPW signature with Spanish-specific analysis.
        """
        # Get base signature
        signature = super().calculate_field_signature(text, context)
        
        text_lower = text.lower()
        
        # 1. Theological term detection
        for term, coords in self.spanish_theological.items():
            if term.lower() in text_lower:
                # Moderate blend (less aggressive than Greek)
                signature['L'] = (signature['L'] * 0.5 + coords[0] * 0.5)
                signature['J'] = (signature['J'] * 0.5 + coords[1] * 0.5)
                signature['P'] = (signature['P'] * 0.5 + coords[2] * 0.5)
                signature['W'] = (signature['W'] * 0.5 + coords[3] * 0.5)
                signature['confidence'] += 0.3
                signature['evidence'].append(f"Spanish theological: {term}")
        
        # 2. Particle detection
        for particle, adjustments in self.spanish_particles.items():
            if particle in text_lower.split():  # Word boundary
                count = text_lower.split().count(particle)
                for dim, value in adjustments.items():
                    if dim == 'L':
                        signature['L'] += value * count * 0.5
                    elif dim == 'J':
                        signature['J'] += value * count * 0.5
                    elif dim == 'W':
                        signature['W'] += value * count * 0.5
                signature['confidence'] += 0.08 * count
                signature['evidence'].append(f"Spanish particle: {particle}")
        
        # 3. Romance language phonetic boost (moderate Love)
        vowel_count = sum(1 for c in text_lower if c in 'aeiouáéíóú')
        vowel_ratio = vowel_count / len(text) if len(text) > 0 else 0
        
        if vowel_ratio > 0.35:  # Spanish has high vowel content
            signature['L'] += self.spanish_phonetic_boost['vowels']
            signature['evidence'].append(f"Spanish phonetics (vowel ratio: {vowel_ratio:.2f})")
        
        # Normalize
        signature['L'] = np.clip(signature['L'], 0, 1)
        signature['J'] = np.clip(signature['J'], 0, 1)
        signature['P'] = np.clip(signature['P'], 0, 1)
        signature['W'] = np.clip(signature['W'], 0, 1)
        
        return signature
