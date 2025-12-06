"""
Greek (Koine) Pattern Detector
For Biblical Greek theological validation
"""

import sys
sys.path.append('experiments')

from enhanced_pattern_detector import EnhancedPatternDetector
import numpy as np
import re


class GreekPatternDetector(EnhancedPatternDetector):
    """
    Biblical Greek (Koine) pattern detector.
    
    Focuses on:
    - Theological vocabulary
    - Morphological patterns (case, number, gender)
    - Syntactic structures
    """
    
    def __init__(self):
        super().__init__()
        
        # Core theological terms with LJPW coordinates
        self.greek_theological = {
            # God/Divine
            'θεός': [0.88, 0.90, 0.75, 0.98],  # theos (God)
            'κύριος': [0.85, 0.90, 0.80, 0.95],  # kyrios (Lord)
            'πατήρ': [0.90, 0.85, 0.70, 0.92],  # pater (Father)
            'υἱός': [0.85, 0.88, 0.72, 0.90],  # huios (Son)
            
            # Kingdom/Reign
            'βασιλεία': [0.75, 0.90, 0.85, 0.88],  # basileia (kingdom)
            'βασιλεύς': [0.70, 0.88, 0.90, 0.85],  # basileus (king)
            
            # Spirit
            'πνεῦμα': [0.90, 0.70, 0.60, 0.95],  # pneuma (spirit)
            'ἅγιος': [0.88, 0.88, 0.48, 0.95],  # hagios (holy)
            
            # Love
            'ἀγάπη': [0.95, 0.50, 0.30, 0.60],  # agape (divine love)
            'φιλέω': [0.85, 0.55, 0.40, 0.65],  # phileo (brotherly love)
            
            # Gospel/Message
            'εὐαγγέλιον': [0.90, 0.85, 0.70, 0.95],  # euangelion (gospel/good news)
            'λόγος': [0.75, 0.85, 0.70, 0.92],  # logos (word)
            'κήρυγμα': [0.80, 0.82, 0.75, 0.88],  # kerygma (proclamation)
            
            # Faith/Belief
            'πίστις': [0.82, 0.75, 0.55, 0.88],  # pistis (faith)
            'πιστεύω': [0.80, 0.73, 0.58, 0.85],  # pisteuo (believe)
            
            # Baptism
            'βάπτισμα': [0.70, 0.80, 0.60, 0.75],  # baptisma (baptism)
            'βαπτίζω': [0.68, 0.78, 0.62, 0.73],  # baptizo (baptize)
            
            # Teaching/Authority
            'διδάσκω': [0.65, 0.75, 0.60, 0.85],  # didasko (teach)
            'ἐξουσία': [0.60, 0.85, 0.88, 0.82],  # exousia (authority)
            'γραμματεύς': [0.55, 0.80, 0.70, 0.85],  # grammateus (scribe)
            
            # Repentance
            'μετάνοια': [0.75, 0.88, 0.50, 0.85],  # metanoia (repentance)
            'μετανοέω': [0.73, 0.86, 0.52, 0.83],  # metanoeo (repent)
            
            # Demon/Unclean
            'δαιμόνιον': [0.30, 0.40, 0.85, 0.45],  # daimonion (demon)
            'ἀκάθαρτος': [0.25, 0.45, 0.80, 0.40],  # akathartos (unclean)
        }
        
        # Case markers (Greek morphology)
        self.case_semantics = {
            'nominative': {'J': 0.15},  # Subject (doer)
            'genitive': {'J': 0.20, 'W': 0.10},  # Possession/source
            'dative': {'L': 0.20},  # Indirect object (giving)
            'accusative': {'P': 0.15},  # Direct object (receiving)
        }
        
        # Verb tenses
        self.tense_semantics = {
            'aorist': {'P': 0.15},  # Completed action
            'present': {'P': 0.10, 'W': 0.10},  # Ongoing action
            'perfect': {'J': 0.15, 'W': 0.15},  # Completed with ongoing effect
            'future': {'W': 0.20},  # Anticipation
        }
        
        # Common Greek particles
        self.greek_particles = {
            'καί': {'J': 0.05},  # kai (and)
            'δέ': {'J': 0.08},  # de (but/and)
            'γάρ': {'W': 0.12},  # gar (for/because)
            'οὖν': {'W': 0.15},  # oun (therefore)
            'ἀλλά': {'J': 0.10},  # alla (but)
        }
    
    def calculate_field_signature(self, text: str, context=None):
        """
        Calculate LJPW signature with Greek-specific analysis.
        """
        # Get base signature
        signature = super().calculate_field_signature(text, context)
        
        text_lower = text.lower()
        
        # 1. Theological term detection
        theological_found = False
        for term, coords in self.greek_theological.items():
            if term in text_lower:
                # Strong blend with theological coordinates
                signature['L'] = (signature['L'] * 0.3 + coords[0] * 0.7)
                signature['J'] = (signature['J'] * 0.3 + coords[1] * 0.7)
                signature['P'] = (signature['P'] * 0.3 + coords[2] * 0.7)
                signature['W'] = (signature['W'] * 0.3 + coords[3] * 0.7)
                signature['confidence'] += 0.4
                signature['evidence'].append(f"Greek theological: {term}")
                theological_found = True
        
        # 2. Particle detection
        for particle, adjustments in self.greek_particles.items():
            if particle in text_lower:
                count = text_lower.count(particle)
                for dim, value in adjustments.items():
                    if dim == 'J':
                        signature['J'] += value * count * 0.5
                    elif dim == 'W':
                        signature['W'] += value * count * 0.5
                signature['confidence'] += 0.08 * count
                signature['evidence'].append(f"Greek particle: {particle}")
        
        # 3. Detect article patterns (ὁ, ἡ, τό, etc.)
        if re.search(r'[ὁἡτό]', text):
            signature['J'] += 0.10  # Definiteness = Precision
            signature['evidence'].append("Greek article (definiteness)")
        
        # 4. Detect genitive constructions (τοῦ, τῆς, etc.)
        if re.search(r'τοῦ|τῆς|τῶν', text):
            signature['J'] += 0.15
            signature['W'] += 0.10
            signature['evidence'].append("Greek genitive construction")
        
        # 5. Theological boost for divine names
        if any(term in text_lower for term in ['θεός', 'κύριος', 'πατήρ']):
            signature['L'] += 0.15
            signature['W'] += 0.20
            signature['evidence'].append("Divine name detected")
        
        # Normalize
        signature['L'] = np.clip(signature['L'], 0, 1)
        signature['J'] = np.clip(signature['J'], 0, 1)
        signature['P'] = np.clip(signature['P'], 0, 1)
        signature['W'] = np.clip(signature['W'], 0, 1)
        
        return signature


def test_greek_detector():
    """Test the Greek detector."""
    detector = GreekPatternDetector()
    
    test_cases = [
        "Ἀρχὴ τοῦ εὐαγγελίου Ἰησοῦ Χριστοῦ",  # Mark 1:1
        "ἡ βασιλεία τοῦ θεοῦ",  # Kingdom of God
        "τὸ πνεῦμα τὸ ἅγιον",  # Holy Spirit
        "ἀγάπη θεοῦ",  # Love of God
        "μετανοεῖτε καὶ πιστεύετε",  # Repent and believe
    ]
    
    print("="*80)
    print("GREEK DETECTOR TEST")
    print("="*80)
    
    for text in test_cases:
        sig = detector.calculate_field_signature(text)
        print(f"\nText: {text}")
        print(f"Coords: L={sig['L']:.3f}, J={sig['J']:.3f}, P={sig['P']:.3f}, W={sig['W']:.3f}")
        print(f"Confidence: {sig['confidence']:.2f}")
        print(f"Evidence: {', '.join(sig['evidence'][:3])}")


if __name__ == "__main__":
    test_greek_detector()
