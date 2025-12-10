#!/usr/bin/env python3
"""
Word-Meaning Correlation Analysis
==================================

Analyzes 100 common English words to find correlations between:
- Word categories (verbs, nouns, adjectives)
- LJPW dimensions (Love, Justice, Power, Wisdom)
- Semantic clusters

Goal: Find patterns that can help vocabulary expansion.
"""

import sys
import os
import numpy as np
from typing import Dict, List, Tuple
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from experiments.enhanced_pattern_detector import EnhancedPatternDetector

# 100 Common English Words (categorized)
COMMON_WORDS = {
    # Relational (expected: high Love)
    'love': 'relational',
    'friend': 'relational',
    'family': 'relational',
    'mother': 'relational',
    'father': 'relational',
    'child': 'relational',
    'brother': 'relational',
    'sister': 'relational',
    'heart': 'relational',
    'care': 'relational',
    'help': 'relational',
    'together': 'relational',
    'forgive': 'relational',
    'mercy': 'relational',
    'compassion': 'relational',
    
    # Structural (expected: high Justice)
    'law': 'structural',
    'rule': 'structural',
    'order': 'structural',
    'truth': 'structural',
    'right': 'structural',
    'wrong': 'structural',
    'fair': 'structural',
    'equal': 'structural',
    'balance': 'structural',
    'command': 'structural',
    'covenant': 'structural',
    'promise': 'structural',
    'judgment': 'structural',
    'worthy': 'structural',
    'deserve': 'structural',
    
    # Dynamic (expected: high Power)
    'king': 'dynamic',
    'power': 'dynamic',
    'strong': 'dynamic',
    'mighty': 'dynamic',
    'authority': 'dynamic',
    'command': 'dynamic',
    'rule': 'dynamic',
    'victory': 'dynamic',
    'conquer': 'dynamic',
    'rise': 'dynamic',
    'fight': 'dynamic',
    'kingdom': 'dynamic',
    'glory': 'dynamic',
    'throne': 'dynamic',
    'force': 'dynamic',
    
    # Knowledge (expected: high Wisdom)
    'wisdom': 'knowledge',
    'know': 'knowledge',
    'understand': 'knowledge',
    'learn': 'knowledge',
    'teach': 'knowledge',
    'truth': 'knowledge',
    'light': 'knowledge',
    'see': 'knowledge',
    'reveal': 'knowledge',
    'mystery': 'knowledge',
    'secret': 'knowledge',
    'disciple': 'knowledge',
    'prophet': 'knowledge',
    'word': 'knowledge',
    'scripture': 'knowledge',
    
    # Common verbs
    'go': 'verb',
    'come': 'verb',
    'say': 'verb',
    'give': 'verb',
    'take': 'verb',
    'make': 'verb',
    'do': 'verb',
    'have': 'verb',
    'be': 'verb',
    'see': 'verb',
    
    # Common nouns
    'man': 'noun',
    'woman': 'noun',
    'people': 'noun',
    'world': 'noun',
    'day': 'noun',
    'time': 'noun',
    'life': 'noun',
    'death': 'noun',
    'heaven': 'noun',
    'earth': 'noun',
    
    # Religious terms
    'god': 'religious',
    'jesus': 'religious',
    'spirit': 'religious',
    'holy': 'religious',
    'sin': 'religious',
    'save': 'religious',
    'faith': 'religious',
    'believe': 'religious',
    'pray': 'religious',
    'bless': 'religious',
}


def analyze_words():
    """Analyze all words and compute LJPW coordinates."""
    
    detector = EnhancedPatternDetector()
    results = []
    
    for word, category in COMMON_WORDS.items():
        result = detector.calculate_field_signature_v2(word)
        coords = [result['L'], result['J'], result['P'], result['W']]
        
        # Find dominant dimension
        dims = ['Love', 'Justice', 'Power', 'Wisdom']
        dominant_idx = np.argmax(coords)
        dominant = dims[dominant_idx]
        
        results.append({
            'word': word,
            'category': category,
            'L': coords[0],
            'J': coords[1],
            'P': coords[2],
            'W': coords[3],
            'dominant': dominant,
            'harmony': np.mean(coords)
        })
    
    return results


def find_correlations(results: List[Dict]):
    """Find correlations between categories and dimensions."""
    
    category_dims = defaultdict(lambda: {'L': [], 'J': [], 'P': [], 'W': []})
    
    for r in results:
        cat = r['category']
        category_dims[cat]['L'].append(r['L'])
        category_dims[cat]['J'].append(r['J'])
        category_dims[cat]['P'].append(r['P'])
        category_dims[cat]['W'].append(r['W'])
    
    correlations = {}
    for cat, dims in category_dims.items():
        correlations[cat] = {
            'avg_L': np.mean(dims['L']),
            'avg_J': np.mean(dims['J']),
            'avg_P': np.mean(dims['P']),
            'avg_W': np.mean(dims['W']),
            'dominant': ['Love', 'Justice', 'Power', 'Wisdom'][
                np.argmax([np.mean(dims['L']), np.mean(dims['J']), 
                          np.mean(dims['P']), np.mean(dims['W'])])
            ],
            'count': len(dims['L'])
        }
    
    return correlations


def find_clusters(results: List[Dict]):
    """Find semantic clusters based on dominant dimension."""
    
    clusters = {'Love': [], 'Justice': [], 'Power': [], 'Wisdom': []}
    
    for r in results:
        clusters[r['dominant']].append(r['word'])
    
    return clusters


def main():
    print("=" * 70)
    print("WORD-MEANING CORRELATION ANALYSIS")
    print("100 Common English Words in LJPW Space")
    print("=" * 70)
    
    results = analyze_words()
    
    # Print all words with their LJPW coordinates
    print("\n" + "-" * 70)
    print(f"{'Word':<15} {'Category':<12} {'L':<8} {'J':<8} {'P':<8} {'W':<8} {'Dominant'}")
    print("-" * 70)
    
    for r in sorted(results, key=lambda x: x['category']):
        print(f"{r['word']:<15} {r['category']:<12} {r['L']:<8.3f} {r['J']:<8.3f} "
              f"{r['P']:<8.3f} {r['W']:<8.3f} {r['dominant']}")
    
    # Category correlations
    print("\n" + "=" * 70)
    print("CATEGORY -> DIMENSION CORRELATIONS")
    print("=" * 70)
    
    correlations = find_correlations(results)
    
    print(f"\n{'Category':<12} {'Avg L':<8} {'Avg J':<8} {'Avg P':<8} {'Avg W':<8} {'Dominant':<10} {'Count'}")
    print("-" * 70)
    
    for cat, data in sorted(correlations.items()):
        print(f"{cat:<12} {data['avg_L']:<8.3f} {data['avg_J']:<8.3f} "
              f"{data['avg_P']:<8.3f} {data['avg_W']:<8.3f} {data['dominant']:<10} {data['count']}")
    
    # Semantic clusters
    print("\n" + "=" * 70)
    print("SEMANTIC CLUSTERS (by dominant dimension)")
    print("=" * 70)
    
    clusters = find_clusters(results)
    
    for dim, words in clusters.items():
        print(f"\n{dim} ({len(words)} words):")
        print(f"  {', '.join(sorted(words))}")
    
    # Key insights
    print("\n" + "=" * 70)
    print("KEY INSIGHTS")
    print("=" * 70)
    
    # Check if categories match expected dimensions
    expected = {
        'relational': 'Love',
        'structural': 'Justice',
        'dynamic': 'Power',
        'knowledge': 'Wisdom'
    }
    
    print("\nCategory-Dimension Alignment:")
    for cat, exp_dim in expected.items():
        if cat in correlations:
            actual = correlations[cat]['dominant']
            match = "YES" if actual == exp_dim else "NO"
            print(f"  {cat}: Expected {exp_dim}, Got {actual} [{match}]")
    
    # Find words with unexpected mappings
    print("\nInteresting Mappings (category differs from dominant dimension):")
    category_to_dim = {
        'relational': 'Love',
        'structural': 'Justice', 
        'dynamic': 'Power',
        'knowledge': 'Wisdom'
    }
    
    for r in results:
        cat = r['category']
        if cat in category_to_dim:
            expected_dim = category_to_dim[cat]
            if r['dominant'] != expected_dim:
                print(f"  '{r['word']}' ({cat}): Expected {expected_dim}, Got {r['dominant']}")


if __name__ == '__main__':
    main()
