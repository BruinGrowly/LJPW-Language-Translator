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

def analyze_character_coupling(character_name, search_terms):
    """Analyze a character using coupling-aware composition."""
    verses = find_character_verses(search_terms)
    
    if len(verses) == 0:
        return None
    
    # Baseline (simple average)
    all_coords = np.array([v['coords'] for v in verses])
    baseline = np.mean(all_coords, axis=0)
    baseline_harmony = calculate_harmony(baseline)
    
    # Coupling-aware composition
    coupled = verses[0]['coords'].copy()
    for verse in verses[1:]:
        H = calculate_harmony(coupled)
        coupled = coupling_aware_composition(coupled, verse['coords'], H)
    
    coupled_harmony = calculate_harmony(coupled)
    
    return {
        'name': character_name,
        'verse_count': len(verses),
        'baseline': baseline,
        'baseline_harmony': baseline_harmony,
        'coupled': coupled,
        'coupled_harmony': coupled_harmony,
        'delta': coupled - baseline,
        'delta_harmony': coupled_harmony - baseline_harmony
    }

def analyze_fictional_character(character_name, descriptions):
    """Analyze a fictional character using text descriptions."""
    detector = EnhancedPatternDetector()
    
    coords_list = []
    for desc in descriptions:
        result = detector.calculate_field_signature_v2(desc)
        coords_list.append(np.array([result['L'], result['J'], result['P'], result['W']]))
    
    # Baseline
    baseline = np.mean(coords_list, axis=0)
    baseline_harmony = calculate_harmony(baseline)
    
    # Coupling-aware
    coupled = coords_list[0].copy()
    for coords in coords_list[1:]:
        H = calculate_harmony(coupled)
        coupled = coupling_aware_composition(coupled, coords, H)
    
    coupled_harmony = calculate_harmony(coupled)
    
    return {
        'name': character_name,
        'verse_count': len(descriptions),
        'baseline': baseline,
        'baseline_harmony': baseline_harmony,
        'coupled': coupled,
        'coupled_harmony': coupled_harmony,
        'delta': coupled - baseline,
        'delta_harmony': coupled_harmony - baseline_harmony
    }

def main():
    print("=" * 80)
    print("COUPLING MATRIX TEST: Multiple Characters (Bible, Fiction, Reality)")
    print("=" * 80)
    
    results = []
    
    # BIBLICAL CHARACTERS
    print("\n" + "=" * 80)
    print("BIBLICAL CHARACTERS (from Gospel corpus)")
    print("=" * 80)
    
    biblical_chars = [
        ("Peter", ["peter", "simon", "cephas"]),
        ("John", ["john"]),
        ("Jesus", ["jesus", "christ", "lord"]),
        ("Mary", ["mary"]),
        ("Judas", ["judas"])
    ]
    
    for name, terms in biblical_chars:
        result = analyze_character_coupling(name, terms)
        if result:
            results.append(result)
            print(f"\n{name}: {result['verse_count']} verses")
            print(f"  Baseline:  L={result['baseline'][0]:.3f}, J={result['baseline'][1]:.3f}, "
                  f"P={result['baseline'][2]:.3f}, W={result['baseline'][3]:.3f}, H={result['baseline_harmony']:.3f}")
            print(f"  Coupled:   L={result['coupled'][0]:.3f}, J={result['coupled'][1]:.3f}, "
                  f"P={result['coupled'][2]:.3f}, W={result['coupled'][3]:.3f}, H={result['coupled_harmony']:.3f}")
            print(f"  Delta H:   {result['delta_harmony']:+.3f}")
    
    # FICTIONAL CHARACTERS
    print("\n" + "=" * 80)
    print("FICTIONAL CHARACTERS (from descriptions)")
    print("=" * 80)
    
    fictional_chars = [
        ("Sherlock Holmes", [
            "Sherlock Holmes, the brilliant detective",
            "Holmes solved the mystery with logic and deduction",
            "The detective observed every detail with keen wisdom",
            "Holmes was cold and calculating, driven by justice"
        ]),
        ("Harry Potter", [
            "Harry Potter, the boy who lived",
            "Harry fought bravely against dark forces",
            "The young wizard showed great courage and love for his friends",
            "Harry sacrificed himself to save others"
        ]),
        ("Darth Vader", [
            "Darth Vader, the dark lord of the Sith",
            "Vader ruled with an iron fist and terrible power",
            "The Sith lord was consumed by anger and hatred",
            "Vader ultimately chose redemption through love for his son"
        ])
    ]
    
    for name, descriptions in fictional_chars:
        result = analyze_fictional_character(name, descriptions)
        results.append(result)
        print(f"\n{name}: {result['verse_count']} descriptions")
        print(f"  Baseline:  L={result['baseline'][0]:.3f}, J={result['baseline'][1]:.3f}, "
              f"P={result['baseline'][2]:.3f}, W={result['baseline'][3]:.3f}, H={result['baseline_harmony']:.3f}")
        print(f"  Coupled:   L={result['coupled'][0]:.3f}, J={result['coupled'][1]:.3f}, "
              f"P={result['coupled'][2]:.3f}, W={result['coupled'][3]:.3f}, H={result['coupled_harmony']:.3f}")
        print(f"  Delta H:   {result['delta_harmony']:+.3f}")
    
    # REAL PEOPLE
    print("\n" + "=" * 80)
    print("REAL PEOPLE (from descriptions)")
    print("=" * 80)
    
    real_people = [
        ("Martin Luther King Jr.", [
            "Martin Luther King Jr. fought for civil rights with nonviolent resistance",
            "King preached love and justice for all people",
            "The civil rights leader inspired millions with his wisdom and compassion",
            "King gave his life for the cause of equality"
        ]),
        ("Albert Einstein", [
            "Albert Einstein revolutionized physics with his theories",
            "Einstein was driven by curiosity and a love of knowledge",
            "The physicist sought to understand the fundamental laws of the universe",
            "Einstein was humble despite his great wisdom and achievements"
        ]),
        ("Napoleon Bonaparte", [
            "Napoleon Bonaparte conquered much of Europe through military genius",
            "Napoleon ruled France with absolute power and authority",
            "The emperor reformed laws and brought order to chaos",
            "Napoleon's ambition ultimately led to his downfall"
        ])
    ]
    
    for name, descriptions in real_people:
        result = analyze_fictional_character(name, descriptions)
        results.append(result)
        print(f"\n{name}: {result['verse_count']} descriptions")
        print(f"  Baseline:  L={result['baseline'][0]:.3f}, J={result['baseline'][1]:.3f}, "
              f"P={result['baseline'][2]:.3f}, W={result['baseline'][3]:.3f}, H={result['baseline_harmony']:.3f}")
        print(f"  Coupled:   L={result['coupled'][0]:.3f}, J={result['coupled'][1]:.3f}, "
              f"P={result['coupled'][2]:.3f}, W={result['coupled'][3]:.3f}, H={result['coupled_harmony']:.3f}")
        print(f"  Delta H:   {result['delta_harmony']:+.3f}")
    
    # SUMMARY
    print("\n" + "=" * 80)
    print("SUMMARY: Harmony Amplification Ranking")
    print("=" * 80)
    
    ranked = sorted(results, key=lambda x: x['delta_harmony'], reverse=True)
    print("\nRank | Character              | Delta H | Coupled H | Interpretation")
    print("-" * 80)
    for i, r in enumerate(ranked, 1):
        interpretation = ""
        if r['delta_harmony'] > 0.2:
            interpretation = "HIGH coherence"
        elif r['delta_harmony'] > 0.1:
            interpretation = "MODERATE coherence"
        elif r['delta_harmony'] > 0:
            interpretation = "LOW coherence"
        else:
            interpretation = "INCOHERENT"
        
        print(f"{i:2d}   | {r['name']:22s} | {r['delta_harmony']:+.3f}  | {r['coupled_harmony']:.3f}     | {interpretation}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
