"""
Cross-Language LJPW Calibration System

Problem: Same verse in different languages produces different LJPW coordinates
Solution: Learn calibration transforms to normalize coordinates across languages

Example:
  English v1: [0.800, 0.750, 0.500, 0.850]
  Spanish v1: [0.953, 0.971, 0.686, 0.929]
  Distance: 0.509 (should be ~0.0 for same verse!)

Approach:
  1. Use parallel verses (same verse in multiple languages)
  2. Learn affine transform: coords_normalized = A * coords_raw + b
  3. Minimize distance between parallel verses
"""

import sys
import os
import numpy as np
from typing import Dict, List, Tuple
import json
from scipy.optimize import minimize

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from experiments.enhanced_pattern_detector import EnhancedPatternDetector
from experiments.greek_pattern_detector import GreekPatternDetector
from experiments.spanish_pattern_detector import SpanishPatternDetector
from experiments.chinese_pattern_detector import ChinesePatternDetector


class CrossLanguageCalibrator:
    """
    Calibrates LJPW coordinates across languages using parallel verses.
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
        
        # Calibration transforms: coords_calibrated = scale * coords_raw + offset
        self.calibrations = {}
        
        # Load verse data
        self.verse_data = {}
        self._load_verse_data()
    
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
                print(f"Warning: {filepath} not found")
                self.verse_data[lang] = {}
    
    def get_coords(self, text: str, language: str) -> np.ndarray:
        """Get LJPW coordinates for text."""
        detector = self.detectors[language]
        sig = detector.calculate_field_signature(text)
        return np.array([sig['L'], sig['J'], sig['P'], sig['W']])
    
    def extract_parallel_verses(self, lang1: str, lang2: str) -> List[Tuple[np.ndarray, np.ndarray]]:
        """
        Extract parallel verses between two languages.
        
        Returns: List of (coords1, coords2) tuples
        """
        pairs = []
        
        # Find common verse numbers
        verses1 = set(self.verse_data[lang1].keys())
        verses2 = set(self.verse_data[lang2].keys())
        common_verses = verses1 & verses2
        
        for verse_num in sorted(common_verses, key=int):
            text1 = self.verse_data[lang1][verse_num]
            text2 = self.verse_data[lang2][verse_num]
            
            coords1 = self.get_coords(text1, lang1)
            coords2 = self.get_coords(text2, lang2)
            
            pairs.append((coords1, coords2))
        
        return pairs
    
    def learn_calibration(self, source_lang: str, target_lang: str) -> Dict:
        """
        Learn calibration transform from source_lang to target_lang.
        
        Finds scale and offset such that:
          coords_target_calibrated = scale * coords_source + offset
        
        Minimizes: sum of distances between calibrated source and target
        """
        pairs = self.extract_parallel_verses(source_lang, target_lang)
        
        if len(pairs) < 5:
            print(f"Warning: Only {len(pairs)} parallel verses found")
            return {
                'scale': np.ones(4),
                'offset': np.zeros(4),
                'error': float('inf')
            }
        
        # Initial guess: identity transform
        x0 = np.concatenate([np.ones(4), np.zeros(4)])  # [scale, offset]
        
        def objective(x):
            """Minimize sum of squared distances."""
            scale = x[:4]
            offset = x[4:]
            
            total_error = 0.0
            for coords_source, coords_target in pairs:
                coords_calibrated = scale * coords_source + offset
                distance = np.linalg.norm(coords_calibrated - coords_target)
                total_error += distance ** 2
            
            return total_error / len(pairs)
        
        # Optimize
        result = minimize(objective, x0, method='BFGS')
        
        scale = result.x[:4]
        offset = result.x[4:]
        error = np.sqrt(result.fun)
        
        return {
            'source_lang': source_lang,
            'target_lang': target_lang,
            'scale': scale.tolist(),
            'offset': offset.tolist(),
            'error': float(error),
            'num_verses': len(pairs)
        }
    
    def apply_calibration(self, coords: np.ndarray, calibration: Dict) -> np.ndarray:
        """Apply calibration transform to coordinates."""
        scale = np.array(calibration['scale'])
        offset = np.array(calibration['offset'])
        return scale * coords + offset
    
    def calibrate_all_to_reference(self):
        """
        Calibrate all languages to reference language.
        """
        print(f"Calibrating all languages to reference: {self.reference_language}")
        print("=" * 80)
        
        for lang in self.detectors.keys():
            if lang == self.reference_language:
                # Reference language has identity transform
                self.calibrations[lang] = {
                    'source_lang': lang,
                    'target_lang': self.reference_language,
                    'scale': [1.0, 1.0, 1.0, 1.0],
                    'offset': [0.0, 0.0, 0.0, 0.0],
                    'error': 0.0,
                    'num_verses': 0
                }
                continue
            
            print(f"\nCalibrating {lang} -> {self.reference_language}...")
            calibration = self.learn_calibration(lang, self.reference_language)
            self.calibrations[lang] = calibration
            
            print(f"  Scale: {[f'{x:.3f}' for x in calibration['scale']]}")
            print(f"  Offset: {[f'{x:.3f}' for x in calibration['offset']]}")
            print(f"  Error: {calibration['error']:.4f}")
            print(f"  Verses: {calibration['num_verses']}")
        
        # Save calibrations
        with open('experiments/language_calibrations.json', 'w', encoding='utf-8') as f:
            json.dump(self.calibrations, f, indent=2)
        
        print(f"\nCalibrations saved to: experiments/language_calibrations.json")
    
    def test_calibration(self):
        """Test calibration on sample verses."""
        print("\n" + "=" * 80)
        print("TESTING CALIBRATION")
        print("=" * 80)
        
        test_verses = [1, 8, 15, 24]
        
        for verse_num in test_verses:
            verse_str = str(verse_num)
            
            print(f"\n{'=' * 80}")
            print(f"Verse {verse_num}")
            print('=' * 80)
            
            # Get reference coords
            if verse_str not in self.verse_data[self.reference_language]:
                continue
            
            ref_text = self.verse_data[self.reference_language][verse_str]
            ref_coords = self.get_coords(ref_text, self.reference_language)
            
            print(f"\nReference ({self.reference_language}):")
            print(f"  Coords: {[f'{x:.3f}' for x in ref_coords]}")
            
            for lang in ['spanish', 'greek', 'chinese']:
                if verse_str not in self.verse_data[lang]:
                    continue
                
                text = self.verse_data[lang][verse_str]
                raw_coords = self.get_coords(text, lang)
                calibrated_coords = self.apply_calibration(raw_coords, self.calibrations[lang])
                
                raw_distance = np.linalg.norm(raw_coords - ref_coords)
                calibrated_distance = np.linalg.norm(calibrated_coords - ref_coords)
                
                improvement = (raw_distance - calibrated_distance) / raw_distance * 100
                
                print(f"\n{lang.capitalize()}:")
                print(f"  Raw coords:        {[f'{x:.3f}' for x in raw_coords]}")
                print(f"  Calibrated coords: {[f'{x:.3f}' for x in calibrated_coords]}")
                print(f"  Raw distance:        {raw_distance:.4f}")
                print(f"  Calibrated distance: {calibrated_distance:.4f}")
                print(f"  Improvement:         {improvement:+.1f}%")
        
        # Overall statistics
        print(f"\n{'=' * 80}")
        print("OVERALL IMPROVEMENT")
        print('=' * 80)
        
        total_raw_dist = 0.0
        total_cal_dist = 0.0
        count = 0
        
        for lang in ['spanish', 'greek', 'chinese']:
            pairs = self.extract_parallel_verses(self.reference_language, lang)
            
            for ref_coords, lang_coords in pairs:
                calibrated_coords = self.apply_calibration(lang_coords, self.calibrations[lang])
                
                raw_dist = np.linalg.norm(lang_coords - ref_coords)
                cal_dist = np.linalg.norm(calibrated_coords - ref_coords)
                
                total_raw_dist += raw_dist
                total_cal_dist += cal_dist
                count += 1
        
        avg_raw = total_raw_dist / count
        avg_cal = total_cal_dist / count
        improvement = (avg_raw - avg_cal) / avg_raw * 100
        
        print(f"\nAverage raw distance:        {avg_raw:.4f}")
        print(f"Average calibrated distance: {avg_cal:.4f}")
        print(f"Overall improvement:         {improvement:+.1f}%")


def main():
    """Run calibration."""
    calibrator = CrossLanguageCalibrator(reference_language='english')
    
    # Learn calibrations
    calibrator.calibrate_all_to_reference()
    
    # Test calibrations
    calibrator.test_calibration()


if __name__ == "__main__":
    main()
