import sys
import os
import json
import numpy as np
from pathlib import Path

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from experiments.enhanced_pattern_detector import EnhancedPatternDetector

# Coupling Matrix (from LJPW Codex)
COUPLING_MATRIX = np.array([
    [1.0, 1.4, 1.3, 1.5],  # Love → [L, J, P, W]
    [0.9, 1.0, 0.7, 1.2],  # Justice → [L, J, P, W]
    [0.6, 0.8, 1.0, 0.5],  # Power → [L, J, P, W]
    [1.3, 1.1, 1.0, 1.0]   # Wisdom → [L, J, P, W]
])

def calculate_harmony(ljpw_coords):
    """Calculate harmony index (distance from Anchor)."""
    anchor = np.array([1.0, 1.0, 1.0, 1.0])
    distance = np.linalg.norm(ljpw_coords - anchor)
    return 1.0 / (1.0 + distance)

def coupling_aware_composition(coords1, coords2, harmony):
    """
    Compose two LJPW vectors using the coupling matrix.
    
    Args:
        coords1: First LJPW vector [L, J, P, W]
        coords2: Second LJPW vector [L, J, P, W]
        harmony: Harmony index (0-1)
    """
    # Base composition (simple average)
    base = (coords1 + coords2) / 2
    
    # State-dependent coupling coefficients
    kappa_LJ = 1.0 + 0.4 * harmony
    kappa_LP = 1.0 + 0.3 * harmony
    kappa_LW = 1.0 + 0.5 * harmony
    
    # Apply coupling effects
    L_composed = base[0]
    J_composed = base[1] + base[0] * 0.4 * kappa_LJ  # Love → Justice
    P_composed = base[2] + base[0] * 0.3 * kappa_LP  # Love → Power
    W_composed = base[3] + base[0] * 0.5 * kappa_LW  # Love → Wisdom
    
    # Clip to [0, 1]
    composed = np.clip([L_composed, J_composed, P_composed, W_composed], 0, 1)
    
    return composed

def find_peter_verses():
    """Search the corpus for verses mentioning Peter."""
    corpus_root = Path('corpus')
    peter_verses = []
    
    books = ['mark', 'matthew', 'luke', 'john']
    
    for book in books:
        book_dir = corpus_root / book
        if not book_dir.exists():
            continue
            
        for json_file in sorted(book_dir.glob('*.json')):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                verses = data.get('verses', {})
                coords_map = data.get('ljpw_coordinates', {})
                
                for v_num, text in verses.items():
                    # Search for Peter mentions (various forms)
                    if any(name in text.lower() for name in ['peter', 'simon', 'cephas']):
                        if v_num in coords_map:
                            peter_verses.append({
                                'ref': f"{data['book']} {data['chapter']}:{v_num}",
                                'text': text.strip(),
                                'coords': np.array(coords_map[v_num])
                            })
            except Exception as e:
                print(f"Error reading {json_file}: {e}")
    
    return peter_verses

def analyze_peter_with_coupling():
    """Analyze Peter using coupling-aware composition."""
    print("=" * 80)
    print("COUPLING MATRIX TEST: Apostle Peter in Context")
    print("=" * 80)
    
    # Find all Peter verses
    peter_verses = find_peter_verses()
    print(f"\nFound {len(peter_verses)} verses mentioning Peter/Simon/Cephas")
    
    if len(peter_verses) == 0:
        print("No Peter verses found in corpus.")
        return
    
    # Show sample verses
    print("\n" + "-" * 80)
    print("SAMPLE PETER VERSES:")
    print("-" * 80)
    for i, verse in enumerate(peter_verses[:5]):
        print(f"\n{verse['ref']}")
        print(f"  Text: {verse['text'][:70]}...")
        print(f"  LJPW: L={verse['coords'][0]:.3f}, J={verse['coords'][1]:.3f}, "
              f"P={verse['coords'][2]:.3f}, W={verse['coords'][3]:.3f}")
    
    # Calculate average "Peter signature" (baseline)
    print("\n" + "=" * 80)
    print("BASELINE: Simple Average of All Peter Verses")
    print("=" * 80)
    
    all_coords = np.array([v['coords'] for v in peter_verses])
    baseline_peter = np.mean(all_coords, axis=0)
    baseline_harmony = calculate_harmony(baseline_peter)
    
    print(f"\nBaseline Peter Signature:")
    print(f"  L={baseline_peter[0]:.3f}, J={baseline_peter[1]:.3f}, "
          f"P={baseline_peter[2]:.3f}, W={baseline_peter[3]:.3f}")
    print(f"  Harmony: {baseline_harmony:.3f}")
    
    # Calculate coupling-aware "Peter signature"
    print("\n" + "=" * 80)
    print("COUPLING-AWARE: Iterative Composition with Coupling Matrix")
    print("=" * 80)
    
    # Start with first verse
    coupled_peter = peter_verses[0]['coords'].copy()
    
    # Iteratively compose with each subsequent verse using coupling
    for verse in peter_verses[1:]:
        H = calculate_harmony(coupled_peter)
        coupled_peter = coupling_aware_composition(coupled_peter, verse['coords'], H)
    
    coupled_harmony = calculate_harmony(coupled_peter)
    
    print(f"\nCoupling-Aware Peter Signature:")
    print(f"  L={coupled_peter[0]:.3f}, J={coupled_peter[1]:.3f}, "
          f"P={coupled_peter[2]:.3f}, W={coupled_peter[3]:.3f}")
    print(f"  Harmony: {coupled_harmony:.3f}")
    
    # Compare
    print("\n" + "=" * 80)
    print("COMPARISON: Baseline vs. Coupling-Aware")
    print("=" * 80)
    
    delta = coupled_peter - baseline_peter
    print(f"\nDelta_L = {delta[0]:+.3f}")
    print(f"Delta_J = {delta[1]:+.3f}")
    print(f"Delta_P = {delta[2]:+.3f}")
    print(f"Delta_W = {delta[3]:+.3f}")
    print(f"Delta_Harmony = {coupled_harmony - baseline_harmony:+.3f}")
    
    # Interpretation
    print("\n" + "-" * 80)
    print("INTERPRETATION:")
    print("-" * 80)
    
    if delta[0] > 0.05:
        print("[+] Love AMPLIFIED by coupling (L->W effect)")
    if delta[3] > 0.05:
        print("[+] Wisdom AMPLIFIED by coupling (L->W = 1.5)")
    if delta[1] > 0.05:
        print("[+] Justice AMPLIFIED by coupling (L->J = 1.4)")
    if coupled_harmony > baseline_harmony:
        print("[+] Overall Harmony INCREASED through coupling")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    analyze_peter_with_coupling()
