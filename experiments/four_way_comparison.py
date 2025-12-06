"""
Four-Way Comparison: English, Wedau, Greek, Spanish
Testing Romance language predictions
"""

import sys
sys.path.append('experiments')

from enhanced_pattern_detector import EnhancedPatternDetector
from greek_pattern_detector import GreekPatternDetector
from spanish_pattern_detector import SpanishPatternDetector
import numpy as np
import json


def four_way_comparison():
    """Compare Mark 1 across four languages."""
    
    # Load data
    with open('experiments/nwt_mark_chapter1.json', 'r', encoding='utf-8') as f:
        english_data = json.load(f)
    
    with open('experiments/wedau_mark_chapter1.json', 'r', encoding='utf-8') as f:
        wedau_data = json.load(f)
    
    with open('experiments/greek_mark_chapter1.json', 'r', encoding='utf-8') as f:
        greek_data = json.load(f)
    
    with open('experiments/spanish_mark_chapter1.json', 'r', encoding='utf-8') as f:
        spanish_data = json.load(f)
    
    # Create detectors
    english_detector = EnhancedPatternDetector()
    wedau_detector = EnhancedPatternDetector()
    greek_detector = GreekPatternDetector()
    spanish_detector = SpanishPatternDetector()
    
    print("="*80)
    print("FOUR-WAY COMPARISON: English vs Wedau vs Greek vs Spanish")
    print("="*80)
    print("\nTesting Romance language predictions:\n")
    print("1. Spanish Love: +0.10-0.15 above English")
    print("2. Spanish-English distance: 0.15-0.25")
    print("3. Spanish Justice < Greek Justice")
    print("4. Consistent theological terms\n")
    
    # Key theological verses
    key_verses = [1, 8, 11, 14, 15, 24]
    
    results = []
    
    for verse_num in key_verses:
        verse_str = str(verse_num)
        
        # Get texts
        eng_text = english_data['verses'][verse_str]
        wed_text = wedau_data['verses'][verse_str]
        grk_text = greek_data['verses'][verse_str]
        spa_text = spanish_data['verses'][verse_str]
        
        # Analyze
        eng_sig = english_detector.calculate_field_signature(eng_text)
        wed_sig = wedau_detector.calculate_field_signature(wed_text)
        grk_sig = greek_detector.calculate_field_signature(grk_text)
        spa_sig = spanish_detector.calculate_field_signature(spa_text)
        
        eng_coords = [eng_sig['L'], eng_sig['J'], eng_sig['P'], eng_sig['W']]
        wed_coords = [wed_sig['L'], wed_sig['J'], wed_sig['P'], wed_sig['W']]
        grk_coords = [grk_sig['L'], grk_sig['J'], grk_sig['P'], grk_sig['W']]
        spa_coords = [spa_sig['L'], spa_sig['J'], spa_sig['P'], spa_sig['W']]
        
        # Calculate centroid
        centroid = np.mean([eng_coords, wed_coords, grk_coords, spa_coords], axis=0)
        
        # Calculate distances
        eng_spa_dist = np.linalg.norm(np.array(eng_coords) - np.array(spa_coords))
        
        # Calculate variance
        variances = [
            np.linalg.norm(np.array(coords) - centroid)
            for coords in [eng_coords, wed_coords, grk_coords, spa_coords]
        ]
        avg_variance = np.mean(variances)
        
        results.append({
            'verse': verse_num,
            'english_coords': eng_coords,
            'wedau_coords': wed_coords,
            'greek_coords': grk_coords,
            'spanish_coords': spa_coords,
            'centroid': centroid.tolist(),
            'eng_spa_distance': float(eng_spa_dist),
            'variance': float(avg_variance)
        })
        
        print(f"\nVerse {verse_num}:")
        print(f"  English: L={eng_coords[0]:.3f}, J={eng_coords[1]:.3f}, "
              f"P={eng_coords[2]:.3f}, W={eng_coords[3]:.3f}")
        print(f"  Spanish: L={spa_coords[0]:.3f}, J={spa_coords[1]:.3f}, "
              f"P={spa_coords[2]:.3f}, W={spa_coords[3]:.3f}")
        print(f"  Greek:   L={grk_coords[0]:.3f}, J={grk_coords[1]:.3f}, "
              f"P={grk_coords[2]:.3f}, W={grk_coords[3]:.3f}")
        print(f"  Wedau:   L={wed_coords[0]:.3f}, J={wed_coords[1]:.3f}, "
              f"P={wed_coords[2]:.3f}, W={wed_coords[3]:.3f}")
        print(f"  Centroid: L={centroid[0]:.3f}, J={centroid[1]:.3f}, "
              f"P={centroid[2]:.3f}, W={centroid[3]:.3f}")
        print(f"  Eng-Spa distance: {eng_spa_dist:.3f}")
        print(f"  Variance: {avg_variance:.3f}")
        
        # Test predictions
        spa_love_boost = spa_coords[0] - eng_coords[0]
        spa_justice_vs_greek = spa_coords[1] - grk_coords[1]
        
        print(f"  Spanish Love boost: {spa_love_boost:+.3f} "
              f"{'[PREDICTED]' if 0.10 <= spa_love_boost <= 0.15 else '[OFF]'}")
        print(f"  Spanish J vs Greek J: {spa_justice_vs_greek:+.3f} "
              f"{'[PREDICTED]' if spa_justice_vs_greek < 0 else '[OFF]'}")
    
    # Overall statistics
    print(f"\n{'='*80}")
    print("OVERALL STATISTICS")
    print('='*80)
    
    avg_eng_spa = np.mean([r['eng_spa_distance'] for r in results])
    avg_variance = np.mean([r['variance'] for r in results])
    
    # Test predictions
    avg_spa_love_boost = np.mean([
        r['spanish_coords'][0] - r['english_coords'][0] for r in results
    ])
    avg_spa_j_vs_grk = np.mean([
        r['spanish_coords'][1] - r['greek_coords'][1] for r in results
    ])
    
    print(f"\nAverage English-Spanish Distance: {avg_eng_spa:.3f}")
    print(f"  Prediction: 0.15-0.25")
    print(f"  Result: {'[CONFIRMED]' if 0.15 <= avg_eng_spa <= 0.25 else '[OFF]'}")
    
    print(f"\nAverage Spanish Love Boost: {avg_spa_love_boost:+.3f}")
    print(f"  Prediction: +0.10 to +0.15")
    print(f"  Result: {'[CONFIRMED]' if 0.10 <= avg_spa_love_boost <= 0.15 else '[OFF]'}")
    
    print(f"\nAverage Spanish J vs Greek J: {avg_spa_j_vs_grk:+.3f}")
    print(f"  Prediction: Negative (Spanish < Greek)")
    print(f"  Result: {'[CONFIRMED]' if avg_spa_j_vs_grk < 0 else '[OFF]'}")
    
    print(f"\nAverage Variance (4 languages): {avg_variance:.3f}")
    
    # Save results
    output = {
        'summary': {
            'avg_eng_spa_distance': float(avg_eng_spa),
            'avg_spanish_love_boost': float(avg_spa_love_boost),
            'avg_spanish_j_vs_greek_j': float(avg_spa_j_vs_grk),
            'avg_variance': float(avg_variance),
            'predictions': {
                'eng_spa_distance': bool(0.15 <= avg_eng_spa <= 0.25),
                'love_boost': bool(0.10 <= avg_spa_love_boost <= 0.15),
                'justice_lower_than_greek': bool(avg_spa_j_vs_grk < 0)
            }
        },
        'results': results
    }
    
    with open('experiments/four_way_comparison_results.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved to: experiments/four_way_comparison_results.json")
    
    print(f"\n{'='*80}")
    print("FOUR-WAY COMPARISON COMPLETE")
    print("="*80)


if __name__ == "__main__":
    four_way_comparison()
