#!/usr/bin/env python3
"""
Comprehensive Translation System Test Suite
============================================

Exhaustive testing of the LJPW translation system across:
- All 5 languages (Greek, English, Spanish, Chinese, Wedau)
- All verse combinations
- Dimension-by-dimension analysis
- Edge case identification
- Statistical robustness tests
"""

import json
import sys
import os
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple
from collections import defaultdict
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_quantum.resonance_engine import ResonanceEngine
from experiments.enhanced_pattern_detector import EnhancedPatternDetector


class ComprehensiveTestSuite:
    """Full test suite for LJPW translation validation."""
    
    def __init__(self):
        self.engine = ResonanceEngine()
        self.detector = EnhancedPatternDetector()
        self.corpora = {}
        self.results = {}
        
    def load_all_corpora(self):
        """Load all available language corpora."""
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        corpus_files = {
            'Greek': 'greek_mark_chapter1.json',
            'English': 'nwt_mark_chapter1.json',
            'Spanish': 'spanish_mark_chapter1.json',
            'Chinese': 'chinese_mark_chapter1.json',
            'Wedau': 'wedau_mark_chapter1.json',
        }
        
        for lang, filename in corpus_files.items():
            filepath = os.path.join(base_path, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.corpora[lang] = json.load(f)
        
        return len(self.corpora)
    
    def get_ljpw_coords(self, text: str) -> List[float]:
        """Get LJPW coordinates for text."""
        result = self.detector.calculate_field_signature_v2(text)
        return [result['L'], result['J'], result['P'], result['W']]
    
    def test_language_pair(self, lang1: str, lang2: str) -> Dict:
        """Test all verse translations between two languages."""
        
        corpus1 = self.corpora[lang1]
        corpus2 = self.corpora[lang2]
        
        common = set(corpus1['verses'].keys()) & set(corpus2['verses'].keys())
        
        passed_euclidean = 0
        passed_resonance = 0
        verse_results = []
        
        euclidean_dists = []
        convergence_dists = []
        dimension_diffs = {'L': [], 'J': [], 'P': [], 'W': []}
        
        for verse_num in sorted(common, key=int):
            text1 = corpus1['verses'][verse_num]
            text2 = corpus2['verses'][verse_num]
            
            coords1 = self.get_ljpw_coords(text1)
            coords2 = self.get_ljpw_coords(text2)
            
            # Euclidean
            euc = np.linalg.norm(np.array(coords1) - np.array(coords2))
            euclidean_dists.append(euc)
            
            # Dimension differences
            for i, dim in enumerate(['L', 'J', 'P', 'W']):
                dimension_diffs[dim].append(abs(coords1[i] - coords2[i]))
            
            # Resonance
            analysis = self.engine.analyze_translation_pair(coords1, coords2, cycles=100)
            conv = analysis['convergence_distance']
            convergence_dists.append(conv)
            same_attr = analysis['same_deficit']
            
            if euc < 0.10:
                passed_euclidean += 1
            if conv < 0.10 and same_attr:
                passed_resonance += 1
        
        return {
            'pair': f"{lang1}-{lang2}",
            'total_verses': len(common),
            'passed_euclidean': passed_euclidean,
            'passed_resonance': passed_resonance,
            'euclidean_mean': float(np.mean(euclidean_dists)),
            'euclidean_max': float(max(euclidean_dists)),
            'euclidean_min': float(min(euclidean_dists)),
            'euclidean_std': float(np.std(euclidean_dists)),
            'convergence_mean': float(np.mean(convergence_dists)),
            'dimension_analysis': {
                dim: {
                    'mean_diff': float(np.mean(diffs)),
                    'max_diff': float(max(diffs)),
                    'std': float(np.std(diffs))
                }
                for dim, diffs in dimension_diffs.items()
            }
        }
    
    def test_all_pairs(self) -> Dict:
        """Test all language pair combinations."""
        
        languages = list(self.corpora.keys())
        all_results = {}
        
        for lang1, lang2 in combinations(languages, 2):
            pair_key = f"{lang1}-{lang2}"
            print(f"  Testing: {pair_key}...")
            all_results[pair_key] = self.test_language_pair(lang1, lang2)
        
        return all_results
    
    def find_edge_cases(self) -> Dict:
        """Find verses with extreme characteristics."""
        
        all_harmonies = []
        all_euclideans = []
        
        # Collect all verse data
        for lang, corpus in self.corpora.items():
            for verse_num, text in corpus['verses'].items():
                coords = self.get_ljpw_coords(text)
                harmony = self.engine.calculate_harmony(np.array(coords))
                all_harmonies.append({
                    'verse': verse_num,
                    'language': lang,
                    'harmony': float(harmony),
                    'coords': coords
                })
        
        # Sort by harmony
        sorted_by_harmony = sorted(all_harmonies, key=lambda x: x['harmony'])
        
        return {
            'lowest_harmony': sorted_by_harmony[:5],
            'highest_harmony': sorted_by_harmony[-5:],
            'harmony_range': {
                'min': sorted_by_harmony[0]['harmony'],
                'max': sorted_by_harmony[-1]['harmony']
            }
        }
    
    def stress_test(self, cycles: int = 10000) -> Dict:
        """Stress test with high cycle counts."""
        
        # Pick a challenging pair (Greek-Wedau)
        if 'Greek' not in self.corpora or 'Wedau' not in self.corpora:
            return {'error': 'Missing corpora'}
        
        greek = self.corpora['Greek']
        wedau = self.corpora['Wedau']
        
        # Test verse 15 (known to have high euclidean distance)
        verse = '15'
        
        greek_coords = self.get_ljpw_coords(greek['verses'][verse])
        wedau_coords = self.get_ljpw_coords(wedau['verses'][verse])
        
        # Run at different cycle counts
        cycle_tests = [100, 1000, 5000, 10000]
        results = {}
        
        for c in cycle_tests:
            analysis = self.engine.analyze_translation_pair(greek_coords, wedau_coords, cycles=c)
            results[str(c)] = {
                'convergence': float(analysis['convergence_distance']),
                'same_attractor': bool(analysis['same_deficit']),
                'quality': analysis['quality_assessment']
            }
        
        return {
            'verse': verse,
            'euclidean_distance': float(np.linalg.norm(np.array(greek_coords) - np.array(wedau_coords))),
            'cycle_results': results
        }
    
    def generate_summary(self) -> Dict:
        """Generate comprehensive summary statistics."""
        
        total_pairs = len(self.results['pair_tests'])
        total_verses = sum(r['total_verses'] for r in self.results['pair_tests'].values())
        
        all_euclidean_passed = sum(r['passed_euclidean'] for r in self.results['pair_tests'].values())
        all_resonance_passed = sum(r['passed_resonance'] for r in self.results['pair_tests'].values())
        
        avg_euclidean = np.mean([r['euclidean_mean'] for r in self.results['pair_tests'].values()])
        max_euclidean = max(r['euclidean_max'] for r in self.results['pair_tests'].values())
        
        return {
            'timestamp': datetime.now().isoformat(),
            'languages_tested': list(self.corpora.keys()),
            'language_pairs': total_pairs,
            'total_verse_comparisons': total_verses,
            'euclidean_passed': all_euclidean_passed,
            'resonance_passed': all_resonance_passed,
            'euclidean_pass_rate': f"{all_euclidean_passed/total_verses*100:.1f}%",
            'resonance_pass_rate': f"{all_resonance_passed/total_verses*100:.1f}%",
            'avg_euclidean': float(avg_euclidean),
            'max_euclidean': float(max_euclidean),
            'conclusion': 'VALIDATED' if all_resonance_passed == total_verses else 'NEEDS_REVIEW'
        }
    
    def run_all(self):
        """Run complete test suite."""
        
        print("=" * 70)
        print("COMPREHENSIVE LJPW TRANSLATION SYSTEM TEST")
        print("=" * 70)
        
        # 1. Load corpora
        print("\n[1/5] Loading corpora...")
        count = self.load_all_corpora()
        print(f"      Loaded {count} languages: {', '.join(self.corpora.keys())}")
        
        # 2. Test all pairs
        print("\n[2/5] Testing all language pairs...")
        self.results['pair_tests'] = self.test_all_pairs()
        
        # 3. Edge cases
        print("\n[3/5] Finding edge cases...")
        self.results['edge_cases'] = self.find_edge_cases()
        
        # 4. Stress test
        print("\n[4/5] Running stress tests...")
        self.results['stress_test'] = self.stress_test()
        
        # 5. Summary
        print("\n[5/5] Generating summary...")
        self.results['summary'] = self.generate_summary()
        
        return self.results


def main():
    suite = ComprehensiveTestSuite()
    results = suite.run_all()
    
    # Print results
    print("\n" + "=" * 70)
    print("LANGUAGE PAIR RESULTS")
    print("=" * 70)
    
    print(f"\n{'Pair':<20} {'Verses':<8} {'Euc Pass':<10} {'Res Pass':<10} {'Euc Mean':<10} {'Euc Max'}")
    print("-" * 70)
    
    for pair, data in results['pair_tests'].items():
        euc_rate = f"{data['passed_euclidean']}/{data['total_verses']}"
        res_rate = f"{data['passed_resonance']}/{data['total_verses']}"
        print(f"{pair:<20} {data['total_verses']:<8} {euc_rate:<10} {res_rate:<10} "
              f"{data['euclidean_mean']:<10.4f} {data['euclidean_max']:.4f}")
    
    # Dimension analysis
    print("\n" + "=" * 70)
    print("DIMENSION ANALYSIS (Average difference by dimension)")
    print("=" * 70)
    
    print(f"\n{'Pair':<20} {'L diff':<10} {'J diff':<10} {'P diff':<10} {'W diff'}")
    print("-" * 60)
    
    for pair, data in results['pair_tests'].items():
        dims = data['dimension_analysis']
        print(f"{pair:<20} {dims['L']['mean_diff']:<10.4f} {dims['J']['mean_diff']:<10.4f} "
              f"{dims['P']['mean_diff']:<10.4f} {dims['W']['mean_diff']:.4f}")
    
    # Edge cases
    print("\n" + "=" * 70)
    print("EDGE CASES")
    print("=" * 70)
    
    print("\nLowest Harmony Verses:")
    for item in results['edge_cases']['lowest_harmony']:
        print(f"  Verse {item['verse']} ({item['language']}): H={item['harmony']:.4f}")
    
    print("\nHighest Harmony Verses:")
    for item in results['edge_cases']['highest_harmony']:
        print(f"  Verse {item['verse']} ({item['language']}): H={item['harmony']:.4f}")
    
    # Stress test
    print("\n" + "=" * 70)
    print("STRESS TEST (Greek-Wedau Verse 15)")
    print("=" * 70)
    
    st = results['stress_test']
    print(f"\nEuclidean distance: {st['euclidean_distance']:.4f}")
    print("\nConvergence by cycle count:")
    for cycles, data in st['cycle_results'].items():
        print(f"  {cycles:>5} cycles: Conv={data['convergence']:.6f}, "
              f"Same Attractor={data['same_attractor']}")
    
    # Final summary
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    
    s = results['summary']
    print(f"\nLanguages: {', '.join(s['languages_tested'])}")
    print(f"Language pairs tested: {s['language_pairs']}")
    print(f"Total verse comparisons: {s['total_verse_comparisons']}")
    print(f"\nTraditional (Euclidean < 0.10): {s['euclidean_pass_rate']}")
    print(f"Resonance (Convergence < 0.10): {s['resonance_pass_rate']}")
    print(f"\nMax Euclidean observed: {s['max_euclidean']:.4f}")
    print(f"\n>>> CONCLUSION: {s['conclusion']}")
    
    # Save results
    save_path = os.path.join(os.path.dirname(__file__), 'comprehensive_test_results.json')
    with open(save_path, 'w') as f:
        # Convert numpy types for JSON
        def convert(obj):
            if isinstance(obj, (np.floating, np.integer)):
                return float(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            if isinstance(obj, np.bool_):
                return bool(obj)
            return obj
        
        import copy
        results_clean = json.loads(json.dumps(results, default=convert))
        json.dump(results_clean, f, indent=2)
    
    print(f"\nFull results saved to: {save_path}")


if __name__ == '__main__':
    main()
