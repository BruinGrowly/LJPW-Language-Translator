#!/usr/bin/env python3
"""
Resonance Demo: Real Verse Translation Analysis
================================================

Demonstrates how LJPW resonance helps semantic translation by analyzing
actual Mark Chapter 1 verses across Greek, English (NWT), and Wedau.

Shows:
1. How translations converge to same semantic attractor
2. Quality assessment via resonance dynamics
3. Why resonance is deeper than simple distance metrics
"""

import json
import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_quantum.resonance_engine import ResonanceEngine
from experiments.enhanced_pattern_detector import EnhancedPatternDetector


def load_verses():
    """Load Mark chapter 1 from multiple languages."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    with open(os.path.join(base_path, 'greek_mark_chapter1.json'), 'r', encoding='utf-8') as f:
        greek = json.load(f)
    
    with open(os.path.join(base_path, 'nwt_mark_chapter1.json'), 'r', encoding='utf-8') as f:
        english = json.load(f)
    
    with open(os.path.join(base_path, 'wedau_mark_chapter1.json'), 'r', encoding='utf-8') as f:
        wedau = json.load(f)
    
    return greek, english, wedau


def get_ljpw_coords(text: str, detector: EnhancedPatternDetector) -> list:
    """Get LJPW coordinates for text using pattern detector."""
    result = detector.calculate_field_signature_v2(text)
    return [result['L'], result['J'], result['P'], result['W']]


def analyze_verse_translations(verse_num: str, greek_text: str, english_text: str, wedau_text: str):
    """Analyze how a verse translates across languages using resonance."""
    
    detector = EnhancedPatternDetector()
    engine = ResonanceEngine()
    
    # Get LJPW coordinates for each translation
    greek_coords = get_ljpw_coords(greek_text, detector)
    english_coords = get_ljpw_coords(english_text, detector)
    wedau_coords = get_ljpw_coords(wedau_text, detector)
    
    print(f"\nMark 1:{verse_num}")
    print("=" * 70)
    
    # Show the texts (truncated, ASCII-safe)
    try:
        print(f"\nGreek:   {greek_text[:60]}...")
    except:
        print(f"\nGreek:   [Greek text - {len(greek_text)} chars]")
    try:
        print(f"English: {english_text[:60]}...")
    except:
        print(f"English: [English text - {len(english_text)} chars]")
    try:
        print(f"Wedau:   {wedau_text[:60]}...")
    except:
        print(f"Wedau:   [Wedau text - {len(wedau_text)} chars]")
    
    # Show LJPW coordinates
    print(f"\nInitial LJPW Coordinates:")
    print(f"  Greek:   L={greek_coords[0]:.3f}, J={greek_coords[1]:.3f}, P={greek_coords[2]:.3f}, W={greek_coords[3]:.3f}")
    print(f"  English: L={english_coords[0]:.3f}, J={english_coords[1]:.3f}, P={english_coords[2]:.3f}, W={english_coords[3]:.3f}")
    print(f"  Wedau:   L={wedau_coords[0]:.3f}, J={wedau_coords[1]:.3f}, P={wedau_coords[2]:.3f}, W={wedau_coords[3]:.3f}")
    
    # Calculate euclidean distances (traditional metric)
    grk_eng_dist = np.linalg.norm(np.array(greek_coords) - np.array(english_coords))
    grk_wed_dist = np.linalg.norm(np.array(greek_coords) - np.array(wedau_coords))
    eng_wed_dist = np.linalg.norm(np.array(english_coords) - np.array(wedau_coords))
    
    print(f"\nTraditional Euclidean Distances:")
    print(f"  Greek -> English: {grk_eng_dist:.4f}")
    print(f"  Greek -> Wedau:   {grk_wed_dist:.4f}")
    print(f"  English -> Wedau: {eng_wed_dist:.4f}")
    
    # Run resonance analysis
    print(f"\n--- Resonance Analysis (100 cycles) ---")
    
    grk_eng = engine.analyze_translation_pair(greek_coords, english_coords, cycles=100)
    grk_wed = engine.analyze_translation_pair(greek_coords, wedau_coords, cycles=100)
    eng_wed = engine.analyze_translation_pair(english_coords, wedau_coords, cycles=100)
    
    print(f"\nGreek -> English:")
    print(f"  Resonance convergence: {grk_eng['convergence_distance']:.4f}")
    print(f"  Same semantic attractor: {grk_eng['same_deficit']}")
    print(f"  Quality: {grk_eng['quality_assessment']}")
    
    print(f"\nGreek -> Wedau:")
    print(f"  Resonance convergence: {grk_wed['convergence_distance']:.4f}")
    print(f"  Same semantic attractor: {grk_wed['same_deficit']}")
    print(f"  Quality: {grk_wed['quality_assessment']}")
    
    print(f"\nEnglish -> Wedau:")
    print(f"  Resonance convergence: {eng_wed['convergence_distance']:.4f}")
    print(f"  Same semantic attractor: {eng_wed['same_deficit']}")
    print(f"  Quality: {eng_wed['quality_assessment']}")
    
    # Key insight
    print("\n>>> KEY INSIGHT:")
    if grk_eng_dist > 0.05 or grk_wed_dist > 0.05:
        print(f"    Traditional distance shows drift ({max(grk_eng_dist, grk_wed_dist):.4f})")
        if grk_eng['convergence_distance'] < 0.001 and grk_wed['convergence_distance'] < 0.001:
            print(f"    BUT resonance shows ALL converge to SAME attractor!")
            print(f"    -> Translations are SEMANTICALLY EQUIVALENT despite surface differences")
    else:
        print(f"    All translations are close in both metrics - excellent preservation!")
    
    return {
        'verse': verse_num,
        'traditional_distances': {'grk_eng': grk_eng_dist, 'grk_wed': grk_wed_dist, 'eng_wed': eng_wed_dist},
        'resonance_quality': {'grk_eng': grk_eng['quality_assessment'], 'grk_wed': grk_wed['quality_assessment']}
    }


def main():
    print("=" * 70)
    print("RESONANCE TRANSLATION DEMO: Mark Chapter 1")
    print("Greek -> English (NWT) -> Wedau")
    print("=" * 70)
    print("\nThis demonstrates how LJPW resonance provides deeper semantic")
    print("equivalence testing than simple coordinate distance.")
    
    greek, english, wedau = load_verses()
    
    # Analyze key verses
    results = []
    for verse_num in ['1', '11', '15', '41']:  # Diverse theological content
        if verse_num in greek['verses'] and verse_num in english['verses'] and verse_num in wedau['verses']:
            result = analyze_verse_translations(
                verse_num,
                greek['verses'][verse_num],
                english['verses'][verse_num],
                wedau['verses'][verse_num]
            )
            results.append(result)
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY: Why Resonance Matters for Translation")
    print("=" * 70)
    print("""
Traditional metric (Euclidean distance):
  - Measures HOW FAR coordinates are apart
  - Same meaning in different languages may have different coordinates
  - Can falsely flag good translations as problematic

Resonance metric (Attractor convergence):
  - Measures WHERE coordinates converge under dynamics
  - Translations to the SAME attractor = semantically equivalent
  - Reveals deep meaning equivalence regardless of surface differences

Key insight: "Resonance finds semantic equivalence that distance misses"
""")
    
    # Save results
    save_path = os.path.join(os.path.dirname(__file__), 'resonance_demo_results.json')
    with open(save_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to: {save_path}")


if __name__ == '__main__':
    main()
