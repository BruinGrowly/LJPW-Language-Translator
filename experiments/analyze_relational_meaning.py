"""
Relational Meaning Analysis
Examines concepts through their relationships in the semantic field
rather than their absolute positions.
"""

import json
import numpy as np
from collections import defaultdict

# Natural Equilibrium
PHI_INV = 1 / ((1 + np.sqrt(5)) / 2)
SQRT2_M1 = np.sqrt(2) - 1
E_M2 = np.e - 2
LN2 = np.log(2)
EQUILIBRIUM = np.array([PHI_INV, SQRT2_M1, E_M2, LN2])
DIMENSION_NAMES = ['Love', 'Justice', 'Power', 'Wisdom']


def load_semantic_space(filepath):
    """Load semantic space."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_concepts_with_names(semantic_space):
    """Extract concepts with their names and coordinates."""
    concepts = []
    for domain_key, domain_data in semantic_space['domains'].items():
        for concept_key, concept_data in domain_data['concepts'].items():
            name = concept_data.get('name', concept_key.replace('_', ' ').title())
            concepts.append({
                'key': concept_key,
                'name': name,
                'definition': concept_data.get('definition', ''),
                'coordinates': np.array(concept_data['coordinates']),
                'domain': domain_data.get('name', domain_key)
            })
    return concepts


def calculate_relational_signature(concept, all_coords):
    """
    Calculate a concept's relational signature:
    - Distance to equilibrium
    - Relationship to dimensional axes
    - Harmonic ratios between dimensions
    """
    coords = concept['coordinates']
    
    # Distance from equilibrium (potential energy)
    eq_distance = np.linalg.norm(coords - EQUILIBRIUM)
    
    # Dimensional relationships (ratios)
    L, J, P, W = coords
    
    # Key ratios
    lj_ratio = L / J if J > 0.01 else 0
    pw_ratio = P / W if W > 0.01 else 0
    lw_ratio = L / W if W > 0.01 else 0
    pj_ratio = P / J if J > 0.01 else 0
    
    # Emergent dimensions (diagonals)
    compassion_wisdom = (L + W) - (J + P)  # Soft vs Hard
    loving_power = (L + P) - (J + W)  # Passionate vs Measured
    
    # Position in field
    # High in multiple dimensions = universal quality
    high_count = sum(1 for c in coords if c > 0.7)
    low_count = sum(1 for c in coords if c < 0.3)
    
    # Harmonic resonance (how close to musical ratios)
    harmonic_score = 0
    if 1.45 < lj_ratio < 1.55:  # Near 3/2 (perfect fifth)
        harmonic_score += 1
    if 0.95 < pw_ratio < 1.05:  # Near 1/1 (unison)
        harmonic_score += 1
    if 1.70 < pj_ratio < 1.80:  # Near √3
        harmonic_score += 1
    
    return {
        'eq_distance': eq_distance,
        'lj_ratio': lj_ratio,
        'pw_ratio': pw_ratio,
        'lw_ratio': lw_ratio,
        'pj_ratio': pj_ratio,
        'compassion_wisdom': compassion_wisdom,
        'loving_power': loving_power,
        'high_count': high_count,
        'low_count': low_count,
        'harmonic_score': harmonic_score
    }


def find_semantic_neighbors(concept, all_concepts, n=5):
    """Find nearest semantic neighbors."""
    distances = []
    for other in all_concepts:
        if other['key'] == concept['key']:
            continue
        dist = np.linalg.norm(concept['coordinates'] - other['coordinates'])
        distances.append((dist, other))
    
    distances.sort(key=lambda x: x[0])
    return distances[:n]


def analyze_meaning_through_relationships(concept, all_concepts, all_coords):
    """Analyze what a concept MEANS through its relationships."""
    sig = calculate_relational_signature(concept, all_coords)
    neighbors = find_semantic_neighbors(concept, all_concepts, n=5)
    
    # Interpret meaning from relationships
    meaning_profile = {
        'name': concept['name'],
        'coordinates': concept['coordinates'].tolist(),
        'relational_meaning': []
    }
    
    # 1. Equilibrium relationship
    if sig['eq_distance'] < 0.1:
        meaning_profile['relational_meaning'].append(
            f"BALANCED: Near equilibrium - represents harmony across all dimensions"
        )
    elif sig['eq_distance'] > 0.4:
        meaning_profile['relational_meaning'].append(
            f"EXTREME: Far from equilibrium - represents strong polarity"
        )
    
    # 2. Dimensional relationships
    if sig['high_count'] >= 3:
        meaning_profile['relational_meaning'].append(
            f"UNIVERSAL: High in {sig['high_count']} dimensions - transcendent quality"
        )
    elif sig['low_count'] >= 2:
        meaning_profile['relational_meaning'].append(
            f"MINIMAL: Low in {sig['low_count']} dimensions - represents absence/lack"
        )
    
    # 3. Emergent dimension interpretation
    if sig['compassion_wisdom'] > 0.2:
        meaning_profile['relational_meaning'].append(
            f"SOFT: Compassion-Wisdom dominant - gentle, understanding quality"
        )
    elif sig['compassion_wisdom'] < -0.2:
        meaning_profile['relational_meaning'].append(
            f"HARD: Justice-Power dominant - firm, structured quality"
        )
    
    if sig['loving_power'] > 0.2:
        meaning_profile['relational_meaning'].append(
            f"PASSIONATE: Love-Power dominant - dynamic, expressive quality"
        )
    elif sig['loving_power'] < -0.2:
        meaning_profile['relational_meaning'].append(
            f"MEASURED: Justice-Wisdom dominant - thoughtful, deliberate quality"
        )
    
    # 4. Harmonic resonance
    if sig['harmonic_score'] >= 2:
        meaning_profile['relational_meaning'].append(
            f"HARMONIC: Resonates at musical ratios - naturally coherent"
        )
    
    # 5. Semantic neighborhood
    neighbor_names = [n[1]['name'] for n in neighbors]
    meaning_profile['semantic_neighborhood'] = neighbor_names
    meaning_profile['relational_meaning'].append(
        f"CONTEXT: Exists in semantic field with {', '.join(neighbor_names[:3])}"
    )
    
    return meaning_profile


def main():
    """Analyze meaning through relationships."""
    print("="*70)
    print("RELATIONAL MEANING ANALYSIS")
    print("Viewing concepts as nodes in a meaning field")
    print("="*70)
    
    # Load semantic space
    semantic_space = load_semantic_space("experiments/semantic_space_6353_VALIDATED.json")
    concepts = extract_concepts_with_names(semantic_space)
    all_coords = np.array([c['coordinates'] for c in concepts])
    
    print(f"\nAnalyzing {len(concepts):,} concepts through relational lens...\n")
    
    # Analyze key concepts
    key_concept_names = [
        'Love', 'Justice', 'Power', 'Wisdom',  # The dimensions themselves
        'Equilibrium', 'Balance', 'Harmony',  # Near equilibrium
        'Chaos', 'Ignorance',  # Low extremes
        'Consciousness', 'Compassion', 'Truth'  # High-weight concepts
    ]
    
    analyses = []
    
    for concept in concepts:
        if concept['name'] in key_concept_names:
            analysis = analyze_meaning_through_relationships(concept, concepts, all_coords)
            analyses.append(analysis)
    
    # Display results
    for analysis in analyses:
        print(f"\n{'='*70}")
        print(f"CONCEPT: {analysis['name']}")
        print(f"Coordinates: L={analysis['coordinates'][0]:.3f}, J={analysis['coordinates'][1]:.3f}, "
              f"P={analysis['coordinates'][2]:.3f}, W={analysis['coordinates'][3]:.3f}")
        print(f"\nRELATIONAL MEANING:")
        for meaning in analysis['relational_meaning']:
            print(f"  • {meaning}")
        print(f"\nSEMANTIC NEIGHBORHOOD:")
        print(f"  Closest concepts: {', '.join(analysis['semantic_neighborhood'])}")
    
    # Find interesting relational patterns
    print(f"\n\n{'='*70}")
    print("RELATIONAL PATTERNS DISCOVERED")
    print(f"{'='*70}\n")
    
    # Find concepts with high harmonic resonance
    harmonic_concepts = []
    for concept in concepts:
        sig = calculate_relational_signature(concept, all_coords)
        if sig['harmonic_score'] >= 2:
            harmonic_concepts.append((concept['name'], sig['harmonic_score']))
    
    print(f"Harmonically Resonant Concepts ({len(harmonic_concepts)} found):")
    harmonic_concepts.sort(key=lambda x: x[1], reverse=True)
    for name, score in harmonic_concepts[:10]:
        print(f"  • {name} (harmonic score: {score})")
    
    # Find concepts at emergent dimension extremes
    print(f"\nEmergent Dimension Extremes:")
    
    soft_concepts = []
    hard_concepts = []
    for concept in concepts:
        sig = calculate_relational_signature(concept, all_coords)
        if sig['compassion_wisdom'] > 0.3:
            soft_concepts.append((concept['name'], sig['compassion_wisdom']))
        elif sig['compassion_wisdom'] < -0.3:
            hard_concepts.append((concept['name'], sig['compassion_wisdom']))
    
    print(f"\n  Softest (Compassion-Wisdom dominant):")
    soft_concepts.sort(key=lambda x: x[1], reverse=True)
    for name, score in soft_concepts[:5]:
        print(f"    • {name} ({score:.3f})")
    
    print(f"\n  Hardest (Justice-Power dominant):")
    hard_concepts.sort(key=lambda x: x[1])
    for name, score in hard_concepts[:5]:
        print(f"    • {name} ({score:.3f})")
    
    print(f"\n{'='*70}")
    print("INSIGHT: Meaning emerges from relationships, not positions")
    print("="*70)


if __name__ == "__main__":
    main()
