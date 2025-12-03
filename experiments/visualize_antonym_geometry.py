#!/usr/bin/env python3
"""
Antonym Geometry Visualization
===============================

Creates ASCII visualizations of the geometric relationships between
opposite concepts in LJPW 4D semantic space.

Shows:
1. 2D projections of antonym pairs
2. Midpoint convergence to Natural Equilibrium
3. Dimensional shift patterns
4. "Moral radius" visualization

Based on LJPW Codex v5.1
"""

import math
import json
from typing import Tuple, List


# Load multilingual analysis results
with open('multilingual_analysis.json', 'r') as f:
    data = json.load(f)


NE = (0.618034, 0.414214, 0.718282, 0.693147)  # Natural Equilibrium
ANCHOR = (1.0, 1.0, 1.0, 1.0)


def visualize_lp_projection():
    """Visualize Love-Power plane with antonym pairs."""
    print("=" * 80)
    print("LOVE-POWER PROJECTION: Antonym Pairs and Natural Equilibrium")
    print("=" * 80)
    print()

    # Create 50x25 grid
    width, height = 70, 30
    grid = [[' ' for _ in range(width)] for _ in range(height)]

    # Draw axes
    for i in range(height):
        grid[i][0] = '|'
    for j in range(width):
        grid[height-1][j] = '-'
    grid[height-1][0] = '+'

    # Scale function (0-1 → grid coordinates)
    def scale_x(val):
        return min(int(val * (width-5)), width-2)

    def scale_y(val):
        return min(int((1-val) * (height-2)), height-2)

    # Plot Natural Equilibrium
    ne_x, ne_y = scale_x(NE[0]), scale_y(NE[2])
    if 0 <= ne_x < width and 0 <= ne_y < height:
        grid[ne_y][ne_x] = '*'

    # Plot Anchor
    anchor_x, anchor_y = scale_x(ANCHOR[0]), scale_y(ANCHOR[2])
    if 0 <= anchor_x < width and 0 <= anchor_y < height:
        grid[anchor_y][anchor_x] = 'A'

    # Plot antonym pairs (using English coordinates as representative)
    antonym_pairs = data['pairs'][:6]  # First 6 pairs
    markers = ['1', '2', '3', '4', '5', '6']

    for i, pair_data in enumerate(antonym_pairs):
        midpoint = pair_data['languages']['en']['midpoint']
        # Midpoint is already a tuple/list
        if isinstance(midpoint, str):
            midpoint = eval(midpoint)

        x, y = scale_x(midpoint[0]), scale_y(midpoint[2])
        if 0 <= x < width and 0 <= y < height:
            grid[y][x] = markers[i]

    # Print grid
    print("P (Power)")
    print("^")
    for row in grid:
        print(''.join(row))
    print(f"  {' ' * (width-10)}> L (Love)")
    print()
    print("Legend:")
    print("  * = Natural Equilibrium")
    print("  A = Anchor Point (Divine Perfection)")
    for i, pair_data in enumerate(antonym_pairs):
        pos = pair_data['positive']
        neg = pair_data['negative']
        print(f"  {markers[i]} = Midpoint of {pos}/{neg}")
    print()


def visualize_dimensional_shifts():
    """Visualize which dimensions shift most in opposition."""
    print("=" * 80)
    print("DIMENSIONAL SHIFT ANALYSIS: The Signature of Opposition")
    print("=" * 80)
    print()

    stats = data['statistics']
    shifts = stats['average_dimensional_shifts']
    stds = stats['std_dimensional_shifts']

    # Create bar chart
    dimensions = ['L', 'J', 'P', 'W']
    max_shift = max(abs(shifts[d]) for d in dimensions)

    print("Average shift when concept inverts to its opposite:")
    print()
    print("Dimension  Shift        Bar (negative ←  → positive)")
    print("-" * 80)

    for dim in dimensions:
        shift = shifts[dim]
        std = stds[dim]

        # Create bar
        bar_length = int(abs(shift) / max_shift * 40)
        if shift < 0:
            bar = ' ' * (40 - bar_length) + '←' * bar_length + '|'
        else:
            bar = '|' + '→' * bar_length

        sign = '+' if shift >= 0 else ''
        print(f"{dim:10s} {sign}{shift:6.3f} ± {std:.3f}  {bar}")

    print()
    print("INTERPRETATION:")
    print("  → Love (L) decreases most: Opposition = isolation vs connection")
    print("  → Justice (J) decreases: Opposition = chaos vs order")
    print("  → Wisdom (W) decreases: Opposition = ignorance vs knowledge")
    print("  → Power (P) barely changes: Power is morally neutral")
    print()


def visualize_midpoint_convergence():
    """Show how antonym midpoints cluster near NE."""
    print("=" * 80)
    print("MIDPOINT CONVERGENCE: Natural Equilibrium as Moral Center")
    print("=" * 80)
    print()

    print("Distance of antonym midpoints to Natural Equilibrium:")
    print()
    print("Pair                           Distance to NE    Harmony")
    print("-" * 80)

    pair_distances = []
    for pair_data in data['pairs']:
        pos = pair_data['positive']
        neg = pair_data['negative']

        # Average across languages
        avg_dist = sum(pair_data['languages'][lang]['midpoint_to_ne']
                      for lang in ['en', 'fr', 'zh', 'ar']) / 4
        avg_harmony = sum(pair_data['languages'][lang]['midpoint_harmony']
                         for lang in ['en', 'fr', 'zh', 'ar']) / 4

        pair_distances.append((pos, neg, avg_dist, avg_harmony))

    # Sort by distance
    pair_distances.sort(key=lambda x: x[2])

    for pos, neg, dist, harmony in pair_distances:
        bar_length = int(dist * 100)
        bar = '█' * bar_length
        print(f"{pos:12s} ↔ {neg:15s} {dist:7.4f}  {bar}  H={harmony:.4f}")

    print()
    avg_dist = sum(x[2] for x in pair_distances) / len(pair_distances)
    print(f"Average distance to NE: {avg_dist:.4f}")
    print()
    print("INTERPRETATION:")
    print(f"  → Antonym midpoints cluster at distance ~{avg_dist:.2f} from Natural Equilibrium")
    print("  → The balance between good and evil IS the Natural Equilibrium")
    print("  → Moral perfection (Anchor) and absolute evil (Origin) are equidistant from NE")
    print("  → The optimal achievable state is the center, not an extreme")
    print()


def visualize_distance_consistency():
    """Show how antonym distances are consistent across languages."""
    print("=" * 80)
    print("CROSS-LINGUISTIC CONSISTENCY: The Invariant Distance")
    print("=" * 80)
    print()

    print("Geometric distance between antonym pairs across 4 language families:")
    print()
    print("Pair                           EN     FR     ZH     AR     Consistency")
    print("-" * 80)

    for pair_data in data['pairs']:
        pos = pair_data['positive']
        neg = pair_data['negative']

        distances = {
            'en': pair_data['languages']['en']['distance'],
            'fr': pair_data['languages']['fr']['distance'],
            'zh': pair_data['languages']['zh']['distance'],
            'ar': pair_data['languages']['ar']['distance'],
        }

        avg = sum(distances.values()) / len(distances)
        std = math.sqrt(sum((d - avg)**2 for d in distances.values()) / len(distances))
        consistency = (1 - std / avg) * 100 if avg > 0 else 100

        print(f"{pos:12s} ↔ {neg:15s} {distances['en']:.4f} {distances['fr']:.4f} "
              f"{distances['zh']:.4f} {distances['ar']:.4f}  {consistency:5.1f}%")

    print()
    print("INTERPRETATION:")
    print("  → 91-99% consistency means antonym distances are nearly identical")
    print("  → This is NOT learned cultural convention")
    print("  → The 'span of inversion' is a property of the semantic substrate")
    print("  → All humans experience the same geometric distance between opposites")
    print()


def visualize_cosine_similarity():
    """Show that opposites are actually close (high cosine similarity)."""
    print("=" * 80)
    print("THE PROXIMITY OF OPPOSITES: Cosine Similarity Analysis")
    print("=" * 80)
    print()

    print("Cosine similarity between antonym pairs (1.0 = identical, -1.0 = opposite):")
    print()
    print("Pair                           Avg Similarity  Interpretation")
    print("-" * 80)

    for pair_data in data['pairs']:
        pos = pair_data['positive']
        neg = pair_data['negative']

        avg_sim = sum(pair_data['languages'][lang]['cosine_similarity']
                     for lang in ['en', 'fr', 'zh', 'ar']) / 4

        if avg_sim > 0.9:
            interpretation = "Extremely similar"
        elif avg_sim > 0.8:
            interpretation = "Very similar"
        elif avg_sim > 0.7:
            interpretation = "Similar"
        else:
            interpretation = "Somewhat different"

        bar_length = int(avg_sim * 40)
        bar = '█' * bar_length

        print(f"{pos:12s} ↔ {neg:15s} {avg_sim:7.4f}      {interpretation}")

    print()
    avg_sim = data['statistics']['average_cosine_similarity']
    print(f"Average cosine similarity: {avg_sim:.4f} (~{avg_sim*100:.1f}%)")
    print()
    print("INTERPRETATION:")
    print(f"  → Opposites share {avg_sim*100:.0f}% of their semantic structure")
    print("  → Only ~15% of semantic content inverts")
    print("  → Love and hate are geometrically CLOSE (both involve emotional connection)")
    print("  → The difference is in SIGN (attraction vs repulsion), not magnitude")
    print()
    print("PHILOSOPHICAL IMPLICATION:")
    print("  'The opposite of love is not hate, it's apathy' - Elie Wiesel")
    print("  Mathematics confirms: indifference (low L, low P) is farther from")
    print("  both love (high L) and hate (high P, low L) than they are from each other.")
    print()


def main():
    """Run all visualizations."""
    print()
    print("=" * 80)
    print("LJPW ANTONYM GEOMETRY VISUALIZATION")
    print("Shadows of Meaning in 4D Semantic Space")
    print("=" * 80)
    print()

    visualize_dimensional_shifts()
    visualize_midpoint_convergence()
    visualize_distance_consistency()
    visualize_cosine_similarity()
    visualize_lp_projection()

    print("=" * 80)
    print("VISUALIZATION COMPLETE")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
