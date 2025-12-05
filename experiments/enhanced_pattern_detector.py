"""
Enhanced Pattern Detection for Pure Meaning Translation
Refines semantic field signature detection with advanced linguistic analysis.
"""

import json
import numpy as np
import re
from collections import Counter, defaultdict

# Natural Equilibrium
PHI_INV = 1 / ((1 + np.sqrt(5)) / 2)
SQRT2_M1 = np.sqrt(2) - 1
E_M2 = np.e - 2
LN2 = np.log(2)
EQUILIBRIUM = np.array([PHI_INV, SQRT2_M1, E_M2, LN2])


class EnhancedPatternDetector:
    """Advanced pattern detection for semantic field signatures."""
    
    def __init__(self):
        # Phonetic feature mappings
        self.soft_phonemes = set('aeiouywh')
        self.harsh_phonemes = set('kgtdpb')
        self.liquid_phonemes = set('lrmn')
        self.fricative_phonemes = set('fvszsh')
        
        # Semantic markers (language-agnostic patterns)
        self.divine_markers = {
            'god', 'yesu', 'jesus', 'christ', 'keriso', 'lord', 'taumi',
            'holy', 'sacred', 'divine', 'spirit', 'aruwa', 'vivivire'
        }
        
        self.power_markers = {
            'king', 'kingdom', 'vibadana', 'rule', 'reign', 'authority',
            'power', 'force', 'strength', 'might'
        }
        
        self.wisdom_markers = {
            'teach', 'learn', 'know', 'understand', 'wise', 'wisdom',
            'truth', 'knowledge', 'haraman'
        }
        
        self.love_markers = {
            'love', 'compassion', 'mercy', 'grace', 'kindness',
            'gentle', 'tender', 'care', 'nuwabo'
        }
        
        self.justice_markers = {
            'just', 'justice', 'right', 'law', 'order', 'fair',
            'raugagayo', 'righteous'
        }
        
        self.negative_markers = {
            'sin', 'wrong', 'evil', 'bad', 'apoapoe', 'ghoha',
            'error', 'fault', 'transgression'
        }
    
    def analyze_phonetic_profile(self, text):
        """Analyze phonetic characteristics of text."""
        text_lower = text.lower()
        total_chars = len([c for c in text_lower if c.isalpha()])
        
        if total_chars == 0:
            return {}
        
        soft_count = sum(1 for c in text_lower if c in self.soft_phonemes)
        harsh_count = sum(1 for c in text_lower if c in self.harsh_phonemes)
        liquid_count = sum(1 for c in text_lower if c in self.liquid_phonemes)
        fricative_count = sum(1 for c in text_lower if c in self.fricative_phonemes)
        
        return {
            'soft_ratio': soft_count / total_chars,
            'harsh_ratio': harsh_count / total_chars,
            'liquid_ratio': liquid_count / total_chars,
            'fricative_ratio': fricative_count / total_chars,
            'dominant': max([
                ('soft', soft_count),
                ('harsh', harsh_count),
                ('liquid', liquid_count),
                ('fricative', fricative_count)
            ], key=lambda x: x[1])[0]
        }
    
    def analyze_morphological_structure(self, text):
        """Analyze word structure and morphology."""
        words = text.split()
        
        if not words:
            return {}
        
        avg_word_length = sum(len(w) for w in words) / len(words)
        
        # Detect reduplication (common in many languages for emphasis)
        reduplication = any(
            words[i] == words[i+1] 
            for i in range(len(words)-1)
        )
        
        # Detect compound words (hyphens, long words)
        compounds = sum(1 for w in words if '-' in w or len(w) > 10)
        
        # Syllable complexity (rough estimate)
        vowel_clusters = sum(
            1 for w in words 
            for i in range(len(w)-1) 
            if w[i] in 'aeiou' and w[i+1] in 'aeiou'
        )
        
        return {
            'avg_word_length': avg_word_length,
            'reduplication': reduplication,
            'compound_ratio': compounds / len(words),
            'vowel_clusters': vowel_clusters,
            'complexity': 'high' if avg_word_length > 8 else 'moderate' if avg_word_length > 5 else 'low'
        }
    
    def detect_semantic_markers(self, text, context=None):
        """Detect semantic category markers."""
        text_lower = text.lower()
        context_lower = context.lower() if context else ""
        combined = text_lower + " " + context_lower
        
        markers_found = {
            'divine': sum(1 for m in self.divine_markers if m in combined),
            'power': sum(1 for m in self.power_markers if m in combined),
            'wisdom': sum(1 for m in self.wisdom_markers if m in combined),
            'love': sum(1 for m in self.love_markers if m in combined),
            'justice': sum(1 for m in self.justice_markers if m in combined),
            'negative': sum(1 for m in self.negative_markers if m in combined)
        }
        
        total_markers = sum(markers_found.values())
        
        if total_markers > 0:
            return {
                'markers': markers_found,
                'dominant': max(markers_found.items(), key=lambda x: x[1])[0],
                'confidence': min(total_markers / 3.0, 1.0)
            }
        
        return {'markers': markers_found, 'dominant': None, 'confidence': 0.0}
    
    def calculate_field_signature(self, text, context=None):
        """Calculate enhanced semantic field signature."""
        # Initialize signature
        signature = {
            'L': 0.5,
            'J': 0.5,
            'P': 0.5,
            'W': 0.5,
            'confidence': 0.0,
            'evidence': []
        }
        
        # Phonetic analysis
        phonetic = self.analyze_phonetic_profile(text)
        if phonetic:
            if phonetic['soft_ratio'] > 0.5:
                signature['L'] += 0.20 * phonetic['soft_ratio']
                signature['P'] -= 0.15 * phonetic['soft_ratio']
                signature['confidence'] += 0.2
                signature['evidence'].append(f"Soft phonetics ({phonetic['soft_ratio']:.2f})")
            
            if phonetic['harsh_ratio'] > 0.25:
                signature['P'] += 0.20 * phonetic['harsh_ratio']
                signature['J'] += 0.15 * phonetic['harsh_ratio']
                signature['confidence'] += 0.2
                signature['evidence'].append(f"Harsh phonetics ({phonetic['harsh_ratio']:.2f})")
            
            if phonetic['liquid_ratio'] > 0.2:
                signature['L'] += 0.10 * phonetic['liquid_ratio']
                signature['W'] += 0.10 * phonetic['liquid_ratio']
                signature['confidence'] += 0.1
                signature['evidence'].append(f"Liquid phonemes ({phonetic['liquid_ratio']:.2f})")
        
        # Morphological analysis
        morphology = self.analyze_morphological_structure(text)
        if morphology:
            if morphology['reduplication']:
                signature['W'] += 0.15
                signature['J'] += 0.10
                signature['confidence'] += 0.2
                signature['evidence'].append("Reduplication (emphasis)")
            
            if morphology['complexity'] == 'high':
                signature['W'] += 0.15
                signature['confidence'] += 0.15
                signature['evidence'].append("High morphological complexity")
            
            if morphology['compound_ratio'] > 0.3:
                signature['W'] += 0.10
                signature['confidence'] += 0.1
                signature['evidence'].append(f"Compound words ({morphology['compound_ratio']:.2f})")
        
        # Semantic marker analysis
        markers = self.detect_semantic_markers(text, context)
        if markers['dominant']:
            marker_strength = markers['confidence']
            
            if markers['dominant'] == 'divine':
                signature['L'] += 0.30 * marker_strength
                signature['J'] += 0.25 * marker_strength
                signature['W'] += 0.35 * marker_strength
                signature['confidence'] += 0.4
                signature['evidence'].append(f"Divine markers (strength: {marker_strength:.2f})")
            
            elif markers['dominant'] == 'power':
                signature['P'] += 0.35 * marker_strength
                signature['J'] += 0.25 * marker_strength
                signature['W'] += 0.20 * marker_strength
                signature['confidence'] += 0.4
                signature['evidence'].append(f"Power markers (strength: {marker_strength:.2f})")
            
            elif markers['dominant'] == 'wisdom':
                signature['W'] += 0.40 * marker_strength
                signature['J'] += 0.20 * marker_strength
                signature['confidence'] += 0.4
                signature['evidence'].append(f"Wisdom markers (strength: {marker_strength:.2f})")
            
            elif markers['dominant'] == 'love':
                signature['L'] += 0.40 * marker_strength
                signature['P'] -= 0.15 * marker_strength
                signature['W'] += 0.20 * marker_strength
                signature['confidence'] += 0.4
                signature['evidence'].append(f"Love markers (strength: {marker_strength:.2f})")
            
            elif markers['dominant'] == 'justice':
                signature['J'] += 0.40 * marker_strength
                signature['W'] += 0.25 * marker_strength
                signature['P'] += 0.15 * marker_strength
                signature['confidence'] += 0.4
                signature['evidence'].append(f"Justice markers (strength: {marker_strength:.2f})")
            
            elif markers['dominant'] == 'negative':
                signature['L'] -= 0.30 * marker_strength
                signature['J'] -= 0.30 * marker_strength
                signature['confidence'] += 0.4
                signature['evidence'].append(f"Negative markers (strength: {marker_strength:.2f})")
        
        # Normalize to [0, 1]
        signature['L'] = np.clip(signature['L'], 0, 1)
        signature['J'] = np.clip(signature['J'], 0, 1)
        signature['P'] = np.clip(signature['P'], 0, 1)
        signature['W'] = np.clip(signature['W'], 0, 1)
        
        signature['coordinates'] = np.array([
            signature['L'],
            signature['J'],
            signature['P'],
            signature['W']
        ])
        
        # Calculate field properties
        signature['equilibrium_distance'] = float(np.linalg.norm(
            signature['coordinates'] - EQUILIBRIUM
        ))
        
        # Emergent dimensions
        cw = (signature['L'] + signature['W']) - (signature['J'] + signature['P'])
        lp = (signature['L'] + signature['P']) - (signature['J'] + signature['W'])
        
        emergent = []
        if cw > 0.2:
            emergent.append('Soft')
        elif cw < -0.2:
            emergent.append('Hard')
        
        if lp > 0.2:
            emergent.append('Passionate')
        elif lp < -0.2:
            emergent.append('Measured')
        
        signature['emergent_dimension'] = ', '.join(emergent) if emergent else 'Balanced'
        
        return signature


def test_enhanced_detector():
    """Test the enhanced pattern detector."""
    print("="*70)
    print("ENHANCED PATTERN DETECTION TEST")
    print("="*70)
    
    detector = EnhancedPatternDetector()
    
    test_cases = [
        {
            'text': 'Tuyeghana Ahiahina',
            'context': 'Good news/Gospel',
            'expected': 'Divine message, soft, high wisdom'
        },
        {
            'text': 'Aruwa Vivivireinei',
            'context': 'Holy Spirit',
            'expected': 'Divine, spiritual, very high L+W, low P'
        },
        {
            'text': 'vibadana vouna',
            'context': 'Kingdom',
            'expected': 'Power, justice, governance'
        },
        {
            'text': 'apoapoe',
            'context': 'sin/wrong',
            'expected': 'Low L+J, negative'
        },
        {
            'text': 'God God Taumi',
            'context': 'Lord God',
            'expected': 'Divine, reduplication emphasis'
        }
    ]
    
    print("\n")
    for i, test in enumerate(test_cases, 1):
        print(f"Test {i}: '{test['text']}'")
        print(f"Context: {test['context']}")
        print(f"Expected: {test['expected']}\n")
        
        signature = detector.calculate_field_signature(test['text'], test['context'])
        
        print(f"Detected Signature:")
        print(f"  L={signature['L']:.3f}, J={signature['J']:.3f}, "
              f"P={signature['P']:.3f}, W={signature['W']:.3f}")
        print(f"  Confidence: {signature['confidence']:.2f}")
        print(f"  Equilibrium distance: {signature['equilibrium_distance']:.3f}")
        print(f"  Emergent: {signature['emergent_dimension']}")
        print(f"\nEvidence:")
        for evidence in signature['evidence']:
            print(f"  - {evidence}")
        print(f"\n{'-'*70}\n")
    
    print("="*70)
    print("ENHANCED DETECTION COMPLETE")
    print("="*70)


if __name__ == "__main__":
    test_enhanced_detector()
