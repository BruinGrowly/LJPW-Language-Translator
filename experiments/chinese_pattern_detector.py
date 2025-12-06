"""
Mandarin Chinese Pattern Detector
Character-based semantic analysis with radical decomposition
"""

import sys
sys.path.append('experiments')

from enhanced_pattern_detector import EnhancedPatternDetector
import numpy as np


class ChinesePatternDetector(EnhancedPatternDetector):
    """
    Mandarin Chinese pattern detector.
    
    Character-based language with:
    - Radical semantics (character components carry meaning)
    - Tonal system (not captured in text)
    - Compact expression (fewer characters, dense meaning)
    """
    
    def __init__(self):
        super().__init__()
        
        # Core theological terms
        self.chinese_theological = {
            # God/Divine
            '神': [0.88, 0.90, 0.75, 0.98],  # God/spirit
            '主': [0.85, 0.90, 0.80, 0.95],  # Lord
            '父': [0.90, 0.85, 0.70, 0.92],  # Father
            '子': [0.85, 0.88, 0.72, 0.90],  # Son
            
            # Kingdom
            '国': [0.75, 0.90, 0.85, 0.88],  # kingdom/nation
            '王': [0.70, 0.88, 0.90, 0.85],  # king
            
            # Spirit
            '灵': [0.90, 0.70, 0.60, 0.95],  # spirit/soul
            '圣': [0.88, 0.88, 0.48, 0.95],  # holy/saint
            '圣灵': [0.90, 0.70, 0.60, 0.95],  # Holy Spirit
            
            # Gospel/Message
            '福音': [0.90, 0.85, 0.70, 0.95],  # gospel (blessing-sound)
            '道': [0.75, 0.85, 0.70, 0.92],  # way/word/Tao
            
            # Faith/Belief
            '信': [0.82, 0.75, 0.55, 0.88],  # faith/believe
            
            # Baptism
            '洗': [0.70, 0.80, 0.60, 0.75],  # wash/baptize
            '施洗': [0.70, 0.80, 0.60, 0.75],  # baptize (administer-wash)
            
            # Love/Mercy
            '爱': [0.95, 0.50, 0.30, 0.60],  # love
            '慈': [0.92, 0.70, 0.35, 0.85],  # mercy/compassion
            
            # Repentance
            '悔改': [0.75, 0.88, 0.50, 0.85],  # repent (regret-change)
        }
        
        # Radical semantics (character components)
        self.radical_semantics = {
            '心': {'L': 0.25},  # Heart radical (emotional)
            '言': {'W': 0.20},  # Speech radical (wisdom/communication)
            '人': {'L': 0.15},  # Person radical (relational)
            '手': {'P': 0.20},  # Hand radical (action)
            '水': {'L': 0.10, 'J': 0.10},  # Water radical (cleansing/life)
            '示': {'W': 0.25, 'J': 0.20},  # Spirit/altar radical (divine)
            '王': {'P': 0.25, 'J': 0.20},  # King radical (authority)
        }
        
        # Common Chinese particles/function words
        self.chinese_particles = {
            '的': {'J': 0.05},  # Possessive/attributive particle
            '了': {'P': 0.08},  # Completed action particle
            '在': {'J': 0.05},  # At/in (location)
            '就': {'P': 0.10},  # Then/immediately (action sequence)
            '都': {'J': 0.08},  # All/both (totality)
        }
    
    def analyze_radicals(self, char: str) -> dict:
        """
        Analyze character radicals for semantic content.
        Note: This is simplified - full radical decomposition requires a database.
        """
        adjustments = {'L': 0, 'J': 0, 'P': 0, 'W': 0}
        
        # Check if character contains known radicals
        for radical, values in self.radical_semantics.items():
            if radical in char:
                for dim, value in values.items():
                    adjustments[dim] += value * 0.3  # Moderate boost
        
        return adjustments
    
    def calculate_field_signature(self, text: str, context=None):
        """
        Calculate LJPW signature with Chinese-specific analysis.
        """
        # Get base signature
        signature = super().calculate_field_signature(text, context)
        
        # 1. Theological term detection
        for term, coords in self.chinese_theological.items():
            if term in text:
                # Strong blend for Chinese (compact language)
                signature['L'] = (signature['L'] * 0.4 + coords[0] * 0.6)
                signature['J'] = (signature['J'] * 0.4 + coords[1] * 0.6)
                signature['P'] = (signature['P'] * 0.4 + coords[2] * 0.6)
                signature['W'] = (signature['W'] * 0.4 + coords[3] * 0.6)
                signature['confidence'] += 0.4
                signature['evidence'].append(f"Chinese theological: {term}")
        
        # 2. Particle detection
        for particle, adjustments in self.chinese_particles.items():
            if particle in text:
                count = text.count(particle)
                for dim, value in adjustments.items():
                    if dim == 'J':
                        signature['J'] += value * count * 0.5
                    elif dim == 'P':
                        signature['P'] += value * count * 0.5
                signature['confidence'] += 0.05 * count
                signature['evidence'].append(f"Chinese particle: {particle}")
        
        # 3. Radical analysis (simplified)
        radical_adjustments = {'L': 0, 'J': 0, 'P': 0, 'W': 0}
        for char in text:
            char_adj = self.analyze_radicals(char)
            for dim in ['L', 'J', 'P', 'W']:
                radical_adjustments[dim] += char_adj[dim]
        
        # Apply radical adjustments (normalized by text length)
        if len(text) > 0:
            for dim in ['L', 'J', 'P', 'W']:
                signature[dim] += radical_adjustments[dim] / len(text)
        
        if any(radical_adjustments.values()):
            signature['evidence'].append("Chinese radical semantics")
        
        # 4. Compact language boost
        # Chinese is very compact - fewer characters, more meaning
        # This tends to increase Wisdom (integration/complexity)
        char_count = len(text)
        if char_count < 30:  # Short but meaningful
            signature['W'] += 0.10
            signature['evidence'].append("Chinese compact expression")
        
        # Normalize
        signature['L'] = np.clip(signature['L'], 0, 1)
        signature['J'] = np.clip(signature['J'], 0, 1)
        signature['P'] = np.clip(signature['P'], 0, 1)
        signature['W'] = np.clip(signature['W'], 0, 1)
        
        return signature
