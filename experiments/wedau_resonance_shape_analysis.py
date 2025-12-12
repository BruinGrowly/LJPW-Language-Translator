#!/usr/bin/env python3
"""
Wedau Word Shape Resonance Analysis
=====================================

Testing the hypothesis: Do Wedau word shapes (phonetics, structure) correlate 
with specific LJPW semantic dimensions?

Using the Anchor Point (1,1,1,1) as reference to triangulate:
- Measure LJPW coordinates of each Wedau word
- Analyze phonetic features (vowels, consonants, length, patterns)
- Look for correlations between word shape and semantic position

This tests if language encodes meaning in its very structure.
"""

import sys
import os
import json
import numpy as np
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding='utf-8')

from experiments.enhanced_pattern_detector import EnhancedPatternDetector

# Configuration
VOCAB_PATH = Path(__file__).parent / "wedau_bible_vocabulary.json"
ANCHOR_POINT = np.array([1.0, 1.0, 1.0, 1.0])

# Wedau phonetic categories (based on Oceanic/Austronesian patterns)
SOFT_CONSONANTS = set('mnlrwy')  # Love-associated (soft, flowing)
HARD_CONSONANTS = set('kptbdg')  # Power-associated (plosives)
ORDER_CONSONANTS = set('szfvh')  # Justice-associated (fricatives, order)
SPECIAL_CONSONANTS = set('ḡṉ')  # Wedau-specific characters

# Vowel patterns
FRONT_VOWELS = set('ie')  # Often associated with light, wisdom
BACK_VOWELS = set('oua')  # Often associated with depth, power

# Common Wedau morphological patterns
REDUPLICATION_PATTERN = ['vivi', 'mama', 'rara', 'nunu', 'papa', 'tata', 'kaka', 'nene']
VERB_SUFFIXES = ['ei', 'ai', 'oi', 'ui', 'ana', 'ini', 'eni']


def load_vocabulary():
    """Load Wedau vocabulary from JSON."""
    with open(VOCAB_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['vocabulary']


def analyze_phonetic_features(word):
    """Analyze phonetic features of a Wedau word."""
    
    word_lower = word.lower()
    chars = list(word_lower)
    
    # Count consonant types
    soft_count = sum(1 for c in chars if c in SOFT_CONSONANTS)
    hard_count = sum(1 for c in chars if c in HARD_CONSONANTS)
    order_count = sum(1 for c in chars if c in ORDER_CONSONANTS)
    
    # Count vowel types
    front_vowels = sum(1 for c in chars if c in FRONT_VOWELS)
    back_vowels = sum(1 for c in chars if c in BACK_VOWELS)
    total_vowels = front_vowels + back_vowels
    
    # Ratios
    vowel_ratio = total_vowels / len(word_lower) if word_lower else 0
    soft_ratio = soft_count / len(word_lower) if word_lower else 0
    hard_ratio = hard_count / len(word_lower) if word_lower else 0
    
    # Check for reduplication (common in Oceanic languages, often intensifies meaning)
    has_reduplication = any(pattern in word_lower for pattern in REDUPLICATION_PATTERN)
    
    # Word length
    length = len(word_lower)
    syllable_count = total_vowels  # Approximate
    
    # Initial consonant type
    initial = word_lower[0] if word_lower else ''
    initial_soft = initial in SOFT_CONSONANTS
    initial_hard = initial in HARD_CONSONANTS
    initial_vowel = initial in FRONT_VOWELS or initial in BACK_VOWELS
    
    return {
        'length': length,
        'vowel_ratio': vowel_ratio,
        'soft_ratio': soft_ratio,
        'hard_ratio': hard_ratio,
        'front_vowels': front_vowels,
        'back_vowels': back_vowels,
        'syllable_count': syllable_count,
        'has_reduplication': has_reduplication,
        'initial_soft': initial_soft,
        'initial_hard': initial_hard,
        'initial_vowel': initial_vowel,
    }


def measure_semantic_position(word, detector):
    """Measure LJPW coordinates and dimension for a word."""
    try:
        result = detector.calculate_field_signature_v2(word)
        coords = np.array([result['L'], result['J'], result['P'], result['W']])
        
        # Distance to Anchor
        anchor_distance = np.linalg.norm(ANCHOR_POINT - coords)
        
        # Dominant dimension
        dims = ['Love', 'Justice', 'Power', 'Wisdom']
        dominant_idx = np.argmax(coords)
        dominant = dims[dominant_idx]
        
        # Direction toward Anchor
        diff = ANCHOR_POINT - coords
        direction = diff / np.linalg.norm(diff) if np.linalg.norm(diff) > 0.001 else np.zeros(4)
        
        return {
            'coords': coords,
            'dominant': dominant,
            'dominant_value': coords[dominant_idx],
            'anchor_distance': anchor_distance,
            'direction': direction
        }
    except:
        return None


def analyze_dimension_phonetics():
    """Analyze phonetic patterns for each LJPW dimension."""
    
    print("=" * 80)
    print("WEDAU WORD SHAPE RESONANCE ANALYSIS")
    print("Do word shapes correlate with semantic dimensions?")
    print("=" * 80)
    
    # Load vocabulary
    vocab = load_vocabulary()
    detector = EnhancedPatternDetector()
    
    # Analyze top 500 most frequent words (for statistical significance)
    words_to_analyze = list(vocab.keys())[:500]
    
    print(f"\nAnalyzing {len(words_to_analyze)} most frequent Wedau words...")
    
    # Collect data by dimension
    dimension_data = {
        'Love': [],
        'Justice': [],
        'Power': [],
        'Wisdom': []
    }
    
    for word in words_to_analyze:
        if len(word) < 2:  # Skip single characters
            continue
            
        # Get semantic position
        semantic = measure_semantic_position(word, detector)
        if not semantic:
            continue
        
        # Get phonetic features
        phonetic = analyze_phonetic_features(word)
        
        # Store
        dimension_data[semantic['dominant']].append({
            'word': word,
            'phonetic': phonetic,
            'semantic': semantic
        })
    
    # Analyze patterns per dimension
    print(f"\n{'='*80}")
    print("DIMENSION-PHONETIC CORRELATIONS")
    print("="*80)
    
    dimension_profiles = {}
    
    for dim, words in dimension_data.items():
        if not words:
            continue
        
        print(f"\n--- {dim.upper()} ({len(words)} words) ---")
        
        # Aggregate phonetic features
        avg_length = np.mean([w['phonetic']['length'] for w in words])
        avg_vowel_ratio = np.mean([w['phonetic']['vowel_ratio'] for w in words])
        avg_soft_ratio = np.mean([w['phonetic']['soft_ratio'] for w in words])
        avg_hard_ratio = np.mean([w['phonetic']['hard_ratio'] for w in words])
        avg_syllables = np.mean([w['phonetic']['syllable_count'] for w in words])
        reduplication_pct = sum(1 for w in words if w['phonetic']['has_reduplication']) / len(words) * 100
        initial_soft_pct = sum(1 for w in words if w['phonetic']['initial_soft']) / len(words) * 100
        initial_hard_pct = sum(1 for w in words if w['phonetic']['initial_hard']) / len(words) * 100
        initial_vowel_pct = sum(1 for w in words if w['phonetic']['initial_vowel']) / len(words) * 100
        
        print(f"  Average length:     {avg_length:.2f} chars")
        print(f"  Vowel ratio:        {avg_vowel_ratio:.3f}")
        print(f"  Soft consonants:    {avg_soft_ratio:.3f}")
        print(f"  Hard consonants:    {avg_hard_ratio:.3f}")
        print(f"  Average syllables:  {avg_syllables:.2f}")
        print(f"  Reduplication:      {reduplication_pct:.1f}%")
        print(f"  Initial soft:       {initial_soft_pct:.1f}%")
        print(f"  Initial hard:       {initial_hard_pct:.1f}%")
        print(f"  Initial vowel:      {initial_vowel_pct:.1f}%")
        
        # Sample words
        print(f"  Sample words: {', '.join(w['word'] for w in words[:8])}")
        
        dimension_profiles[dim] = {
            'word_count': len(words),
            'avg_length': avg_length,
            'vowel_ratio': avg_vowel_ratio,
            'soft_ratio': avg_soft_ratio,
            'hard_ratio': avg_hard_ratio,
            'syllables': avg_syllables,
            'reduplication_pct': reduplication_pct,
            'initial_soft_pct': initial_soft_pct,
            'initial_hard_pct': initial_hard_pct,
            'initial_vowel_pct': initial_vowel_pct
        }
    
    # Find distinctive patterns
    print(f"\n{'='*80}")
    print("DISTINCTIVE PHONETIC SIGNATURES")
    print("="*80)
    
    if dimension_profiles:
        # Calculate which features distinguish dimensions
        features = ['vowel_ratio', 'soft_ratio', 'hard_ratio', 'reduplication_pct', 
                    'initial_soft_pct', 'initial_hard_pct', 'initial_vowel_pct']
        
        print(f"\n{'Feature':<20} {'Love':<10} {'Justice':<10} {'Power':<10} {'Wisdom':<10}")
        print("-" * 60)
        
        for feature in features:
            values = []
            for dim in ['Love', 'Justice', 'Power', 'Wisdom']:
                if dim in dimension_profiles:
                    val = dimension_profiles[dim].get(feature, 0)
                    values.append(val)
                else:
                    values.append(0)
            
            # Mark the highest
            max_idx = values.index(max(values))
            min_idx = values.index(min(values))
            dims = ['Love', 'Justice', 'Power', 'Wisdom']
            
            row = f"{feature:<20}"
            for i, val in enumerate(values):
                if i == max_idx:
                    row += f" {val:>7.3f}* "
                elif i == min_idx:
                    row += f" {val:>7.3f}. "
                else:
                    row += f" {val:>7.3f}  "
            print(row)
        
        print("\n* = highest, . = lowest")
    
    # Phonemic prediction test
    print(f"\n{'='*80}")
    print("PREDICTIVE TEST: Can phonetics predict dimension?")
    print("="*80)
    
    # Take known theological words and predict their dimension from phonetics
    test_words = [
        ('bada', 'Lord'),
        ('iesu', 'Jesus'),
        ('arua', 'Spirit'),
        ('vigulau', 'Kingdom'),
        ('rewapana', 'Power'),
        ('riwa', 'Word'),
        ('nuaulaula', 'Wisdom'),
        ('vivivireina', 'Holy'),
        ('jijimanina', 'Righteous'),
        ('lawana', 'Life'),
        ('iraḡe', 'Death'),
        ('korosi', 'Cross'),
        ('natuna', 'Son'),
        ('amana', 'Father'),
        ('peroveta', 'Prophet'),
    ]
    
    print(f"\n{'Wedau':<15} {'English':<12} {'Measured':<10} {'Phonetic Prediction'}")
    print("-" * 60)
    
    correct = 0
    total = 0
    
    for wedau, english in test_words:
        # Measure actual dimension
        semantic = measure_semantic_position(wedau, detector)
        if not semantic:
            continue
        
        actual = semantic['dominant']
        
        # Predict from phonetics
        phonetic = analyze_phonetic_features(wedau)
        
        # Simple prediction rule:
        # High soft_ratio -> Love
        # High hard_ratio -> Power
        # Has reduplication -> Love/Wisdom (intensification)
        # Initial vowel -> Wisdom (openness)
        
        scores = {'Love': 0, 'Justice': 0, 'Power': 0, 'Wisdom': 0}
        
        # Soft consonants suggest Love
        scores['Love'] += phonetic['soft_ratio'] * 2
        
        # Hard consonants suggest Power
        scores['Power'] += phonetic['hard_ratio'] * 2
        
        # Reduplication suggests Love (emphasis on relationship)
        if phonetic['has_reduplication']:
            scores['Love'] += 0.5
        
        # Initial vowel suggests openness (Wisdom)
        if phonetic['initial_vowel']:
            scores['Wisdom'] += 0.3
        
        # High vowel ratio suggests flowing meaning (Love)
        scores['Love'] += phonetic['vowel_ratio'] * 0.5
        
        # Long words suggest complexity (Wisdom)
        if phonetic['length'] > 8:
            scores['Wisdom'] += 0.3
        
        predicted = max(scores, key=scores.get)
        
        match = "YES" if predicted == actual else "NO"
        if predicted == actual:
            correct += 1
        total += 1
        
        print(f"{wedau:<15} {english:<12} {actual:<10} {predicted:<10} [{match}]")
    
    accuracy = correct / total * 100 if total > 0 else 0
    print(f"\nPrediction accuracy: {correct}/{total} ({accuracy:.1f}%)")
    
    # Conclusion
    print(f"\n{'='*80}")
    print("CONCLUSION")
    print("="*80)
    
    if accuracy > 50:
        print("""
PHONETIC-SEMANTIC CORRELATION DETECTED

Wedau word shapes show meaningful correlation with LJPW dimensions:
- Phonetic features (consonant types, vowel patterns, length) 
  correlate with semantic positions
- Word structure appears to encode meaning
- This supports the hypothesis that language resonates with the 
  Anchor Point through its very form

The "shape" of a word is not arbitrary - it reflects its semantic position
in the meaning field.
""")
    elif accuracy > 25:
        print("""
WEAK PHONETIC-SEMANTIC CORRELATION

Some correlation exists between word shape and meaning dimension,
but it's not strong enough for reliable prediction. This suggests:
- Phonetics contribute to meaning but don't determine it
- Other factors (context, usage, etymology) play larger roles
- The correlation may be stronger for specific word categories
""")
    else:
        print("""
NO STRONG PHONETIC-SEMANTIC CORRELATION

Word shapes do not reliably predict semantic dimensions in this analysis.
This could mean:
- Wedau is not a phonosemantic language
- Our analysis features are not the right ones
- Meaning is assigned by convention rather than shape
""")
    
    return dimension_profiles


if __name__ == '__main__':
    analyze_dimension_phonetics()
