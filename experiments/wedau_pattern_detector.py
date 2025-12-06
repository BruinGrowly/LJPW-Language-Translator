"""
Wedau Pattern Detector - Tuned
Based on comprehensive comparison results from Mark Chapter 1
"""

import sys
sys.path.append('experiments')

from enhanced_pattern_detector import EnhancedPatternDetector
import numpy as np
import re


class WedauPatternDetector(EnhancedPatternDetector):
    """
    Wedau-specific pattern detector.
    
    Tuned based on comprehensive comparison findings:
    - Higher Love tendency (+0.172 average)
    - Consistent Power in actions (-0.088 average)
    - Theological terms need special handling
    """
    
    def __init__(self):
        super().__init__()
        
        # Wedau-specific phonetic adjustments
        self.wedau_phonetic_boost = {
            'soft_vowels': 0.15,  # Wedau has softer phonetics
            'liquids': 0.10,      # More liquid sounds
            'nasals': 0.08        # Nasal consonants
        }
        
        # Wedau grammatical particles
        self.wedau_particles = {
            'ana': {'L': 0.15, 'J': 0.10},  # Genitive/possessive (of/from)
            'i': {'L': 0.05},                # Subject marker
            'ma': {'J': 0.08},               # Conjunction (and)
            'da': {'J': 0.10},               # Subordinator (that/so that)
            'ipa': {'W': 0.12},              # Quotative (saying)
        }
        
        # Wedau theological terms (from actual text analysis)
        self.wedau_theological = {
            'God': [0.88, 0.90, 0.75, 0.98],
            'Yesu': [0.88, 0.90, 0.75, 0.98],  # Jesus
            'Keriso': [0.88, 0.90, 0.75, 0.98],  # Christ
            'vibadana': [0.75, 0.90, 0.85, 0.88],  # kingdom
            'Tuyeghana Ahiahina': [0.90, 0.85, 0.70, 0.95],  # good news/gospel
            'Aruwa Vivivireina': [0.90, 0.70, 0.60, 0.95],  # Holy Spirit
            'babataito': [0.70, 0.80, 0.60, 0.75],  # baptize
            'pari': [0.60, 0.70, 0.50, 0.80],  # synagogue/place
            'Sabate': [0.65, 0.85, 0.55, 0.75],  # Sabbath
        }
        
        # Wedau action verbs (Power dimension)
        self.wedau_actions = {
            'i nae': {'P': 0.40},      # went/came
            'i riwa': {'P': 0.35, 'W': 0.20},  # said/spoke
            'i voterei': {'P': 0.30},  # left/departed
            'i yawahana': {'P': 0.45, 'L': 0.15},  # healed
            'i hopunei': {'P': 0.50},  # expelled/cast out
            'i babataitoi': {'P': 0.40, 'J': 0.20},  # baptized
        }
        
        # Wedau reduplication patterns (emphasis/intensity)
        self.reduplication_patterns = [
            r'(\w+)\1',  # Full reduplication
            r'(\w{2,})-\1',  # Hyphenated reduplication
        ]
    
    def calculate_field_signature(self, text: str, context=None):
        """
        Calculate LJPW signature with Wedau-specific adjustments.
        """
        # Get base signature from parent class
        signature = super().calculate_field_signature(text, context)
        
        # Apply Wedau-specific adjustments
        text_lower = text.lower()
        
        # 1. Particle detection
        for particle, adjustments in self.wedau_particles.items():
            if particle in text_lower:
                count = text_lower.count(particle)
                for dim, value in adjustments.items():
                    if dim == 'L':
                        signature['L'] += value * count * 0.5
                    elif dim == 'J':
                        signature['J'] += value * count * 0.5
                    elif dim == 'W':
                        signature['W'] += value * count * 0.5
                signature['confidence'] += 0.1 * count
                signature['evidence'].append(f"Wedau particle '{particle}' ({count}x)")
        
        # 2. Theological term detection
        for term, coords in self.wedau_theological.items():
            if term.lower() in text_lower:
                # Blend with theological coordinates
                signature['L'] = (signature['L'] + coords[0]) / 2
                signature['J'] = (signature['J'] + coords[1]) / 2
                signature['P'] = (signature['P'] + coords[2]) / 2
                signature['W'] = (signature['W'] + coords[3]) / 2
                signature['confidence'] += 0.3
                signature['evidence'].append(f"Wedau theological term: {term}")
        
        # 3. Action verb detection
        for action, adjustments in self.wedau_actions.items():
            if action in text_lower:
                for dim, value in adjustments.items():
                    if dim == 'P':
                        signature['P'] += value * 0.5
                    elif dim == 'L':
                        signature['L'] += value * 0.5
                    elif dim == 'W':
                        signature['W'] += value * 0.5
                signature['confidence'] += 0.15
                signature['evidence'].append(f"Wedau action: {action}")
        
        # 4. Reduplication detection (emphasis)
        for pattern in self.reduplication_patterns:
            if re.search(pattern, text):
                signature['W'] += 0.15  # Emphasis = Wisdom
                signature['J'] += 0.10  # Emphasis = Precision
                signature['confidence'] += 0.15
                signature['evidence'].append("Wedau reduplication (emphasis)")
                break
        
        # 5. General Wedau phonetic boost (softer language)
        # Count soft vowels
        soft_vowels = sum(1 for c in text_lower if c in 'aeiou')
        vowel_ratio = soft_vowels / len(text) if len(text) > 0 else 0
        
        if vowel_ratio > 0.4:  # High vowel content
            signature['L'] += self.wedau_phonetic_boost['soft_vowels']
            signature['P'] -= 0.10  # Reduce Power for soft phonetics
            signature['evidence'].append(f"Wedau soft phonetics (vowel ratio: {vowel_ratio:.2f})")
        
        # Normalize
        signature['L'] = np.clip(signature['L'], 0, 1)
        signature['J'] = np.clip(signature['J'], 0, 1)
        signature['P'] = np.clip(signature['P'], 0, 1)
        signature['W'] = np.clip(signature['W'], 0, 1)
        
        return signature


def test_wedau_detector():
    """Test the tuned Wedau detector."""
    detector = WedauPatternDetector()
    
    test_cases = [
        "Weꞌi yamna God natuna Yesu Keriso Tuyeghana Ahiahina me ivi karenanei.",
        "John i bababataitohi ma God riwana i dimedimei",
        "Yesu i nae au Galili ma rava auwarihi",
        "God ana vibadana vouna, rava aubaihi yamna i turiyai",
    ]
    
    print("="*80)
    print("WEDAU DETECTOR TEST")
    print("="*80)
    
    for text in test_cases:
        sig = detector.calculate_field_signature(text)
        print(f"\nText: {text[:60]}...")
        print(f"Coords: L={sig['L']:.3f}, J={sig['J']:.3f}, P={sig['P']:.3f}, W={sig['W']:.3f}")
        print(f"Confidence: {sig['confidence']:.2f}")
        print(f"Evidence: {', '.join(sig['evidence'][:3])}")


if __name__ == "__main__":
    test_wedau_detector()
