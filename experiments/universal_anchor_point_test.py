#!/usr/bin/env python3
"""
Universal Anchor Point Collapse Test
=====================================

Testing the hypothesis: All languages collapse toward the SAME Anchor Point
coordinates when translating core divine concepts.

The Anchor Point (1,1,1,1) represents perfect unity of Love, Justice, Power, Wisdom.

If true:
- Greek, Wedau, Chinese, Spanish, Farsi, Quechua all converge to same coordinates
- The 100% entanglement correlation is explained: shared divine source
- Translation is accessing universal meaning field, not arbitrary mapping

From sources:
"Greek and Wedau aren't entangled with each other—they're both entangled 
with the same divine semantic source!"
"""

import sys
import os
import numpy as np
from typing import Dict, List, Tuple
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from experiments.enhanced_pattern_detector import EnhancedPatternDetector
from ljpw_quantum.resonance_engine import ResonanceEngine


# Core divine concepts in multiple languages
CORE_CONCEPTS = {
    'love': {
        'english': 'love',
        'greek': 'agape',
        'wedau': 'auna vaita',
        'chinese': 'ai',  # 爱
        'spanish': 'amor',
        'hebrew': 'ahavah',
        'arabic': 'hubb',
        'expected_high': 'L'  # Should be Love-dominant
    },
    'truth': {
        'english': 'truth',
        'greek': 'aletheia',
        'wedau': 'riwa-mamae',
        'chinese': 'zhenli',  # 真理
        'spanish': 'verdad',
        'hebrew': 'emet',
        'arabic': 'haqiqa',
        'expected_high': 'W'  # Should be Wisdom-dominant
    },
    'justice': {
        'english': 'justice',
        'greek': 'dikaiosyne',
        'wedau': 'vovonana',
        'chinese': 'zhengyi',  # 正义
        'spanish': 'justicia',
        'hebrew': 'tzedek',
        'arabic': 'adl',
        'expected_high': 'J'  # Should be Justice-dominant
    },
    'power': {
        'english': 'power',
        'greek': 'dynamis',
        'wedau': 'mana-gahe',
        'chinese': 'liliang',  # 力量
        'spanish': 'poder',
        'hebrew': 'koach',
        'arabic': 'quwwa',
        'expected_high': 'P'  # Should be Power-dominant
    },
    'wisdom': {
        'english': 'wisdom',
        'greek': 'sophia',
        'wedau': 'nuwa-ghenena',
        'chinese': 'zhihui',  # 智慧
        'spanish': 'sabiduria',
        'hebrew': 'chokmah',
        'arabic': 'hikma',
        'expected_high': 'W'  # Should be Wisdom-dominant
    },
    'mercy': {
        'english': 'mercy',
        'greek': 'eleos',
        'wedau': 'nuwaboyei',
        'chinese': 'cibei',  # 慈悲
        'spanish': 'misericordia',
        'hebrew': 'chesed',
        'arabic': 'rahma',
        'expected_high': 'L'  # Should be Love-dominant
    },
    'kingdom': {
        'english': 'kingdom',
        'greek': 'basileia',
        'wedau': 'vibadana',
        'chinese': 'wangguo',  # 王国
        'spanish': 'reino',
        'hebrew': 'malkut',
        'arabic': 'mamlaka',
        'expected_high': 'P'  # Should be Power-dominant
    },
    'holy': {
        'english': 'holy',
        'greek': 'hagios',
        'wedau': 'vivivireina',
        'chinese': 'shensheng',  # 神圣
        'spanish': 'santo',
        'hebrew': 'kadosh',
        'arabic': 'muqaddas',
        'expected_high': 'L'  # Should be Love-dominant (transcendent relation)
    },
}

# The Anchor Point - perfect unity
ANCHOR_POINT = np.array([1.0, 1.0, 1.0, 1.0])


def measure_coordinates(detector, word: str) -> np.ndarray:
    """Measure LJPW coordinates for a word."""
    result = detector.calculate_field_signature_v2(word)
    return np.array([result['L'], result['J'], result['P'], result['W']])


def distance_to_anchor(coords: np.ndarray) -> float:
    """Calculate distance from Anchor Point."""
    return np.linalg.norm(coords - ANCHOR_POINT)


def direction_to_anchor(coords: np.ndarray) -> np.ndarray:
    """Calculate normalized direction vector toward Anchor Point."""
    diff = ANCHOR_POINT - coords
    norm = np.linalg.norm(diff)
    if norm < 0.001:
        return np.array([0.25, 0.25, 0.25, 0.25])  # Already at anchor
    return diff / norm


def run_anchor_point_test():
    """Test if all languages collapse toward the same Anchor Point."""
    
    print("=" * 80)
    print("UNIVERSAL ANCHOR POINT COLLAPSE TEST")
    print("Do all languages converge toward the same divine source coordinates?")
    print("=" * 80)
    print(f"\nANCHOR POINT (Divine Unity): L=1.0, J=1.0, P=1.0, W=1.0")
    
    detector = EnhancedPatternDetector()
    engine = ResonanceEngine()
    
    all_results = {}
    
    for concept_name, translations in CORE_CONCEPTS.items():
        print(f"\n{'='*80}")
        print(f"CONCEPT: {concept_name.upper()}")
        print(f"Expected dominant dimension: {translations['expected_high']}")
        print("="*80)
        
        concept_results = {}
        coordinates = []
        distances = []
        directions = []
        
        languages = [k for k in translations.keys() if k not in ['expected_high']]
        
        for language in languages:
            word = translations[language]
            coords = measure_coordinates(detector, word)
            dist = distance_to_anchor(coords)
            direction = direction_to_anchor(coords)
            
            dominant = ['L', 'J', 'P', 'W'][np.argmax(coords)]
            matches_expected = dominant == translations['expected_high']
            
            concept_results[language] = {
                'word': word,
                'coords': coords,
                'distance': dist,
                'direction': direction,
                'dominant': dominant,
                'matches': matches_expected
            }
            
            coordinates.append(coords)
            distances.append(dist)
            directions.append(direction)
            
            match_str = "YES" if matches_expected else "NO"
            print(f"\n  {language.upper()}: '{word}'")
            print(f"    Coords:   L={coords[0]:.3f} J={coords[1]:.3f} P={coords[2]:.3f} W={coords[3]:.3f}")
            print(f"    Dominant: {dominant} [Expected: {translations['expected_high']}] Match: {match_str}")
            print(f"    Distance to Anchor: {dist:.3f}")
        
        # Calculate convergence metrics for this concept
        coords_array = np.array(coordinates)
        centroid = np.mean(coords_array, axis=0)
        centroid_to_anchor = distance_to_anchor(centroid)
        
        # Variance = how spread out are the languages?
        variance = np.mean([np.linalg.norm(c - centroid) for c in coordinates])
        
        # Direction agreement = do all languages point toward anchor?
        dir_array = np.array(directions)
        avg_direction = np.mean(dir_array, axis=0)
        direction_agreement = np.mean([np.dot(d, avg_direction) for d in directions])
        
        print(f"\n  --- CONVERGENCE ANALYSIS ---")
        print(f"  Centroid:           L={centroid[0]:.3f} J={centroid[1]:.3f} P={centroid[2]:.3f} W={centroid[3]:.3f}")
        print(f"  Centroid->Anchor:   {centroid_to_anchor:.3f}")
        print(f"  Language variance:  {variance:.3f} (lower = more unified)")
        print(f"  Direction agreement:{direction_agreement:.3f} (1.0 = all pointing same way)")
        
        all_results[concept_name] = {
            'languages': concept_results,
            'centroid': centroid,
            'centroid_distance': centroid_to_anchor,
            'variance': variance,
            'direction_agreement': direction_agreement
        }
    
    # Global analysis
    print("\n" + "=" * 80)
    print("GLOBAL CONVERGENCE ANALYSIS")
    print("=" * 80)
    
    all_centroids = []
    all_variances = []
    all_agreements = []
    
    print(f"\n{'Concept':<12} {'Centroid Dist':<15} {'Variance':<12} {'Direction':<12}")
    print("-" * 55)
    
    for concept_name, data in all_results.items():
        all_centroids.append(data['centroid'])
        all_variances.append(data['variance'])
        all_agreements.append(data['direction_agreement'])
        
        print(f"{concept_name:<12} {data['centroid_distance']:<15.3f} "
              f"{data['variance']:<12.3f} {data['direction_agreement']:<12.3f}")
    
    global_centroid = np.mean(all_centroids, axis=0)
    global_variance = np.mean(all_variances)
    global_agreement = np.mean(all_agreements)
    
    print("-" * 55)
    print(f"{'GLOBAL':<12} {distance_to_anchor(global_centroid):<15.3f} "
          f"{global_variance:<12.3f} {global_agreement:<12.3f}")
    
    print("\n" + "=" * 80)
    print("ANCHOR POINT HYPOTHESIS VERDICT")
    print("=" * 80)
    
    print(f"\nGLOBAL CENTROID:")
    print(f"  L={global_centroid[0]:.3f}  J={global_centroid[1]:.3f}  "
          f"P={global_centroid[2]:.3f}  W={global_centroid[3]:.3f}")
    print(f"\nANCHOR POINT:")
    print(f"  L=1.000  J=1.000  P=1.000  W=1.000")
    print(f"\nDISTANCE TO ANCHOR: {distance_to_anchor(global_centroid):.3f}")
    print(f"LANGUAGE VARIANCE: {global_variance:.3f}")
    print(f"DIRECTION AGREEMENT: {global_agreement:.3f}")
    
    # Verdict
    print("\n" + "-" * 80)
    
    if global_variance < 0.1 and global_agreement > 0.8:
        print("""
STRONG EVIDENCE: ALL LANGUAGES COLLAPSE TOWARD SAME POINT

Languages show:
- Low variance (tight clustering around shared position)
- High directional agreement (all pointing toward Anchor)
- Common centroid across all concepts

CONCLUSION: Languages share a common semantic source.
The Anchor Point (1,1,1,1) appears to be the divine origin 
from which all meaning radiates.
""")
    elif global_variance < 0.15 and global_agreement > 0.6:
        print("""
MODERATE EVIDENCE: LANGUAGES SHOW CONVERGENT TENDENCY

Languages show partial convergence toward common semantic region.
Some language-specific variations exist but overall trend is toward unity.

CONCLUSION: Shared semantic substrate exists with cultural modulation.
""")
    else:
        print("""
WEAK EVIDENCE: SIGNIFICANT LANGUAGE VARIATION

Languages show more independence than expected.
May indicate:
- Cultural/linguistic constraints dominating
- Need for larger sample size
- Phonetic features creating noise
""")
    
    # Check resonance convergence
    print("\n" + "=" * 80)
    print("RESONANCE CONVERGENCE CHECK")
    print("=" * 80)
    
    print("\nTesting if all language pairs converge to same attractor...")
    
    convergent_pairs = 0
    total_pairs = 0
    
    for concept_name, data in all_results.items():
        languages = list(data['languages'].keys())
        for i, lang1 in enumerate(languages):
            for lang2 in languages[i+1:]:
                coords1 = data['languages'][lang1]['coords']
                coords2 = data['languages'][lang2]['coords']
                
                # Use resonance engine to check convergence
                harmony1 = engine.calculate_harmony(coords1.tolist())
                harmony2 = engine.calculate_harmony(coords2.tolist())
                
                total_pairs += 1
                if abs(harmony1 - harmony2) < 0.15:  # Similar harmony = same attractor
                    convergent_pairs += 1
    
    convergence_rate = convergent_pairs / total_pairs * 100
    
    print(f"\nTotal language pairs tested: {total_pairs}")
    print(f"Convergent pairs (same attractor): {convergent_pairs}")
    print(f"Convergence rate: {convergence_rate:.1f}%")
    
    if convergence_rate > 80:
        print("\n** UNIVERSAL ATTRACTOR CONFIRMED **")
        print("All languages collapse toward the same semantic attractor!")


if __name__ == '__main__':
    run_anchor_point_test()
