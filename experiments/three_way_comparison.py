"""
Three-Way Comparison: English, Wedau, Greek
Theological validation across languages
"""

import sys
sys.path.append('experiments')

from enhanced_pattern_detector import EnhancedPatternDetector
from greek_pattern_detector import GreekPatternDetector
import numpy as np
import json


def three_way_comparison():
    """Compare Mark 1 across three languages."""
    
    # Load data
    with open('experiments/nwt_mark_chapter1.json', 'r', encoding='utf-8') as f:
        english_data = json.load(f)
    
    with open('experiments/wedau_mark_chapter1.json', 'r', encoding='utf-8') as f:
        wedau_data = json.load(f)
    
    with open('experiments/greek_mark_chapter1.json', 'r', encoding='utf-8') as f:
        greek_data = json.load(f)
    
    # Create detectors
    english_detector = EnhancedPatternDetector()
    wedau_detector = EnhancedPatternDetector()  # Use original for Wedau
    greek_detector = GreekPatternDetector()
    
    print("="*80)
    print("THREE-WAY COMPARISON: English vs Wedau vs Greek")
    print("="*80)
    print(f"\nAnalyzing {english_data['verse_count']} verses across 3 languages\n")
    
    # Focus on key theological verses
    key_verses = [1, 8, 11, 14, 15, 24]  # Theologically significant
    
    results = []
    
    for verse_num in key_verses:
        verse_str = str(verse_num)
        
        # Get texts
        eng_text = english_data['verses'][verse_str]
        wed_text = wedau_data['verses'][verse_str]
        grk_text = greek_data['verses'][verse_str]
        
        # Analyze
        eng_sig = english_detector.calculate_field_signature(eng_text)
        wed_sig = wedau_detector.calculate_field_signature(wed_text)
        grk_sig = greek_detector.calculate_field_signature(grk_text)
        
        eng_coords = [eng_sig['L'], eng_sig['J'], eng_sig['P'], eng_sig['W']]
        wed_coords = [wed_sig['L'], wed_sig['J'], wed_sig['P'], wed_sig['W']]
        grk_coords = [grk_sig['L'], grk_sig['J'], grk_sig['P'], grk_sig['W']]
        
        # Calculate distances
        eng_wed_dist = np.linalg.norm(np.array(eng_coords) - np.array(wed_coords))
        eng_grk_dist = np.linalg.norm(np.array(eng_coords) - np.array(grk_coords))
        wed_grk_dist = np.linalg.norm(np.array(wed_coords) - np.array(grk_coords))
        
        # Calculate centroid (average coordinates)
        centroid = np.mean([eng_coords, wed_coords, grk_coords], axis=0)
        
        # Calculate variance from centroid
        eng_var = np.linalg.norm(np.array(eng_coords) - centroid)
        wed_var = np.linalg.norm(np.array(wed_coords) - centroid)
        grk_var = np.linalg.norm(np.array(grk_coords) - centroid)
        avg_variance = np.mean([eng_var, wed_var, grk_var])
        
        results.append({
            'verse': verse_num,
            'english_coords': eng_coords,
            'wedau_coords': wed_coords,
            'greek_coords': grk_coords,
            'centroid': centroid.tolist(),
            'distances': {
                'eng_wed': float(eng_wed_dist),
                'eng_grk': float(eng_grk_dist),
                'wed_grk': float(wed_grk_dist)
            },
            'variance': float(avg_variance),
            'consistent': bool(avg_variance < 0.20)
        })
        
        print(f"\nVerse {verse_num}:")
        print(f"  English: L={eng_coords[0]:.3f}, J={eng_coords[1]:.3f}, "
              f"P={eng_coords[2]:.3f}, W={eng_coords[3]:.3f}")
        print(f"  Wedau:   L={wed_coords[0]:.3f}, J={wed_coords[1]:.3f}, "
              f"P={wed_coords[2]:.3f}, W={wed_coords[3]:.3f}")
        print(f"  Greek:   L={grk_coords[0]:.3f}, J={grk_coords[1]:.3f}, "
              f"P={grk_coords[2]:.3f}, W={grk_coords[3]:.3f}")
        print(f"  Centroid: L={centroid[0]:.3f}, J={centroid[1]:.3f}, "
              f"P={centroid[2]:.3f}, W={centroid[3]:.3f}")
        print(f"  Distances: Eng-Wed={eng_wed_dist:.3f}, Eng-Grk={eng_grk_dist:.3f}, "
              f"Wed-Grk={wed_grk_dist:.3f}")
        print(f"  Variance: {avg_variance:.3f} {'[CONSISTENT]' if avg_variance < 0.20 else '[DIVERGENT]'}")
    
    # Overall statistics
    print(f"\n{'='*80}")
    print("OVERALL STATISTICS")
    print('='*80)
    
    avg_eng_wed = np.mean([r['distances']['eng_wed'] for r in results])
    avg_eng_grk = np.mean([r['distances']['eng_grk'] for r in results])
    avg_wed_grk = np.mean([r['distances']['wed_grk'] for r in results])
    avg_variance = np.mean([r['variance'] for r in results])
    consistency_rate = sum(1 for r in results if r['consistent']) / len(results)
    
    print(f"\nPairwise Distances (Average):")
    print(f"  English-Wedau: {avg_eng_wed:.3f}")
    print(f"  English-Greek: {avg_eng_grk:.3f}")
    print(f"  Wedau-Greek:   {avg_wed_grk:.3f}")
    
    print(f"\nAverage Variance from Centroid: {avg_variance:.3f}")
    print(f"Consistency Rate: {consistency_rate:.0%}")
    
    print(f"\nInterpretation:")
    if avg_variance < 0.15:
        print("  [EXCELLENT]: All three languages converge on same meaning")
    elif avg_variance < 0.25:
        print("  [GOOD]: Languages show semantic consistency")
    else:
        print("  [MODERATE]: Some divergence across languages")
    
    # Save results
    output = {
        'summary': {
            'verses_analyzed': len(results),
            'avg_distances': {
                'english_wedau': float(avg_eng_wed),
                'english_greek': float(avg_eng_grk),
                'wedau_greek': float(avg_wed_grk)
            },
            'avg_variance': float(avg_variance),
            'consistency_rate': float(consistency_rate)
        },
        'results': results
    }
    
    with open('experiments/three_way_comparison_results.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved to: experiments/three_way_comparison_results.json")
    
    print(f"\n{'='*80}")
    print("THREE-WAY COMPARISON COMPLETE")
    print("="*80)


if __name__ == "__main__":
    three_way_comparison()
