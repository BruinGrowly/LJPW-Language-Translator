"""
Improved Verse Matching System
Implements semantic distance thresholding, context-aware matching, and dimension weighting
"""

import sys
sys.path.append('experiments')

from enhanced_pattern_detector import EnhancedPatternDetector
from greek_pattern_detector import GreekPatternDetector
from spanish_pattern_detector import SpanishPatternDetector
from chinese_pattern_detector import ChinesePatternDetector
import numpy as np
import json


class ImprovedVerseMatcher:
    """
    Enhanced verse matching with:
    - Semantic distance thresholding
    - Context-aware matching (surrounding verses)
    - Dimension weighting (emphasize stable dimensions)
    """
    
    def __init__(self):
        self.detectors = {
            'english': EnhancedPatternDetector(),
            'wedau': EnhancedPatternDetector(),
            'greek': GreekPatternDetector(),
            'spanish': SpanishPatternDetector(),
            'chinese': ChinesePatternDetector()
        }
        
        # Load verse data
        self.verse_data = {}
        self._load_verse_data()
        
        # Dimension weights (based on stability analysis)
        # Power is most stable (0.088), Love is least stable (0.172)
        self.dimension_weights = {
            'P': 2.0,  # Power: highest weight (most stable)
            'J': 1.5,  # Justice: high weight
            'W': 1.3,  # Wisdom: moderate weight
            'L': 1.0   # Love: baseline weight (most cultural)
        }
        
        # Distance thresholds
        self.thresholds = {
            'excellent': 0.15,  # Very close match
            'good': 0.25,       # Good match
            'moderate': 0.40,   # Acceptable match
            'poor': 0.60        # Questionable match
        }
        
        # Context window (verses before/after to consider)
        self.context_window = 2
    
    def _load_verse_data(self):
        """Load all verse data."""
        files = {
            'english': 'experiments/nwt_mark_chapter1.json',
            'wedau': 'experiments/wedau_mark_chapter1.json',
            'greek': 'experiments/greek_mark_chapter1.json',
            'spanish': 'experiments/spanish_mark_chapter1.json',
            'chinese': 'experiments/chinese_mark_chapter1.json'
        }
        
        for lang, filepath in files.items():
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.verse_data[lang] = data['verses']
    
    def weighted_distance(self, coords1: list, coords2: list) -> float:
        """
        Calculate weighted Euclidean distance.
        Emphasizes stable dimensions (Power, Justice).
        """
        L1, J1, P1, W1 = coords1
        L2, J2, P2, W2 = coords2
        
        weighted_sq_diff = (
            self.dimension_weights['L'] * (L1 - L2)**2 +
            self.dimension_weights['J'] * (J1 - J2)**2 +
            self.dimension_weights['P'] * (P1 - P2)**2 +
            self.dimension_weights['W'] * (W1 - W2)**2
        )
        
        # Normalize by sum of weights
        total_weight = sum(self.dimension_weights.values())
        return np.sqrt(weighted_sq_diff / total_weight)
    
    def get_context_coords(self, verse_num: int, language: str, window: int = 2) -> list:
        """
        Get average coordinates of surrounding verses for context.
        """
        context_coords = []
        
        for offset in range(-window, window + 1):
            if offset == 0:
                continue  # Skip the verse itself
            
            context_verse = verse_num + offset
            if 1 <= context_verse <= 45:  # Valid verse range
                verse_str = str(context_verse)
                if verse_str in self.verse_data[language]:
                    text = self.verse_data[language][verse_str]
                    sig = self.detectors[language].calculate_field_signature(text)
                    coords = [sig['L'], sig['J'], sig['P'], sig['W']]
                    context_coords.append(coords)
        
        if context_coords:
            return np.mean(context_coords, axis=0).tolist()
        else:
            return None
    
    def find_best_match(self, coords: list, target_language: str, 
                       source_verse: int = None, use_context: bool = True,
                       use_weighting: bool = True) -> dict:
        """
        Find best matching verse with multiple strategies.
        
        Returns top 5 candidates with quality ratings.
        """
        candidates = []
        
        for verse_num, text in self.verse_data[target_language].items():
            verse_int = int(verse_num)
            
            # Analyze target verse
            sig = self.detectors[target_language].calculate_field_signature(text)
            target_coords = [sig['L'], sig['J'], sig['P'], sig['W']]
            
            # Calculate base distance
            if use_weighting:
                base_distance = self.weighted_distance(coords, target_coords)
            else:
                base_distance = np.linalg.norm(np.array(coords) - np.array(target_coords))
            
            # Context-aware adjustment
            context_bonus = 0.0
            if use_context and source_verse:
                # If verse numbers are close, give bonus
                verse_diff = abs(verse_int - source_verse)
                if verse_diff <= self.context_window:
                    context_bonus = -0.05 * (self.context_window - verse_diff + 1)
            
            adjusted_distance = base_distance + context_bonus
            
            # Determine quality
            if adjusted_distance < self.thresholds['excellent']:
                quality = 'EXCELLENT'
            elif adjusted_distance < self.thresholds['good']:
                quality = 'GOOD'
            elif adjusted_distance < self.thresholds['moderate']:
                quality = 'MODERATE'
            elif adjusted_distance < self.thresholds['poor']:
                quality = 'POOR'
            else:
                quality = 'VERY_POOR'
            
            candidates.append({
                'verse': verse_int,
                'text': text,
                'coords': target_coords,
                'base_distance': float(base_distance),
                'adjusted_distance': float(adjusted_distance),
                'context_bonus': float(context_bonus),
                'quality': quality
            })
        
        # Sort by adjusted distance
        candidates.sort(key=lambda x: x['adjusted_distance'])
        
        return {
            'best_match': candidates[0],
            'top_5': candidates[:5],
            'total_candidates': len(candidates)
        }
    
    def compare_matching_strategies(self, verse_num: int, source_lang: str, 
                                   target_lang: str) -> dict:
        """
        Compare different matching strategies.
        """
        verse_str = str(verse_num)
        source_text = self.verse_data[source_lang][verse_str]
        
        # Analyze source
        sig = self.detectors[source_lang].calculate_field_signature(source_text)
        source_coords = [sig['L'], sig['J'], sig['P'], sig['W']]
        
        # Strategy 1: Basic (unweighted, no context)
        basic = self.find_best_match(source_coords, target_lang, 
                                     use_context=False, use_weighting=False)
        
        # Strategy 2: Weighted only
        weighted = self.find_best_match(source_coords, target_lang,
                                       use_context=False, use_weighting=True)
        
        # Strategy 3: Context-aware only
        context = self.find_best_match(source_coords, target_lang,
                                      source_verse=verse_num, use_context=True, 
                                      use_weighting=False)
        
        # Strategy 4: Full (weighted + context)
        full = self.find_best_match(source_coords, target_lang,
                                    source_verse=verse_num, use_context=True,
                                    use_weighting=True)
        
        return {
            'verse': verse_num,
            'source_lang': source_lang,
            'target_lang': target_lang,
            'source_coords': source_coords,
            'strategies': {
                'basic': basic['best_match'],
                'weighted': weighted['best_match'],
                'context': context['best_match'],
                'full': full['best_match']
            },
            'correct_match': {
                'basic': basic['best_match']['verse'] == verse_num,
                'weighted': weighted['best_match']['verse'] == verse_num,
                'context': context['best_match']['verse'] == verse_num,
                'full': full['best_match']['verse'] == verse_num
            }
        }


def test_improved_matching():
    """Test improved matching strategies."""
    matcher = ImprovedVerseMatcher()
    
    print("="*80)
    print("IMPROVED VERSE MATCHING TEST")
    print("="*80)
    print("\nComparing matching strategies:\n")
    print("1. Basic: Unweighted distance, no context")
    print("2. Weighted: Emphasize stable dimensions (Power, Justice)")
    print("3. Context: Consider verse proximity")
    print("4. Full: Weighted + Context\n")
    
    # Test cases (same as round-trip tests)
    test_cases = [
        (1, 'english', 'spanish'),
        (8, 'english', 'greek'),
        (15, 'english', 'chinese'),
        (24, 'spanish', 'chinese'),
        (11, 'greek', 'english'),
    ]
    
    results = []
    
    for verse_num, source_lang, target_lang in test_cases:
        print(f"\n{'='*80}")
        print(f"Test: Verse {verse_num} ({source_lang} -> {target_lang})")
        print('='*80)
        
        result = matcher.compare_matching_strategies(verse_num, source_lang, target_lang)
        results.append(result)
        
        print(f"\nSource coords: {[f'{x:.3f}' for x in result['source_coords']]}")
        print(f"\nMatching Results:")
        
        for strategy, match in result['strategies'].items():
            correct = "[YES]" if result['correct_match'][strategy] else "[NO]"
            print(f"\n{strategy.upper():12} {correct}")
            print(f"  Matched verse: {match['verse']}")
            print(f"  Distance: {match['adjusted_distance']:.3f}")
            print(f"  Quality: {match['quality']}")
    
    # Overall statistics
    print(f"\n{'='*80}")
    print("OVERALL STATISTICS")
    print('='*80)
    
    for strategy in ['basic', 'weighted', 'context', 'full']:
        success_rate = sum(1 for r in results if r['correct_match'][strategy]) / len(results)
        avg_distance = np.mean([r['strategies'][strategy]['adjusted_distance'] for r in results])
        
        print(f"\n{strategy.upper()}:")
        print(f"  Success Rate: {success_rate:.0%}")
        print(f"  Avg Distance: {avg_distance:.3f}")
    
    # Save results
    with open('experiments/improved_matching_results.json', 'w', encoding='utf-8') as f:
        json.dump({
            'test_cases': len(results),
            'results': results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved to: experiments/improved_matching_results.json")
    
    print(f"\n{'='*80}")
    print("IMPROVED MATCHING TEST COMPLETE")
    print("="*80)


if __name__ == "__main__":
    test_improved_matching()
