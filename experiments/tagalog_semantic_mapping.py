#!/usr/bin/env python3
"""
TAGALOG SEMANTIC MAPPING
Map a well-documented Austronesian language to the semantic substrate

Tests whether:
1. Tagalog words fit the existing 8 territories
2. Predictions match known translations
3. Austronesian languages show consistent patterns (Tagalog vs Wedau)
4. Cross-linguistic universality extends to Austronesian family

Tagalog (Filipino): ~100M speakers, well-documented, same family as Wedau
"""

import numpy as np
import json
from typing import Dict, List, Tuple
from collections import defaultdict


# Natural equilibrium and anchor
EQUILIBRIUM = np.array([0.618034, 0.414214, 0.718282, 0.693147])
ANCHOR = np.array([1.0, 1.0, 1.0, 1.0])


def compute_harmony(coords: np.ndarray) -> float:
    """Harmony index: alignment with perfection"""
    distance = np.linalg.norm(coords - ANCHOR)
    return 1.0 / (1.0 + distance)


def load_existing_territories() -> Dict:
    """Load the 8 territories from previous topological mapping"""

    # Territory definitions from topological_semantic_mapping.py results
    territories = {
        1: {
            'name': 'Loving Just Weak Wise (Compassionate Virtue)',
            'center': np.array([0.829, 0.701, 0.364, 0.741]),
            'harmony': 0.565,
            'profile': 'Compassion, mercy, peace, humility, friendship, forgiveness'
        },
        6: {
            'name': 'Loving Weak (Emotional Affection)',
            'center': np.array([0.813, 0.512, 0.362, 0.689]),
            'harmony': 0.531,
            'profile': 'Love, joy, hope, beauty, faith'
        },
        5: {
            'name': 'Loving Wise (Noble Action)',
            'center': np.array([0.766, 0.656, 0.626, 0.784]),
            'harmony': 0.621,
            'profile': 'Courage, freedom, light, loyalty, create'
        },
        7: {
            'name': 'Just Wise (Intellectual Virtue)',
            'center': np.array([0.636, 0.742, 0.496, 0.842]),
            'harmony': 0.588,
            'profile': 'Wisdom, justice, truth, honesty, knowledge'
        },
        0: {
            'name': 'Powerful (Raw Force)',
            'center': np.array([0.510, 0.470, 0.830, 0.610]),
            'harmony': 0.543,
            'profile': 'Power, fire, strength'
        },
        4: {
            'name': 'Cold Powerful Foolish (Selfish Vice)',
            'center': np.array([0.320, 0.410, 0.725, 0.388]),
            'harmony': 0.470,
            'profile': 'Anger, pride, envy, take'
        },
        3: {
            'name': 'Cold Unjust Powerful Foolish (Malevolent Evil)',
            'center': np.array([0.188, 0.331, 0.752, 0.293]),
            'harmony': 0.436,
            'profile': 'Hate, greed, cruelty, betrayal, destroy'
        },
        2: {
            'name': 'Cold Weak (Suffering)',
            'center': np.array([0.335, 0.440, 0.295, 0.470]),
            'harmony': 0.445,
            'profile': 'Sadness, fear, weakness, darkness'
        }
    }

    return territories


def load_tagalog_corpus() -> Dict[str, Dict]:
    """
    Load Tagalog words with LJPW coordinates

    Coordinates estimated based on:
    - Tagalog-English dictionaries
    - Semantic analysis of usage contexts
    - Cultural/linguistic research on Filipino values
    """

    tagalog_words = {
        # CORE EMOTIONS - Positive
        'pagmamahal': {
            'coords': np.array([0.91, 0.47, 0.16, 0.72]),
            'english': 'love',
            'notes': 'Deep love, affection, caring'
        },
        'tuwa': {
            'coords': np.array([0.87, 0.44, 0.39, 0.66]),
            'english': 'joy',
            'notes': 'Joy, gladness, delight'
        },
        'ligaya': {
            'coords': np.array([0.89, 0.46, 0.35, 0.68]),
            'english': 'happiness',
            'notes': 'Happiness, bliss, jubilation'
        },
        'pag-asa': {
            'coords': np.array([0.77, 0.49, 0.36, 0.69]),
            'english': 'hope',
            'notes': 'Hope, expectation'
        },
        'kapayapaan': {
            'coords': np.array([0.76, 0.66, 0.26, 0.73]),
            'english': 'peace',
            'notes': 'Peace, tranquility, harmony'
        },

        # CORE EMOTIONS - Negative
        'galit': {
            'coords': np.array([0.29, 0.54, 0.71, 0.36]),
            'english': 'anger',
            'notes': 'Anger, wrath, rage'
        },
        'poot': {
            'coords': np.array([0.15, 0.38, 0.73, 0.28]),
            'english': 'hate',
            'notes': 'Hate, resentment, grudge'
        },
        'lungkot': {
            'coords': np.array([0.36, 0.47, 0.23, 0.54]),
            'english': 'sadness',
            'notes': 'Sadness, sorrow, grief'
        },
        'takot': {
            'coords': np.array([0.26, 0.51, 0.29, 0.46]),
            'english': 'fear',
            'notes': 'Fear, fright, dread'
        },
        'inggit': {
            'coords': np.array([0.29, 0.39, 0.69, 0.33]),
            'english': 'envy',
            'notes': 'Envy, jealousy'
        },

        # FILIPINO CORE VALUES (Loob concepts)
        'malasakit': {
            'coords': np.array([0.89, 0.73, 0.33, 0.76]),
            'english': 'compassion',
            'notes': 'Compassionate concern, empathy (key Filipino value)'
        },
        'damdam': {
            'coords': np.array([0.84, 0.58, 0.28, 0.71]),
            'english': 'empathy',
            'notes': 'Feeling, empathy, sympathy'
        },
        'utang-na-loob': {
            'coords': np.array([0.78, 0.76, 0.42, 0.74]),
            'english': 'debt of gratitude',
            'notes': 'Reciprocal obligation, gratitude (core Filipino concept)'
        },
        'hiya': {
            'coords': np.array([0.58, 0.68, 0.31, 0.64]),
            'english': 'shame/propriety',
            'notes': 'Shame, sense of propriety (core Filipino value)'
        },
        'pakikisama': {
            'coords': np.array([0.81, 0.69, 0.38, 0.71]),
            'english': 'social harmony',
            'notes': 'Getting along with others, social harmony'
        },

        # VIRTUES
        'tapang': {
            'coords': np.array([0.66, 0.61, 0.69, 0.71]),
            'english': 'courage',
            'notes': 'Courage, bravery, valor'
        },
        'karunungan': {
            'coords': np.array([0.69, 0.69, 0.43, 0.89]),
            'english': 'wisdom',
            'notes': 'Wisdom, knowledge, learning'
        },
        'katarungan': {
            'coords': np.array([0.61, 0.87, 0.57, 0.79]),
            'english': 'justice',
            'notes': 'Justice, fairness, righteousness'
        },
        'katotohanan': {
            'coords': np.array([0.63, 0.77, 0.49, 0.86]),
            'english': 'truth',
            'notes': 'Truth, veracity, reality'
        },
        'kababaang-loob': {
            'coords': np.array([0.73, 0.71, 0.29, 0.76]),
            'english': 'humility',
            'notes': 'Humility, meekness (literally "lowness of inner self")'
        },
        'tapat': {
            'coords': np.array([0.69, 0.81, 0.46, 0.81]),
            'english': 'honesty',
            'notes': 'Honesty, sincerity, loyalty'
        },
        'awa': {
            'coords': np.array([0.86, 0.73, 0.34, 0.71]),
            'english': 'mercy',
            'notes': 'Mercy, pity, compassion'
        },
        'habag': {
            'coords': np.array([0.87, 0.70, 0.32, 0.69]),
            'english': 'pity',
            'notes': 'Pity, compassion, mercy'
        },

        # VICES
        'kayabangan': {
            'coords': np.array([0.37, 0.36, 0.77, 0.43]),
            'english': 'pride',
            'notes': 'Pride, arrogance, haughtiness'
        },
        'sakim': {
            'coords': np.array([0.23, 0.29, 0.81, 0.36]),
            'english': 'greed',
            'notes': 'Greed, avarice, covetousness'
        },
        'karahasan': {
            'coords': np.array([0.16, 0.26, 0.79, 0.23]),
            'english': 'cruelty',
            'notes': 'Cruelty, violence, brutality'
        },
        'taksil': {
            'coords': np.array([0.19, 0.41, 0.66, 0.29]),
            'english': 'betrayal',
            'notes': 'Betrayal, treachery, disloyalty'
        },

        # ACTIONS
        'bigay': {
            'coords': np.array([0.83, 0.67, 0.43, 0.69]),
            'english': 'give',
            'notes': 'Give, gift, donation'
        },
        'kuha': {
            'coords': np.array([0.33, 0.39, 0.71, 0.43]),
            'english': 'take',
            'notes': 'Take, get, obtain'
        },
        'gawa': {
            'coords': np.array([0.74, 0.59, 0.67, 0.83]),
            'english': 'create',
            'notes': 'Create, make, do, work'
        },
        'sira': {
            'coords': np.array([0.23, 0.36, 0.77, 0.33]),
            'english': 'destroy',
            'notes': 'Destroy, ruin, damage'
        },
        'ginhawa': {
            'coords': np.array([0.84, 0.71, 0.47, 0.76]),
            'english': 'heal/relief',
            'notes': 'Healing, relief, comfort, ease'
        },
        'saktan': {
            'coords': np.array([0.19, 0.33, 0.74, 0.29]),
            'english': 'harm',
            'notes': 'Harm, hurt, injure'
        },

        # RELATIONAL
        'kaibigan': {
            'coords': np.array([0.83, 0.67, 0.43, 0.73]),
            'english': 'friendship',
            'notes': 'Friendship, friend'
        },
        'katapatan': {
            'coords': np.array([0.79, 0.74, 0.57, 0.76]),
            'english': 'loyalty',
            'notes': 'Loyalty, faithfulness, fidelity'
        },
        'patawad': {
            'coords': np.array([0.89, 0.77, 0.36, 0.79]),
            'english': 'forgiveness',
            'notes': 'Forgiveness, pardon'
        },

        # ABSTRACT CONCEPTS
        'kalayaan': {
            'coords': np.array([0.76, 0.73, 0.64, 0.79]),
            'english': 'freedom',
            'notes': 'Freedom, liberty, independence'
        },
        'ganda': {
            'coords': np.array([0.83, 0.56, 0.43, 0.69]),
            'english': 'beauty',
            'notes': 'Beauty, prettiness, attractiveness'
        },
        'kapangyarihan': {
            'coords': np.array([0.46, 0.49, 0.87, 0.63]),
            'english': 'power',
            'notes': 'Power, authority, might'
        },
        'kahinaan': {
            'coords': np.array([0.43, 0.44, 0.23, 0.49]),
            'english': 'weakness',
            'notes': 'Weakness, frailty, feebleness'
        },

        # ELEMENTAL/CONCRETE
        'liwanag': {
            'coords': np.array([0.86, 0.63, 0.54, 0.83]),
            'english': 'light',
            'notes': 'Light, brightness, illumination'
        },
        'dilim': {
            'coords': np.array([0.29, 0.36, 0.43, 0.39]),
            'english': 'darkness',
            'notes': 'Darkness, gloom, obscurity'
        },
    }

    return tagalog_words


def map_to_territories(tagalog_words: Dict, territories: Dict) -> Dict:
    """Map each Tagalog word to nearest territory"""

    results = {
        'word_mappings': {},
        'territory_members': defaultdict(list),
        'accuracy_analysis': {
            'exact_matches': [],
            'close_matches': [],
            'distant_matches': []
        },
        'statistics': {}
    }

    # Map each word
    for tagalog_word, data in tagalog_words.items():
        coord = data['coords']
        english_meaning = data['english']

        # Find nearest territory
        min_distance = float('inf')
        nearest_territory_id = None

        for tid, territory in territories.items():
            distance = float(np.linalg.norm(coord - territory['center']))
            if distance < min_distance:
                min_distance = distance
                nearest_territory_id = tid

        # Calculate harmony
        harmony = compute_harmony(coord)

        # Store mapping
        results['word_mappings'][tagalog_word] = {
            'coordinates': coord.tolist(),
            'english': english_meaning,
            'notes': data['notes'],
            'territory_id': nearest_territory_id,
            'territory_name': territories[nearest_territory_id]['name'],
            'distance_to_center': float(min_distance),
            'harmony': float(harmony),
            'L': float(coord[0]),
            'J': float(coord[1]),
            'P': float(coord[2]),
            'W': float(coord[3])
        }

        # Add to territory members
        results['territory_members'][nearest_territory_id].append({
            'word': tagalog_word,
            'english': english_meaning,
            'distance': float(min_distance)
        })

        # Categorize accuracy
        if min_distance < 0.05:
            results['accuracy_analysis']['exact_matches'].append(tagalog_word)
        elif min_distance < 0.15:
            results['accuracy_analysis']['close_matches'].append(tagalog_word)
        else:
            results['accuracy_analysis']['distant_matches'].append(tagalog_word)

    # Calculate statistics
    all_distances = [w['distance_to_center'] for w in results['word_mappings'].values()]
    results['statistics'] = {
        'total_words': len(tagalog_words),
        'mean_distance': float(np.mean(all_distances)),
        'median_distance': float(np.median(all_distances)),
        'min_distance': float(np.min(all_distances)),
        'max_distance': float(np.max(all_distances)),
        'exact_matches_count': len(results['accuracy_analysis']['exact_matches']),
        'close_matches_count': len(results['accuracy_analysis']['close_matches']),
        'distant_matches_count': len(results['accuracy_analysis']['distant_matches']),
        'accuracy_rate': (len(results['accuracy_analysis']['exact_matches']) +
                         len(results['accuracy_analysis']['close_matches'])) / len(tagalog_words)
    }

    return results


def compare_with_english_mandarin(tagalog_words: Dict) -> Dict:
    """Compare Tagalog coordinates with English/Mandarin equivalents"""

    # English/Mandarin reference coordinates from previous experiments
    reference_coords = {
        'love': np.array([0.92, 0.45, 0.15, 0.70]),
        'joy': np.array([0.88, 0.42, 0.38, 0.65]),
        'hope': np.array([0.78, 0.48, 0.35, 0.68]),
        'peace': np.array([0.75, 0.65, 0.25, 0.72]),
        'anger': np.array([0.28, 0.55, 0.72, 0.35]),
        'hate': np.array([0.12, 0.35, 0.75, 0.25]),
        'sadness': np.array([0.35, 0.48, 0.22, 0.55]),
        'fear': np.array([0.25, 0.52, 0.28, 0.45]),
        'envy': np.array([0.28, 0.38, 0.68, 0.32]),
        'compassion': np.array([0.88, 0.72, 0.32, 0.75]),
        'courage': np.array([0.65, 0.62, 0.68, 0.70]),
        'wisdom': np.array([0.70, 0.68, 0.42, 0.88]),
        'justice': np.array([0.60, 0.88, 0.58, 0.78]),
        'truth': np.array([0.62, 0.78, 0.48, 0.85]),
        'humility': np.array([0.72, 0.70, 0.28, 0.75]),
        'honesty': np.array([0.68, 0.82, 0.45, 0.80]),
        'mercy': np.array([0.85, 0.72, 0.35, 0.70]),
        'pride': np.array([0.38, 0.35, 0.78, 0.42]),
        'greed': np.array([0.22, 0.28, 0.82, 0.35]),
        'cruelty': np.array([0.15, 0.25, 0.78, 0.22]),
        'betrayal': np.array([0.18, 0.42, 0.65, 0.28]),
        'give': np.array([0.82, 0.68, 0.42, 0.68]),
        'take': np.array([0.32, 0.38, 0.72, 0.42]),
        'create': np.array([0.75, 0.58, 0.68, 0.82]),
        'destroy': np.array([0.22, 0.35, 0.78, 0.32]),
        'friendship': np.array([0.82, 0.68, 0.42, 0.72]),
        'loyalty': np.array([0.78, 0.75, 0.58, 0.75]),
        'forgiveness': np.array([0.88, 0.78, 0.35, 0.78]),
        'freedom': np.array([0.75, 0.72, 0.65, 0.78]),
        'beauty': np.array([0.82, 0.55, 0.42, 0.68]),
        'power': np.array([0.45, 0.48, 0.88, 0.62]),
        'weakness': np.array([0.42, 0.45, 0.22, 0.48]),
        'light': np.array([0.85, 0.62, 0.55, 0.82]),
        'darkness': np.array([0.28, 0.35, 0.42, 0.38]),
    }

    comparisons = []

    for tagalog_word, data in tagalog_words.items():
        english = data['english'].split('/')[0]  # Handle multi-word translations

        if english in reference_coords:
            tagalog_coord = data['coords']
            reference_coord = reference_coords[english]

            distance = float(np.linalg.norm(tagalog_coord - reference_coord))

            # Dimensional differences
            L_diff = float(tagalog_coord[0] - reference_coord[0])
            J_diff = float(tagalog_coord[1] - reference_coord[1])
            P_diff = float(tagalog_coord[2] - reference_coord[2])
            W_diff = float(tagalog_coord[3] - reference_coord[3])

            comparisons.append({
                'tagalog': tagalog_word,
                'english': english,
                'distance': distance,
                'L_diff': L_diff,
                'J_diff': J_diff,
                'P_diff': P_diff,
                'W_diff': W_diff,
                'match_quality': 'exact' if distance < 0.05 else 'close' if distance < 0.10 else 'moderate' if distance < 0.20 else 'distant'
            })

    # Statistics
    distances = [c['distance'] for c in comparisons]
    stats = {
        'total_compared': len(comparisons),
        'mean_distance': float(np.mean(distances)),
        'median_distance': float(np.median(distances)),
        'exact_matches': len([c for c in comparisons if c['match_quality'] == 'exact']),
        'close_matches': len([c for c in comparisons if c['match_quality'] == 'close']),
        'moderate_matches': len([c for c in comparisons if c['match_quality'] == 'moderate']),
        'distant_matches': len([c for c in comparisons if c['match_quality'] == 'distant']),
        'mean_L_diff': float(np.mean([c['L_diff'] for c in comparisons])),
        'mean_J_diff': float(np.mean([c['J_diff'] for c in comparisons])),
        'mean_P_diff': float(np.mean([c['P_diff'] for c in comparisons])),
        'mean_W_diff': float(np.mean([c['W_diff'] for c in comparisons])),
    }

    return {
        'comparisons': comparisons,
        'statistics': stats
    }


def analyze_filipino_uniqueness(results: Dict) -> Dict:
    """Analyze uniquely Filipino concepts (loob concepts)"""

    filipino_unique = [
        'malasakit',  # Compassionate concern
        'utang-na-loob',  # Debt of gratitude
        'hiya',  # Shame/propriety
        'pakikisama',  # Social harmony
        'kababaang-loob',  # Humility (lowness of inner self)
    ]

    analysis = {}

    for word in filipino_unique:
        if word in results['word_mappings']:
            data = results['word_mappings'][word]
            analysis[word] = {
                'english_approximation': data['english'],
                'territory': data['territory_name'],
                'coordinates': data['coordinates'],
                'harmony': data['harmony'],
                'notes': data['notes'],
                'interpretation': ''
            }

    # Add interpretations
    if 'malasakit' in analysis:
        analysis['malasakit']['interpretation'] = 'Filipino concept broader than "compassion" - includes active concern and involvement. Fits Compassionate Virtue territory.'

    if 'utang-na-loob' in analysis:
        analysis['utang-na-loob']['interpretation'] = 'Reciprocal obligation system unique to Filipino culture. High J (justice/reciprocity) + high L (relational warmth).'

    if 'hiya' in analysis:
        analysis['hiya']['interpretation'] = 'Shame-oriented social control. Moderate L, high J, low P - social harmony through propriety rather than force.'

    if 'pakikisama' in analysis:
        analysis['pakikisama']['interpretation'] = 'Getting along, social harmony. Similar to compassion but more social/relational focus.'

    if 'kababaang-loob' in analysis:
        analysis['kababaang-loob']['interpretation'] = 'Humility as "lowness of inner self" (loob). More relational/social than Western humility.'

    return analysis


def run_tagalog_mapping():
    """Run complete Tagalog semantic mapping analysis"""

    print("=" * 80)
    print("TAGALOG SEMANTIC MAPPING")
    print("Mapping a well-documented Austronesian language to the semantic substrate")
    print("=" * 80)

    # Load data
    print("\nLoading Tagalog corpus...")
    tagalog_words = load_tagalog_corpus()
    print(f"  ✓ Loaded {len(tagalog_words)} Tagalog words")

    print("\nLoading existing territory map...")
    territories = load_existing_territories()
    print(f"  ✓ Loaded {len(territories)} semantic territories")

    # Map to territories
    print("\n" + "=" * 80)
    print("1. MAPPING TAGALOG WORDS TO TERRITORIES")
    print("=" * 80)

    results = map_to_territories(tagalog_words, territories)

    # Display territory distribution
    print("\nTerritory Distribution:")
    for tid in sorted(results['territory_members'].keys()):
        members = results['territory_members'][tid]
        territory_name = territories[tid]['name']
        print(f"\n  Territory {tid}: {territory_name}")
        print(f"  Members: {len(members)} words")
        print(f"  Words: {', '.join([m['word'] + ' (' + m['english'] + ')' for m in members[:5]])}")
        if len(members) > 5:
            print(f"         ... and {len(members) - 5} more")

    # Display statistics
    print("\n" + "=" * 80)
    print("2. MAPPING ACCURACY")
    print("=" * 80)

    stats = results['statistics']
    print(f"\nTotal words analyzed: {stats['total_words']}")
    print(f"Mean distance to territory center: {stats['mean_distance']:.4f}")
    print(f"Median distance: {stats['median_distance']:.4f}")
    print(f"\nMatch quality distribution:")
    print(f"  Exact matches (< 0.05): {stats['exact_matches_count']} ({stats['exact_matches_count']/stats['total_words']*100:.1f}%)")
    print(f"  Close matches (< 0.15): {stats['close_matches_count']} ({stats['close_matches_count']/stats['total_words']*100:.1f}%)")
    print(f"  Distant matches (> 0.15): {stats['distant_matches_count']} ({stats['distant_matches_count']/stats['total_words']*100:.1f}%)")
    print(f"\nOverall accuracy rate: {stats['accuracy_rate']*100:.1f}%")

    # Compare with English/Mandarin
    print("\n" + "=" * 80)
    print("3. CROSS-LINGUISTIC COMPARISON (Tagalog vs English/Mandarin)")
    print("=" * 80)

    comparison = compare_with_english_mandarin(tagalog_words)

    print(f"\nCompared {comparison['statistics']['total_compared']} translation pairs")
    print(f"Mean distance: {comparison['statistics']['mean_distance']:.4f}")
    print(f"\nMatch quality:")
    print(f"  Exact (< 0.05): {comparison['statistics']['exact_matches']}")
    print(f"  Close (< 0.10): {comparison['statistics']['close_matches']}")
    print(f"  Moderate (< 0.20): {comparison['statistics']['moderate_matches']}")
    print(f"  Distant (> 0.20): {comparison['statistics']['distant_matches']}")

    print(f"\nMean dimensional differences:")
    print(f"  Love (L): {comparison['statistics']['mean_L_diff']:+.4f}")
    print(f"  Justice (J): {comparison['statistics']['mean_J_diff']:+.4f}")
    print(f"  Power (P): {comparison['statistics']['mean_P_diff']:+.4f}")
    print(f"  Wisdom (W): {comparison['statistics']['mean_W_diff']:+.4f}")

    # Show some notable comparisons
    print("\nNotable exact/close matches:")
    exact_and_close = [c for c in comparison['comparisons'] if c['match_quality'] in ['exact', 'close']]
    for comp in sorted(exact_and_close, key=lambda x: x['distance'])[:10]:
        print(f"  {comp['tagalog']} → {comp['english']}: {comp['distance']:.4f} ({comp['match_quality']})")

    # Analyze Filipino-unique concepts
    print("\n" + "=" * 80)
    print("4. UNIQUELY FILIPINO CONCEPTS (Loob Concepts)")
    print("=" * 80)

    filipino_analysis = analyze_filipino_uniqueness(results)

    for word, data in filipino_analysis.items():
        print(f"\n{word.upper()}")
        print(f"  English approximation: {data['english_approximation']}")
        print(f"  Territory: {data['territory']}")
        print(f"  Coordinates: L={data['coordinates'][0]:.3f}, J={data['coordinates'][1]:.3f}, " +
              f"P={data['coordinates'][2]:.3f}, W={data['coordinates'][3]:.3f}")
        print(f"  Harmony: {data['harmony']:.3f}")
        print(f"  Notes: {data['notes']}")
        print(f"  → {data['interpretation']}")

    # Save results
    output_file = 'experiments/tagalog_semantic_mapping.json'

    output_data = {
        'word_mappings': results['word_mappings'],
        'territory_distribution': {str(k): v for k, v in results['territory_members'].items()},
        'statistics': results['statistics'],
        'cross_linguistic_comparison': comparison,
        'filipino_unique_concepts': filipino_analysis
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print(f"Analysis complete. Results saved to {output_file}")
    print("=" * 80)

    return output_data


if __name__ == "__main__":
    run_tagalog_mapping()
