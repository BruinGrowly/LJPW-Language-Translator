"""
Universal Translator Core
The central engine that orchestrates Pattern Detection, Cosmic Resonance, and Semantic Mapping
to achieve pure meaning translation.
"""

import json
import numpy as np
import os
from typing import Dict, List, Optional, Any, Tuple
from experiments.enhanced_pattern_detector import EnhancedPatternDetector
from experiments.cosmic_resonator import CosmicResonator

class UniversalTranslator:
    """
    The Universal Translator.
    Maps source text -> Field Signature -> Resonant Concepts -> Target Meaning.
    """
    
    def __init__(self, semantic_space_path: str = "experiments/semantic_space_6386_ENRICHED.json"):
        self.detector = EnhancedPatternDetector()
        self.resonator = CosmicResonator()
        self.semantic_space = self._load_semantic_space(semantic_space_path)
        self.concepts = self._extract_concepts(self.semantic_space)
        print(f"Universal Translator initialized with {len(self.concepts)} concepts.")

    def _load_semantic_space(self, path: str) -> Dict[str, Any]:
        """Load the semantic space JSON."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Semantic space file not found: {path}")
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _extract_concepts(self, space: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Flatten concept structure for efficient iteration."""
        concepts = []
        if 'domains' in space:
            for domain_name, domain_data in space['domains'].items():
                if 'concepts' in domain_data:
                    for key, data in domain_data['concepts'].items():
                        # Filter out generated noise concepts
                        if 'Concept ' in key or 'Concept ' in data.get('name', ''):
                            continue
                            
                        concepts.append({
                            'key': key,
                            'name': data.get('name', key.replace('_', ' ').title()),
                            'coordinates': np.array(data['coordinates']),
                            'definition': data.get('definition', ''),
                            'domain': domain_name
                        })
        return concepts

    def find_best_matches(self, field_signature: Dict[str, Any], top_n: int = 15) -> List[Dict[str, Any]]:
        """Find concepts that resonate most strongly with the signature."""
        target_coords = field_signature['coordinates']
        matches = []
        
        for concept in self.concepts:
            resonance = self.resonator.calculate_resonance(target_coords, concept['coordinates'])
            matches.append({
                'concept': concept,
                'resonance': resonance
            })
            
        # Sort by total resonance strength descending
        matches.sort(key=lambda x: x['resonance']['strength'], reverse=True)
        return matches[:top_n]

    def translate(self, text: str, context_hint: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform the full translation pipeline.
        
        1. Detect Field Signature (L, J, P, W)
        2. Calculate Resonance with all known concepts
        3. Identify Top Matches
        4. Formulate Translation
        """
        # Step 1: Detect
        signature = self.detector.calculate_field_signature(text, context_hint)
        
        # Step 2 & 3: Resonate & Match
        top_matches = self.find_best_matches(signature, top_n=20)
        
        # Step 4: Formulate
        # Filter for strong matches first
        strong_matches = [m for m in top_matches if m['resonance']['type'] in ('strong', 'perfect')]
        candidates = strong_matches[:5] if strong_matches else top_matches[:5]
        
        suggested_text = " / ".join([c['concept']['name'] for c in candidates[:3]]) if candidates else "Unknown"
        
        return {
            'source_text': text,
            'context_hint': context_hint,
            'field_signature': signature,
            'top_matches': [
                {
                    'name': m['concept']['name'],
                    'strength': m['resonance']['strength'],
                    'type': m['resonance']['type'],
                    'harmonic_matches': m['resonance']['matches'],
                    'components': m['resonance']['components']
                }
                for m in top_matches[:10]
            ],
            'translation': suggested_text
        }

if __name__ == "__main__":
    # Quick instantiation test
    try:
        ut = UniversalTranslator()
        print("UniversalTranslator instantiated successfully.")
    except Exception as e:
        print(f"Initialization failed: {e}")
