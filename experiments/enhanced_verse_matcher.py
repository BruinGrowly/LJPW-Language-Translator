"""
Enhanced Verse Matching System
Fixes known issues:
1. Semantic distance thresholding (prevents bad matches)
2. Context-aware matching (weights by verse proximity)
3. Dimensional weighting (prioritizes stable dimensions)
"""

import sys
import os
import numpy as np
from typing import Dict, List, Tuple, Optional
import json

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from experiments.enhanced_pattern_detector import EnhancedPatternDetector
from experiments.greek_pattern_detector import GreekPatternDetector
from experiments.spanish_pattern_detector import SpanishPatternDetector
from experiments.chinese_pattern_detector import ChinesePatternDetector


class EnhancedVerseMatcher:
    """
    Improved verse matching with:
    - Semantic distance thresholding
    - Context-aware weighting
    - Dimensional importance weighting
    """
    
    def __init__(self):
        self.detectors = {
            'english': EnhancedPatternDetector(),
            'wedau': EnhancedPatternDetector(),
            'greek': GreekPatternDetector(),
            'spanish': SpanishPatternDetector(),
            'chinese': ChinesePatternDetector()
        }
        
        # Dimensional weights (from empirical analysis)
        # Power is most stable (0.088 variance), Love most variable (0.172)
        self.dimension_weights = {
            'P': 2.0,  # Power - most universal (highest weight)
            'W': 1.5,  # Wisdom - moderate stability
            'J': 1.3,  # Justice - moderate stability
            'L': 1.0   # Love - most cultural (lowest weight for matching)
        }
        
        # Quality thresholds
        self.thresholds = {
            'excellent': 0.08,   # LJPW distance < 0.08
            'good': 0.15,        # LJPW distance < 0.15
            'acceptable': 0.25,  # LJPW distance < 0.25
            'poor': 0.40         # LJPW distance < 0.40
        }
        
        # Context window for proximity weighting
        self.context_window = 5  # Consider ±5 verses
        
        # Load verse data
        self.verse_data = {}
        self._load_verse_data()
    
    def _load_verse_data(self):
        """Load all verse data for lookup."""
        files = {
            'english': 'experiments/nwt_mark_chapter1.json',
            'wedau': 'experiments/wedau_mark_chapter1.json',
            'greek': 'experiments/greek_mark_chapter1.json',
            'spanish': 'experiments/spanish_mark_chapter1.json',
            'chinese': 'experiments/chinese_mark_chapter1.json'
        }
        
        for lang, filepath in files.items():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.verse_data[lang] = data['verses']
            except FileNotFoundError:
                print(f"Warning: {filepath} not found")
                self.verse_data[lang] = {}
    
    def weighted_distance(self, coords1: np.ndarray, coords2: np.ndarray) -> float:
        """
        Calculate weighted Euclidean distance.
        
        Weights dimensions by stability:
        - Power (most stable) gets highest weight
        - Love (most variable) gets lowest weight
        """
        L1, J1, P1, W1 = coords1
        L2, J2, P2, W2 = coords2
        
        weighted_diff = np.array([
            (L1 - L2) * self.dimension_weights['L'],
            (J1 - J2) * self.dimension_weights['J'],
            (P1 - P2) * self.dimension_weights['P'],
            (W1 - W2) * self.dimension_weights['W']
        ])
        
        return np.linalg.norm(weighted_diff)
    
    def context_weight(self, source_verse: int, candidate_verse: int) -> float:
        """
        Calculate context proximity weight.
        
        Verses closer to source verse get higher weight (lower effective distance).
        
        Returns: multiplier (1.0 = same verse, increases with distance)
        """
        verse_distance = abs(source_verse - candidate_verse)
        
        if verse_distance == 0:
            return 0.5  # Same verse - very strong match
        elif verse_distance <= self.context_window:
            # Linear increase within context window
            return 1.0 + (verse_distance * 0.1)
        else:
            # Exponential increase outside context window
            return 1.0 + (self.context_window * 0.1) + ((verse_distance - self.context_window) * 0.2)
    
    def find_best_match(
        self,
        coords: np.ndarray,
        target_language: str,
        source_verse: Optional[int] = None,
        exclude_verse: Optional[int] = None,
        return_all_candidates: bool = False
    ) -> Dict:
        """
        Find best matching verse with quality assessment.
        
        Args:
            coords: Source LJPW coordinates
            target_language: Language to search
            source_verse: Source verse number (for context weighting)
            exclude_verse: Verse to exclude from search
            return_all_candidates: Return top 5 candidates
        
        Returns:
            Dictionary with match info and quality assessment
        """
        candidates = []
        
        for verse_num, text in self.verse_data[target_language].items():
            verse_int = int(verse_num)
            
            # Skip excluded verse
            if exclude_verse and verse_int == exclude_verse:
                continue
            
            # Analyze candidate
            detector = self.detectors[target_language]
            sig = detector.calculate_field_signature(text)
            candidate_coords = np.array([sig['L'], sig['J'], sig['P'], sig['W']])
            
            # Calculate weighted distance
            base_distance = self.weighted_distance(coords, candidate_coords)
            
            # Apply context weighting if source verse provided
            if source_verse is not None:
                context_multiplier = self.context_weight(source_verse, verse_int)
                effective_distance = base_distance * context_multiplier
            else:
                effective_distance = base_distance
            
            candidates.append({
                'verse': verse_int,
                'text': text,
                'coords': candidate_coords.tolist(),
                'base_distance': float(base_distance),
                'effective_distance': float(effective_distance),
                'context_boost': source_verse is not None and abs(source_verse - verse_int) <= self.context_window
            })
        
        # Sort by effective distance
        candidates.sort(key=lambda x: x['effective_distance'])
        
        # Get best match
        best_match = candidates[0] if candidates else None
        
        if best_match is None:
            return {'error': 'No candidates found'}
        
        # Assess quality
        quality = self._assess_quality(best_match['base_distance'])
        
        result = {
            'verse': best_match['verse'],
            'text': best_match['text'],
            'coords': best_match['coords'],
            'distance': best_match['base_distance'],
            'effective_distance': best_match['effective_distance'],
            'quality': quality,
            'context_boost': best_match['context_boost'],
            'confidence': self._calculate_confidence(best_match, candidates)
        }
        
        if return_all_candidates:
            result['top_candidates'] = candidates[:5]
        
        return result
    
    def _assess_quality(self, distance: float) -> str:
        """Assess match quality based on distance thresholds."""
        if distance < self.thresholds['excellent']:
            return 'EXCELLENT'
        elif distance < self.thresholds['good']:
            return 'GOOD'
        elif distance < self.thresholds['acceptable']:
            return 'ACCEPTABLE'
        elif distance < self.thresholds['poor']:
            return 'POOR'
        else:
            return 'VERY_POOR'
    
    def _calculate_confidence(self, best_match: Dict, all_candidates: List[Dict]) -> float:
        """
        Calculate confidence in match.
        
        High confidence if:
        - Best match is much better than second-best
        - Distance is low
        - Context boost applied
        
        Returns: 0.0-1.0
        """
        if len(all_candidates) < 2:
            return 0.5
        
        best_dist = best_match['effective_distance']
        second_best_dist = all_candidates[1]['effective_distance']
        
        # Separation score (how much better is best than second-best)
        separation = (second_best_dist - best_dist) / (second_best_dist + 0.001)
        separation_score = min(separation, 1.0)
        
        # Distance score (lower distance = higher confidence)
        distance_score = max(0, 1.0 - (best_dist / self.thresholds['poor']))
        
        # Context score
        context_score = 0.2 if best_match['context_boost'] else 0.0
        
        # Combined confidence
        confidence = (0.4 * separation_score + 
                     0.4 * distance_score + 
                     0.2 * context_score)
        
        return float(confidence)
    
    def round_trip_with_quality(
        self,
        verse_num: int,
        source_lang: str,
        intermediate_lang: str
    ) -> Dict:
        """
        Enhanced round-trip translation with quality assessment.
        """
        verse_str = str(verse_num)
        
        # Step 1: Analyze source
        source_text = self.verse_data[source_lang][verse_str]
        detector = self.detectors[source_lang]
        source_sig = detector.calculate_field_signature(source_text)
        source_coords = np.array([source_sig['L'], source_sig['J'], source_sig['P'], source_sig['W']])
        
        # Step 2: Find best match in intermediate language (with context)
        intermediate_match = self.find_best_match(
            source_coords,
            intermediate_lang,
            source_verse=verse_num,
            return_all_candidates=True
        )
        
        # Step 3: Find best match back in source language (with context)
        final_match = self.find_best_match(
            np.array(intermediate_match['coords']),
            source_lang,
            source_verse=intermediate_match['verse'],
            exclude_verse=verse_num,
            return_all_candidates=True
        )
        
        # Calculate overall metrics
        source_to_final_dist = np.linalg.norm(source_coords - np.array(final_match['coords']))
        preservation_rate = 1.0 - (source_to_final_dist / 2.0)
        
        return {
            'verse_num': verse_num,
            'source_lang': source_lang,
            'intermediate_lang': intermediate_lang,
            'source': {
                'verse': verse_num,
                'text': source_text,
                'coords': source_coords.tolist()
            },
            'intermediate': {
                'verse': intermediate_match['verse'],
                'text': intermediate_match['text'],
                'coords': intermediate_match['coords'],
                'distance': intermediate_match['distance'],
                'quality': intermediate_match['quality'],
                'confidence': intermediate_match['confidence'],
                'matched_same': intermediate_match['verse'] == verse_num,
                'top_candidates': intermediate_match.get('top_candidates', [])
            },
            'final': {
                'verse': final_match['verse'],
                'text': final_match['text'],
                'coords': final_match['coords'],
                'distance': final_match['distance'],
                'quality': final_match['quality'],
                'confidence': final_match['confidence'],
                'matched_original': final_match['verse'] == verse_num,
                'top_candidates': final_match.get('top_candidates', [])
            },
            'overall': {
                'source_to_final_distance': float(source_to_final_dist),
                'preservation_rate': float(preservation_rate),
                'success': final_match['verse'] == verse_num,
                'intermediate_quality': intermediate_match['quality'],
                'final_quality': final_match['quality']
            }
        }


def test_enhanced_matching():
    """Test enhanced verse matching system."""
    print("=" * 80)
    print("ENHANCED VERSE MATCHING TEST")
    print("=" * 80)
    print("Testing improvements:")
    print("  1. Semantic distance thresholding")
    print("  2. Context-aware matching")
    print("  3. Dimensional weighting")
    print("-" * 80)
    
    matcher = EnhancedVerseMatcher()
    
    # Test cases
    test_cases = [
        (1, 'english', 'spanish'),
        (8, 'english', 'greek'),
        (15, 'english', 'chinese'),
        (24, 'spanish', 'chinese'),
        (11, 'greek', 'english'),
    ]
    
    results = []
    
    for verse_num, source_lang, intermediate_lang in test_cases:
        print(f"\n{'=' * 80}")
        print(f"Test: {source_lang.upper()} -> {intermediate_lang.upper()} -> {source_lang.upper()}")
        print(f"Verse {verse_num}")
        print('=' * 80)
        
        result = matcher.round_trip_with_quality(verse_num, source_lang, intermediate_lang)
        results.append(result)
        
        print(f"\nSource ({source_lang} v{verse_num}):")
        print(f"  Coords: {[f'{x:.3f}' for x in result['source']['coords']]}")
        
        print(f"\nIntermediate Match ({intermediate_lang}):")
        print(f"  Verse: {result['intermediate']['verse']} "
              f"{'[SAME]' if result['intermediate']['matched_same'] else '[DIFFERENT]'}")
        print(f"  Distance: {result['intermediate']['distance']:.4f}")
        print(f"  Quality: {result['intermediate']['quality']}")
        print(f"  Confidence: {result['intermediate']['confidence']:.1%}")
        
        # Show top candidates
        if 'top_candidates' in result['intermediate']:
            print(f"  Top 3 candidates:")
            for i, cand in enumerate(result['intermediate']['top_candidates'][:3], 1):
                print(f"    {i}. Verse {cand['verse']}: dist={cand['base_distance']:.4f} "
                      f"{'[CONTEXT]' if cand['context_boost'] else ''}")
        
        print(f"\nFinal Match ({source_lang}):")
        print(f"  Verse: {result['final']['verse']} "
              f"{'[ORIGINAL]' if result['final']['matched_original'] else '[DIFFERENT]'}")
        print(f"  Distance: {result['final']['distance']:.4f}")
        print(f"  Quality: {result['final']['quality']}")
        print(f"  Confidence: {result['final']['confidence']:.1%}")
        
        print(f"\nOverall:")
        print(f"  Preservation: {result['overall']['preservation_rate']:.1%}")
        print(f"  Success: {'YES' if result['overall']['success'] else 'NO'}")
    
    # Statistics
    print(f"\n{'=' * 80}")
    print("OVERALL STATISTICS")
    print('=' * 80)
    
    success_rate = sum(1 for r in results if r['overall']['success']) / len(results)
    avg_preservation = np.mean([r['overall']['preservation_rate'] for r in results])
    avg_confidence = np.mean([r['intermediate']['confidence'] for r in results])
    
    print(f"\nSuccess Rate: {success_rate:.0%}")
    print(f"Avg Preservation: {avg_preservation:.1%}")
    print(f"Avg Confidence: {avg_confidence:.1%}")
    
    # Quality distribution
    intermediate_qualities = [r['intermediate']['quality'] for r in results]
    final_qualities = [r['final']['quality'] for r in results]
    
    print(f"\nIntermediate Match Quality:")
    for quality in ['EXCELLENT', 'GOOD', 'ACCEPTABLE', 'POOR']:
        count = intermediate_qualities.count(quality)
        if count > 0:
            print(f"  {quality}: {count}")
    
    print(f"\nFinal Match Quality:")
    for quality in ['EXCELLENT', 'GOOD', 'ACCEPTABLE', 'POOR']:
        count = final_qualities.count(quality)
        if count > 0:
            print(f"  {quality}: {count}")
    
    # Save results
    with open('experiments/enhanced_matching_results.json', 'w', encoding='utf-8') as f:
        json.dump({
            'summary': {
                'success_rate': float(success_rate),
                'avg_preservation': float(avg_preservation),
                'avg_confidence': float(avg_confidence)
            },
            'results': results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved to: experiments/enhanced_matching_results.json")
    print(f"\n{'=' * 80}")
    print("ENHANCED MATCHING TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    test_enhanced_matching()
