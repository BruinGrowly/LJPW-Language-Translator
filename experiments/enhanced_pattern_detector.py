"""
Enhanced Pattern Detection for Pure Meaning Translation
Refines semantic field signature detection with advanced linguistic analysis.
Phase 2: Integrated with Context and Multi-Layer Combination.
"""

import numpy as np
import re
from typing import Dict, List, Optional, Any, Set

# Import Phase 2 modules
from context_integrator import ContextIntegrator
from multi_layer_combiner import MultiLayerCombiner

# Natural Equilibrium Constants
PHI_INV = 1 / ((1 + np.sqrt(5)) / 2)
SQRT2_M1 = np.sqrt(2) - 1
E_M2 = np.e - 2
LN2 = np.log(2)
EQUILIBRIUM = np.array([PHI_INV, SQRT2_M1, E_M2, LN2])


class EnhancedPatternDetector:
    """Advanced pattern detection for semantic field signatures."""
    
    def __init__(self):
        # Phase 2: Initialize context and combination modules
        self.context_integrator = ContextIntegrator()
        self.multi_layer_combiner = MultiLayerCombiner()
        
        # Phonetic feature mappings
        # Phonetic feature mappings
        self.soft_phonemes: Set[str] = set('aeiouywh')
        self.harsh_phonemes: Set[str] = set('kgtdpb')
        self.liquid_phonemes: Set[str] = set('lrmn')
        self.fricative_phonemes: Set[str] = set('fvszsh')
        
        # Semantic markers (language-agnostic patterns)
        self.divine_markers: Set[str] = {
            'god', 'yesu', 'jesus', 'christ', 'keriso', 'lord', 'taumi',
            'holy', 'sacred', 'divine', 'spirit', 'aruwa', 'vivivire'
        }
        
        self.power_markers: Set[str] = {
            'king', 'kingdom', 'vibadana', 'rule', 'reign', 'authority',
            'power', 'force', 'strength', 'might'
        }
        
        self.wisdom_markers: Set[str] = {
            'teach', 'learn', 'know', 'understand', 'wise', 'wisdom',
            'truth', 'knowledge', 'haraman'
        }
        
        self.love_markers: Set[str] = {
            'love', 'compassion', 'mercy', 'grace', 'kindness',
            'gentle', 'tender', 'care', 'nuwabo'
        }
        
        self.justice_markers: Set[str] = {
            'just', 'justice', 'right', 'law', 'order', 'fair',
            'raugagayo', 'righteous'
        }
        
        self.negative_markers: Set[str] = {
            'sin', 'wrong', 'evil', 'bad', 'apoapoe', 'ghoha',
            'error', 'fault', 'transgression'
        }
    
    def analyze_phonetic_profile(self, text: str) -> Dict[str, Any]:
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
    
    def analyze_morphological_structure(self, text: str) -> Dict[str, Any]:
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
    
    def detect_semantic_markers(self, text: str, context: Optional[str] = None) -> Dict[str, Any]:
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
    
    def calculate_field_signature(self, text: str, context: Optional[str] = None) -> Dict[str, Any]:
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
        
        # Check for Synergy (Divine + Power -> Kingdom/Glory -> High W)
        if markers['markers']['divine'] > 0 and markers['markers']['power'] > 0:
            signature['W'] += 0.20
            signature['J'] += 0.10   # Boost Justice (Rule/Law)
            signature['L'] += 0.10   # Boost Love (Benevolence)
            signature['P'] -= 0.05   # Reduce Power (Authority > Force) - Tuned for Unison w/ Love
            signature['confidence'] += 0.2
            signature['evidence'].append("Synergy: Divine + Power -> Kingly Authority")
        
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
        
        signature['emergent_dimension'] = ', '.join(emergent) if emergent else 'Balanced'
        
        # Normalize confidence
        signature['confidence'] = np.clip(signature['confidence'], 0, 1)
        
        return signature
    
    def calculate_field_signature_v2(self, text: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Calculate enhanced semantic field signature with Phase 2 improvements.
        Uses context integration and multi-layer combination.
        """
        # Step 1: Analyze phrase structure and context
        phrase_analysis = self.context_integrator.analyze_phrase_structure(text)
        flow_analysis = self.context_integrator.calculate_semantic_flow(text)
        
        # Step 2: Get base signatures from each layer
        # Phonetic layer
        phonetic = self.analyze_phonetic_profile(text)
        phonetic_sig = {'L': 0.5, 'J': 0.5, 'P': 0.5, 'W': 0.5}
        phonetic_conf = 0.0
        
        if phonetic:
            if phonetic['soft_ratio'] > 0.5:
                phonetic_sig['L'] += 0.20 * phonetic['soft_ratio']
                phonetic_sig['P'] -= 0.15 * phonetic['soft_ratio']
                phonetic_conf += 0.3
            if phonetic['harsh_ratio'] > 0.25:
                phonetic_sig['P'] += 0.20 * phonetic['harsh_ratio']
                phonetic_sig['J'] += 0.15 * phonetic['harsh_ratio']
                phonetic_conf += 0.3
            if phonetic['liquid_ratio'] > 0.2:
                phonetic_sig['L'] += 0.10 * phonetic['liquid_ratio']
                phonetic_sig['W'] += 0.10 * phonetic['liquid_ratio']
                phonetic_conf += 0.2
        
        # Morphological layer
        morphology = self.analyze_morphological_structure(text)
        morphological_sig = {'L': 0.5, 'J': 0.5, 'P': 0.5, 'W': 0.5}
        morphological_conf = 0.0
        
        if morphology:
            if morphology['reduplication']:
                morphological_sig['W'] += 0.15
                morphological_sig['J'] += 0.10
                morphological_conf += 0.4
            if morphology['complexity'] == 'high':
                morphological_sig['W'] += 0.15
                morphological_conf += 0.3
            if morphology['compound_ratio'] > 0.3:
                morphological_sig['W'] += 0.10
                morphological_conf += 0.2
        
        # Semantic layer
        markers = self.detect_semantic_markers(text, context)
        semantic_sig = {'L': 0.5, 'J': 0.5, 'P': 0.5, 'W': 0.5}
        semantic_conf = markers.get('confidence', 0.0)
        
        if markers['dominant']:
            marker_strength = markers['confidence']
            
            if markers['dominant'] == 'divine':
                semantic_sig['L'] += 0.30 * marker_strength
                semantic_sig['J'] += 0.25 * marker_strength
                semantic_sig['W'] += 0.35 * marker_strength
            elif markers['dominant'] == 'power':
                semantic_sig['P'] += 0.35 * marker_strength
                semantic_sig['J'] += 0.25 * marker_strength
                semantic_sig['W'] += 0.20 * marker_strength
            elif markers['dominant'] == 'wisdom':
                semantic_sig['W'] += 0.40 * marker_strength
                semantic_sig['J'] += 0.20 * marker_strength
            elif markers['dominant'] == 'love':
                semantic_sig['L'] += 0.40 * marker_strength
                semantic_sig['P'] -= 0.15 * marker_strength
                semantic_sig['W'] += 0.20 * marker_strength
            elif markers['dominant'] == 'justice':
                semantic_sig['J'] += 0.40 * marker_strength
                semantic_sig['W'] += 0.25 * marker_strength
                semantic_sig['P'] += 0.15 * marker_strength
            elif markers['dominant'] == 'negative':
                semantic_sig['L'] -= 0.30 * marker_strength
                semantic_sig['J'] -= 0.30 * marker_strength
        
        # Context layer
        context_integration = self.context_integrator.integrate_context_into_signature(
            base_signature=semantic_sig.copy(),
            phrase_analysis=phrase_analysis,
            flow_analysis=flow_analysis
        )
        
        context_sig = context_integration['signature']
        context_conf = context_integration['context_confidence']
        
        # Step 3: Combine all layers with adaptive weighting
        layer_confidences = {
            'phonetic': phonetic_conf,
            'morphological': morphological_conf,
            'semantic': semantic_conf,
            'context': context_conf
        }
        
        combined = self.multi_layer_combiner.combine_signatures(
            phonetic_sig=phonetic_sig,
            morphological_sig=morphological_sig,
            semantic_sig=semantic_sig,
            context_sig=context_sig,
            layer_confidences=layer_confidences
        )
        
        # Step 4: Build comprehensive result
        result = {
            'L': combined['signature']['L'],
            'J': combined['signature']['J'],
            'P': combined['signature']['P'],
            'W': combined['signature']['W'],
            'confidence': combined['confidence'],
            'evidence': [],
            'phase2_metadata': {
                'phrase_analysis': phrase_analysis,
                'flow_analysis': flow_analysis,
                'layer_weights': combined['weights'],
                'layer_confidences': layer_confidences
            }
        }
        
        # Collect evidence
        if phonetic_conf > 0:
            result['evidence'].append(f"Phonetic: conf={phonetic_conf:.2f}")
        if morphological_conf > 0:
            result['evidence'].append(f"Morphological: conf={morphological_conf:.2f}")
        if semantic_conf > 0:
            result['evidence'].append(f"Semantic: {markers['dominant']} (conf={semantic_conf:.2f})")
        if context_conf > 0:
            result['evidence'].extend(context_integration['evidence'])
        
        return result


if __name__ == "__main__":
    detector = EnhancedPatternDetector()
    print("EnhancedPatternDetector (Phase 2) instantiated successfully.")
    
    # Test Phase 2 features
    print("\n" + "="*70)
    print("PHASE 2 ENHANCED DETECTION TEST")
    print("="*70)
    
    test_cases = [
        ("Kingdom of God", "Divine rule"),
        ("Holy Spirit", "Divine presence"),
        ("The king rules with justice", None),
        ("Simple word", None)
    ]
    
    for text, context in test_cases:
        print(f"\n\nText: '{text}'")
        if context:
            print(f"Context: '{context}'")
        
        # Compare v1 and v2
        sig_v1 = detector.calculate_field_signature(text, context)
        sig_v2 = detector.calculate_field_signature_v2(text, context)
        
        print("\nV1 Signature:")
        print(f"  L={sig_v1['L']:.3f}, J={sig_v1['J']:.3f}, P={sig_v1['P']:.3f}, W={sig_v1['W']:.3f}")
        print(f"  Confidence: {sig_v1['confidence']:.2f}")
        
        print("\nV2 Signature (Phase 2):")
        print(f"  L={sig_v2['L']:.3f}, J={sig_v2['J']:.3f}, P={sig_v2['P']:.3f}, W={sig_v2['W']:.3f}")
        print(f"  Confidence: {sig_v2['confidence']:.2f}")
        print(f"  Weights: {sig_v2['phase2_metadata']['layer_weights']}")
