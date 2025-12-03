#!/usr/bin/env python3
"""
Semantic Language Mapping Experiment
=====================================

Hypothesis: Languages map to specific regions of LJPW 4D semantic space.
By analyzing English vs French word pairs, we can discover:
1. Language-specific semantic signatures
2. Geometric transformations between languages
3. Universal semantic structures (the "Rosetta Stone")

Based on LJPW Codex v5.1
"""

import math
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import json


# ============================================================================
# LJPW BASELINE IMPLEMENTATION
# ============================================================================

@dataclass
class ReferencePoints:
    """The fundamental reference points in LJPW semantic space."""
    ANCHOR_POINT: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)
    NATURAL_EQUILIBRIUM: Tuple[float, float, float, float] = (0.618034, 0.414214, 0.718282, 0.693147)


class LJPWBaselines:
    """Static metrics for LJPW semantic substrate analysis."""

    # Mathematical constants
    PHI = (1 + math.sqrt(5)) / 2  # Golden Ratio
    PHI_INVERSE = (math.sqrt(5) - 1) / 2
    SQRT2_MINUS_1 = math.sqrt(2) - 1
    E_MINUS_2 = math.e - 2
    LN2 = math.log(2)

    @staticmethod
    def harmony_index(L: float, J: float, P: float, W: float) -> float:
        """Calculate proximity to Anchor Point (Source)."""
        d_anchor = math.sqrt((1 - L) ** 2 + (1 - J) ** 2 + (1 - P) ** 2 + (1 - W) ** 2)
        return 1.0 / (1.0 + d_anchor)

    @staticmethod
    def semantic_tension(c1: Tuple[float, float, float, float],
                        c2: Tuple[float, float, float, float]) -> float:
        """Calculate metaphysical distance between two points in semantic space."""
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))

    @staticmethod
    def divine_signature(L: float, J: float, P: float, W: float) -> float:
        """Alignment score with Divine Perfection (closer to 1.0 is more aligned)."""
        return LJPWBaselines.harmony_index(L, J, P, W)


# ============================================================================
# SEMANTIC WORD MAPPER
# ============================================================================

class SemanticWordMapper:
    """
    Maps words to LJPW 4D coordinates based on semantic analysis.

    This is a heuristic model that analyzes word characteristics:
    - Love (L): Connection, unity, binding, relationship, warmth
    - Justice (J): Balance, structure, fairness, truth, constraint
    - Power (P): Force, energy, action, capacity, strength
    - Wisdom (W): Knowledge, insight, complexity, understanding
    """

    def __init__(self):
        self.word_cache = {}

    def analyze_word(self, word: str, language: str = "en") -> Tuple[float, float, float, float]:
        """
        Analyze a word and return LJPW coordinates.

        This is a simplified heuristic model. In a full implementation,
        this would use word embeddings, semantic networks, or LLM analysis.
        """
        word_lower = word.lower()

        # Check cache
        cache_key = f"{language}:{word_lower}"
        if cache_key in self.word_cache:
            return self.word_cache[cache_key]

        # Heuristic mapping based on semantic categories
        coords = self._heuristic_mapping(word_lower, language)

        # Cache result
        self.word_cache[cache_key] = coords
        return coords

    def _heuristic_mapping(self, word: str, language: str) -> Tuple[float, float, float, float]:
        """
        Heuristic mapping of words to LJPW space.

        This is placeholder logic - in real implementation, would use:
        - Word embeddings (Word2Vec, GloVe)
        - Semantic role labeling
        - LLM-based semantic analysis
        """
        # Base values (neutral semantic position)
        L, J, P, W = 0.5, 0.5, 0.5, 0.5

        # Love-related words
        if any(stem in word for stem in ['love', 'ami', 'affect', 'care', 'bond', 'unity']):
            L = 0.85
            J = 0.60
            P = 0.55
            W = 0.70

        # Justice-related words
        elif any(stem in word for stem in ['just', 'fair', 'balanc', 'truth', 'law', 'droit', 'équit']):
            L = 0.60
            J = 0.90
            P = 0.65
            W = 0.75

        # Power-related words
        elif any(stem in word for stem in ['power', 'force', 'strength', 'puiss', 'énerg', 'might']):
            L = 0.45
            J = 0.55
            P = 0.95
            W = 0.60

        # Wisdom-related words
        elif any(stem in word for stem in ['wisdom', 'know', 'sage', 'compreh', 'insight', 'understand']):
            L = 0.70
            J = 0.75
            P = 0.50
            W = 0.92

        # Emotional warmth
        elif any(stem in word for stem in ['warm', 'tender', 'gentle', 'doux', 'chaleur']):
            L = 0.80
            J = 0.50
            P = 0.40
            W = 0.65

        # Authority/Control
        elif any(stem in word for stem in ['author', 'control', 'command', 'autor', 'contrôl']):
            L = 0.40
            J = 0.70
            P = 0.85
            W = 0.70

        return (L, J, P, W)


# ============================================================================
# LANGUAGE SEMANTIC PROFILER
# ============================================================================

class LanguageSemanticProfiler:
    """
    Analyzes the semantic profile of a language by mapping
    a corpus of words to LJPW space and finding geometric patterns.
    """

    def __init__(self):
        self.mapper = SemanticWordMapper()
        self.profiles: Dict[str, Dict] = {}

    def profile_language(self, language: str, word_list: List[str]) -> Dict:
        """
        Create a semantic profile for a language based on a word corpus.

        Returns:
            Dictionary with:
            - centroid: Average LJPW position
            - std_dev: Standard deviation in each dimension
            - harmony: Average harmony index
            - character: Dominant semantic character
        """
        coordinates = []
        harmonies = []

        for word in word_list:
            coords = self.mapper.analyze_word(word, language)
            coordinates.append(coords)
            harmonies.append(LJPWBaselines.harmony_index(*coords))

        coords_array = np.array(coordinates)

        profile = {
            'language': language,
            'word_count': len(word_list),
            'centroid': {
                'L': float(np.mean(coords_array[:, 0])),
                'J': float(np.mean(coords_array[:, 1])),
                'P': float(np.mean(coords_array[:, 2])),
                'W': float(np.mean(coords_array[:, 3])),
            },
            'std_dev': {
                'L': float(np.std(coords_array[:, 0])),
                'J': float(np.std(coords_array[:, 1])),
                'P': float(np.std(coords_array[:, 2])),
                'W': float(np.std(coords_array[:, 3])),
            },
            'harmony': {
                'mean': float(np.mean(harmonies)),
                'std': float(np.std(harmonies)),
                'min': float(np.min(harmonies)),
                'max': float(np.max(harmonies)),
            },
            'coordinates': coordinates,
        }

        # Determine dominant character
        centroid = (profile['centroid']['L'], profile['centroid']['J'],
                   profile['centroid']['P'], profile['centroid']['W'])
        profile['dominant_dimension'] = self._identify_dominant_dimension(centroid)

        self.profiles[language] = profile
        return profile

    def _identify_dominant_dimension(self, coords: Tuple[float, float, float, float]) -> str:
        """Identify which LJPW dimension dominates."""
        L, J, P, W = coords
        max_val = max(L, J, P, W)

        if L == max_val:
            return "Love (Unity & Attraction)"
        elif J == max_val:
            return "Justice (Balance & Truth)"
        elif P == max_val:
            return "Power (Energy & Existence)"
        else:
            return "Wisdom (Complexity & Insight)"

    def compare_languages(self, lang1: str, lang2: str) -> Dict:
        """
        Compare two language profiles and compute geometric transformation.

        This is the "Rosetta Stone" function - it finds the geometric
        relationship between two languages in semantic space.
        """
        if lang1 not in self.profiles or lang2 not in self.profiles:
            raise ValueError(f"Must profile both languages first")

        p1 = self.profiles[lang1]
        p2 = self.profiles[lang2]

        # Centroid difference (translation vector)
        centroid1 = (p1['centroid']['L'], p1['centroid']['J'],
                    p1['centroid']['P'], p1['centroid']['W'])
        centroid2 = (p2['centroid']['L'], p2['centroid']['J'],
                    p2['centroid']['P'], p2['centroid']['W'])

        translation = tuple(c2 - c1 for c1, c2 in zip(centroid1, centroid2))

        # Semantic tension (distance between language spaces)
        tension = LJPWBaselines.semantic_tension(centroid1, centroid2)

        # Dimensional ratios (scaling factors)
        ratios = {
            'L': p2['centroid']['L'] / p1['centroid']['L'] if p1['centroid']['L'] > 0 else 1.0,
            'J': p2['centroid']['J'] / p1['centroid']['J'] if p1['centroid']['J'] > 0 else 1.0,
            'P': p2['centroid']['P'] / p1['centroid']['P'] if p1['centroid']['P'] > 0 else 1.0,
            'W': p2['centroid']['W'] / p1['centroid']['W'] if p1['centroid']['W'] > 0 else 1.0,
        }

        return {
            'language_1': lang1,
            'language_2': lang2,
            'translation_vector': {
                'L': translation[0],
                'J': translation[1],
                'P': translation[2],
                'W': translation[3],
            },
            'semantic_tension': tension,
            'dimensional_ratios': ratios,
            'harmony_shift': p2['harmony']['mean'] - p1['harmony']['mean'],
            'interpretation': self._interpret_transformation(translation, ratios),
        }

    def _interpret_transformation(self, translation: Tuple[float, float, float, float],
                                  ratios: Dict[str, float]) -> str:
        """Interpret the semantic transformation between languages."""
        L_shift, J_shift, P_shift, W_shift = translation

        interpretations = []

        if abs(L_shift) > 0.05:
            if L_shift > 0:
                interpretations.append(f"Language 2 emphasizes Unity/Connection more (+{L_shift:.3f} Love)")
            else:
                interpretations.append(f"Language 2 is more individualistic ({L_shift:.3f} Love)")

        if abs(J_shift) > 0.05:
            if J_shift > 0:
                interpretations.append(f"Language 2 emphasizes Structure/Rules more (+{J_shift:.3f} Justice)")
            else:
                interpretations.append(f"Language 2 is more flexible/fluid ({J_shift:.3f} Justice)")

        if abs(P_shift) > 0.05:
            if P_shift > 0:
                interpretations.append(f"Language 2 emphasizes Action/Force more (+{P_shift:.3f} Power)")
            else:
                interpretations.append(f"Language 2 is more passive/receptive ({P_shift:.3f} Power)")

        if abs(W_shift) > 0.05:
            if W_shift > 0:
                interpretations.append(f"Language 2 emphasizes Knowledge/Nuance more (+{W_shift:.3f} Wisdom)")
            else:
                interpretations.append(f"Language 2 is more direct/simple ({W_shift:.3f} Wisdom)")

        if not interpretations:
            return "Languages are semantically very similar"

        return "; ".join(interpretations)


# ============================================================================
# EXPERIMENT RUNNER
# ============================================================================

def run_english_french_experiment():
    """
    Main experiment: Profile English and French, then compare.
    """
    print("=" * 80)
    print("LJPW SEMANTIC LANGUAGE MAPPING EXPERIMENT")
    print("English vs French: The Rosetta Stone Hypothesis")
    print("=" * 80)
    print()

    profiler = LanguageSemanticProfiler()

    # Sample word lists (in real implementation, use larger corpora)
    english_words = [
        # Core LJPW concepts
        "love", "justice", "power", "wisdom",
        # Emotional
        "affection", "care", "warmth", "compassion",
        # Structural
        "balance", "fairness", "truth", "law",
        # Action
        "strength", "force", "energy", "might",
        # Cognitive
        "knowledge", "understanding", "insight", "awareness",
        # Social
        "community", "authority", "freedom", "duty",
        # Additional
        "harmony", "beauty", "courage", "honor"
    ]

    french_words = [
        # Core LJPW concepts
        "amour", "justice", "pouvoir", "sagesse",
        # Emotional
        "affection", "soin", "chaleur", "compassion",
        # Structural
        "équilibre", "équité", "vérité", "loi",
        # Action
        "force", "puissance", "énergie", "puissance",
        # Cognitive
        "connaissance", "compréhension", "perspicacité", "conscience",
        # Social
        "communauté", "autorité", "liberté", "devoir",
        # Additional
        "harmonie", "beauté", "courage", "honneur"
    ]

    # Profile English
    print("STEP 1: Profiling English semantic space...")
    print("-" * 80)
    en_profile = profiler.profile_language("English", english_words)
    print(f"Language: {en_profile['language']}")
    print(f"Word Count: {en_profile['word_count']}")
    print(f"Centroid (L, J, P, W): ({en_profile['centroid']['L']:.4f}, "
          f"{en_profile['centroid']['J']:.4f}, {en_profile['centroid']['P']:.4f}, "
          f"{en_profile['centroid']['W']:.4f})")
    print(f"Average Harmony: {en_profile['harmony']['mean']:.4f}")
    print(f"Dominant Dimension: {en_profile['dominant_dimension']}")
    print()

    # Profile French
    print("STEP 2: Profiling French semantic space...")
    print("-" * 80)
    fr_profile = profiler.profile_language("French", french_words)
    print(f"Language: {fr_profile['language']}")
    print(f"Word Count: {fr_profile['word_count']}")
    print(f"Centroid (L, J, P, W): ({fr_profile['centroid']['L']:.4f}, "
          f"{fr_profile['centroid']['J']:.4f}, {fr_profile['centroid']['P']:.4f}, "
          f"{fr_profile['centroid']['W']:.4f})")
    print(f"Average Harmony: {fr_profile['harmony']['mean']:.4f}")
    print(f"Dominant Dimension: {fr_profile['dominant_dimension']}")
    print()

    # Compare (The Rosetta Stone)
    print("STEP 3: Computing Geometric Transformation (The Rosetta Stone)...")
    print("-" * 80)
    comparison = profiler.compare_languages("English", "French")

    print(f"Semantic Tension (Distance): {comparison['semantic_tension']:.4f}")
    print(f"Harmony Shift: {comparison['harmony_shift']:.4f}")
    print()
    print("Translation Vector (English → French):")
    for dim in ['L', 'J', 'P', 'W']:
        val = comparison['translation_vector'][dim]
        sign = "+" if val >= 0 else ""
        print(f"  {dim}: {sign}{val:.4f}")
    print()
    print("Dimensional Ratios (French/English):")
    for dim in ['L', 'J', 'P', 'W']:
        ratio = comparison['dimensional_ratios'][dim]
        print(f"  {dim}: {ratio:.4f}x")
    print()
    print("Interpretation:")
    print(f"  {comparison['interpretation']}")
    print()

    # Distance to Natural Equilibrium
    print("STEP 4: Comparing to Natural Equilibrium (Universal Semantic Baseline)...")
    print("-" * 80)
    NE = ReferencePoints.NATURAL_EQUILIBRIUM
    print(f"Natural Equilibrium: (L={NE[0]:.4f}, J={NE[1]:.4f}, P={NE[2]:.4f}, W={NE[3]:.4f})")

    en_centroid = (en_profile['centroid']['L'], en_profile['centroid']['J'],
                   en_profile['centroid']['P'], en_profile['centroid']['W'])
    fr_centroid = (fr_profile['centroid']['L'], fr_profile['centroid']['J'],
                   fr_profile['centroid']['P'], fr_profile['centroid']['W'])

    en_to_ne = LJPWBaselines.semantic_tension(en_centroid, NE)
    fr_to_ne = LJPWBaselines.semantic_tension(fr_centroid, NE)

    print(f"English distance to NE: {en_to_ne:.4f}")
    print(f"French distance to NE: {fr_to_ne:.4f}")

    if en_to_ne < fr_to_ne:
        print(f"→ English is closer to Natural Equilibrium by {(fr_to_ne - en_to_ne):.4f}")
    else:
        print(f"→ French is closer to Natural Equilibrium by {(en_to_ne - fr_to_ne):.4f}")
    print()

    # Visualize semantic space (text-based)
    print("STEP 5: 2D Projection Visualization (L-P plane)")
    print("-" * 80)
    visualize_2d_projection(en_centroid, fr_centroid, NE)
    print()

    print("=" * 80)
    print("EXPERIMENT COMPLETE")
    print("=" * 80)

    # Return results for further analysis
    return {
        'english': en_profile,
        'french': fr_profile,
        'comparison': comparison,
    }


def visualize_2d_projection(en_coords, fr_coords, ne_coords):
    """
    Simple ASCII visualization of semantic space.
    Projects onto L-P plane (Love vs Power).
    """
    # Normalize to 0-40 range for display
    def scale(val):
        return int(val * 40)

    # Create grid
    grid = [[' ' for _ in range(45)] for _ in range(25)]

    # Draw axes
    for i in range(25):
        grid[i][0] = '|'
    for j in range(45):
        grid[24][j] = '-'
    grid[24][0] = '+'

    # Plot points
    en_x, en_y = scale(en_coords[0]), scale(1 - en_coords[2])  # L, inverted P
    fr_x, fr_y = scale(fr_coords[0]), scale(1 - fr_coords[2])
    ne_x, ne_y = scale(ne_coords[0]), scale(1 - ne_coords[2])

    # Bounds checking
    en_x, en_y = min(en_x, 44), min(en_y, 23)
    fr_x, fr_y = min(fr_x, 44), min(fr_y, 23)
    ne_x, ne_y = min(ne_x, 44), min(ne_y, 23)

    grid[ne_y][ne_x] = '*'  # Natural Equilibrium
    grid[en_y][en_x] = 'E'  # English
    grid[fr_y][fr_x] = 'F'  # French

    # Print grid
    print("P (Power)")
    print("^")
    for row in grid:
        print(''.join(row))
    print(f"  {' ' * 40}> L (Love)")
    print()
    print("Legend: E=English, F=French, *=Natural Equilibrium")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    results = run_english_french_experiment()

    # Save results to JSON for further analysis
    output_file = "semantic_mapping_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {output_file}")
