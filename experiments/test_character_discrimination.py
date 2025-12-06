import sys
import os
import json
import numpy as np
from pathlib import Path
from collections import defaultdict

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from experiments.enhanced_pattern_detector import EnhancedPatternDetector

def calculate_harmony(ljpw_coords):
    """Calculate harmony index (distance from Anchor)."""
    anchor = np.array([1.0, 1.0, 1.0, 1.0])
    distance = np.linalg.norm(ljpw_coords - anchor)
    return 1.0 / (1.0 + distance)

def coupling_aware_composition(coords1, coords2, harmony):
    """Compose two LJPW vectors using the coupling matrix."""
    base = (coords1 + coords2) / 2
    
    # State-dependent coupling coefficients
    kappa_LJ = 1.0 + 0.4 * harmony
    kappa_LP = 1.0 + 0.3 * harmony
    kappa_LW = 1.0 + 0.5 * harmony
    
    # Apply coupling effects
    L_composed = base[0]
    J_composed = base[1] + base[0] * 0.4 * kappa_LJ
    P_composed = base[2] + base[0] * 0.3 * kappa_LP
    W_composed = base[3] + base[0] * 0.5 * kappa_LW
    
    composed = np.clip([L_composed, J_composed, P_composed, W_composed], 0, 1)
    return composed

def find_character_verses(character_names):
    """Search corpus for verses mentioning a character."""
    corpus_root = Path('corpus')
    verses = []
    
    books = ['mark', 'matthew', 'luke', 'john']
    
    for book in books:
        book_dir = corpus_root / book
        if not book_dir.exists():
            continue
            
        for json_file in sorted(book_dir.glob('*.json')):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                chapter_verses = data.get('verses', {})
                coords_map = data.get('ljpw_coordinates', {})
                
                for v_num, text in chapter_verses.items():
                    if any(name.lower() in text.lower() for name in character_names):
                        if v_num in coords_map:
                            verses.append({
                                'ref': f"{data['book']} {data['chapter']}:{v_num}",
                                'text': text.strip(),
                                'coords': np.array(coords_map[v_num])
                            })
            except Exception as e:
                pass
    
    return verses

def calculate_coupling_signature(verses):
    """Calculate detailed coupling signature for a character."""
    if len(verses) == 0:
        return None
    
    # Track evolution through composition
    evolution = []
    
    coupled = verses[0]['coords'].copy()
    evolution.append({
        'step': 0,
        'coords': coupled.copy(),
        'harmony': calculate_harmony(coupled)
    })
    
    for i, verse in enumerate(verses[1:], 1):
        H = calculate_harmony(coupled)
        coupled = coupling_aware_composition(coupled, verse['coords'], H)
        evolution.append({
            'step': i,
            'coords': coupled.copy(),
            'harmony': calculate_harmony(coupled)
        })
    
    # Calculate statistics
    baseline = np.mean([v['coords'] for v in verses], axis=0)
    final_coupled = evolution[-1]['coords']
    
    return {
        'verse_count': len(verses),
        'baseline': baseline,
        'baseline_harmony': calculate_harmony(baseline),
        'final_coupled': final_coupled,
        'final_harmony': evolution[-1]['harmony'],
        'delta_harmony': evolution[-1]['harmony'] - calculate_harmony(baseline),
        'evolution': evolution,
        'harmony_trajectory': [e['harmony'] for e in evolution]
    }

def compare_characters():
    """Compare coupling signatures of different biblical characters."""
    print("=" * 80)
    print("IDENTITY DISCRIMINATION TEST: Can Coupling Distinguish Characters?")
    print("=" * 80)
    
    characters = {
        'Peter': ['peter', 'simon', 'cephas'],
        'John': ['john'],
        'James': ['james'],
        'Andrew': ['andrew'],
        'Philip': ['philip'],
        'Thomas': ['thomas'],
        'Matthew': ['matthew'],
        'Judas': ['judas']
    }
    
    signatures = {}
    
    print("\n" + "=" * 80)
    print("CALCULATING COUPLING SIGNATURES")
    print("=" * 80)
    
    for name, terms in characters.items():
        verses = find_character_verses(terms)
        sig = calculate_coupling_signature(verses)
        
        if sig and sig['verse_count'] >= 5:  # Only include if enough data
            signatures[name] = sig
            print(f"\n{name}: {sig['verse_count']} verses")
            print(f"  Baseline:  L={sig['baseline'][0]:.3f}, J={sig['baseline'][1]:.3f}, "
                  f"P={sig['baseline'][2]:.3f}, W={sig['baseline'][3]:.3f}, H={sig['baseline_harmony']:.3f}")
            print(f"  Coupled:   L={sig['final_coupled'][0]:.3f}, J={sig['final_coupled'][1]:.3f}, "
                  f"P={sig['final_coupled'][2]:.3f}, W={sig['final_coupled'][3]:.3f}, H={sig['final_harmony']:.3f}")
            print(f"  Delta H:   {sig['delta_harmony']:+.3f}")
    
    # Analyze distinguishability
    print("\n" + "=" * 80)
    print("DISTINGUISHABILITY ANALYSIS")
    print("=" * 80)
    
    print("\n1. HARMONY AMPLIFICATION PATTERNS:")
    print("-" * 80)
    
    sorted_by_delta = sorted(signatures.items(), key=lambda x: x[1]['delta_harmony'], reverse=True)
    for name, sig in sorted_by_delta:
        print(f"  {name:15s}: Delta H = {sig['delta_harmony']:+.3f} ({sig['verse_count']:3d} verses)")
    
    # Calculate pairwise distances in coupled space
    print("\n2. PAIRWISE DISTANCES (Coupled Signatures):")
    print("-" * 80)
    
    char_names = list(signatures.keys())
    distances = {}
    
    for i, name1 in enumerate(char_names):
        for name2 in char_names[i+1:]:
            dist = np.linalg.norm(signatures[name1]['final_coupled'] - signatures[name2]['final_coupled'])
            distances[(name1, name2)] = dist
    
    sorted_distances = sorted(distances.items(), key=lambda x: x[1])
    
    print("\nMost Similar Pairs (smallest distance):")
    for (n1, n2), dist in sorted_distances[:5]:
        print(f"  {n1:10s} <-> {n2:10s}: {dist:.3f}")
    
    print("\nMost Different Pairs (largest distance):")
    for (n1, n2), dist in sorted_distances[-5:]:
        print(f"  {n1:10s} <-> {n2:10s}: {dist:.3f}")
    
    # Analyze Love dimension specifically
    print("\n3. LOVE DIMENSION ANALYSIS (Character-Specific):")
    print("-" * 80)
    
    sorted_by_love = sorted(signatures.items(), key=lambda x: x[1]['final_coupled'][0], reverse=True)
    for name, sig in sorted_by_love:
        print(f"  {name:15s}: L = {sig['final_coupled'][0]:.3f}")
    
    # Test: Can we identify a character by their coupling signature?
    print("\n" + "=" * 80)
    print("IDENTITY TEST: Character Recognition")
    print("=" * 80)
    
    print("\nHypothesis: Each character has a unique coupling signature.")
    print("Test: Can we distinguish Peter from John based on coupling alone?")
    
    if 'Peter' in signatures and 'John' in signatures:
        peter = signatures['Peter']
        john = signatures['John']
        
        print(f"\nPeter's Signature:")
        print(f"  Final: L={peter['final_coupled'][0]:.3f}, J={peter['final_coupled'][1]:.3f}, "
              f"P={peter['final_coupled'][2]:.3f}, W={peter['final_coupled'][3]:.3f}")
        print(f"  Delta H: {peter['delta_harmony']:+.3f}")
        
        print(f"\nJohn's Signature:")
        print(f"  Final: L={john['final_coupled'][0]:.3f}, J={john['final_coupled'][1]:.3f}, "
              f"P={john['final_coupled'][2]:.3f}, W={john['final_coupled'][3]:.3f}")
        print(f"  Delta H: {john['delta_harmony']:+.3f}")
        
        distance = np.linalg.norm(peter['final_coupled'] - john['final_coupled'])
        print(f"\nDistance between signatures: {distance:.3f}")
        
        # Key differentiator
        love_diff = abs(peter['final_coupled'][0] - john['final_coupled'][0])
        delta_h_diff = abs(peter['delta_harmony'] - john['delta_harmony'])
        
        print(f"\nKey Differentiators:")
        print(f"  Love difference:    {love_diff:.3f}")
        print(f"  Delta H difference: {delta_h_diff:.3f}")
        
        if love_diff > 0.1 or delta_h_diff > 0.05:
            print("\n[RESULT] Characters are DISTINGUISHABLE by coupling signature!")
        else:
            print("\n[RESULT] Characters are NOT easily distinguishable by coupling alone.")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    compare_characters()
