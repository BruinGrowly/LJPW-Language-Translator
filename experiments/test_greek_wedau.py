#!/usr/bin/env python3
"""
Greek-Wedau Translation Quality Test
=====================================

Comprehensive test of translation quality between Koine Greek and Wedau
using the resonance paradigm. Tests ALL verses in Mark Chapter 1.
"""

import json
import sys
import os
import numpy as np
from typing import Dict, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_quantum.resonance_engine import ResonanceEngine
from experiments.enhanced_pattern_detector import EnhancedPatternDetector


def load_corpora():
    """Load Greek and Wedau translations."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    with open(os.path.join(base_path, 'greek_mark_chapter1.json'), 'r', encoding='utf-8') as f:
        greek = json.load(f)
    
    with open(os.path.join(base_path, 'wedau_mark_chapter1.json'), 'r', encoding='utf-8') as f:
        wedau = json.load(f)
    
    return greek, wedau


def test_verse_translation(verse_num: str, greek_text: str, wedau_text: str, 
                          detector: EnhancedPatternDetector, engine: ResonanceEngine) -> Dict:
    """Test translation quality for a single verse."""
    
    # Get LJPW coordinates
    greek_result = detector.calculate_field_signature_v2(greek_text)
    greek_coords = [greek_result['L'], greek_result['J'], greek_result['P'], greek_result['W']]
    
    wedau_result = detector.calculate_field_signature_v2(wedau_text)
    wedau_coords = [wedau_result['L'], wedau_result['J'], wedau_result['P'], wedau_result['W']]
    
    # Traditional euclidean distance
    euclidean = np.linalg.norm(np.array(greek_coords) - np.array(wedau_coords))
    
    # Resonance analysis
    analysis = engine.analyze_translation_pair(greek_coords, wedau_coords, cycles=100)
    
    # Calculate harmonies
    greek_harmony = engine.calculate_harmony(np.array(greek_coords))
    wedau_harmony = engine.calculate_harmony(np.array(wedau_coords))
    
    return {
        'verse': verse_num,
        'greek_ljpw': greek_coords,
        'wedau_ljpw': wedau_coords,
        'greek_harmony': greek_harmony,
        'wedau_harmony': wedau_harmony,
        'euclidean_distance': euclidean,
        'resonance_convergence': analysis['convergence_distance'],
        'same_attractor': analysis['same_deficit'],
        'quality': analysis['quality_assessment'],
        'passes_traditional': euclidean < 0.10,
        'passes_resonance': analysis['convergence_distance'] < 0.10 and analysis['same_deficit']
    }


def main():
    print("=" * 70)
    print("GREEK-WEDAU TRANSLATION QUALITY TEST")
    print("Koine Greek -> Wedau (Mark Chapter 1)")
    print("=" * 70)
    
    greek, wedau = load_corpora()
    detector = EnhancedPatternDetector()
    engine = ResonanceEngine()
    
    print(f"\nGreek verses: {len(greek['verses'])}")
    print(f"Wedau verses: {len(wedau['verses'])}")
    
    # Find common verses
    common_verses = set(greek['verses'].keys()) & set(wedau['verses'].keys())
    print(f"Common verses: {len(common_verses)}")
    
    # Test all common verses
    results = []
    passed_traditional = 0
    passed_resonance = 0
    
    print("\n" + "-" * 70)
    print(f"{'Verse':<8} {'Euclidean':<12} {'Resonance':<12} {'Same Attr':<10} {'Quality'}")
    print("-" * 70)
    
    for verse_num in sorted(common_verses, key=int):
        result = test_verse_translation(
            verse_num,
            greek['verses'][verse_num],
            wedau['verses'][verse_num],
            detector, engine
        )
        results.append(result)
        
        if result['passes_traditional']:
            passed_traditional += 1
        if result['passes_resonance']:
            passed_resonance += 1
        
        # Short quality indicator
        qual = "EXCELLENT" if "EXCELLENT" in result['quality'] else "GOOD" if "GOOD" in result['quality'] else "CHECK"
        
        print(f"{verse_num:<8} {result['euclidean_distance']:<12.4f} {result['resonance_convergence']:<12.4f} "
              f"{'Yes' if result['same_attractor'] else 'NO':<10} {qual}")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    total = len(results)
    euclidean_dists = [r['euclidean_distance'] for r in results]
    
    print(f"\nTotal verses tested: {total}")
    print(f"\n--- Traditional Metric (Euclidean < 0.10) ---")
    print(f"Passed: {passed_traditional}/{total} ({passed_traditional/total*100:.1f}%)")
    print(f"Euclidean range: {min(euclidean_dists):.4f} - {max(euclidean_dists):.4f}")
    print(f"Euclidean mean: {np.mean(euclidean_dists):.4f}")
    
    print(f"\n--- Resonance Metric (Convergence < 0.10, Same Attractor) ---")
    print(f"Passed: {passed_resonance}/{total} ({passed_resonance/total*100:.1f}%)")
    
    # Key insight
    print(f"\n>>> KEY INSIGHT:")
    if passed_resonance > passed_traditional:
        rescued = passed_resonance - passed_traditional
        print(f"    Resonance 'rescued' {rescued} verses that failed traditional threshold!")
        print(f"    These have high euclidean distance but converge to same attractor.")
    elif passed_resonance == total:
        print(f"    ALL {total} verses pass resonance validation!")
        print(f"    Greek and Wedau occupy the same semantic basin.")
    
    # Save results
    save_path = os.path.join(os.path.dirname(__file__), 'greek_wedau_test_results.json')
    with open(save_path, 'w') as f:
        json.dump({
            'summary': {
                'total_verses': total,
                'passed_traditional': passed_traditional,
                'passed_resonance': passed_resonance,
                'euclidean_mean': np.mean(euclidean_dists),
                'euclidean_max': max(euclidean_dists)
            },
            'verses': results
        }, f, indent=2)
    
    print(f"\nResults saved to: {save_path}")


if __name__ == '__main__':
    main()
