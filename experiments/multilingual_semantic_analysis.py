#!/usr/bin/env python3
"""
Multilingual Semantic Analysis: Universal vs Cultural Structures
=================================================================

Expands semantic mapping to 4 languages from different families:
- English (Indo-European, Germanic)
- French (Indo-European, Romance)
- Chinese Mandarin (Sino-Tibetan)
- Arabic (Semitic)

Tests:
1. Universal semantic structures across diverse language families
2. Cultural divergences in semantic space
3. Geometric relationships between similar and opposite concepts
4. Mathematical patterns (symmetries, ratios, reflections)

Based on LJPW Codex v5.1
"""

import math
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
import statistics


# ============================================================================
# LJPW CORE
# ============================================================================

class LJPWCore:
    """Core LJPW functions for semantic analysis."""

    NE = (0.618034, 0.414214, 0.718282, 0.693147)  # Natural Equilibrium
    ANCHOR = (1.0, 1.0, 1.0, 1.0)  # Divine Perfection

    @staticmethod
    def harmony_index(coords: Tuple[float, float, float, float]) -> float:
        """Proximity to Anchor Point."""
        L, J, P, W = coords
        d = math.sqrt((1-L)**2 + (1-J)**2 + (1-P)**2 + (1-W)**2)
        return 1.0 / (1.0 + d)

    @staticmethod
    def semantic_distance(c1: Tuple[float, float, float, float],
                         c2: Tuple[float, float, float, float]) -> float:
        """Euclidean distance in 4D semantic space."""
        return math.sqrt(sum((a-b)**2 for a, b in zip(c1, c2)))

    @staticmethod
    def cosine_similarity(c1: Tuple[float, float, float, float],
                         c2: Tuple[float, float, float, float]) -> float:
        """Cosine similarity between two semantic vectors."""
        dot_product = sum(a*b for a, b in zip(c1, c2))
        mag1 = math.sqrt(sum(a**2 for a in c1))
        mag2 = math.sqrt(sum(b**2 for b in c2))
        if mag1 == 0 or mag2 == 0:
            return 0.0
        return dot_product / (mag1 * mag2)

    @staticmethod
    def reflection_point(coords: Tuple[float, float, float, float],
                        center: Tuple[float, float, float, float]) -> Tuple[float, float, float, float]:
        """Calculate reflection of coords through center point."""
        return tuple(2*c - v for c, v in zip(center, coords))

    @staticmethod
    def midpoint(c1: Tuple[float, float, float, float],
                c2: Tuple[float, float, float, float]) -> Tuple[float, float, float, float]:
        """Calculate midpoint between two coordinates."""
        return tuple((a + b) / 2 for a, b in zip(c1, c2))


# ============================================================================
# SEMANTIC DATABASE (Expanded for 4 languages)
# ============================================================================

SEMANTIC_DATABASE = {
    # Core LJPW concepts
    'love': {
        'en': (0.95, 0.60, 0.50, 0.70),
        'fr': (0.95, 0.55, 0.50, 0.70),
        'zh': (0.92, 0.58, 0.48, 0.75),  # 爱 (ài)
        'ar': (0.93, 0.62, 0.52, 0.72),  # حب (hubb)
    },
    'hate': {
        'en': (0.20, 0.45, 0.85, 0.40),
        'fr': (0.20, 0.45, 0.85, 0.40),  # haine
        'zh': (0.18, 0.42, 0.88, 0.38),  # 恨 (hèn)
        'ar': (0.22, 0.48, 0.87, 0.42),  # كراهية (karāhiya)
    },
    'justice': {
        'en': (0.60, 0.95, 0.70, 0.80),
        'fr': (0.60, 0.95, 0.70, 0.80),
        'zh': (0.62, 0.93, 0.68, 0.82),  # 正义 (zhèngyì)
        'ar': (0.58, 0.96, 0.72, 0.78),  # عدالة (ʿadāla)
    },
    'injustice': {
        'en': (0.25, 0.15, 0.80, 0.45),
        'fr': (0.25, 0.15, 0.80, 0.45),
        'zh': (0.23, 0.18, 0.82, 0.43),  # 不公 (bùgōng)
        'ar': (0.27, 0.12, 0.85, 0.47),  # ظلم (ẓulm)
    },
    'power': {
        'en': (0.45, 0.60, 0.95, 0.65),
        'fr': (0.50, 0.55, 0.95, 0.65),
        'zh': (0.42, 0.58, 0.96, 0.63),  # 力量 (lìliàng)
        'ar': (0.48, 0.62, 0.94, 0.67),  # قوة (quwwa)
    },
    'weakness': {
        'en': (0.40, 0.50, 0.20, 0.45),
        'fr': (0.40, 0.50, 0.20, 0.45),  # faiblesse
        'zh': (0.38, 0.48, 0.18, 0.43),  # 弱 (ruò)
        'ar': (0.42, 0.52, 0.22, 0.47),  # ضعف (ḍuʿf)
    },
    'wisdom': {
        'en': (0.70, 0.75, 0.50, 0.95),
        'fr': (0.70, 0.75, 0.45, 0.95),
        'zh': (0.75, 0.78, 0.45, 0.97),  # 智慧 (zhìhuì)
        'ar': (0.68, 0.73, 0.48, 0.96),  # حكمة (ḥikma)
    },
    'ignorance': {
        'en': (0.35, 0.40, 0.50, 0.15),
        'fr': (0.35, 0.40, 0.50, 0.15),
        'zh': (0.33, 0.38, 0.52, 0.12),  # 无知 (wúzhī)
        'ar': (0.37, 0.42, 0.48, 0.18),  # جهل (jahl)
    },
    'peace': {
        'en': (0.85, 0.80, 0.40, 0.75),
        'fr': (0.85, 0.78, 0.40, 0.75),  # paix
        'zh': (0.88, 0.82, 0.35, 0.80),  # 和平 (hépíng)
        'ar': (0.83, 0.85, 0.38, 0.73),  # سلام (salām)
    },
    'war': {
        'en': (0.25, 0.55, 0.95, 0.50),
        'fr': (0.25, 0.55, 0.95, 0.50),  # guerre
        'zh': (0.22, 0.52, 0.97, 0.48),  # 战争 (zhànzhēng)
        'ar': (0.28, 0.58, 0.96, 0.52),  # حرب (ḥarb)
    },
    'harmony': {
        'en': (0.80, 0.85, 0.65, 0.85),
        'fr': (0.80, 0.85, 0.65, 0.85),
        'zh': (0.85, 0.88, 0.60, 0.90),  # 和谐 (héxié)
        'ar': (0.78, 0.83, 0.67, 0.83),  # تناغم (tanāghum)
    },
    'chaos': {
        'en': (0.30, 0.20, 0.85, 0.40),
        'fr': (0.30, 0.20, 0.85, 0.40),
        'zh': (0.28, 0.18, 0.88, 0.38),  # 混乱 (hùnluàn)
        'ar': (0.32, 0.22, 0.87, 0.42),  # فوضى (fawḍā)
    },
    'order': {
        'en': (0.55, 0.90, 0.70, 0.75),
        'fr': (0.50, 0.90, 0.70, 0.75),
        'zh': (0.58, 0.92, 0.68, 0.78),  # 秩序 (zhìxù)
        'ar': (0.52, 0.93, 0.72, 0.73),  # نظام (niẓām)
    },
    'truth': {
        'en': (0.65, 0.95, 0.60, 0.85),
        'fr': (0.65, 0.95, 0.60, 0.85),
        'zh': (0.68, 0.96, 0.58, 0.88),  # 真理 (zhēnlǐ)
        'ar': (0.63, 0.97, 0.62, 0.83),  # حقيقة (ḥaqīqa)
    },
    'lie': {
        'en': (0.25, 0.30, 0.65, 0.35),
        'fr': (0.25, 0.30, 0.65, 0.35),  # mensonge
        'zh': (0.23, 0.28, 0.68, 0.32),  # 谎言 (huǎngyán)
        'ar': (0.27, 0.32, 0.67, 0.37),  # كذب (kadhib)
    },
    'compassion': {
        'en': (0.90, 0.70, 0.50, 0.75),
        'fr': (0.90, 0.70, 0.50, 0.75),
        'zh': (0.93, 0.68, 0.48, 0.78),  # 慈悲 (cíbēi)
        'ar': (0.88, 0.72, 0.52, 0.73),  # رحمة (raḥma)
    },
    'cruelty': {
        'en': (0.15, 0.35, 0.90, 0.40),
        'fr': (0.15, 0.35, 0.90, 0.40),  # cruauté
        'zh': (0.12, 0.32, 0.92, 0.38),  # 残酷 (cánkù)
        'ar': (0.18, 0.38, 0.93, 0.42),  # قسوة (qaswah)
    },
    'freedom': {
        'en': (0.75, 0.70, 0.80, 0.75),
        'fr': (0.80, 0.65, 0.85, 0.75),
        'zh': (0.70, 0.68, 0.82, 0.73),  # 自由 (zìyóu)
        'ar': (0.78, 0.72, 0.83, 0.77),  # حرية (ḥurriyya)
    },
    'oppression': {
        'en': (0.20, 0.30, 0.90, 0.45),
        'fr': (0.20, 0.30, 0.90, 0.45),
        'zh': (0.18, 0.28, 0.92, 0.43),  # 压迫 (yāpò)
        'ar': (0.22, 0.32, 0.93, 0.47),  # قمع (qamʿ)
    },
    'hope': {
        'en': (0.80, 0.65, 0.60, 0.70),
        'fr': (0.82, 0.63, 0.60, 0.70),  # espoir
        'zh': (0.83, 0.67, 0.58, 0.72),  # 希望 (xīwàng)
        'ar': (0.78, 0.68, 0.62, 0.68),  # أمل (amal)
    },
    'despair': {
        'en': (0.25, 0.40, 0.35, 0.30),
        'fr': (0.25, 0.40, 0.35, 0.30),  # désespoir
        'zh': (0.23, 0.38, 0.33, 0.28),  # 绝望 (juéwàng)
        'ar': (0.27, 0.42, 0.37, 0.32),  # يأس (yaʾs)
    },
    'courage': {
        'en': (0.70, 0.75, 0.85, 0.70),
        'fr': (0.70, 0.75, 0.85, 0.70),
        'zh': (0.72, 0.78, 0.87, 0.72),  # 勇气 (yǒngqì)
        'ar': (0.68, 0.73, 0.88, 0.68),  # شجاعة (shajāʿa)
    },
    'fear': {
        'en': (0.30, 0.45, 0.40, 0.45),
        'fr': (0.30, 0.45, 0.40, 0.45),  # peur
        'zh': (0.28, 0.43, 0.38, 0.43),  # 恐惧 (kǒngjù)
        'ar': (0.32, 0.47, 0.42, 0.47),  # خوف (khawf)
    },
}


# ============================================================================
# MULTILINGUAL ANALYZER
# ============================================================================

@dataclass
class MultilingualConcept:
    """A concept across multiple languages."""
    concept: str
    en_coords: Tuple[float, float, float, float]
    fr_coords: Tuple[float, float, float, float]
    zh_coords: Tuple[float, float, float, float]
    ar_coords: Tuple[float, float, float, float]

    @property
    def centroid(self) -> Tuple[float, float, float, float]:
        """Average position across all languages."""
        return tuple(
            statistics.mean([self.en_coords[i], self.fr_coords[i],
                           self.zh_coords[i], self.ar_coords[i]])
            for i in range(4)
        )

    @property
    def variance(self) -> Tuple[float, float, float, float]:
        """Variance in each dimension."""
        return tuple(
            statistics.variance([self.en_coords[i], self.fr_coords[i],
                               self.zh_coords[i], self.ar_coords[i]])
            for i in range(4)
        )

    def is_universal(self, threshold: float = 0.05) -> bool:
        """True if all languages cluster tightly."""
        return all(v < threshold for v in self.variance)

    def get_max_distance(self) -> float:
        """Maximum distance between any two language versions."""
        coords = [self.en_coords, self.fr_coords, self.zh_coords, self.ar_coords]
        max_dist = 0.0
        for i in range(len(coords)):
            for j in range(i+1, len(coords)):
                dist = LJPWCore.semantic_distance(coords[i], coords[j])
                max_dist = max(max_dist, dist)
        return max_dist


class AntonymAnalyzer:
    """Analyzes geometric relationships between opposite concepts."""

    def __init__(self):
        self.antonym_pairs = []

    def add_antonym_pair(self, positive: str, negative: str):
        """Add an antonym pair for analysis."""
        if positive not in SEMANTIC_DATABASE or negative not in SEMANTIC_DATABASE:
            return

        pos_data = SEMANTIC_DATABASE[positive]
        neg_data = SEMANTIC_DATABASE[negative]

        self.antonym_pairs.append({
            'positive': positive,
            'negative': negative,
            'en_pos': pos_data['en'],
            'en_neg': neg_data['en'],
            'fr_pos': pos_data['fr'],
            'fr_neg': neg_data['fr'],
            'zh_pos': pos_data['zh'],
            'zh_neg': neg_data['zh'],
            'ar_pos': pos_data['ar'],
            'ar_neg': neg_data['ar'],
        })

    def analyze_geometric_patterns(self) -> Dict:
        """Analyze geometric patterns in antonym relationships."""
        results = {
            'pairs': [],
            'statistics': {},
        }

        for pair in self.antonym_pairs:
            analysis = self._analyze_single_pair(pair)
            results['pairs'].append(analysis)

        # Aggregate statistics
        if results['pairs']:
            results['statistics'] = self._compute_aggregate_statistics(results['pairs'])

        return results

    def _analyze_single_pair(self, pair: Dict) -> Dict:
        """Analyze a single antonym pair."""
        pos = pair['positive']
        neg = pair['negative']

        # Analyze across languages
        languages = ['en', 'fr', 'zh', 'ar']
        analyses = {}

        for lang in languages:
            pos_coords = pair[f'{lang}_pos']
            neg_coords = pair[f'{lang}_neg']

            # Calculate metrics
            distance = LJPWCore.semantic_distance(pos_coords, neg_coords)
            midpoint = LJPWCore.midpoint(pos_coords, neg_coords)
            cosine_sim = LJPWCore.cosine_similarity(pos_coords, neg_coords)

            # Distance to Natural Equilibrium
            ne_to_pos = LJPWCore.semantic_distance(LJPWCore.NE, pos_coords)
            ne_to_neg = LJPWCore.semantic_distance(LJPWCore.NE, neg_coords)
            ne_to_mid = LJPWCore.semantic_distance(LJPWCore.NE, midpoint)

            # Harmony indices
            pos_harmony = LJPWCore.harmony_index(pos_coords)
            neg_harmony = LJPWCore.harmony_index(neg_coords)
            mid_harmony = LJPWCore.harmony_index(midpoint)

            # Dimensional shifts
            shifts = tuple(n - p for p, n in zip(pos_coords, neg_coords))

            analyses[lang] = {
                'distance': distance,
                'cosine_similarity': cosine_sim,
                'midpoint': midpoint,
                'midpoint_to_ne': ne_to_mid,
                'positive_harmony': pos_harmony,
                'negative_harmony': neg_harmony,
                'midpoint_harmony': mid_harmony,
                'dimensional_shifts': {
                    'L': shifts[0],
                    'J': shifts[1],
                    'P': shifts[2],
                    'W': shifts[3],
                },
            }

        return {
            'positive': pos,
            'negative': neg,
            'languages': analyses,
        }

    def _compute_aggregate_statistics(self, pair_analyses: List[Dict]) -> Dict:
        """Compute aggregate statistics across all pairs."""
        # Collect metrics
        all_distances = []
        all_cosine_sims = []
        all_midpoint_harmonies = []
        all_L_shifts = []
        all_J_shifts = []
        all_P_shifts = []
        all_W_shifts = []

        for pair in pair_analyses:
            for lang in ['en', 'fr', 'zh', 'ar']:
                lang_data = pair['languages'][lang]
                all_distances.append(lang_data['distance'])
                all_cosine_sims.append(lang_data['cosine_similarity'])
                all_midpoint_harmonies.append(lang_data['midpoint_harmony'])
                all_L_shifts.append(lang_data['dimensional_shifts']['L'])
                all_J_shifts.append(lang_data['dimensional_shifts']['J'])
                all_P_shifts.append(lang_data['dimensional_shifts']['P'])
                all_W_shifts.append(lang_data['dimensional_shifts']['W'])

        return {
            'average_distance': statistics.mean(all_distances),
            'std_distance': statistics.stdev(all_distances) if len(all_distances) > 1 else 0,
            'average_cosine_similarity': statistics.mean(all_cosine_sims),
            'average_midpoint_harmony': statistics.mean(all_midpoint_harmonies),
            'average_dimensional_shifts': {
                'L': statistics.mean(all_L_shifts),
                'J': statistics.mean(all_J_shifts),
                'P': statistics.mean(all_P_shifts),
                'W': statistics.mean(all_W_shifts),
            },
            'std_dimensional_shifts': {
                'L': statistics.stdev(all_L_shifts) if len(all_L_shifts) > 1 else 0,
                'J': statistics.stdev(all_J_shifts) if len(all_J_shifts) > 1 else 0,
                'P': statistics.stdev(all_P_shifts) if len(all_P_shifts) > 1 else 0,
                'W': statistics.stdev(all_W_shifts) if len(all_W_shifts) > 1 else 0,
            },
        }


# ============================================================================
# MAIN EXPERIMENT
# ============================================================================

def run_multilingual_experiment():
    """Main multilingual semantic analysis."""
    print("=" * 80)
    print("MULTILINGUAL SEMANTIC ANALYSIS")
    print("Testing Universal Structures Across Language Families")
    print("=" * 80)
    print()
    print("Languages:")
    print("  English (EN)  - Indo-European, Germanic")
    print("  French (FR)   - Indo-European, Romance")
    print("  Chinese (ZH)  - Sino-Tibetan")
    print("  Arabic (AR)   - Semitic")
    print()

    # Part 1: Universal Concepts
    print("=" * 80)
    print("PART 1: TESTING UNIVERSAL SEMANTIC STRUCTURES")
    print("=" * 80)
    print()

    concepts = list(SEMANTIC_DATABASE.keys())
    multilingual_concepts = []

    for concept in concepts:
        data = SEMANTIC_DATABASE[concept]
        mc = MultilingualConcept(
            concept=concept,
            en_coords=data['en'],
            fr_coords=data['fr'],
            zh_coords=data['zh'],
            ar_coords=data['ar'],
        )
        multilingual_concepts.append(mc)

    # Find universals
    universals = [mc for mc in multilingual_concepts if mc.is_universal(threshold=0.05)]

    print(f"Concepts analyzed: {len(multilingual_concepts)}")
    print(f"Universal concepts (variance < 0.05): {len(universals)}")
    print()

    if universals:
        print("UNIVERSAL CONCEPTS (All 4 languages agree):")
        print("-" * 80)
        for mc in sorted(universals, key=lambda x: sum(x.variance)):
            total_var = sum(mc.variance)
            max_dist = mc.get_max_distance()
            print(f"  {mc.concept:15s}  variance: {total_var:.4f}  max_dist: {max_dist:.4f}")
        print()

    # Part 2: Antonym Geometry
    print("=" * 80)
    print("PART 2: ANTONYM GEOMETRY - SHADOWS OF MEANING")
    print("=" * 80)
    print()

    analyzer = AntonymAnalyzer()

    # Add antonym pairs
    antonym_pairs = [
        ('love', 'hate'),
        ('justice', 'injustice'),
        ('power', 'weakness'),
        ('wisdom', 'ignorance'),
        ('peace', 'war'),
        ('harmony', 'chaos'),
        ('order', 'chaos'),
        ('truth', 'lie'),
        ('compassion', 'cruelty'),
        ('freedom', 'oppression'),
        ('hope', 'despair'),
        ('courage', 'fear'),
    ]

    for pos, neg in antonym_pairs:
        analyzer.add_antonym_pair(pos, neg)

    results = analyzer.analyze_geometric_patterns()

    # Display results
    print(f"Antonym pairs analyzed: {len(results['pairs'])}")
    print()

    # Show aggregate statistics
    stats = results['statistics']
    print("AGGREGATE ANTONYM STATISTICS:")
    print("-" * 80)
    print(f"Average semantic distance: {stats['average_distance']:.4f} ± {stats['std_distance']:.4f}")
    print(f"Average cosine similarity: {stats['average_cosine_similarity']:.4f}")
    print(f"Average midpoint harmony: {stats['average_midpoint_harmony']:.4f}")
    print()
    print("Average Dimensional Shifts (Positive → Negative):")
    for dim in ['L', 'J', 'P', 'W']:
        avg = stats['average_dimensional_shifts'][dim]
        std = stats['std_dimensional_shifts'][dim]
        sign = "+" if avg >= 0 else ""
        print(f"  Δ{dim}: {sign}{avg:.4f} ± {std:.4f}")
    print()

    # Show individual pairs
    print("DETAILED ANTONYM ANALYSIS:")
    print("-" * 80)
    for pair_data in results['pairs'][:5]:  # Show first 5
        pos = pair_data['positive']
        neg = pair_data['negative']
        print(f"\n{pos.upper()} ↔ {neg.upper()}")
        print(f"{'':15s} {'Distance':>10s} {'Cos Sim':>10s} {'Mid Harm':>10s}")
        for lang in ['en', 'fr', 'zh', 'ar']:
            lang_data = pair_data['languages'][lang]
            print(f"  {lang.upper():13s} {lang_data['distance']:10.4f} "
                  f"{lang_data['cosine_similarity']:10.4f} "
                  f"{lang_data['midpoint_harmony']:10.4f}")

    print()
    print("=" * 80)
    print("PART 3: MATHEMATICAL PATTERNS IN OPPOSITION")
    print("=" * 80)
    print()

    # Analyze mathematical patterns
    analyze_mathematical_patterns(results)

    # Save results
    output_file = "multilingual_analysis.json"
    with open(output_file, 'w') as f:
        # Convert tuples to lists for JSON serialization
        serializable_results = results
        json.dump(serializable_results, f, indent=2, default=str)

    print()
    print(f"Results saved to: {output_file}")
    print()
    print("=" * 80)
    print("EXPERIMENT COMPLETE")
    print("=" * 80)

    return results


def analyze_mathematical_patterns(results: Dict):
    """Analyze mathematical patterns in antonym relationships."""

    # Pattern 1: Distance consistency
    print("PATTERN 1: Distance Consistency Across Languages")
    print("-" * 80)
    for pair_data in results['pairs']:
        pos = pair_data['positive']
        neg = pair_data['negative']
        distances = [pair_data['languages'][lang]['distance']
                    for lang in ['en', 'fr', 'zh', 'ar']]
        avg_dist = statistics.mean(distances)
        std_dist = statistics.stdev(distances) if len(distances) > 1 else 0
        consistency = std_dist / avg_dist if avg_dist > 0 else 0

        print(f"  {pos:12s} ↔ {neg:12s}  "
              f"avg_dist: {avg_dist:.4f}  std: {std_dist:.4f}  "
              f"consistency: {(1-consistency)*100:.1f}%")
    print()

    # Pattern 2: Midpoint harmony
    print("PATTERN 2: Midpoint Harmony (Balance Point)")
    print("-" * 80)
    print("Do antonym midpoints cluster near Natural Equilibrium?")
    print()

    ne_distances = []
    for pair_data in results['pairs']:
        pos = pair_data['positive']
        neg = pair_data['negative']
        # Average midpoint distance to NE across languages
        avg_mid_to_ne = statistics.mean([
            pair_data['languages'][lang]['midpoint_to_ne']
            for lang in ['en', 'fr', 'zh', 'ar']
        ])
        ne_distances.append(avg_mid_to_ne)
        print(f"  {pos:12s} ↔ {neg:12s}  midpoint_to_NE: {avg_mid_to_ne:.4f}")

    print()
    print(f"Average midpoint distance to NE: {statistics.mean(ne_distances):.4f}")
    print(f"Natural Equilibrium appears to be near antonym midpoints: "
          f"{'YES' if statistics.mean(ne_distances) < 0.3 else 'NO'}")
    print()

    # Pattern 3: Dimensional shift patterns
    print("PATTERN 3: Dimensional Shift Signatures")
    print("-" * 80)
    print("When concepts invert, which dimensions shift most?")
    print()

    stats = results['statistics']
    shifts = stats['average_dimensional_shifts']
    shift_magnitudes = [(dim, abs(shifts[dim])) for dim in ['L', 'J', 'P', 'W']]
    shift_magnitudes.sort(key=lambda x: x[1], reverse=True)

    print("Ranking by magnitude of shift (Positive → Negative):")
    for i, (dim, mag) in enumerate(shift_magnitudes, 1):
        direction = "increases" if shifts[dim] > 0 else "decreases"
        print(f"  {i}. {dim} {direction} by {mag:.4f}")

    print()
    print("INTERPRETATION:")
    if shift_magnitudes[0][0] == 'L':
        print("  → Opposition primarily shifts LOVE (connection vs isolation)")
    elif shift_magnitudes[0][0] == 'P':
        print("  → Opposition primarily shifts POWER (strength vs weakness)")
    elif shift_magnitudes[0][0] == 'J':
        print("  → Opposition primarily shifts JUSTICE (order vs chaos)")
    else:
        print("  → Opposition primarily shifts WISDOM (knowledge vs ignorance)")
    print()


if __name__ == "__main__":
    run_multilingual_experiment()
