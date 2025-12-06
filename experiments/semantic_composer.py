"""
Semantic Composer - Dynamic Phrase Composition
Uses LJPW coordinates to emergently determine how concepts compose.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from semantic_space_lookup import SemanticSpaceLookup


class SemanticComposer:
    """Dynamic semantic composition using coordinate-based weighting."""
    
    def __init__(self, semantic_space_path: str):
        """Initialize composer with semantic space."""
        self.lookup = SemanticSpaceLookup(semantic_space_path)
        
        # Semantic weight formula coefficients
        # These determine how much each dimension contributes to influence
        self.weight_formula = {
            'W': 0.40,  # Wisdom: primary meaning carrier
            'L': 0.30,  # Love: constructive amplification
            'J': 0.20,  # Justice: structural ordering
            'P': 0.10   # Power: force multiplier
        }
        
        # Positional boost factors
        self.positional_boosts = {
            'modifier_head': {'head': 0.8, 'modifier': 1.2},  # Modifier dominates
            'attribute_noun': {'noun': 1.0, 'attribute': 0.6},  # Noun anchors
            'conjunction': {'concept1': 1.0, 'concept2': 1.0}  # Equal
        }
    
    def calculate_semantic_weight(self, coords: np.ndarray) -> float:
        """
        Calculate inherent semantic weight from LJPW coordinates.
        
        Higher weight = more influence in composition.
        """
        L, J, P, W = coords
        
        weight = (
            W * self.weight_formula['W'] +
            L * self.weight_formula['L'] +
            J * self.weight_formula['J'] +
            P * self.weight_formula['P']
        )
        
        return weight
    
    def calculate_synergy(self, coord1: np.ndarray, coord2: np.ndarray) -> float:
        """
        Detect synergistic or conflicting interactions.
        
        Returns:
            Synergy score: -0.5 (conflict) to 1.0 (synergy)
        """
        L1, J1, P1, W1 = coord1
        L2, J2, P2, W2 = coord2
        
        # Love-Wisdom synergy (compassionate wisdom)
        lw_synergy = min(L1, W2) + min(L2, W1)
        
        # Justice-Power synergy (righteous authority)
        jp_synergy = min(J1, P2) + min(J2, P1)
        
        # Love-Power conflict (compassion vs force)
        lp_conflict = abs(L1 - P2) + abs(L2 - P1)
        
        synergy_score = (lw_synergy + jp_synergy - lp_conflict * 0.5) / 4
        
        return synergy_score
    
    def parse_structure(self, phrase: str) -> Dict[str, Any]:
        """
        Identify syntactic structure.
        
        Returns:
            {
                'type': str,  # 'modifier_head', 'attribute_noun', 'conjunction', 'single'
                'components': List[str]
            }
        """
        phrase_lower = phrase.lower()
        
        # Pattern: "X of Y"
        if ' of ' in phrase_lower:
            parts = phrase.split(' of ', 1)
            return {
                'type': 'modifier_head',
                'components': [parts[0].strip(), parts[1].strip()],
                'roles': ['head', 'modifier']
            }
        
        # Pattern: "X and Y"
        if ' and ' in phrase_lower:
            parts = phrase.split(' and ', 1)
            return {
                'type': 'conjunction',
                'components': [parts[0].strip(), parts[1].strip()],
                'roles': ['concept1', 'concept2']
            }
        
        # Pattern: "not X"
        if phrase_lower.startswith('not '):
            return {
                'type': 'negation',
                'components': [phrase[4:].strip()],
                'roles': ['concept']
            }
        
        # Pattern: "Adj Noun" (2 words)
        words = phrase.split()
        if len(words) == 2:
            return {
                'type': 'attribute_noun',
                'components': words,
                'roles': ['attribute', 'noun']
            }
        
        # Single concept
        return {
            'type': 'single',
            'components': [phrase],
            'roles': ['concept']
        }
    
    def lookup_components(
        self,
        structure: Dict[str, Any]
    ) -> List[Tuple[str, Optional[Dict]]]:
        """
        Look up components in semantic space.
        
        Returns:
            List of (component_name, concept_dict) tuples
        """
        components = structure['components']
        return self.lookup.find_multiple(components)
    
    def compose(self, phrase: str) -> Dict[str, Any]:
        """
        Main composition method.
        
        Returns:
            {
                'coordinates': np.ndarray,
                'confidence': float,
                'components': List[str],
                'weights': Dict[str, float],
                'synergy': float,
                'explanation': str
            }
        """
        # Parse structure
        structure = self.parse_structure(phrase)
        
        # Look up components
        component_lookups = self.lookup_components(structure)
        
        # Check if all components found
        missing = [name for name, concept in component_lookups if concept is None]
        if missing:
            return {
                'coordinates': np.array([0.5, 0.5, 0.5, 0.5]),
                'confidence': 0.0,
                'components': [name for name, _ in component_lookups],
                'weights': {},
                'synergy': 0.0,
                'explanation': f"Missing concepts: {', '.join(missing)}",
                'error': 'missing_components'
            }
        
        # Extract coordinates
        components = [(name, concept['coordinates']) for name, concept in component_lookups]
        
        # Handle single concept
        if structure['type'] == 'single':
            return {
                'coordinates': components[0][1],
                'confidence': 1.0,
                'components': [components[0][0]],
                'weights': {components[0][0]: 1.0},
                'synergy': 0.0,
                'explanation': f"Single concept: {components[0][0]}"
            }
        
        # Handle negation
        if structure['type'] == 'negation':
            negated = 1.0 - components[0][1]
            return {
                'coordinates': np.clip(negated, 0, 1),
                'confidence': 0.8,
                'components': [components[0][0]],
                'weights': {components[0][0]: -1.0},
                'synergy': 0.0,
                'explanation': f"Negation of {components[0][0]}"
            }
        
        # Calculate semantic weights
        semantic_weights = {}
        for name, coords in components:
            semantic_weights[name] = self.calculate_semantic_weight(coords)
        
        # Apply positional boosts
        structure_type = structure['type']
        roles = structure['roles']
        
        if structure_type in self.positional_boosts:
            boosts = self.positional_boosts[structure_type]
            adjusted_weights = {}
            for (name, coords), role in zip(components, roles):
                boost = boosts.get(role, 1.0)
                adjusted_weights[name] = semantic_weights[name] * boost
        else:
            adjusted_weights = semantic_weights
        
        # Normalize weights
        total_weight = sum(adjusted_weights.values())
        influences = {name: w / total_weight for name, w in adjusted_weights.items()}
        
        # Calculate synergy (for 2-component phrases)
        if len(components) == 2:
            synergy = self.calculate_synergy(components[0][1], components[1][1])
        else:
            synergy = 0.0
        
        # Weighted composition
        composed = np.zeros(4)
        for (name, coords), influence in zip(components, influences.values()):
            composed += coords * influence
        
        # Apply synergy adjustment
        if synergy > 0:
            adjustment = 1.0 + (synergy * 0.2)  # Up to 20% boost
        else:
            adjustment = 1.0 + (synergy * 0.1)  # Up to 5% reduction
        
        composed = composed * adjustment
        composed = np.clip(composed, 0, 1)
        
        # Calculate confidence
        confidence = min(total_weight / len(components), 1.0)
        if synergy > 0:
            confidence = min(confidence * 1.1, 1.0)
        
        # Generate explanation
        explanation = self.explain_composition(
            components, semantic_weights, adjusted_weights, influences, synergy
        )
        
        return {
            'coordinates': composed,
            'confidence': confidence,
            'components': [name for name, _ in components],
            'weights': influences,
            'synergy': synergy,
            'explanation': explanation
        }
    
    def explain_composition(
        self,
        components: List[Tuple[str, np.ndarray]],
        semantic_weights: Dict[str, float],
        adjusted_weights: Dict[str, float],
        influences: Dict[str, float],
        synergy: float
    ) -> str:
        """Generate human-readable explanation of composition."""
        lines = []
        
        lines.append(f"Composing: {' + '.join(name for name, _ in components)}")
        
        lines.append("\nSemantic Weights (from LJPW coordinates):")
        for name, weight in semantic_weights.items():
            coords = next(c for n, c in components if n == name)
            lines.append(f"  {name}: {weight:.3f} [L={coords[0]:.2f}, J={coords[1]:.2f}, P={coords[2]:.2f}, W={coords[3]:.2f}]")
        
        lines.append("\nAdjusted Weights (with positional boost):")
        for name, weight in adjusted_weights.items():
            lines.append(f"  {name}: {weight:.3f}")
        
        lines.append("\nComposition Influence:")
        for name, influence in influences.items():
            lines.append(f"  {name}: {influence:.1%}")
        
        if synergy != 0:
            if synergy > 0:
                lines.append(f"\nSynergy: +{synergy:.3f} (reinforcing, +{synergy*20:.1f}% boost)")
            else:
                lines.append(f"\nConflict: {synergy:.3f} (tension, {synergy*10:.1f}% reduction)")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Test the composer
    composer = SemanticComposer('experiments/semantic_space_6854_SOCIAL.json')
    
    print("="*70)
    print("SEMANTIC COMPOSER TEST")
    print("="*70)
    
    test_phrases = [
        "Kingdom of God",
        "Holy Spirit",
        "Love and Justice",
        "not love"
    ]
    
    for phrase in test_phrases:
        print(f"\n{'='*70}")
        print(f"PHRASE: '{phrase}'")
        print('='*70)
        
        result = composer.compose(phrase)
        
        print(f"\nComposed Coordinates:")
        print(f"  L={result['coordinates'][0]:.3f}")
        print(f"  J={result['coordinates'][1]:.3f}")
        print(f"  P={result['coordinates'][2]:.3f}")
        print(f"  W={result['coordinates'][3]:.3f}")
        print(f"\nConfidence: {result['confidence']:.2f}")
        print(f"\n{result['explanation']}")
    
    print("\n" + "="*70)
    print("Semantic Composer initialized successfully!")
    print("="*70)
