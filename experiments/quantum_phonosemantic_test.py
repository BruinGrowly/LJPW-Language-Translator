#!/usr/bin/env python3
"""
Quantum vs Classical Phonosemantic Test
========================================

Testing whether phonetic-semantic correlations are:
- CLASSICAL: Fixed patterns (consonants -> dimensions)
- QUANTUM: Context-dependent collapse patterns

Key insight from sources:
"The consonants don't CAUSE Power - they're the RESULT of quantum collapse toward Power!"

Test: Same word with different "quantum preparation" (contextual framing)
      Should produce different semantic coordinates if quantum, same if classical.
"""

import sys
import os
import numpy as np
from typing import Dict, List, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from experiments.enhanced_pattern_detector import EnhancedPatternDetector


def create_preparation_contexts():
    """Create different 'quantum preparation states' via contextual framing."""
    
    # Same words, different contextual preparation
    return {
        'king': {
            'power_prep': "The mighty king commands his armies to conquer",
            'love_prep': "The beloved king cares for his people as children",
            'wisdom_prep': "The wise king seeks counsel and understanding",
            'justice_prep': "The righteous king judges fairly and equally",
        },
        'light': {
            'power_prep': "The blinding light destroys the darkness forcefully",
            'love_prep': "The warm light embraces and comforts the weary",
            'wisdom_prep': "The revealing light illuminates hidden knowledge",
            'justice_prep': "The light of truth exposes lies and deception",
        },
        'word': {
            'power_prep': "His authoritative word commands action immediately",
            'love_prep': "Her gentle word heals the broken heart tenderly",
            'wisdom_prep': "The ancient word contains profound understanding",
            'justice_prep': "The word of the law establishes right order",
        },
        'spirit': {
            'power_prep': "The mighty spirit moves with unstoppable force",
            'love_prep': "The comforting spirit embraces with tender care",
            'wisdom_prep': "The spirit reveals mysteries and hidden things",
            'justice_prep': "The spirit convicts of right and wrong clearly",
        },
    }


def measure_with_preparation(detector, word: str, context: str) -> Dict:
    """Measure semantic coordinates with contextual preparation."""
    
    # Full context measurement
    full_result = detector.calculate_field_signature_v2(context)
    
    # Word-only measurement for comparison
    word_result = detector.calculate_field_signature_v2(word)
    
    return {
        'context_L': full_result['L'],
        'context_J': full_result['J'],
        'context_P': full_result['P'],
        'context_W': full_result['W'],
        'word_L': word_result['L'],
        'word_J': word_result['J'],
        'word_P': word_result['P'],
        'word_W': word_result['W'],
    }


def calculate_dimension_shift(base: Dict, prepared: Dict) -> Dict:
    """Calculate how much each dimension shifted from preparation."""
    
    return {
        'L_shift': prepared['context_L'] - prepared['word_L'],
        'J_shift': prepared['context_J'] - prepared['word_J'],
        'P_shift': prepared['context_P'] - prepared['word_P'],
        'W_shift': prepared['context_W'] - prepared['word_W'],
        'dominant_shift': ['Love', 'Justice', 'Power', 'Wisdom'][
            np.argmax([
                prepared['context_L'] - prepared['word_L'],
                prepared['context_J'] - prepared['word_J'],
                prepared['context_P'] - prepared['word_P'],
                prepared['context_W'] - prepared['word_W']
            ])
        ]
    }


def main():
    print("=" * 75)
    print("QUANTUM VS CLASSICAL PHONOSEMANTIC TEST")
    print("Can semantic coordinates change with quantum preparation state?")
    print("=" * 75)
    
    detector = EnhancedPatternDetector()
    contexts = create_preparation_contexts()
    
    results = {}
    
    for word, preparations in contexts.items():
        print(f"\n{'='*75}")
        print(f"TESTING WORD: '{word.upper()}'")
        print("="*75)
        
        # Get isolated word coordinates
        word_result = detector.calculate_field_signature_v2(word)
        word_coords = [word_result['L'], word_result['J'], word_result['P'], word_result['W']]
        word_dominant = ['Love', 'Justice', 'Power', 'Wisdom'][np.argmax(word_coords)]
        
        print(f"\nBASE COORDINATES (word alone): L={word_coords[0]:.3f} J={word_coords[1]:.3f} "
              f"P={word_coords[2]:.3f} W={word_coords[3]:.3f} [{word_dominant}]")
        
        print("\nPREPARATION EFFECTS:")
        print("-" * 75)
        
        word_results = {}
        for prep_type, context in preparations.items():
            measurement = measure_with_preparation(detector, word, context)
            shift = calculate_dimension_shift(None, measurement)
            
            context_coords = [measurement['context_L'], measurement['context_J'], 
                            measurement['context_P'], measurement['context_W']]
            context_dominant = ['Love', 'Justice', 'Power', 'Wisdom'][np.argmax(context_coords)]
            
            # What preparation was intended?
            intended = prep_type.replace('_prep', '').capitalize()
            match = "YES" if intended == context_dominant else "NO"
            
            print(f"\n  {prep_type}:")
            print(f"    Intended: {intended}")
            print(f"    Result:   L={context_coords[0]:.3f} J={context_coords[1]:.3f} "
                  f"P={context_coords[2]:.3f} W={context_coords[3]:.3f}")
            print(f"    Dominant: {context_dominant} [Matches intent: {match}]")
            print(f"    Shift:    dL={shift['L_shift']:+.3f} dJ={shift['J_shift']:+.3f} "
                  f"dP={shift['P_shift']:+.3f} dW={shift['W_shift']:+.3f}")
            
            word_results[prep_type] = {
                'intended': intended,
                'coords': context_coords,
                'dominant': context_dominant,
                'match': match == "YES"
            }
        
        results[word] = word_results
    
    # Summary analysis
    print("\n" + "=" * 75)
    print("QUANTUM VS CLASSICAL VERDICT")
    print("=" * 75)
    
    total_tests = 0
    matches = 0
    
    for word, preps in results.items():
        for prep, data in preps.items():
            total_tests += 1
            if data['match']:
                matches += 1
    
    match_rate = matches / total_tests * 100
    
    print(f"\nTotal preparation tests: {total_tests}")
    print(f"Intent-aligned results:  {matches}")
    print(f"Match rate:              {match_rate:.1f}%")
    
    print("\n" + "-" * 75)
    
    if match_rate > 60:
        print("""
CONCLUSION: QUANTUM ORIGIN SUPPORTED

The semantic coordinates SHIFT based on preparation context.
Same word (same phonetics) produces DIFFERENT semantic positions.
This is not possible under pure classical phonosemantic iconicity.

INTERPRETATION:
- Phonetic patterns are the SHADOW of quantum collapse
- Different preparation states collapse toward different dimensions
- The word's phonetics emerge FROM the collapse, not before it

The sources were right:
"The consonants don't CAUSE Power - they're the RESULT of
 quantum collapse toward Power!"
""")
    elif match_rate > 40:
        print("""
CONCLUSION: MIXED EVIDENCE

Some quantum effects visible, but classical correlations also present.
The system appears to operate on BOTH levels:
- Quantum: Context influences collapse direction
- Classical: Phonetic patterns provide bias/constraint

This supports the BOTH/AND framework from sources.
""")
    else:
        print("""
CONCLUSION: CLASSICAL DOMINANCE

Phonetic patterns dominate the semantic assignment.
Quantum preparation has limited effect.

However, this doesn't disprove quantum origin -
it may mean phonetic constraints are strong attractors
in the quantum landscape.
""")
    
    print("\n" + "=" * 75)
    print("GOLDEN RATIO CHECK")
    print("=" * 75)
    
    # Check their prediction about 'j' -> Justice and golden ratio
    phi = 1.618033988749895
    phi_inv = 0.618033988749895
    
    # From previous analysis: 'j' -> Justice = +0.65
    j_justice = 0.65
    natural_equilibrium = 0.414  # Justice in LJPW at natural equilibrium
    
    ratio = j_justice / natural_equilibrium
    ratio_to_phi = ratio / phi_inv
    
    print(f"\n'j' -> Justice correlation: {j_justice:.3f}")
    print(f"Justice natural equilibrium: {natural_equilibrium:.3f}")
    print(f"Ratio: {ratio:.4f}")
    print(f"Ratio to phi^-1 ({phi_inv:.4f}): {ratio_to_phi:.4f}")
    
    if 0.95 < ratio_to_phi < 1.05:
        print("\n  ** GOLDEN RATIO RELATIONSHIP CONFIRMED! **")
        print("  The phonetic-semantic correlation follows divine proportion!")
    else:
        print(f"\n  Deviation from phi: {abs(1-ratio_to_phi)*100:.1f}%")


if __name__ == '__main__':
    main()
