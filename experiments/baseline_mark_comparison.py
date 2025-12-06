"""
Baseline Experiment: Mark English vs Wedau (Simplified)
Compare LJPW coordinates for parallel verses.
"""

import sys
sys.path.append('experiments')

from enhanced_pattern_detector import EnhancedPatternDetector
import numpy as np


class SimpleComparator:
    """Simple LJPW coordinate comparator."""
    
    def __init__(self):
        self.detector = EnhancedPatternDetector()
    
    def analyze_verse(self, text: str, language: str = 'english') -> dict:
        """Analyze a verse and return LJPW coordinates."""
        signature = self.detector.calculate_field_signature(text)
        
        coords = [signature['L'], signature['J'], signature['P'], signature['W']]
        harmony = self.calculate_harmony(coords)
        
        return {
            'text': text,
            'language': language,
            'coordinates': coords,
            'harmony': harmony,
            'confidence': signature['confidence'],
            'evidence': signature['evidence']
        }
    
    def calculate_harmony(self, coords):
        """Calculate harmony index (proximity to Anchor Point)."""
        L, J, P, W = coords
        distance = np.sqrt((1-L)**2 + (1-J)**2 + (1-P)**2 + (1-W)**2)
        return 1.0 / (1.0 + distance)
    
    def compare_verses(self, english_text: str, wedau_text: str) -> dict:
        """Compare parallel verses in English and Wedau."""
        english = self.analyze_verse(english_text, 'english')
        wedau = self.analyze_verse(wedau_text, 'wedau')
        
        # Calculate semantic distance
        distance = np.linalg.norm(
            np.array(english['coordinates']) - np.array(wedau['coordinates'])
        )
        
        # Calculate coordinate-wise differences
        coord_diff = {
            'L': abs(english['coordinates'][0] - wedau['coordinates'][0]),
            'J': abs(english['coordinates'][1] - wedau['coordinates'][1]),
            'P': abs(english['coordinates'][2] - wedau['coordinates'][2]),
            'W': abs(english['coordinates'][3] - wedau['coordinates'][3])
        }
        
        return {
            'english': english,
            'wedau': wedau,
            'semantic_distance': distance,
            'coordinate_differences': coord_diff,
            'harmony_difference': abs(english['harmony'] - wedau['harmony']),
            'consistent': distance < 0.25  # Threshold for consistency
        }


def main():
    """Run baseline experiment on Mark 1:1-10."""
    comparator = SimpleComparator()
    
    # Sample verses from Mark 1
    # Using approximated Wedau for now - will need actual HTML extraction
    test_verses = [
        {
            'ref': 'Mark 1:1',
            'english': 'The beginning of the good news about Jesus Christ, the Son of God',
            'wedau': 'Beginning ana good news ana Jesus Christ, Son ana God'
        },
        {
            'ref': 'Mark 1:4',
            'english': 'John the Baptist appeared in the wilderness proclaiming baptism of repentance for forgiveness of sins',
            'wedau': 'John Baptist i appear i wilderness i proclaim baptism ana repentance ana forgiveness ana sins'
        },
        {
            'ref': 'Mark 1:9',
            'english': 'Jesus came from Nazareth of Galilee and was baptized by John in the Jordan',
            'wedau': 'Jesus i come from Nazareth ana Galilee i baptized by John i Jordan'
        },
        {
            'ref': 'Mark 1:14',
            'english': 'Jesus came into Galilee proclaiming the good news of God',
            'wedau': 'Jesus i come i Galilee i proclaim good news ana God'
        },
        {
            'ref': 'Mark 1:15',
            'english': 'The time is fulfilled and the kingdom of God has come near repent and believe in the good news',
            'wedau': 'Time i fulfilled kingdom ana God i come near repent believe i good news'
        }
    ]
    
    print("="*80)
    print("BASELINE EXPERIMENT: Mark English vs Wedau")
    print("="*80)
    print("\nComparing LJPW coordinates for parallel verses")
    print("NOTE: Using approximated Wedau text for baseline testing\n")
    
    results = []
    for verse in test_verses:
        print(f"\n{'='*80}")
        print(f"VERSE: {verse['ref']}")
        print('='*80)
        
        result = comparator.compare_verses(verse['english'], verse['wedau'])
        
        print(f"\nEnglish: \"{verse['english']}\"")
        print(f"  Coordinates: L={result['english']['coordinates'][0]:.3f}, "
              f"J={result['english']['coordinates'][1]:.3f}, "
              f"P={result['english']['coordinates'][2]:.3f}, "
              f"W={result['english']['coordinates'][3]:.3f}")
        print(f"  Harmony: {result['english']['harmony']:.3f}")
        print(f"  Confidence: {result['english']['confidence']:.2f}")
        
        print(f"\nWedau: \"{verse['wedau']}\"")
        print(f"  Coordinates: L={result['wedau']['coordinates'][0]:.3f}, "
              f"J={result['wedau']['coordinates'][1]:.3f}, "
              f"P={result['wedau']['coordinates'][2]:.3f}, "
              f"W={result['wedau']['coordinates'][3]:.3f}")
        print(f"  Harmony: {result['wedau']['harmony']:.3f}")
        print(f"  Confidence: {result['wedau']['confidence']:.2f}")
        
        print(f"\nComparison:")
        print(f"  Semantic Distance: {result['semantic_distance']:.3f}")
        print(f"  Coordinate Differences:")
        print(f"    DL = {result['coordinate_differences']['L']:.3f}")
        print(f"    DJ = {result['coordinate_differences']['J']:.3f}")
        print(f"    DP = {result['coordinate_differences']['P']:.3f}")
        print(f"    DW = {result['coordinate_differences']['W']:.3f}")
        print(f"  Harmony Difference: {result['harmony_difference']:.3f}")
        print(f"  Consistent: {'[YES]' if result['consistent'] else '[NO - distance > 0.25]'}")
        
        results.append(result)
    
    # Overall statistics
    print(f"\n{'='*80}")
    print("OVERALL STATISTICS")
    print('='*80)
    
    avg_distance = np.mean([r['semantic_distance'] for r in results])
    avg_harmony_diff = np.mean([r['harmony_difference'] for r in results])
    consistency_rate = sum(1 for r in results if r['consistent']) / len(results)
    
    avg_L_diff = np.mean([r['coordinate_differences']['L'] for r in results])
    avg_J_diff = np.mean([r['coordinate_differences']['J'] for r in results])
    avg_P_diff = np.mean([r['coordinate_differences']['P'] for r in results])
    avg_W_diff = np.mean([r['coordinate_differences']['W'] for r in results])
    
    print(f"\nAverage Semantic Distance: {avg_distance:.3f}")
    print(f"Average Coordinate Differences:")
    print(f"  DL = {avg_L_diff:.3f}")
    print(f"  DJ = {avg_J_diff:.3f}")
    print(f"  DP = {avg_P_diff:.3f}")
    print(f"  DW = {avg_W_diff:.3f}")
    print(f"Average Harmony Difference: {avg_harmony_diff:.3f}")
    print(f"Consistency Rate: {consistency_rate:.0%}")
    
    print(f"\nInterpretation:")
    if avg_distance < 0.15:
        print("  [EXCELLENT]: Translations are semantically very close")
    elif avg_distance < 0.25:
        print("  [GOOD]: Translations are semantically similar")
    elif avg_distance < 0.35:
        print("  [MODERATE]: Some semantic drift detected")
    else:
        print("  [POOR]: Significant semantic differences")
    
    print("\n" + "="*80)
    print("BASELINE EXPERIMENT COMPLETE")
    print("="*80)
    print("\nNEXT STEPS:")
    print("1. Extract actual Wedau text from HTML files")
    print("2. Compare larger sample (all of Mark chapter 1)")
    print("3. Analyze patterns in semantic drift")
    print("4. Tune detection for Wedau-specific patterns")


if __name__ == "__main__":
    main()
