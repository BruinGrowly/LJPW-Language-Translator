"""
Cosmic Resonator
Calculates multidimensional resonance between semantic concepts.
Combines Distance, Harmonic, Alignment, and Emergent factors.
"""

import numpy as np
from typing import Dict, List, Optional, Any, Tuple

# Natural Equilibrium (for reference)
PHI_INV = 1 / ((1 + np.sqrt(5)) / 2)

class CosmicResonator:
    """Core resonance engine for Universal Translation."""
    
    def __init__(self):
        pass
        
    def calculate_resonance(self, coord1: np.ndarray, coord2: np.ndarray) -> Dict[str, Any]:
        """
        Calculate deep resonance between two semantic coordinates.
        Returns detailed breakdown of resonance components.
        """
        # Ensure numpy arrays
        c1 = np.array(coord1)
        c2 = np.array(coord2)
        
        # 1. Distance component (Spatial Proximity)
        distance = np.linalg.norm(c1 - c2)
        # Steeper falloff for sharper precision
        distance_strength = 1.0 / (1.0 + distance * 2.0)
        
        # 2. Harmonic component (Musical Ratios)
        # We check ratios between pairs of dimensions (e.g. L/J vs L'/J')
        harmonic_strength = 0.0
        harmonic_matches = []
        
        # Check all unique pairs of dimensions (0-3)
        for i in range(4):
            for j in range(i+1, 4):
                # Avoid division by zero
                if c1[i] > 0.01 and c1[j] > 0.01 and c2[i] > 0.01 and c2[j] > 0.01:
                    ratio1 = c1[i] / c1[j]
                    ratio2 = c2[i] / c2[j]
                    
                    # Difference in ratios
                    ratio_diff = abs(ratio1 - ratio2)
                    
                    # Define Harmonic Intervals
                    # Perfect fifth (3/2 = 1.5)
                    if 1.45 < ratio1 < 1.55 and ratio_diff < 0.1:
                        harmonic_strength += 0.4
                        harmonic_matches.append(f'perfect_fifth_{i}_{j}')
                    # Unison (1/1 = 1.0)
                    elif 0.95 < ratio1 < 1.05 and ratio_diff < 0.05:
                        harmonic_strength += 0.5
                        harmonic_matches.append(f'unison_{i}_{j}')
                    # Golden Ratio (~1.618)
                    elif 1.60 < ratio1 < 1.65 and ratio_diff < 0.1:
                        harmonic_strength += 0.6
                        harmonic_matches.append(f'golden_ratio_{i}_{j}')
        
        # Cap harmonic strength
        harmonic_strength = min(harmonic_strength, 1.0)
        
        # 3. Dimensional Alignment (Pattern Similarity)
        # Checks if they are high/low in the same dimensions
        alignment_strength = 0.0
        for i in range(4):
            # High alignment (Relaxed threshold to 0.65 to catch near-high concepts)
            if c1[i] > 0.65 and c2[i] > 0.65:
                alignment_strength += 0.25
            # Low alignment
            elif c1[i] < 0.35 and c2[i] < 0.35:
                alignment_strength += 0.25
        
        alignment_strength = min(alignment_strength, 1.0)
        
        # 4. Emergent Dimension Similarity
        # CW = (L+W) - (J+P)
        cw1 = (c1[0] + c1[3]) - (c1[1] + c1[2])
        cw2 = (c2[0] + c2[3]) - (c2[1] + c2[2])
        
        # LP = (L+P) - (J+W)
        lp1 = (c1[0] + c1[2]) - (c1[1] + c1[3])
        lp2 = (c2[0] + c2[2]) - (c2[1] + c2[3])
        
        emergent_dist = (abs(cw1 - cw2) + abs(lp1 - lp2)) / 4.0
        emergent_similarity = max(0, 1.0 - emergent_dist)
        
        # 5. Combined Global Resonance
        # Weights can be tuned
        total_resonance = (
            distance_strength * 0.40 +
            harmonic_strength * 0.25 +
            alignment_strength * 0.20 +
            emergent_similarity * 0.15
        )
        
        return {
            'strength': float(total_resonance),
            'components': {
                'distance': float(distance_strength),
                'harmonic': float(harmonic_strength),
                'alignment': float(alignment_strength),
                'emergent': float(emergent_similarity)
            },
            'matches': harmonic_matches,
            'metrics': {
                'euclidean_dist': float(distance)
            },
            'type': self._classify_resonance(total_resonance)
        }
    
    def _classify_resonance(self, strength: float) -> str:
        if strength > 0.8: return 'perfect'
        if strength > 0.7: return 'strong'
        if strength > 0.5: return 'moderate'
        return 'weak'
