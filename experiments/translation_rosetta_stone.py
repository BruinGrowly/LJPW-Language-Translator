#!/usr/bin/env python3
"""
Translation Rosetta Stone: Word-Pair Geometric Analysis
========================================================

This script analyzes English-French translation pairs to discover:
1. Whether translations maintain semantic position (isometric)
2. If there are consistent geometric transformations
3. Universal semantic structures that transcend language
4. Cultural/philosophical differences encoded in language

Based on LJPW Codex v5.1
"""

import math
import json
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict


# ============================================================================
# LJPW CORE
# ============================================================================

class LJPWCore:
    """Core LJPW functions for semantic analysis."""

    # Natural Equilibrium constants
    NE = (0.618034, 0.414214, 0.718282, 0.693147)  # L, J, P, W
    ANCHOR = (1.0, 1.0, 1.0, 1.0)

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
    def divine_signature(coords: Tuple[float, float, float, float]) -> float:
        """Alignment with Divine Perfection."""
        return LJPWCore.harmony_index(coords)


# ============================================================================
# SEMANTIC ANALYZER (LLM-Informed)
# ============================================================================

@dataclass
class SemanticCoordinates:
    """LJPW coordinates for a concept."""
    word: str
    language: str
    L: float  # Love: unity, connection, attraction
    J: float  # Justice: balance, structure, truth
    P: float  # Power: energy, force, capacity
    W: float  # Wisdom: insight, complexity, understanding

    @property
    def coords(self) -> Tuple[float, float, float, float]:
        return (self.L, self.J, self.P, self.W)

    @property
    def harmony(self) -> float:
        return LJPWCore.harmony_index(self.coords)


class SemanticAnalyzer:
    """
    Analyzes words and assigns LJPW coordinates.

    NOTE: This is a heuristic model. In production, would use:
    - Pre-trained semantic embeddings mapped to LJPW space
    - LLM-based semantic analysis
    - Crowd-sourced semantic ratings
    """

    # Semantic patterns (simplified heuristic)
    PATTERNS = {
        # Pure LJPW concepts
        'love': (0.95, 0.60, 0.50, 0.70),
        'amour': (0.95, 0.55, 0.50, 0.70),
        'justice': (0.60, 0.95, 0.70, 0.80),
        'power': (0.45, 0.60, 0.95, 0.65),
        'pouvoir': (0.50, 0.55, 0.95, 0.65),
        'wisdom': (0.70, 0.75, 0.50, 0.95),
        'sagesse': (0.70, 0.75, 0.45, 0.95),

        # Emotional warmth
        'warmth': (0.85, 0.50, 0.40, 0.60),
        'chaleur': (0.85, 0.45, 0.45, 0.60),
        'tenderness': (0.90, 0.55, 0.35, 0.65),
        'tendresse': (0.92, 0.50, 0.35, 0.65),
        'compassion': (0.90, 0.70, 0.50, 0.75),

        # Structural
        'law': (0.50, 0.90, 0.75, 0.70),
        'loi': (0.50, 0.92, 0.75, 0.70),
        'order': (0.55, 0.85, 0.70, 0.75),
        'ordre': (0.50, 0.90, 0.70, 0.75),
        'balance': (0.65, 0.90, 0.60, 0.80),
        'équilibre': (0.65, 0.88, 0.60, 0.80),

        # Force/Action
        'strength': (0.50, 0.65, 0.90, 0.60),
        'force': (0.45, 0.65, 0.95, 0.60),
        'might': (0.45, 0.60, 0.95, 0.55),
        'puissance': (0.45, 0.55, 0.95, 0.60),
        'energy': (0.55, 0.60, 0.90, 0.65),
        'énergie': (0.55, 0.60, 0.90, 0.65),

        # Knowledge
        'knowledge': (0.60, 0.70, 0.50, 0.90),
        'connaissance': (0.60, 0.70, 0.50, 0.92),
        'understanding': (0.75, 0.70, 0.50, 0.92),
        'compréhension': (0.75, 0.70, 0.48, 0.92),
        'insight': (0.70, 0.75, 0.55, 0.95),
        'perspicacité': (0.70, 0.75, 0.55, 0.95),

        # Social concepts
        'freedom': (0.75, 0.70, 0.80, 0.75),
        'liberté': (0.80, 0.65, 0.85, 0.75),
        'duty': (0.60, 0.85, 0.70, 0.75),
        'devoir': (0.55, 0.90, 0.70, 0.75),
        'honor': (0.70, 0.90, 0.75, 0.80),
        'honneur': (0.70, 0.92, 0.75, 0.80),

        # Beauty and harmony
        'beauty': (0.85, 0.75, 0.55, 0.80),
        'beauté': (0.88, 0.75, 0.55, 0.80),
        'harmony': (0.80, 0.85, 0.65, 0.85),
        'harmonie': (0.80, 0.85, 0.65, 0.85),

        # Authority and control
        'authority': (0.40, 0.75, 0.90, 0.75),
        'autorité': (0.40, 0.78, 0.90, 0.75),
        'control': (0.35, 0.70, 0.90, 0.70),
        'contrôle': (0.35, 0.72, 0.90, 0.70),

        # Community
        'community': (0.90, 0.70, 0.65, 0.70),
        'communauté': (0.92, 0.70, 0.65, 0.70),
        'solidarity': (0.92, 0.75, 0.70, 0.75),
        'solidarité': (0.95, 0.75, 0.70, 0.75),

        # Courage
        'courage': (0.70, 0.75, 0.85, 0.70),

        # Truth
        'truth': (0.65, 0.95, 0.60, 0.85),
        'vérité': (0.65, 0.95, 0.60, 0.85),
    }

    @classmethod
    def analyze(cls, word: str, language: str) -> SemanticCoordinates:
        """Get LJPW coordinates for a word."""
        word_lower = word.lower()

        if word_lower in cls.PATTERNS:
            coords = cls.PATTERNS[word_lower]
            return SemanticCoordinates(
                word=word,
                language=language,
                L=coords[0],
                J=coords[1],
                P=coords[2],
                W=coords[3]
            )
        else:
            # Default neutral position
            return SemanticCoordinates(
                word=word,
                language=language,
                L=0.50, J=0.50, P=0.50, W=0.50
            )


# ============================================================================
# TRANSLATION PAIR ANALYZER
# ============================================================================

@dataclass
class TranslationPair:
    """A word and its translation."""
    english: str
    french: str
    en_coords: SemanticCoordinates
    fr_coords: SemanticCoordinates

    @property
    def semantic_shift(self) -> Tuple[float, float, float, float]:
        """Vector from English to French position."""
        return tuple(f - e for e, f in zip(self.en_coords.coords, self.fr_coords.coords))

    @property
    def shift_magnitude(self) -> float:
        """Distance between English and French semantic positions."""
        return LJPWCore.semantic_distance(self.en_coords.coords, self.fr_coords.coords)

    @property
    def is_isometric(self, threshold: float = 0.05) -> bool:
        """True if translation preserves semantic position."""
        return self.shift_magnitude < threshold

    @property
    def harmony_shift(self) -> float:
        """Change in harmony from English to French."""
        return self.fr_coords.harmony - self.en_coords.harmony

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'english': self.english,
            'french': self.french,
            'en_coords': asdict(self.en_coords),
            'fr_coords': asdict(self.fr_coords),
            'semantic_shift': {
                'L': self.semantic_shift[0],
                'J': self.semantic_shift[1],
                'P': self.semantic_shift[2],
                'W': self.semantic_shift[3],
            },
            'shift_magnitude': self.shift_magnitude,
            'is_isometric': self.is_isometric,
            'harmony_shift': self.harmony_shift,
        }


class RosettaStoneAnalyzer:
    """
    Analyzes translation pairs to discover geometric patterns.
    """

    def __init__(self):
        self.pairs: List[TranslationPair] = []

    def add_pair(self, english: str, french: str):
        """Add a translation pair to the analysis."""
        en_coords = SemanticAnalyzer.analyze(english, "en")
        fr_coords = SemanticAnalyzer.analyze(french, "fr")

        pair = TranslationPair(
            english=english,
            french=french,
            en_coords=en_coords,
            fr_coords=fr_coords
        )
        self.pairs.append(pair)

    def compute_statistics(self) -> Dict:
        """Compute aggregate statistics across all pairs."""
        if not self.pairs:
            return {}

        # Collect shifts
        shifts_L = [p.semantic_shift[0] for p in self.pairs]
        shifts_J = [p.semantic_shift[1] for p in self.pairs]
        shifts_P = [p.semantic_shift[2] for p in self.pairs]
        shifts_W = [p.semantic_shift[3] for p in self.pairs]

        # Calculate means and std devs
        def mean(lst): return sum(lst) / len(lst) if lst else 0
        def std(lst):
            if not lst:
                return 0
            m = mean(lst)
            return math.sqrt(sum((x - m)**2 for x in lst) / len(lst))

        avg_shift = (mean(shifts_L), mean(shifts_J), mean(shifts_P), mean(shifts_W))
        std_shift = (std(shifts_L), std(shifts_J), std(shifts_P), std(shifts_W))

        # Count isometric translations
        isometric_count = sum(1 for p in self.pairs if p.is_isometric)
        isometric_ratio = isometric_count / len(self.pairs)

        # Average shift magnitude
        avg_magnitude = mean([p.shift_magnitude for p in self.pairs])

        # Harmony statistics
        harmony_shifts = [p.harmony_shift for p in self.pairs]
        avg_harmony_shift = mean(harmony_shifts)

        return {
            'total_pairs': len(self.pairs),
            'average_shift': {
                'L': avg_shift[0],
                'J': avg_shift[1],
                'P': avg_shift[2],
                'W': avg_shift[3],
            },
            'std_dev_shift': {
                'L': std_shift[0],
                'J': std_shift[1],
                'P': std_shift[2],
                'W': std_shift[3],
            },
            'average_shift_magnitude': avg_magnitude,
            'isometric_count': isometric_count,
            'isometric_ratio': isometric_ratio,
            'average_harmony_shift': avg_harmony_shift,
        }

    def find_universal_concepts(self, threshold: float = 0.03) -> List[TranslationPair]:
        """Find concepts that are isometric (universal across languages)."""
        return [p for p in self.pairs if p.shift_magnitude < threshold]

    def find_cultural_divergences(self, threshold: float = 0.10) -> List[TranslationPair]:
        """Find concepts with large semantic shifts (cultural differences)."""
        return [p for p in self.pairs if p.shift_magnitude > threshold]

    def generate_report(self) -> Dict:
        """Generate comprehensive analysis report."""
        stats = self.compute_statistics()
        universals = self.find_universal_concepts()
        divergences = self.find_cultural_divergences()

        return {
            'statistics': stats,
            'universal_concepts': [p.to_dict() for p in universals],
            'cultural_divergences': [p.to_dict() for p in divergences],
            'all_pairs': [p.to_dict() for p in self.pairs],
        }


# ============================================================================
# MAIN EXPERIMENT
# ============================================================================

def run_rosetta_stone_experiment():
    """Main experiment runner."""
    print("=" * 80)
    print("LJPW TRANSLATION ROSETTA STONE EXPERIMENT")
    print("Discovering Universal Semantic Structures in English-French Translation")
    print("=" * 80)
    print()

    analyzer = RosettaStoneAnalyzer()

    # Add translation pairs
    translation_pairs = [
        ("love", "amour"),
        ("justice", "justice"),
        ("power", "pouvoir"),
        ("wisdom", "sagesse"),
        ("warmth", "chaleur"),
        ("tenderness", "tendresse"),
        ("compassion", "compassion"),
        ("law", "loi"),
        ("order", "ordre"),
        ("balance", "équilibre"),
        ("strength", "force"),
        ("might", "puissance"),
        ("energy", "énergie"),
        ("knowledge", "connaissance"),
        ("understanding", "compréhension"),
        ("insight", "perspicacité"),
        ("freedom", "liberté"),
        ("duty", "devoir"),
        ("honor", "honneur"),
        ("beauty", "beauté"),
        ("harmony", "harmonie"),
        ("authority", "autorité"),
        ("control", "contrôle"),
        ("community", "communauté"),
        ("solidarity", "solidarité"),
        ("truth", "vérité"),
    ]

    print(f"Analyzing {len(translation_pairs)} translation pairs...")
    print()

    for en, fr in translation_pairs:
        analyzer.add_pair(en, fr)

    # Generate report
    report = analyzer.generate_report()
    stats = report['statistics']

    # Display statistics
    print("AGGREGATE STATISTICS")
    print("-" * 80)
    print(f"Total pairs analyzed: {stats['total_pairs']}")
    print(f"Average shift magnitude: {stats['average_shift_magnitude']:.4f}")
    print(f"Isometric translations: {stats['isometric_count']} ({stats['isometric_ratio']*100:.1f}%)")
    print(f"Average harmony shift: {stats['average_harmony_shift']:.4f}")
    print()

    print("Average Translation Vector (English → French):")
    for dim in ['L', 'J', 'P', 'W']:
        avg = stats['average_shift'][dim]
        std = stats['std_dev_shift'][dim]
        sign = "+" if avg >= 0 else ""
        print(f"  {dim}: {sign}{avg:.4f} ± {std:.4f}")
    print()

    # Universal concepts
    print("UNIVERSAL CONCEPTS (Isometric: shift < 0.03)")
    print("-" * 80)
    universals = report['universal_concepts']
    if universals:
        for pair in universals:
            print(f"  {pair['english']:15s} ↔ {pair['french']:15s}  "
                  f"(shift: {pair['shift_magnitude']:.4f})")
    else:
        print("  None found with threshold < 0.03")
    print()

    # Cultural divergences
    print("CULTURAL DIVERGENCES (Non-isometric: shift > 0.10)")
    print("-" * 80)
    divergences = report['cultural_divergences']
    if divergences:
        for pair in divergences:
            en_h = pair['en_coords']['harmony']
            fr_h = pair['fr_coords']['harmony']
            print(f"  {pair['english']:15s} → {pair['french']:15s}")
            print(f"    Shift: {pair['shift_magnitude']:.4f}  "
                  f"Harmony: {en_h:.3f} → {fr_h:.3f}")
            print(f"    ΔL={pair['semantic_shift']['L']:+.3f}, "
                  f"ΔJ={pair['semantic_shift']['J']:+.3f}, "
                  f"ΔP={pair['semantic_shift']['P']:+.3f}, "
                  f"ΔW={pair['semantic_shift']['W']:+.3f}")
            print()
    else:
        print("  None found with threshold > 0.10")
    print()

    # Key findings
    print("KEY FINDINGS")
    print("-" * 80)

    avg_L = stats['average_shift']['L']
    avg_J = stats['average_shift']['J']
    avg_P = stats['average_shift']['P']
    avg_W = stats['average_shift']['W']

    findings = []

    if abs(avg_L) > 0.01:
        if avg_L > 0:
            findings.append(f"French emphasizes CONNECTION/UNITY more ({avg_L:+.3f} Love)")
        else:
            findings.append(f"English emphasizes CONNECTION/UNITY more ({avg_L:+.3f} Love shift to French)")

    if abs(avg_J) > 0.01:
        if avg_J > 0:
            findings.append(f"French emphasizes STRUCTURE/RULES more ({avg_J:+.3f} Justice)")
        else:
            findings.append(f"English emphasizes STRUCTURE/RULES more ({avg_J:+.3f} Justice shift to French)")

    if abs(avg_P) > 0.01:
        if avg_P > 0:
            findings.append(f"French emphasizes ACTION/FORCE more ({avg_P:+.3f} Power)")
        else:
            findings.append(f"English emphasizes ACTION/FORCE more ({avg_P:+.3f} Power shift to French)")

    if abs(avg_W) > 0.01:
        if avg_W > 0:
            findings.append(f"French emphasizes COMPLEXITY/NUANCE more ({avg_W:+.3f} Wisdom)")
        else:
            findings.append(f"English emphasizes COMPLEXITY/NUANCE more ({avg_W:+.3f} Wisdom shift to French)")

    if stats['isometric_ratio'] > 0.7:
        findings.append(f"Languages are HIGHLY SIMILAR in semantic structure ({stats['isometric_ratio']*100:.0f}% isometric)")
    elif stats['isometric_ratio'] > 0.4:
        findings.append(f"Languages show MODERATE similarity ({stats['isometric_ratio']*100:.0f}% isometric)")
    else:
        findings.append(f"Languages show SIGNIFICANT differences ({stats['isometric_ratio']*100:.0f}% isometric)")

    for i, finding in enumerate(findings, 1):
        print(f"{i}. {finding}")
    print()

    print("=" * 80)
    print("EXPERIMENT COMPLETE")
    print("=" * 80)

    # Save results
    output_file = "rosetta_stone_analysis.json"
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"\nDetailed results saved to: {output_file}")

    return report


if __name__ == "__main__":
    run_rosetta_stone_experiment()
