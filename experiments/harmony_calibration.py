#!/usr/bin/env python3
"""
Cross-Language Harmony Calibration
===================================

Analyzes all available language corpora to discover the natural "resting harmony"
for each language. This calibration enables:

1. Language-specific expectations (Greek ≠ Wedau baseline)
2. Normalized comparison across languages
3. Detection of outliers relative to language norms

Key Insight: Each language has a natural harmony "accent" - structural languages
like Greek may have different average harmony than oral languages like Wedau.
"""

import json
import sys
import os
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_quantum.resonance_engine import ResonanceEngine
from experiments.enhanced_pattern_detector import EnhancedPatternDetector


@dataclass
class LanguageProfile:
    """Harmony profile for a single language."""
    language: str
    verse_count: int
    mean_harmony: float
    std_harmony: float
    min_harmony: float
    max_harmony: float
    mean_ljpw: List[float]  # Average LJPW coordinates
    dominant_dimension: str  # Which dimension is typically strongest
    resonance_convergence_rate: float  # How quickly verses converge
    harmony_distribution: Dict[str, int]  # Binned distribution


class HarmonyCalibrator:
    """
    Discovers and stores the natural harmony profile for each language.
    
    Uses semantic oscillation to find:
    - Baseline harmony for each language
    - Typical LJPW coordinate patterns
    - Convergence characteristics
    """
    
    def __init__(self):
        self.engine = ResonanceEngine()
        self.detector = EnhancedPatternDetector()
        self.profiles: Dict[str, LanguageProfile] = {}
    
    def analyze_corpus(self, verses: Dict[str, str], language: str) -> LanguageProfile:
        """
        Analyze a language corpus to discover its harmony profile.
        
        Args:
            verses: Dictionary of verse_num -> text
            language: Language name
            
        Returns:
            LanguageProfile with natural harmony characteristics
        """
        harmonies = []
        ljpw_coords = []
        convergence_cycles = []
        dimension_counts = defaultdict(int)
        
        for verse_num, text in verses.items():
            # Get LJPW coordinates
            result = self.detector.calculate_field_signature_v2(text)
            coords = [result['L'], result['J'], result['P'], result['W']]
            ljpw_coords.append(coords)
            
            # Calculate harmony
            harmony = self.engine.calculate_harmony(np.array(coords))
            harmonies.append(harmony)
            
            # Track dominant dimension
            dominant_idx = np.argmax(coords)
            dim_names = ['L', 'J', 'P', 'W']
            dimension_counts[dim_names[dominant_idx]] += 1
            
            # Run quick resonance to see convergence rate
            res = self.engine.run_resonance_cycles(coords, cycles=50, record_interval=10)
            if res.peak_harmony > 0.99:
                convergence_cycles.append(res.peak_cycle)
            else:
                convergence_cycles.append(50)  # Didn't fully converge
        
        # Calculate statistics
        harmonies = np.array(harmonies)
        ljpw_mean = np.mean(ljpw_coords, axis=0)
        
        # Create harmony distribution bins
        bins = {'0.0-0.5': 0, '0.5-0.6': 0, '0.6-0.7': 0, '0.7-0.8': 0, '0.8-0.9': 0, '0.9-1.0': 0}
        for h in harmonies:
            if h < 0.5:
                bins['0.0-0.5'] += 1
            elif h < 0.6:
                bins['0.5-0.6'] += 1
            elif h < 0.7:
                bins['0.6-0.7'] += 1
            elif h < 0.8:
                bins['0.7-0.8'] += 1
            elif h < 0.9:
                bins['0.8-0.9'] += 1
            else:
                bins['0.9-1.0'] += 1
        
        # Find dominant dimension
        dominant = max(dimension_counts, key=dimension_counts.get)
        dim_full_names = {'L': 'Love', 'J': 'Justice', 'P': 'Power', 'W': 'Wisdom'}
        
        return LanguageProfile(
            language=language,
            verse_count=len(verses),
            mean_harmony=float(np.mean(harmonies)),
            std_harmony=float(np.std(harmonies)),
            min_harmony=float(np.min(harmonies)),
            max_harmony=float(np.max(harmonies)),
            mean_ljpw=ljpw_mean.tolist(),
            dominant_dimension=dim_full_names[dominant],
            resonance_convergence_rate=float(np.mean(convergence_cycles)),
            harmony_distribution=bins
        )
    
    def calibrate_all_languages(self, corpora_dir: str = None) -> Dict[str, LanguageProfile]:
        """
        Calibrate all available language corpora.
        
        Args:
            corpora_dir: Directory containing corpus JSON files
            
        Returns:
            Dictionary of language -> LanguageProfile
        """
        if corpora_dir is None:
            corpora_dir = os.path.dirname(os.path.abspath(__file__))
        
        corpus_files = {
            'Greek': 'greek_mark_chapter1.json',
            'English': 'nwt_mark_chapter1.json',
            'Spanish': 'spanish_mark_chapter1.json',
            'Chinese': 'chinese_mark_chapter1.json',
            'Wedau': 'wedau_mark_chapter1.json',
        }
        
        for lang, filename in corpus_files.items():
            filepath = os.path.join(corpora_dir, filename)
            if os.path.exists(filepath):
                print(f"\nAnalyzing {lang}...")
                with open(filepath, 'r', encoding='utf-8') as f:
                    corpus = json.load(f)
                
                profile = self.analyze_corpus(corpus['verses'], lang)
                self.profiles[lang] = profile
                
                print(f"  Verses: {profile.verse_count}")
                print(f"  Mean Harmony: {profile.mean_harmony:.4f} (+/- {profile.std_harmony:.4f})")
                print(f"  Dominant: {profile.dominant_dimension}")
        
        return self.profiles
    
    def get_calibrated_threshold(self, language: str, std_multiplier: float = 2.0) -> float:
        """
        Get language-calibrated quality threshold.
        
        Returns threshold = mean - (std * multiplier)
        Translations below this are unusual for this language.
        """
        if language not in self.profiles:
            return 0.5  # Default
        
        profile = self.profiles[language]
        return profile.mean_harmony - (profile.std_harmony * std_multiplier)
    
    def compare_to_baseline(self, coords: List[float], language: str) -> Dict:
        """
        Compare coordinates against that language's baseline.
        
        Returns how typical or unusual this translation is for the language.
        """
        if language not in self.profiles:
            return {'error': f'No profile for {language}'}
        
        profile = self.profiles[language]
        
        # Calculate harmony
        harmony = self.engine.calculate_harmony(np.array(coords))
        
        # Compare to baseline
        z_score = (harmony - profile.mean_harmony) / profile.std_harmony
        
        # Interpret
        if abs(z_score) < 1:
            typicality = "Typical for this language"
        elif abs(z_score) < 2:
            typicality = "Slightly unusual"
        else:
            typicality = "Very unusual - investigate"
        
        return {
            'harmony': harmony,
            'language_mean': profile.mean_harmony,
            'z_score': z_score,
            'typicality': typicality,
            'above_threshold': harmony > self.get_calibrated_threshold(language)
        }
    
    def save_profiles(self, output_path: str):
        """Save calibration profiles to JSON."""
        data = {}
        for lang, profile in self.profiles.items():
            data[lang] = {
                'verse_count': profile.verse_count,
                'mean_harmony': profile.mean_harmony,
                'std_harmony': profile.std_harmony,
                'min_harmony': profile.min_harmony,
                'max_harmony': profile.max_harmony,
                'mean_ljpw': profile.mean_ljpw,
                'dominant_dimension': profile.dominant_dimension,
                'resonance_convergence_rate': profile.resonance_convergence_rate,
                'harmony_distribution': profile.harmony_distribution
            }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_profiles(self, input_path: str):
        """Load calibration profiles from JSON."""
        with open(input_path, 'r') as f:
            data = json.load(f)
        
        for lang, profile_data in data.items():
            self.profiles[lang] = LanguageProfile(
                language=lang,
                **profile_data
            )


def main():
    print("=" * 70)
    print("CROSS-LANGUAGE HARMONY CALIBRATION")
    print("Discovering natural harmony profiles for each language")
    print("=" * 70)
    
    calibrator = HarmonyCalibrator()
    profiles = calibrator.calibrate_all_languages()
    
    # Summary comparison
    print("\n" + "=" * 70)
    print("CALIBRATION RESULTS")
    print("=" * 70)
    
    print(f"\n{'Language':<12} {'Mean H':<10} {'Std':<10} {'Range':<15} {'Dominant':<12}")
    print("-" * 65)
    
    for lang in sorted(profiles.keys()):
        p = profiles[lang]
        range_str = f"{p.min_harmony:.2f}-{p.max_harmony:.2f}"
        print(f"{lang:<12} {p.mean_harmony:<10.4f} {p.std_harmony:<10.4f} {range_str:<15} {p.dominant_dimension:<12}")
    
    # Key insights
    print("\n" + "=" * 70)
    print("KEY INSIGHTS")
    print("=" * 70)
    
    # Sort by mean harmony
    sorted_langs = sorted(profiles.keys(), key=lambda x: profiles[x].mean_harmony, reverse=True)
    highest = profiles[sorted_langs[0]]
    lowest = profiles[sorted_langs[-1]]
    
    print(f"\nHighest baseline harmony: {highest.language} (H = {highest.mean_harmony:.4f})")
    print(f"Lowest baseline harmony: {lowest.language} (H = {lowest.mean_harmony:.4f})")
    print(f"Range across languages: {highest.mean_harmony - lowest.mean_harmony:.4f}")
    
    # Dominant dimension analysis
    print("\nDominant dimensions by language:")
    for lang, p in profiles.items():
        print(f"  {lang}: {p.dominant_dimension} (mean LJPW: [{', '.join(f'{x:.2f}' for x in p.mean_ljpw)}])")
    
    # Save calibration
    save_path = os.path.join(os.path.dirname(__file__), 'language_harmony_calibration.json')
    calibrator.save_profiles(save_path)
    print(f"\nCalibration saved to: {save_path}")
    
    print("\n" + "=" * 70)
    print("CALIBRATION COMPLETE")
    print("=" * 70)
    print("\nUse these baselines to:")
    print("  1. Set language-specific quality thresholds")
    print("  2. Normalize cross-language comparisons")
    print("  3. Detect outlier translations relative to language norms")


if __name__ == '__main__':
    main()
