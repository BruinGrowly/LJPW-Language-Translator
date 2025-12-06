"""
Re-Comparison with Tuned Wedau Detector
Compare results before and after tuning
"""

import sys
sys.path.append('experiments')

from wedau_pattern_detector import WedauPatternDetector
from enhanced_pattern_detector import EnhancedPatternDetector
import numpy as np
import json


def compare_detectors():
    """Compare original vs tuned detector."""
    # Load data
    with open('experiments/nwt_mark_chapter1.json', 'r', encoding='utf-8') as f:
        english_data = json.load(f)
    
    with open('experiments/wedau_mark_chapter1.json', 'r', encoding='utf-8') as f:
        wedau_data = json.load(f)
    
    # Create detectors
    original_detector = EnhancedPatternDetector()
    tuned_detector = WedauPatternDetector()
    
    print("="*80)
    print("DETECTOR COMPARISON: Original vs Tuned Wedau")
    print("="*80)
    
    # Compare on sample verses
    sample_verses = [1, 4, 8, 15, 24]  # Mix of simple and complex
    
    results = {
        'original': [],
        'tuned': [],
        'improvements': []
    }
    
    for verse_num in sample_verses:
        verse_str = str(verse_num)
        english_text = english_data['verses'][verse_str]
        wedau_text = wedau_data['verses'][verse_str]
        
        # Analyze with original detector
        orig_sig = original_detector.calculate_field_signature(wedau_text)
        orig_coords = [orig_sig['L'], orig_sig['J'], orig_sig['P'], orig_sig['W']]
        
        # Analyze with tuned detector
        tuned_sig = tuned_detector.calculate_field_signature(wedau_text)
        tuned_coords = [tuned_sig['L'], tuned_sig['J'], tuned_sig['P'], tuned_sig['W']]
        
        # Analyze English (for comparison)
        eng_sig = original_detector.calculate_field_signature(english_text)
        eng_coords = [eng_sig['L'], eng_sig['J'], eng_sig['P'], eng_sig['W']]
        
        # Calculate distances
        orig_distance = np.linalg.norm(np.array(orig_coords) - np.array(eng_coords))
        tuned_distance = np.linalg.norm(np.array(tuned_coords) - np.array(eng_coords))
        improvement = orig_distance - tuned_distance
        
        results['original'].append({
            'verse': verse_num,
            'coords': orig_coords,
            'distance': float(orig_distance)
        })
        
        results['tuned'].append({
            'verse': verse_num,
            'coords': tuned_coords,
            'distance': float(tuned_distance)
        })
        
        results['improvements'].append({
            'verse': verse_num,
            'improvement': float(improvement),
            'percent': float((improvement / orig_distance * 100) if orig_distance > 0 else 0)
        })
        
        print(f"\nVerse {verse_num}:")
        print(f"  Original distance:  {orig_distance:.3f}")
        print(f"  Tuned distance:     {tuned_distance:.3f}")
        print(f"  Improvement:        {improvement:+.3f} ({improvement/orig_distance*100:+.1f}%)")
    
    # Overall statistics
    avg_orig = np.mean([r['distance'] for r in results['original']])
    avg_tuned = np.mean([r['distance'] for r in results['tuned']])
    avg_improvement = avg_orig - avg_tuned
    
    print(f"\n{'='*80}")
    print("OVERALL IMPROVEMENT")
    print('='*80)
    print(f"Average distance (original):  {avg_orig:.3f}")
    print(f"Average distance (tuned):     {avg_tuned:.3f}")
    print(f"Average improvement:          {avg_improvement:+.3f} ({avg_improvement/avg_orig*100:+.1f}%)")
    
    # Save results
    with open('experiments/detector_comparison_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: experiments/detector_comparison_results.json")
    
    return results


if __name__ == "__main__":
    compare_detectors()
