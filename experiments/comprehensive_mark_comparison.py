"""
Comprehensive Mark Chapter 1 Comparison - All 45 Verses
English (NWT) vs Wedau
"""

import sys
sys.path.append('experiments')

from enhanced_pattern_detector import EnhancedPatternDetector
import numpy as np
import json


class ComprehensiveComparator:
    """Compare all 45 verses in Mark Chapter 1."""
    
    def __init__(self):
        self.detector = EnhancedPatternDetector()
    
    def analyze_verse(self, text: str) -> dict:
        """Analyze a verse and return LJPW coordinates."""
        signature = self.detector.calculate_field_signature(text)
        coords = [signature['L'], signature['J'], signature['P'], signature['W']]
        harmony = self.calculate_harmony(coords)
        
        return {
            'coordinates': coords,
            'harmony': harmony,
            'confidence': signature['confidence']
        }
    
    def calculate_harmony(self, coords):
        """Calculate harmony index."""
        L, J, P, W = coords
        distance = np.sqrt((1-L)**2 + (1-J)**2 + (1-P)**2 + (1-W)**2)
        return 1.0 / (1.0 + distance)
    
    def compare_all_verses(self, english_data: dict, wedau_data: dict) -> list:
        """Compare all verses."""
        results = []
        
        for verse_num in range(1, 46):
            verse_str = str(verse_num)
            
            if verse_str not in english_data['verses'] or verse_str not in wedau_data['verses']:
                continue
            
            english_text = english_data['verses'][verse_str]
            wedau_text = wedau_data['verses'][verse_str]
            
            english_analysis = self.analyze_verse(english_text)
            wedau_analysis = self.analyze_verse(wedau_text)
            
            # Calculate distance
            distance = np.linalg.norm(
                np.array(english_analysis['coordinates']) - 
                np.array(wedau_analysis['coordinates'])
            )
            
            # Coordinate differences
            coord_diff = {
                'L': abs(english_analysis['coordinates'][0] - wedau_analysis['coordinates'][0]),
                'J': abs(english_analysis['coordinates'][1] - wedau_analysis['coordinates'][1]),
                'P': abs(english_analysis['coordinates'][2] - wedau_analysis['coordinates'][2]),
                'W': abs(english_analysis['coordinates'][3] - wedau_analysis['coordinates'][3])
            }
            
            results.append({
                'verse': verse_num,
                'english': english_analysis,
                'wedau': wedau_analysis,
                'distance': distance,
                'coord_diff': coord_diff,
                'consistent': distance < 0.25
            })
        
        return results


def main():
    """Run comprehensive comparison."""
    print("="*80)
    print("COMPREHENSIVE MARK CHAPTER 1 COMPARISON")
    print("All 45 Verses: English (NWT) vs Wedau")
    print("="*80)
    
    # Load data
    with open('experiments/nwt_mark_chapter1.json', 'r', encoding='utf-8') as f:
        english_data = json.load(f)
    
    with open('experiments/wedau_mark_chapter1.json', 'r', encoding='utf-8') as f:
        wedau_data = json.load(f)
    
    print(f"\nEnglish verses: {english_data['verse_count']}")
    print(f"Wedau verses: {wedau_data['verse_count']}")
    
    # Run comparison
    comparator = ComprehensiveComparator()
    results = comparator.compare_all_verses(english_data, wedau_data)
    
    print(f"\nComparing {len(results)} verses...\n")
    
    # Calculate statistics
    distances = [r['distance'] for r in results]
    avg_distance = np.mean(distances)
    min_distance = np.min(distances)
    max_distance = np.max(distances)
    std_distance = np.std(distances)
    consistency_rate = sum(1 for r in results if r['consistent']) / len(results)
    
    # Dimension-wise statistics
    avg_L_diff = np.mean([r['coord_diff']['L'] for r in results])
    avg_J_diff = np.mean([r['coord_diff']['J'] for r in results])
    avg_P_diff = np.mean([r['coord_diff']['P'] for r in results])
    avg_W_diff = np.mean([r['coord_diff']['W'] for r in results])
    
    # Show detailed results for first 10 verses
    print("SAMPLE RESULTS (First 10 verses):")
    print("-"*80)
    for result in results[:10]:
        print(f"\nVerse {result['verse']}:")
        print(f"  Distance: {result['distance']:.3f}")
        print(f"  English:  L={result['english']['coordinates'][0]:.3f}, "
              f"J={result['english']['coordinates'][1]:.3f}, "
              f"P={result['english']['coordinates'][2]:.3f}, "
              f"W={result['english']['coordinates'][3]:.3f}, H={result['english']['harmony']:.3f}")
        print(f"  Wedau:    L={result['wedau']['coordinates'][0]:.3f}, "
              f"J={result['wedau']['coordinates'][1]:.3f}, "
              f"P={result['wedau']['coordinates'][2]:.3f}, "
              f"W={result['wedau']['coordinates'][3]:.3f}, H={result['wedau']['harmony']:.3f}")
        print(f"  Consistent: {'[YES]' if result['consistent'] else '[NO]'}")
    
    # Overall statistics
    print(f"\n{'='*80}")
    print("OVERALL STATISTICS (All 45 Verses)")
    print('='*80)
    print(f"\nSemantic Distance:")
    print(f"  Average:  {avg_distance:.3f}")
    print(f"  Minimum:  {min_distance:.3f}")
    print(f"  Maximum:  {max_distance:.3f}")
    print(f"  Std Dev:  {std_distance:.3f}")
    
    print(f"\nCoordinate Differences (Average):")
    print(f"  DL = {avg_L_diff:.3f}")
    print(f"  DJ = {avg_J_diff:.3f}")
    print(f"  DP = {avg_P_diff:.3f}")
    print(f"  DW = {avg_W_diff:.3f}")
    
    print(f"\nConsistency Rate: {consistency_rate:.0%}")
    print(f"  Consistent (distance < 0.25): {sum(1 for r in results if r['consistent'])}/{len(results)}")
    print(f"  Inconsistent (distance >= 0.25): {sum(1 for r in results if not r['consistent'])}/{len(results)}")
    
    # Interpretation
    print(f"\nInterpretation:")
    if avg_distance < 0.15:
        print("  [EXCELLENT]: Translations are semantically very close")
    elif avg_distance < 0.25:
        print("  [GOOD]: Translations are semantically similar")
    elif avg_distance < 0.35:
        print("  [MODERATE]: Some semantic drift detected")
    else:
        print("  [POOR]: Significant semantic differences")
    
    # Find outliers
    outliers = [r for r in results if r['distance'] > avg_distance + std_distance]
    if outliers:
        print(f"\nOutliers (distance > {avg_distance + std_distance:.3f}):")
        for r in outliers:
            print(f"  Verse {r['verse']}: distance = {r['distance']:.3f}")
    
    # Find best matches
    best_matches = sorted(results, key=lambda x: x['distance'])[:5]
    print(f"\nBest Matches (Top 5):")
    for r in best_matches:
        print(f"  Verse {r['verse']}: distance = {r['distance']:.3f}")
    
    # Save detailed results
    output = {
        'summary': {
            'total_verses': len(results),
            'avg_distance': float(avg_distance),
            'min_distance': float(min_distance),
            'max_distance': float(max_distance),
            'std_distance': float(std_distance),
            'consistency_rate': float(consistency_rate),
            'avg_coord_diff': {
                'L': float(avg_L_diff),
                'J': float(avg_J_diff),
                'P': float(avg_P_diff),
                'W': float(avg_W_diff)
            }
        },
        'results': [
            {
                'verse': r['verse'],
                'distance': float(r['distance']),
                'consistent': bool(r['consistent']),  # Explicitly convert to bool
                'english_coords': [float(x) for x in r['english']['coordinates']],
                'wedau_coords': [float(x) for x in r['wedau']['coordinates']],
                'coord_diff': {k: float(v) for k, v in r['coord_diff'].items()}
            }
            for r in results
        ]
    }
    
    with open('experiments/mark_chapter1_comparison_results.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n{'='*80}")
    print("COMPREHENSIVE COMPARISON COMPLETE")
    print("="*80)
    print("\nResults saved to: experiments/mark_chapter1_comparison_results.json")


if __name__ == "__main__":
    main()
