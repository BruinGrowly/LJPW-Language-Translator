"""
Round-Trip Translation System
Test semantic preservation through multiple transformations
"""

import sys
sys.path.append('experiments')

from enhanced_pattern_detector import EnhancedPatternDetector
from greek_pattern_detector import GreekPatternDetector
from spanish_pattern_detector import SpanishPatternDetector
from chinese_pattern_detector import ChinesePatternDetector
import numpy as np
import json


class RoundTripTranslator:
    """
    Round-trip translation via LJPW coordinates.
    
    Process:
    1. Source text → LJPW coordinates
    2. Find nearest concept in target language
    3. Target text → LJPW coordinates
    4. Measure semantic preservation
    """
    
    def __init__(self):
        self.detectors = {
            'english': EnhancedPatternDetector(),
            'wedau': EnhancedPatternDetector(),
            'greek': GreekPatternDetector(),
            'spanish': SpanishPatternDetector(),
            'chinese': ChinesePatternDetector()
        }
        
        # Load all verse data
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
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.verse_data[lang] = data['verses']
    
    def analyze_text(self, text: str, language: str) -> dict:
        """Analyze text and return LJPW coordinates."""
        detector = self.detectors[language]
        sig = detector.calculate_field_signature(text)
        coords = [sig['L'], sig['J'], sig['P'], sig['W']]
        
        return {
            'text': text,
            'coordinates': coords,
            'harmony': self.calculate_harmony(coords),
            'confidence': sig['confidence']
        }
    
    def calculate_harmony(self, coords):
        """Calculate harmony index."""
        L, J, P, W = coords
        distance = np.sqrt((1-L)**2 + (1-J)**2 + (1-P)**2 + (1-W)**2)
        return 1.0 / (1.0 + distance)
    
    def find_nearest_verse(self, coords: list, target_language: str, exclude_verse: int = None) -> tuple:
        """Find nearest verse in target language by LJPW distance."""
        min_distance = float('inf')
        nearest_verse = None
        nearest_coords = None
        
        for verse_num, text in self.verse_data[target_language].items():
            verse_int = int(verse_num)
            if exclude_verse and verse_int == exclude_verse:
                continue
            
            analysis = self.analyze_text(text, target_language)
            distance = np.linalg.norm(np.array(coords) - np.array(analysis['coordinates']))
            
            if distance < min_distance:
                min_distance = distance
                nearest_verse = verse_int
                nearest_coords = analysis['coordinates']
        
        return nearest_verse, nearest_coords, min_distance
    
    def round_trip(self, verse_num: int, source_lang: str, intermediate_lang: str) -> dict:
        """
        Perform round-trip translation.
        
        Process:
        1. Source verse → LJPW coords
        2. Find nearest verse in intermediate language
        3. Intermediate verse → LJPW coords
        4. Find nearest verse back in source language
        5. Compare original vs final
        """
        verse_str = str(verse_num)
        
        # Step 1: Analyze source
        source_text = self.verse_data[source_lang][verse_str]
        source_analysis = self.analyze_text(source_text, source_lang)
        
        # Step 2: Find nearest in intermediate language
        intermediate_verse, intermediate_coords, dist_1_2 = self.find_nearest_verse(
            source_analysis['coordinates'], intermediate_lang
        )
        intermediate_text = self.verse_data[intermediate_lang][str(intermediate_verse)]
        
        # Step 3: Analyze intermediate
        intermediate_analysis = self.analyze_text(intermediate_text, intermediate_lang)
        
        # Step 4: Find nearest back in source language
        final_verse, final_coords, dist_2_3 = self.find_nearest_verse(
            intermediate_analysis['coordinates'], source_lang, exclude_verse=verse_num
        )
        final_text = self.verse_data[source_lang][str(final_verse)]
        
        # Step 5: Analyze final
        final_analysis = self.analyze_text(final_text, source_lang)
        
        # Calculate preservation metrics
        original_to_final_dist = np.linalg.norm(
            np.array(source_analysis['coordinates']) - np.array(final_analysis['coordinates'])
        )
        
        preservation_rate = 1.0 - (original_to_final_dist / 2.0)  # Normalize to 0-1
        
        return {
            'verse_num': verse_num,
            'source_lang': source_lang,
            'intermediate_lang': intermediate_lang,
            'source': {
                'verse': verse_num,
                'text': source_text,
                'coords': source_analysis['coordinates']
            },
            'intermediate': {
                'verse': intermediate_verse,
                'text': intermediate_text,
                'coords': intermediate_analysis['coordinates'],
                'matched_same_verse': intermediate_verse == verse_num
            },
            'final': {
                'verse': final_verse,
                'text': final_text,
                'coords': final_analysis['coordinates'],
                'matched_original': final_verse == verse_num
            },
            'distances': {
                'source_to_intermediate': float(dist_1_2),
                'intermediate_to_final': float(dist_2_3),
                'source_to_final': float(original_to_final_dist)
            },
            'preservation_rate': float(preservation_rate),
            'success': final_verse == verse_num
        }


def test_round_trips():
    """Test round-trip translations."""
    translator = RoundTripTranslator()
    
    print("="*80)
    print("ROUND-TRIP TRANSLATION TEST")
    print("="*80)
    print("\nTesting semantic preservation through multiple transformations\n")
    
    # Test cases
    test_cases = [
        (1, 'english', 'spanish'),   # Eng → Spa → Eng
        (8, 'english', 'greek'),     # Eng → Grk → Eng
        (15, 'english', 'chinese'),  # Eng → Chn → Eng
        (24, 'spanish', 'chinese'),  # Spa → Chn → Spa
        (11, 'greek', 'english'),    # Grk → Eng → Grk
    ]
    
    results = []
    
    for verse_num, source_lang, intermediate_lang in test_cases:
        print(f"\n{'='*80}")
        print(f"Test: {source_lang.upper()} -> {intermediate_lang.upper()} -> {source_lang.upper()}")
        print(f"Verse {verse_num}")
        print('='*80)
        
        result = translator.round_trip(verse_num, source_lang, intermediate_lang)
        results.append(result)
        
        print(f"\nSource ({source_lang}):")
        print(f"  Verse {result['source']['verse']}")
        print(f"  Coords: {[f'{x:.3f}' for x in result['source']['coords']]}")
        
        print(f"\nIntermediate ({intermediate_lang}):")
        print(f"  Matched verse {result['intermediate']['verse']}: "
              f"{'[SAME]' if result['intermediate']['matched_same_verse'] else '[DIFFERENT]'}")
        print(f"  Coords: {[f'{x:.3f}' for x in result['intermediate']['coords']]}")
        print(f"  Distance from source: {result['distances']['source_to_intermediate']:.3f}")
        
        print(f"\nFinal ({source_lang}):")
        print(f"  Matched verse {result['final']['verse']}: "
              f"{'[ORIGINAL]' if result['final']['matched_original'] else '[DIFFERENT]'}")
        print(f"  Coords: {[f'{x:.3f}' for x in result['final']['coords']]}")
        print(f"  Distance from original: {result['distances']['source_to_final']:.3f}")
        
        print(f"\nPreservation Rate: {result['preservation_rate']:.1%}")
        print(f"Success: {'[YES]' if result['success'] else '[NO]'}")
    
    # Overall statistics
    print(f"\n{'='*80}")
    print("OVERALL STATISTICS")
    print('='*80)
    
    success_rate = sum(1 for r in results if r['success']) / len(results)
    avg_preservation = np.mean([r['preservation_rate'] for r in results])
    avg_source_to_final = np.mean([r['distances']['source_to_final'] for r in results])
    
    print(f"\nSuccess Rate (matched original verse): {success_rate:.0%}")
    print(f"Average Preservation Rate: {avg_preservation:.1%}")
    print(f"Average Source-to-Final Distance: {avg_source_to_final:.3f}")
    
    print(f"\nInterpretation:")
    if success_rate >= 0.8:
        print("  [EXCELLENT]: Framework successfully preserves meaning through round-trips")
    elif success_rate >= 0.6:
        print("  [GOOD]: Most round-trips preserve meaning")
    else:
        print("  [MODERATE]: Some semantic drift in round-trips")
    
    # Save results
    with open('experiments/round_trip_results.json', 'w', encoding='utf-8') as f:
        json.dump({
            'summary': {
                'success_rate': float(success_rate),
                'avg_preservation_rate': float(avg_preservation),
                'avg_source_to_final_distance': float(avg_source_to_final)
            },
            'results': results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved to: experiments/round_trip_results.json")
    
    print(f"\n{'='*80}")
    print("ROUND-TRIP TRANSLATION COMPLETE")
    print("="*80)


if __name__ == "__main__":
    test_round_trips()
