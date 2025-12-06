"""
Five-Way Comparison: English, Wedau, Greek, Spanish, Chinese
Testing character-based language
"""

import sys
sys.path.append('experiments')

from enhanced_pattern_detector import EnhancedPatternDetector
from greek_pattern_detector import GreekPatternDetector
from spanish_pattern_detector import SpanishPatternDetector
from chinese_pattern_detector import ChinesePatternDetector
import numpy as np
import json


def five_way_comparison():
    """Compare Mark 1 across five languages."""
    
    # Load data
    with open('experiments/nwt_mark_chapter1.json', 'r', encoding='utf-8') as f:
        english_data = json.load(f)
    
    with open('experiments/wedau_mark_chapter1.json', 'r', encoding='utf-8') as f:
        wedau_data = json.load(f)
    
    with open('experiments/greek_mark_chapter1.json', 'r', encoding='utf-8') as f:
        greek_data = json.load(f)
    
    with open('experiments/spanish_mark_chapter1.json', 'r', encoding='utf-8') as f:
        spanish_data = json.load(f)
    
    with open('experiments/chinese_mark_chapter1.json', 'r', encoding='utf-8') as f:
        chinese_data = json.load(f)
    
    # Create detectors
    english_detector = EnhancedPatternDetector()
    wedau_detector = EnhancedPatternDetector()
    greek_detector = GreekPatternDetector()
    spanish_detector = SpanishPatternDetector()
    chinese_detector = ChinesePatternDetector()
    
    print("="*80)
    print("FIVE-WAY COMPARISON: English, Wedau, Greek, Spanish, Chinese")
    print("="*80)
    print("\nTesting character-based language (Chinese):\n")
    print("Predictions:")
    print("1. High variance (different structure)")
    print("2. High Wisdom (compact, integrated meaning)")
    print("3. Moderate Justice (Chinese culture values harmony over absolute truth)")
    print()
    
    # Key verses
    key_verses = [1, 8, 11, 14, 15, 24]
    
    results = []
    
    for verse_num in key_verses:
        verse_str = str(verse_num)
        
        # Get texts
        eng_text = english_data['verses'][verse_str]
        wed_text = wedau_data['verses'][verse_str]
        grk_text = greek_data['verses'][verse_str]
        spa_text = spanish_data['verses'][verse_str]
        chn_text = chinese_data['verses'][verse_str]
        
        # Analyze
        eng_sig = english_detector.calculate_field_signature(eng_text)
        wed_sig = wedau_detector.calculate_field_signature(wed_text)
        grk_sig = greek_detector.calculate_field_signature(grk_text)
        spa_sig = spanish_detector.calculate_field_signature(spa_text)
        chn_sig = chinese_detector.calculate_field_signature(chn_text)
        
        eng_coords = [eng_sig['L'], eng_sig['J'], eng_sig['P'], eng_sig['W']]
        wed_coords = [wed_sig['L'], wed_sig['J'], wed_sig['P'], wed_sig['W']]
        grk_coords = [grk_sig['L'], grk_sig['J'], grk_sig['P'], grk_sig['W']]
        spa_coords = [spa_sig['L'], spa_sig['J'], spa_sig['P'], spa_sig['W']]
        chn_coords = [chn_sig['L'], chn_sig['J'], chn_sig['P'], chn_sig['W']]
        
        # Calculate centroid
        centroid = np.mean([eng_coords, wed_coords, grk_coords, spa_coords, chn_coords], axis=0)
        
        # Calculate variance
        variances = [
            np.linalg.norm(np.array(coords) - centroid)
            for coords in [eng_coords, wed_coords, grk_coords, spa_coords, chn_coords]
        ]
        avg_variance = np.mean(variances)
        chn_variance = variances[4]  # Chinese variance
        
        # English-Chinese distance
        eng_chn_dist = np.linalg.norm(np.array(eng_coords) - np.array(chn_coords))
        
        results.append({
            'verse': verse_num,
            'english_coords': eng_coords,
            'wedau_coords': wed_coords,
            'greek_coords': grk_coords,
            'spanish_coords': spa_coords,
            'chinese_coords': chn_coords,
            'centroid': centroid.tolist(),
            'eng_chn_distance': float(eng_chn_dist),
            'chinese_variance': float(chn_variance),
            'avg_variance': float(avg_variance)
        })
        
        print(f"\nVerse {verse_num}:")
        print(f"  English: L={eng_coords[0]:.3f}, J={eng_coords[1]:.3f}, "
              f"P={eng_coords[2]:.3f}, W={eng_coords[3]:.3f}")
        print(f"  Chinese: L={chn_coords[0]:.3f}, J={chn_coords[1]:.3f}, "
              f"P={chn_coords[2]:.3f}, W={chn_coords[3]:.3f}")
        print(f"  Centroid: L={centroid[0]:.3f}, J={centroid[1]:.3f}, "
              f"P={centroid[2]:.3f}, W={centroid[3]:.3f}")
        print(f"  Eng-Chn distance: {eng_chn_dist:.3f}")
        print(f"  Chinese variance: {chn_variance:.3f}")
        print(f"  Avg variance (5 langs): {avg_variance:.3f}")
    
    # Overall statistics
    print(f"\n{'='*80}")
    print("OVERALL STATISTICS")
    print('='*80)
    
    avg_eng_chn = np.mean([r['eng_chn_distance'] for r in results])
    avg_chn_variance = np.mean([r['chinese_variance'] for r in results])
    avg_total_variance = np.mean([r['avg_variance'] for r in results])
    
    # Chinese-specific analysis
    avg_chn_wisdom = np.mean([r['chinese_coords'][3] for r in results])
    avg_eng_wisdom = np.mean([r['english_coords'][3] for r in results])
    wisdom_diff = avg_chn_wisdom - avg_eng_wisdom
    
    avg_chn_justice = np.mean([r['chinese_coords'][1] for r in results])
    avg_grk_justice = np.mean([r['greek_coords'][1] for r in results])
    justice_diff = avg_chn_justice - avg_grk_justice
    
    print(f"\nAverage English-Chinese Distance: {avg_eng_chn:.3f}")
    print(f"Average Chinese Variance: {avg_chn_variance:.3f}")
    print(f"Average Total Variance (5 languages): {avg_total_variance:.3f}")
    
    print(f"\nChinese Wisdom vs English Wisdom: {wisdom_diff:+.3f}")
    print(f"  Prediction: Positive (Chinese higher)")
    print(f"  Result: {'[CONFIRMED]' if wisdom_diff > 0 else '[OFF]'}")
    
    print(f"\nChinese Justice vs Greek Justice: {justice_diff:+.3f}")
    print(f"  Prediction: Negative (Chinese lower)")
    print(f"  Result: {'[CONFIRMED]' if justice_diff < 0 else '[OFF]'}")
    
    # Language clustering
    print(f"\n{'='*80}")
    print("LANGUAGE CLUSTERING")
    print('='*80)
    
    # Calculate all pairwise distances
    languages = ['English', 'Wedau', 'Greek', 'Spanish', 'Chinese']
    coords_list = [
        [r['english_coords'], r['wedau_coords'], r['greek_coords'], 
         r['spanish_coords'], r['chinese_coords']]
        for r in results
    ]
    
    print("\nAverage Pairwise Distances:")
    for i in range(len(languages)):
        for j in range(i+1, len(languages)):
            distances = [
                np.linalg.norm(np.array(coords[i]) - np.array(coords[j]))
                for coords in coords_list
            ]
            avg_dist = np.mean(distances)
            print(f"  {languages[i]}-{languages[j]}: {avg_dist:.3f}")
    
    # Save results
    output = {
        'summary': {
            'avg_eng_chn_distance': float(avg_eng_chn),
            'avg_chinese_variance': float(avg_chn_variance),
            'avg_total_variance': float(avg_total_variance),
            'chinese_wisdom_boost': float(wisdom_diff),
            'chinese_justice_vs_greek': float(justice_diff)
        },
        'results': results
    }
    
    with open('experiments/five_way_comparison_results.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved to: experiments/five_way_comparison_results.json")
    
    print(f"\n{'='*80}")
    print("FIVE-WAY COMPARISON COMPLETE")
    print("="*80)


if __name__ == "__main__":
    five_way_comparison()
