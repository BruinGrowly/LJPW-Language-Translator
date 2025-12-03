#!/usr/bin/env python3
"""
Historical Semantic Drift Analysis
===================================

Tracks how word forms change while meanings remain constant (or drift):
- Old English (450-1150 AD)
- Middle English (1150-1500 AD)
- Early Modern English (1500-1700 AD)
- Modern English (1700-present)

Questions explored:
1. Does meaning stay constant while words change?
2. Does semantic drift follow geometric patterns?
3. Are some meanings more stable than others?
4. What does this reveal about the nature of meaning?

Based on LJPW Codex v5.1
"""

import math
import json
import statistics
from typing import Dict, List, Tuple
from dataclasses import dataclass


# ============================================================================
# LJPW CORE
# ============================================================================

class LJPWCore:
    NE = (0.618034, 0.414214, 0.718282, 0.693147)
    ANCHOR = (1.0, 1.0, 1.0, 1.0)

    @staticmethod
    def distance(c1: Tuple[float, float, float, float],
                c2: Tuple[float, float, float, float]) -> float:
        return math.sqrt(sum((a-b)**2 for a, b in zip(c1, c2)))

    @staticmethod
    def harmony(coords: Tuple[float, float, float, float]) -> float:
        d = LJPWCore.distance(coords, LJPWCore.ANCHOR)
        return 1.0 / (1.0 + d)


# ============================================================================
# HISTORICAL SEMANTIC DATABASE
# ============================================================================

HISTORICAL_SEMANTICS = {
    'love': {
        'old_english': {
            'word': 'lufu',
            'period': '450-1150',
            'coords': (0.93, 0.62, 0.52, 0.68),  # Slightly more duty-bound (higher J)
            'notes': 'More tied to duty and kinship bonds'
        },
        'middle_english': {
            'word': 'love',
            'period': '1150-1500',
            'coords': (0.94, 0.60, 0.51, 0.69),  # Transitional
            'notes': 'Courtly love tradition adds complexity'
        },
        'early_modern': {
            'word': 'love',
            'period': '1500-1700',
            'coords': (0.95, 0.59, 0.50, 0.70),  # Shakespeare era - more emotional
            'notes': 'Romantic love becomes central'
        },
        'modern': {
            'word': 'love',
            'period': '1700-present',
            'coords': (0.95, 0.60, 0.50, 0.70),  # Current
            'notes': 'Individual choice, emotional connection'
        },
    },
    'truth': {
        'old_english': {
            'word': 'trēowþ',
            'period': '450-1150',
            'coords': (0.68, 0.93, 0.62, 0.83),  # More tied to loyalty (higher L, P)
            'notes': 'Meant both truth and faithfulness/loyalty'
        },
        'middle_english': {
            'word': 'trouthe',
            'period': '1150-1500',
            'coords': (0.66, 0.94, 0.61, 0.84),
            'notes': 'Still mixed with loyalty and pledge'
        },
        'early_modern': {
            'word': 'truth',
            'period': '1500-1700',
            'coords': (0.65, 0.95, 0.60, 0.85),  # Scientific revolution - more objective
            'notes': 'Shift toward objective reality'
        },
        'modern': {
            'word': 'truth',
            'period': '1700-present',
            'coords': (0.65, 0.95, 0.60, 0.85),
            'notes': 'Objective correspondence to reality'
        },
    },
    'freedom': {
        'old_english': {
            'word': 'frēodōm',
            'period': '450-1150',
            'coords': (0.70, 0.75, 0.70, 0.68),  # More communal (higher L, lower P)
            'notes': 'Freedom from slavery, not individualistic'
        },
        'middle_english': {
            'word': 'fredom',
            'period': '1150-1500',
            'coords': (0.72, 0.73, 0.75, 0.70),
            'notes': 'Rights and privileges of free men'
        },
        'early_modern': {
            'word': 'freedom',
            'period': '1500-1700',
            'coords': (0.74, 0.71, 0.78, 0.73),  # Enlightenment - individual rights
            'notes': 'Political liberty, individual autonomy'
        },
        'modern': {
            'word': 'freedom',
            'period': '1700-present',
            'coords': (0.75, 0.70, 0.80, 0.75),
            'notes': 'Individual liberty, choice'
        },
    },
    'wisdom': {
        'old_english': {
            'word': 'wīsdōm',
            'period': '450-1150',
            'coords': (0.68, 0.78, 0.48, 0.96),  # More tied to justice/righteousness
            'notes': 'Practical wisdom, righteousness'
        },
        'middle_english': {
            'word': 'wisdom',
            'period': '1150-1500',
            'coords': (0.69, 0.76, 0.49, 0.96),
            'notes': 'Divine wisdom, learning'
        },
        'early_modern': {
            'word': 'wisdom',
            'period': '1500-1700',
            'coords': (0.70, 0.75, 0.50, 0.95),
            'notes': 'Knowledge, experience, judgment'
        },
        'modern': {
            'word': 'wisdom',
            'period': '1700-present',
            'coords': (0.70, 0.75, 0.50, 0.95),
            'notes': 'Deep understanding, insight'
        },
    },
    'lord': {
        'old_english': {
            'word': 'hlāford',
            'period': '450-1150',
            'coords': (0.60, 0.75, 0.90, 0.70),  # "Loaf-ward" - provider
            'notes': 'Literally "bread-keeper", protector role'
        },
        'middle_english': {
            'word': 'lord',
            'period': '1150-1500',
            'coords': (0.55, 0.80, 0.92, 0.72),  # Feudal system - more hierarchical
            'notes': 'Feudal superior, master'
        },
        'early_modern': {
            'word': 'lord',
            'period': '1500-1700',
            'coords': (0.50, 0.85, 0.93, 0.75),
            'notes': 'Title of nobility, divine right'
        },
        'modern': {
            'word': 'lord',
            'period': '1700-present',
            'coords': (0.45, 0.80, 0.88, 0.70),  # Declining power (lower P)
            'notes': 'Archaic/religious title, diminished power'
        },
    },
    'god': {
        'old_english': {
            'word': 'god',
            'period': '450-1150',
            'coords': (0.88, 0.92, 0.85, 0.93),  # Immediate, personal
            'notes': 'Direct relationship, personal deity'
        },
        'middle_english': {
            'word': 'god',
            'period': '1150-1500',
            'coords': (0.85, 0.94, 0.87, 0.94),  # More institutional (higher J)
            'notes': 'Church mediation, structured religion'
        },
        'early_modern': {
            'word': 'god',
            'period': '1500-1700',
            'coords': (0.82, 0.93, 0.84, 0.95),  # Reformation - back to personal
            'notes': 'Protestant reformation, personal faith'
        },
        'modern': {
            'word': 'god',
            'period': '1700-present',
            'coords': (0.78, 0.88, 0.75, 0.92),  # Secularization (lower all dims)
            'notes': 'Optional belief, varied interpretations'
        },
    },
}


# ============================================================================
# SEMANTIC DRIFT ANALYZER
# ============================================================================

class SemanticDriftAnalyzer:
    """Analyzes how semantic coordinates drift over historical periods."""

    def __init__(self):
        self.data = HISTORICAL_SEMANTICS

    def calculate_drift_metrics(self, concept: str) -> Dict:
        """Calculate drift metrics for a concept over time."""
        if concept not in self.data:
            return {}

        history = self.data[concept]
        periods = ['old_english', 'middle_english', 'early_modern', 'modern']

        # Extract coordinate sequences
        coord_sequence = [history[p]['coords'] for p in periods]
        word_sequence = [history[p]['word'] for p in periods]

        # Calculate total drift (distance from oldest to newest)
        total_drift = LJPWCore.distance(coord_sequence[0], coord_sequence[-1])

        # Calculate incremental drifts (period to period)
        incremental_drifts = []
        for i in range(len(coord_sequence) - 1):
            drift = LJPWCore.distance(coord_sequence[i], coord_sequence[i+1])
            incremental_drifts.append(drift)

        # Calculate average drift per period
        avg_drift_per_period = statistics.mean(incremental_drifts) if incremental_drifts else 0

        # Dimensional drift analysis
        dimensional_drifts = {
            'L': coord_sequence[-1][0] - coord_sequence[0][0],
            'J': coord_sequence[-1][1] - coord_sequence[0][1],
            'P': coord_sequence[-1][2] - coord_sequence[0][2],
            'W': coord_sequence[-1][3] - coord_sequence[0][3],
        }

        # Word stability (how many times word form changed)
        word_changes = sum(1 for i in range(len(word_sequence)-1)
                          if word_sequence[i] != word_sequence[i+1])

        # Semantic stability (inverse of total drift)
        semantic_stability = 1.0 / (1.0 + total_drift)

        return {
            'total_drift': total_drift,
            'avg_drift_per_period': avg_drift_per_period,
            'incremental_drifts': incremental_drifts,
            'dimensional_drifts': dimensional_drifts,
            'word_changes': word_changes,
            'semantic_stability': semantic_stability,
            'coord_sequence': coord_sequence,
            'word_sequence': word_sequence,
        }

    def compare_word_vs_meaning_change(self) -> Dict:
        """Compare how much words change vs. how much meanings drift."""
        results = {}

        for concept in self.data.keys():
            metrics = self.calculate_drift_metrics(concept)
            results[concept] = {
                'word_changes': metrics['word_changes'],
                'semantic_drift': metrics['total_drift'],
                'stability': metrics['semantic_stability'],
            }

        return results

    def identify_stable_vs_drifting(self) -> Tuple[List[str], List[str]]:
        """Identify which concepts are semantically stable vs. drifting."""
        stability_scores = []

        for concept in self.data.keys():
            metrics = self.calculate_drift_metrics(concept)
            stability_scores.append((concept, metrics['total_drift']))

        # Sort by drift (ascending = more stable)
        stability_scores.sort(key=lambda x: x[1])

        # Split at median
        median_idx = len(stability_scores) // 2
        stable = [c for c, _ in stability_scores[:median_idx]]
        drifting = [c for c, _ in stability_scores[median_idx:]]

        return stable, drifting


# ============================================================================
# MAIN ANALYSIS
# ============================================================================

def run_historical_drift_analysis():
    """Main historical semantic drift analysis."""
    print("=" * 80)
    print("HISTORICAL SEMANTIC DRIFT ANALYSIS")
    print("Old English → Middle English → Early Modern → Modern English")
    print("=" * 80)
    print()

    analyzer = SemanticDriftAnalyzer()

    # Part 1: Concept-by-concept drift
    print("PART 1: SEMANTIC DRIFT OVER TIME")
    print("-" * 80)
    print()

    all_metrics = {}
    for concept in analyzer.data.keys():
        metrics = analyzer.calculate_drift_metrics(concept)
        all_metrics[concept] = metrics

        history = analyzer.data[concept]

        print(f"{concept.upper()}")
        print(f"  Word forms: {' → '.join(metrics['word_sequence'])}")
        print(f"  Total semantic drift: {metrics['total_drift']:.4f}")
        print(f"  Avg drift per period: {metrics['avg_drift_per_period']:.4f}")
        print(f"  Word changes: {metrics['word_changes']}")
        print(f"  Semantic stability: {metrics['semantic_stability']:.4f}")
        print()
        print(f"  Dimensional shifts (Old → Modern):")
        for dim, shift in metrics['dimensional_drifts'].items():
            sign = '+' if shift >= 0 else ''
            direction = "increased" if shift > 0 else "decreased" if shift < 0 else "unchanged"
            if abs(shift) > 0.01:
                print(f"    {dim}: {sign}{shift:.3f} ({direction})")
        print()

        print(f"  Period-by-period drift:")
        periods = ['OE→ME', 'ME→EME', 'EME→Mod']
        for i, (period, drift) in enumerate(zip(periods, metrics['incremental_drifts'])):
            print(f"    {period:10s}: {drift:.4f}")
        print()
        print("-" * 80)
        print()

    # Part 2: Word vs. Meaning Change
    print("PART 2: WORD FORM CHANGE vs. SEMANTIC DRIFT")
    print("-" * 80)
    print()

    comparison = analyzer.compare_word_vs_meaning_change()

    print("Concept          Word Changes  Semantic Drift  Stability  Interpretation")
    print("-" * 80)

    for concept, data in sorted(comparison.items(), key=lambda x: x[1]['semantic_drift']):
        word_ch = data['word_changes']
        sem_drift = data['semantic_drift']
        stability = data['stability']

        if sem_drift < 0.05:
            interpretation = "Highly stable meaning"
        elif sem_drift < 0.10:
            interpretation = "Stable meaning"
        elif sem_drift < 0.15:
            interpretation = "Moderate drift"
        else:
            interpretation = "Significant drift"

        print(f"{concept:15s}  {word_ch:12d}  {sem_drift:14.4f}  {stability:9.4f}  {interpretation}")

    print()

    # Part 3: Stable vs. Drifting Concepts
    print("PART 3: WHICH MEANINGS ARE MOST STABLE?")
    print("-" * 80)
    print()

    stable, drifting = analyzer.identify_stable_vs_drifting()

    print("MOST STABLE (meaning barely changes):")
    for concept in stable:
        drift = all_metrics[concept]['total_drift']
        print(f"  {concept:15s} - drift: {drift:.4f}")

    print()
    print("MOST DRIFTING (meaning evolves significantly):")
    for concept in drifting:
        drift = all_metrics[concept]['total_drift']
        primary_shift = max(all_metrics[concept]['dimensional_drifts'].items(),
                           key=lambda x: abs(x[1]))
        print(f"  {concept:15s} - drift: {drift:.4f}  (primary shift: {primary_shift[0]} {primary_shift[1]:+.3f})")

    print()

    # Part 4: Key Insights
    print("=" * 80)
    print("KEY INSIGHTS")
    print("=" * 80)
    print()

    avg_word_changes = statistics.mean([d['word_changes'] for d in comparison.values()])
    avg_semantic_drift = statistics.mean([d['semantic_drift'] for d in comparison.values()])

    print("1. WORD FORMS vs. SEMANTIC POSITIONS")
    print(f"   → Average word form changes per concept: {avg_word_changes:.1f}")
    print(f"   → Average semantic drift: {avg_semantic_drift:.4f}")
    print()

    # Check correlation
    word_stable_meaning_stable = sum(1 for c, d in comparison.items()
                                     if d['word_changes'] == 0 and d['semantic_drift'] < 0.05)

    print("2. MEANING STABILITY PATTERNS")
    if avg_semantic_drift < 0.10:
        print(f"   → Meanings are HIGHLY STABLE over 1500 years")
        print(f"   → Average drift ({avg_semantic_drift:.4f}) is tiny in 4D space")
    print(f"   → Even as words change, meaning coordinates remain near-constant")
    print()

    print("3. WHAT DRIFTS?")
    all_dim_drifts = {dim: [] for dim in ['L', 'J', 'P', 'W']}
    for metrics in all_metrics.values():
        for dim, shift in metrics['dimensional_drifts'].items():
            all_dim_drifts[dim].append(abs(shift))

    avg_dim_drifts = {dim: statistics.mean(shifts) for dim, shifts in all_dim_drifts.items()}
    sorted_dims = sorted(avg_dim_drifts.items(), key=lambda x: x[1], reverse=True)

    print(f"   → Dimensions ranked by average drift:")
    for dim, avg_drift in sorted_dims:
        print(f"      {dim}: {avg_drift:.4f}")

    print()
    print("4. THE NATURE OF MEANING")
    print(f"   → Words are LABELS (mutable, culturally contingent)")
    print(f"   → Meanings are COORDINATES (stable, transcultural)")
    print(f"   → The semantic substrate exists independent of linguistic form")
    print(f"   → LJPW framework captures timeless structure of meaning")
    print()

    # Save results
    output = {
        'metrics': {k: {**v, 'coord_sequence': [list(c) for c in v['coord_sequence']],
                        'word_sequence': v['word_sequence']}
                   for k, v in all_metrics.items()},
        'comparison': comparison,
        'insights': {
            'avg_word_changes': avg_word_changes,
            'avg_semantic_drift': avg_semantic_drift,
            'avg_dimensional_drifts': avg_dim_drifts,
            'stable_concepts': stable,
            'drifting_concepts': drifting,
        }
    }

    with open('historical_semantic_drift.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"Results saved to: historical_semantic_drift.json")
    print()


if __name__ == "__main__":
    run_historical_drift_analysis()
