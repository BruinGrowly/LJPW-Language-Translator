"""
Calibrated Verse Matcher
Combines enhanced matching with cross-language calibration
"""

import sys
import os
import numpy as np
from typing import Dict, List, Optional
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from experiments.enhanced_pattern_detector import EnhancedPatternDetector
from experiments.greek_pattern_detector import GreekPatternDetector
from experiments.spanish_pattern_detector import SpanishPatternDetector
from experiments.chinese_pattern_detector import ChinesePatternDetector


class CalibratedVerseMatcher:
    """
    Enhanced verse matching with cross-language calibration.
    
    Fixes:
    1. Cross-language calibration (normalizes coordinates)
    2. Semantic distance thresholding (quality assessment)
    3. Context-aware matching (proximity weighting)
    4. Dimensional weighting (prioritizes stable dimensions)
    """
    
    def __init__(self, reference_language='english'):
        self.reference_language = reference_language
        
        self.detectors = {
            'english': EnhancedPatternDetector(),
            'wedau': EnhancedPatternDetector(),
            'greek': GreekPatternDetector(),
            'spanish': SpanishPatternDetector(),
            'chinese': ChinesePatternDetector()
        }
        
        # Load calibrations
        self.calibrations = self._load_calibrations()
        
        # Dimensional weights
        self.dimension_weights = {
            'P': 2.0,  # Power - most stable
            'W': 1.5,  # Wisdom
            'J': 1.3,  # Justice
            'L': 1.0   # Love - most variable
        }
        
        # Quality thresholds
        self.thresholds = {
            'excellent': 0.08,
            'good': 0.15,
            'acceptable': 0.25,
            'poor': 0.40
        }
        
        # Context window
        self.context_window = 5
        
        # Load verse data
        self.verse_data = {}
        self._load_verse_data()
    
    def _load_calibrations(self) -> Dict:
        """Load calibration transforms."""
        try:
            with open('experiments/language_calibrations.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Warning: No calibrations found, run cross_language_calibrator.py first")
            return {}
    
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
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.verse_data[lang] = data['verses']
            except FileNotFoundError:
                self.verse_data[lang] = {}
    
    def get_coords(self, text: str, language: str, calibrated: bool = True) -> np.ndarray:
        """Get LJPW coordinates, optionally calibrated."""
        detector = self.detectors[language]
        sig = detector.calculate_field_signature(text)
        coords = np.array([sig['L'], sig['J'], sig['P'], sig['W']])
        
        if calibrated and language in self.calibrations:
            cal = self.calibrations[language]
            scale = np.array(cal['scale'])
            offset = np.array(cal['offset'])
            coords = scale * coords + offset
        
        return coords
    
    def weighted_distance(self, coords1: np.ndarray, coords2: np.ndarray) -> float:
        """Calculate weighted Euclidean distance."""
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
        """Calculate context proximity weight."""
        verse_distance = abs(source_verse - candidate_verse)
        
        if verse_distance == 0:
            return 0.5  # Same verse - very strong match
        elif verse_distance <= self.context_window:
            return 1.0 + (verse_distance * 0.1)
        else:
            return 1.0 + (self.context_window * 0.1) + ((verse_distance - self.context_window) * 0.2)
    
    def find_best_match(
        self,
        coords: np.ndarray,
        target_language: str,
        source_verse: Optional[int] = None,
        exclude_verse: Optional[int] = None
    ) -> Dict:
        """Find best matching verse with quality assessment."""
        candidates = []
        
        for verse_num, text in self.verse_data[target_language].items():
            verse_int = int(verse_num)
            
            if exclude_verse and verse_int == exclude_verse:
                continue
            
            # Get calibrated coordinates
            candidate_coords = self.get_coords(text, target_language, calibrated=True)
            
            # Calculate weighted distance
            base_distance = self.weighted_distance(coords, candidate_coords)
            
            # Apply context weighting
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
        
        best_match = candidates[0] if candidates else None
        
        if best_match is None:
            return {'error': 'No candidates found'}
        
        # Assess quality
        quality = self._assess_quality(best_match['base_distance'])
        
        return {
            'verse': best_match['verse'],
            'text': best_match['text'],
            'coords': best_match['coords'],
            'distance': best_match['base_distance'],
            'effective_distance': best_match['effective_distance'],
            'quality': quality,
            'context_boost': best_match['context_boost'],
            'confidence': self._calculate_confidence(best_match, candidates),
            'top_candidates': candidates[:5]
        }
    
    def _assess_quality(self, distance: float) -> str:
        """Assess match quality."""
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
        """Calculate confidence in match."""
        if len(all_candidates) < 2:
            return 0.5
        
        best_dist = best_match['effective_distance']
        second_best_dist = all_candidates[1]['effective_distance']
        
        separation = (second_best_dist - best_dist) / (second_best_dist + 0.001)
        separation_score = min(separation, 1.0)
        
        distance_score = max(0, 1.0 - (best_dist / self.thresholds['poor']))
        
        context_score = 0.2 if best_match['context_boost'] else 0.0
        
        confidence = (0.4 * separation_score + 
                     0.4 * distance_score + 
                     0.2 * context_score)
        
        return float(confidence)
    
    def round_trip_with_calibration(
        self,
        verse_num: int,
        source_lang: str,
        intermediate_lang: str
    ) -> Dict:
        """Enhanced round-trip translation with calibration."""
        verse_str = str(verse_num)
        
        # Get source coords (calibrated)
        source_text = self.verse_data[source_lang][verse_str]
        source_coords = self.get_coords(source_text, source_lang, calibrated=True)
        
        # Find best match in intermediate language
        intermediate_match = self.find_best_match(
            source_coords,
            intermediate_lang,
            source_verse=verse_num
        )
        
        # Find best match back in source language
        final_match = self.find_best_match(
            np.array(intermediate_match['coords']),
            source_lang,
            source_verse=intermediate_match['verse'],
            exclude_verse=verse_num
        )
        
        # Calculate metrics
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
                'matched_same': intermediate_match['verse'] == verse_num
            },
            'final': {
                'verse': final_match['verse'],
                'text': final_match['text'],
                'coords': final_match['coords'],
                'distance': final_match['distance'],
                'quality': final_match['quality'],
                'confidence': final_match['confidence'],
                'matched_original': final_match['verse'] == verse_num
            },
            'overall': {
                'source_to_final_distance': float(source_to_final_dist),
                'preservation_rate': float(preservation_rate),
                'success': final_match['verse'] == verse_num,
                'intermediate_quality': intermediate_match['quality'],
                'final_quality': final_match['quality']
            }
        }


def test_calibrated_matching():
    """Test calibrated verse matching."""
    print("=" * 80)
    print("CALIBRATED VERSE MATCHING TEST")
    print("=" * 80)
    print("Improvements:")
    print("  1. Cross-language calibration (+41.1% avg)")
    print("  2. Semantic distance thresholding")
    print("  3. Context-aware matching")
    print("  4. Dimensional weighting")
    print("-" * 80)
    
    matcher = CalibratedVerseMatcher()
    
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
        
        result = matcher.round_trip_with_calibration(verse_num, source_lang, intermediate_lang)
        results.append(result)
        
        print(f"\nIntermediate Match ({intermediate_lang}):")
        print(f"  Verse: {result['intermediate']['verse']} "
              f"{'[SAME]' if result['intermediate']['matched_same'] else '[DIFFERENT]'}")
        print(f"  Distance: {result['intermediate']['distance']:.4f}")
        print(f"  Quality: {result['intermediate']['quality']}")
        print(f"  Confidence: {result['intermediate']['confidence']:.1%}")
        
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
    for quality in ['EXCELLENT', 'GOOD', 'ACCEPTABLE', 'POOR', 'VERY_POOR']:
        count = intermediate_qualities.count(quality)
        if count > 0:
            print(f"  {quality}: {count}")
    
    print(f"\nFinal Match Quality:")
    for quality in ['EXCELLENT', 'GOOD', 'ACCEPTABLE', 'POOR', 'VERY_POOR']:
        count = final_qualities.count(quality)
        if count > 0:
            print(f"  {quality}: {count}")
    
    # Save results
    with open('experiments/calibrated_matching_results.json', 'w', encoding='utf-8') as f:
        json.dump({
            'summary': {
                'success_rate': float(success_rate),
                'avg_preservation': float(avg_preservation),
                'avg_confidence': float(avg_confidence)
            },
            'results': results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved to: experiments/calibrated_matching_results.json")
    print(f"\n{'=' * 80}")
    print("CALIBRATED MATCHING TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    test_calibrated_matching()
