#!/usr/bin/env python3
"""
Multi-Language Resonance Validation
====================================

Validates resonance-based translation quality across all available
language corpora: Greek, English, Spanish, Chinese, Wedau.

Demonstrates that translations from different languages converge to
the same semantic attractor, proving semantic equivalence.
"""

import json
import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_quantum.resonance_engine import ResonanceEngine
from experiments.enhanced_pattern_detector import EnhancedPatternDetector


def load_all_corpora():
    """Load all available Mark 1 translations."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    corpora = {}
    files = [
        ('greek', 'greek_mark_chapter1.json'),
        ('english', 'nwt_mark_chapter1.json'),
        ('spanish', 'spanish_mark_chapter1.json'),
        ('chinese', 'chinese_mark_chapter1.json'),
        ('wedau', 'wedau_mark_chapter1.json'),
    ]
    
    for lang, filename in files:
        filepath = os.path.join(base_path, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                corpora[lang] = json.load(f)
                print(f"  Loaded: {lang} ({len(corpora[lang]['verses'])} verses)")
    
    return corpora


def validate_resonance_across_languages(corpora, verses_to_test=None):
    """Validate resonance equivalence across all language pairs."""
    
    detector = EnhancedPatternDetector()
    engine = ResonanceEngine()
    
    if verses_to_test is None:
        # Test verses 1, 11, 15, 41 (theological diversity)
        verses_to_test = ['1', '11', '15', '41']
    
    results = {}
    
    for verse_num in verses_to_test:
        print(f"\n{'='*60}")
        print(f"VERSE {verse_num}")
        print('='*60)
        
        # Get LJPW coordinates for each language
        coords = {}
        for lang, corpus in corpora.items():
            if verse_num in corpus['verses']:
                text = corpus['verses'][verse_num]
                result = detector.calculate_field_signature_v2(text)
                coords[lang] = [result['L'], result['J'], result['P'], result['W']]
        
        # Compare all pairs using resonance
        pairs_tested = 0
        all_equivalent = True
        euclidean_dists = []
        
        languages = list(coords.keys())
        for i in range(len(languages)):
            for j in range(i+1, len(languages)):
                lang1, lang2 = languages[i], languages[j]
                
                # Traditional euclidean distance
                euc_dist = np.linalg.norm(np.array(coords[lang1]) - np.array(coords[lang2]))
                euclidean_dists.append(euc_dist)
                
                # Resonance analysis
                analysis = engine.analyze_translation_pair(
                    coords[lang1], coords[lang2], cycles=100
                )
                
                quality = analysis['quality_assessment']
                same_attractor = analysis['same_deficit']
                
                if not same_attractor or analysis['convergence_distance'] > 0.1:
                    all_equivalent = False
                
                pairs_tested += 1
        
        results[verse_num] = {
            'languages': languages,
            'pairs_tested': pairs_tested,
            'all_equivalent': all_equivalent,
            'max_euclidean': max(euclidean_dists) if euclidean_dists else 0,
            'min_euclidean': min(euclidean_dists) if euclidean_dists else 0,
            'avg_euclidean': np.mean(euclidean_dists) if euclidean_dists else 0
        }
        
        print(f"Languages: {', '.join(languages)}")
        print(f"Pairs tested: {pairs_tested}")
        print(f"Euclidean range: {results[verse_num]['min_euclidean']:.3f} - {results[verse_num]['max_euclidean']:.3f}")
        print(f"All resonance-equivalent: {all_equivalent}")
    
    return results


def main():
    print("=" * 60)
    print("MULTI-LANGUAGE RESONANCE VALIDATION")
    print("Proving translations converge to same semantic attractor")
    print("=" * 60)
    
    print("\nLoading corpora...")
    corpora = load_all_corpora()
    
    if len(corpora) < 2:
        print("Error: Need at least 2 language corpora for validation")
        return
    
    print(f"\nLoaded {len(corpora)} languages: {', '.join(corpora.keys())}")
    
    # Run validation
    results = validate_resonance_across_languages(corpora)
    
    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    total_verses = len(results)
    equivalent_verses = sum(1 for v in results.values() if v['all_equivalent'])
    max_euclidean = max(v['max_euclidean'] for v in results.values())
    
    print(f"\nVerses tested: {total_verses}")
    print(f"All pairs resonance-equivalent: {equivalent_verses}/{total_verses}")
    print(f"Maximum euclidean distance: {max_euclidean:.3f}")
    
    print(f"\n>>> KEY FINDING:")
    if equivalent_verses == total_verses:
        print(f"    ALL {total_verses} verses show resonance equivalence across")
        print(f"    {len(corpora)} languages, despite euclidean distances up to {max_euclidean:.3f}")
        print(f"    This VALIDATES the resonance paradigm!")
    else:
        print(f"    {equivalent_verses}/{total_verses} verses show resonance equivalence")
        print(f"    Some pairs may have semantic drift - investigate further")
    
    # Save results
    save_path = os.path.join(os.path.dirname(__file__), 'multilang_resonance_results.json')
    with open(save_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {save_path}")


if __name__ == '__main__':
    main()
