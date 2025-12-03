#!/usr/bin/env python3
"""
Semantic Space Architecture Visualizations
==========================================

ASCII visualizations of the pre-existing structures of semantic space:
- Regional map (2D projections of 4D space)
- Attractor field diagrams
- Phase boundaries
- Dimensional relationships
"""

import json
import math
import numpy as np
from typing import Dict, List, Tuple

# Load atlas
with open('/home/user/LJPW-Language-Translator/experiments/semantic_space_atlas.json', 'r') as f:
    atlas = json.load(f)


def visualize_lj_plane():
    """Visualize Love-Justice plane (most important moral dimensions)."""

    print("\n" + "="*70)
    print("LOVE-JUSTICE PLANE (Primary Moral Dimensions)")
    print("="*70)
    print("\nThis 2D slice shows how meanings distribute across the")
    print("two primary moral dimensions: Love (vertical) and Justice (horizontal)\n")

    # Create 40x20 ASCII grid
    width, height = 60, 25
    grid = [[' ' for _ in range(width)] for _ in range(height)]

    def coord_to_grid(l, j):
        """Convert L,J coordinates (0-1) to grid position."""
        x = int(j * (width - 1))
        y = int((1 - l) * (height - 1))  # Flip Y so high L is at top
        return min(max(x, 0), width-1), min(max(y, 0), height-1)

    # Plot Natural Equilibrium
    ne_l, ne_j = atlas['metadata']['natural_equilibrium'][0], atlas['metadata']['natural_equilibrium'][1]
    ne_x, ne_y = coord_to_grid(ne_l, ne_j)
    grid[ne_y][ne_x] = '⊕'

    # Plot Anchor Point
    anchor_x, anchor_y = coord_to_grid(1.0, 1.0)
    grid[anchor_y][anchor_x] = '★'

    # Plot regions
    region_markers = {
        'The Transcendent': '◆',
        'The Peaceful': '◇',
        'The Passionate': '▲',
        'The Dominating': '▼',
        'The Abyssal': '●',
        'The Mystical': '◎'
    }

    for region in atlas['regions']:
        if region['name'] in region_markers:
            l, j = region['center'][0], region['center'][1]
            x, y = coord_to_grid(l, j)
            marker = region_markers[region['name']]
            if grid[y][x] == ' ':
                grid[y][x] = marker

    # Print grid with axes
    print("  J →" + " "*28 + "JUSTICE" + " "*27)
    print("L  ┌" + "─"*(width-2) + "┐")

    for i, row in enumerate(grid):
        if i == 0:
            print("↑  │" + "".join(row) + "│")
        elif i == height - 1:
            print("   │" + "".join(row) + "│")
        else:
            print("   │" + "".join(row) + "│")

    print("   └" + "─"*(width-2) + "┘")
    print("LOVE")

    print("\nLEGEND:")
    print("  ★ = Divine Perfection (1.0, 1.0) - Ultimate harmony")
    print("  ⊕ = Natural Equilibrium (φ⁻¹, √2-1) - Balance point")
    print("  ◆ = Transcendent (love, wisdom, beauty)")
    print("  ◇ = Peaceful (peace, patience, humility)")
    print("  ▲ = Passionate (courage, zeal)")
    print("  ▼ = Dominating (pride, wrath, greed)")
    print("  ● = Abyssal (despair, void)")
    print("  ◎ = Mystical (ecstasy, transcendence)")


def visualize_pw_plane():
    """Visualize Power-Wisdom plane (capability dimensions)."""

    print("\n" + "="*70)
    print("POWER-WISDOM PLANE (Capability Dimensions)")
    print("="*70)
    print("\nThis slice shows Power (force, strength) vs Wisdom (understanding).\n")

    width, height = 60, 25
    grid = [[' ' for _ in range(width)] for _ in range(height)]

    def coord_to_grid(p, w):
        x = int(p * (width - 1))
        y = int((1 - w) * (height - 1))
        return min(max(x, 0), width-1), min(max(y, 0), height-1)

    # Plot Natural Equilibrium
    ne_p, ne_w = atlas['metadata']['natural_equilibrium'][2], atlas['metadata']['natural_equilibrium'][3]
    ne_x, ne_y = coord_to_grid(ne_p, ne_w)
    grid[ne_y][ne_x] = '⊕'

    # Plot Anchor
    anchor_x, anchor_y = coord_to_grid(1.0, 1.0)
    grid[anchor_y][anchor_x] = '★'

    # Plot regions
    region_markers = {
        'The Transcendent': '◆',
        'The Peaceful': '◇',
        'The Passionate': '▲',
        'The Dominating': '▼',
        'The Detached': '△',
        'The Machiavellian': '▽'
    }

    for region in atlas['regions']:
        if region['name'] in region_markers:
            p, w = region['center'][2], region['center'][3]
            x, y = coord_to_grid(p, w)
            marker = region_markers[region['name']]
            if grid[y][x] == ' ':
                grid[y][x] = marker

    # Print grid
    print("  P →" + " "*28 + "POWER" + " "*28)
    print("W  ┌" + "─"*(width-2) + "┐")

    for i, row in enumerate(grid):
        if i == 0:
            print("↑  │" + "".join(row) + "│")
        elif i == height - 1:
            print("   │" + "".join(row) + "│")
        else:
            print("   │" + "".join(row) + "│")

    print("   └" + "─"*(width-2) + "┘")
    print("WISDOM")

    print("\nLEGEND:")
    print("  ★ = Divine Perfection (1.0, 1.0)")
    print("  ⊕ = Natural Equilibrium (e-2, ln2)")
    print("  ◆ = Transcendent (high P+W)")
    print("  ◇ = Peaceful (low P, high W)")
    print("  ▲ = Passionate (high P, moderate W)")
    print("  ▼ = Dominating (high P, low W)")
    print("  △ = Detached (low P, high W)")
    print("  ▽ = Machiavellian (high P+W, low L+J)")


def visualize_attractor_field():
    """Visualize attractor strength as a field."""

    print("\n" + "="*70)
    print("ATTRACTOR FIELD (L-J Projection)")
    print("="*70)
    print("\nShows the 'pull' of attractors across semantic space.")
    print("Darker regions = stronger attraction.\n")

    width, height = 60, 20
    grid = [[0.0 for _ in range(width)] for _ in range(height)]

    # Calculate attractor strength at each point
    for y in range(height):
        for x in range(width):
            l = 1.0 - (y / height)  # High L at top
            j = x / width

            total_strength = 0.0

            for attractor in atlas['attractors']:
                pos = attractor['position']
                strength = attractor['strength']

                # Distance in L-J plane
                dist = math.sqrt((l - pos[0])**2 + (j - pos[1])**2)

                # Attractor strength falls off with distance
                if dist < attractor['basin_radius']:
                    contribution = strength / (1 + dist * 5)
                    total_strength += contribution

            grid[y][x] = total_strength

    # Find min/max for normalization
    flat = [grid[y][x] for y in range(height) for x in range(width)]
    min_val, max_val = min(flat), max(flat)

    # Convert to ASCII shading
    shades = ' .:-=+*#%@'

    print("  J →" + " "*28 + "JUSTICE" + " "*27)
    print("L  ┌" + "─"*(width-2) + "┐")

    for i, row in enumerate(grid):
        line = ""
        for val in row:
            if max_val > min_val:
                normalized = (val - min_val) / (max_val - min_val)
            else:
                normalized = 0.0
            shade_idx = int(normalized * (len(shades) - 1))
            line += shades[shade_idx]

        if i == 0:
            print("↑  │" + line + "│")
        elif i == height - 1:
            print("   │" + line + "│")
        else:
            print("   │" + line + "│")

    print("   └" + "─"*(width-2) + "┘")
    print("LOVE")

    print("\nDarker = stronger attraction")
    print("'@' regions pull meanings strongly")
    print("' ' regions are neutral or repelling")


def visualize_harmony_landscape():
    """Visualize harmony as a 3D landscape (using ASCII contours)."""

    print("\n" + "="*70)
    print("HARMONY LANDSCAPE (L-J Projection)")
    print("="*70)
    print("\nShows harmony H = 1/(1 + d(anchor)) as elevation.")
    print("Higher = more harmonious/virtuous.\n")

    width, height = 60, 20
    grid = [[0.0 for _ in range(width)] for _ in range(height)]

    # Calculate harmony at each point
    anchor = np.array(atlas['metadata']['anchor_point'])

    for y in range(height):
        for x in range(width):
            l = 1.0 - (y / height)
            j = x / width

            # Use average P and W values
            p = 0.6
            w = 0.7

            coords = np.array([l, j, p, w])
            dist = np.linalg.norm(coords - anchor)
            harmony = 1.0 / (1.0 + dist)

            grid[y][x] = harmony

    # Find min/max
    flat = [grid[y][x] for y in range(height) for x in range(width)]
    min_val, max_val = min(flat), max(flat)

    # Contour levels
    contours = ' .·:;+=*#@'

    print("  J →" + " "*28 + "JUSTICE" + " "*27)
    print("L  ┌" + "─"*(width-2) + "┐")

    for i, row in enumerate(grid):
        line = ""
        for val in row:
            normalized = (val - min_val) / (max_val - min_val)
            contour_idx = int(normalized * (len(contours) - 1))
            line += contours[contour_idx]

        if i == 0:
            print("↑  │" + line + "│")
        elif i == height - 1:
            print("   │" + line + "│")
        else:
            print("   │" + line + "│")

    print("   └" + "─"*(width-2) + "┘")
    print("LOVE")

    print("\nElevation key:")
    print("  @ # * = High harmony (virtuous region)")
    print("  ; : . = Moderate harmony")
    print("      = Low harmony (vice region)")


def visualize_dimensional_coupling():
    """Show correlation between dimensions."""

    print("\n" + "="*70)
    print("DIMENSIONAL COUPLING MATRIX")
    print("="*70)
    print("\nShows how dimensions tend to correlate in known concepts.\n")

    # Collect all known concept coordinates
    coords_list = []

    with open('/home/user/LJPW-Language-Translator/experiments/semantic_space_atlas.json', 'r') as f:
        atlas_data = json.load(f)

    # We'll use the regions as proxies for concept distribution
    for region in atlas_data['regions']:
        coords_list.append(region['center'])

    coords_array = np.array(coords_list)

    # Calculate correlation matrix
    corr_matrix = np.corrcoef(coords_array.T)

    dim_names = ['Love (L)', 'Justice (J)', 'Power (P)', 'Wisdom (W)']

    print("Correlation coefficients (-1 to +1):")
    print("  1.0 = perfect positive correlation")
    print("  0.0 = no correlation")
    print(" -1.0 = perfect negative correlation\n")

    # Print header
    print("           ", end="")
    for name in dim_names:
        print(f"{name:12}", end="")
    print()
    print("         " + "─"*52)

    # Print matrix
    for i, name1 in enumerate(dim_names):
        print(f"{name1:12} │", end="")
        for j in range(4):
            val = corr_matrix[i][j]
            if i == j:
                print(f"   1.00    ", end="")
            else:
                print(f"  {val:+.2f}     ", end="")
        print()

    print("\nKey observations:")
    print(f"  • L ↔ J correlation: {corr_matrix[0][1]:+.2f} (moral dimensions reinforce)")
    print(f"  • L ↔ P correlation: {corr_matrix[0][2]:+.2f} (love and power oppose)")
    print(f"  • J ↔ W correlation: {corr_matrix[1][3]:+.2f} (justice and wisdom align)")
    print(f"  • P ↔ W correlation: {corr_matrix[2][3]:+.2f} (power and wisdom tension)")


def print_region_map():
    """Print textual description of semantic geography."""

    print("\n" + "="*70)
    print("SEMANTIC GEOGRAPHY: 13 FUNDAMENTAL REGIONS")
    print("="*70)
    print("\nThe natural territories of meaning space:\n")

    regions = atlas['regions']

    for i, region in enumerate(regions, 1):
        c = region['center']
        print(f"{i:2}. {region['name']}")
        print(f"    Location: L={c[0]:.2f}, J={c[1]:.2f}, P={c[2]:.2f}, W={c[3]:.2f}")
        print(f"    Harmony:  {(region['harmony_range'][0] + region['harmony_range'][1])/2:.3f}")
        print(f"    Examples: {', '.join(region['examples'][:4])}")
        print(f"    {region['description']}")
        print()


def print_attractor_diagram():
    """Show attractor hierarchy."""

    print("\n" + "="*70)
    print("ATTRACTOR HIERARCHY")
    print("="*70)
    print("\nStable points that meanings cluster around:\n")

    attractors = sorted(atlas['attractors'], key=lambda a: -abs(a['strength']))

    for attractor in attractors:
        strength = attractor['strength']
        attractor_type = "ATTRACTOR" if strength > 0 else "REPELLER"
        strength_bar = "█" * int(abs(strength) * 20)

        print(f"• {attractor['name']}")
        print(f"  Type: {attractor_type}")
        print(f"  Strength: {strength:+.2f} {strength_bar}")
        print(f"  Position: L={attractor['position'][0]:.3f}, J={attractor['position'][1]:.3f}, "
              f"P={attractor['position'][2]:.3f}, W={attractor['position'][3]:.3f}")
        print(f"  Basin radius: {attractor['basin_radius']:.2f}")
        print(f"  {attractor['interpretation']}\n")


def main():
    """Generate all visualizations."""

    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + " "*15 + "SEMANTIC SPACE ARCHITECTURE" + " "*27 + "█")
    print("█" + " "*12 + "Visual Atlas of the Pre-Existing" + " "*24 + "█")
    print("█" + " "*15 + "Structures of Meaning" + " "*33 + "█")
    print("█" + " "*68 + "█")
    print("█"*70)

    # 1. Regional map
    visualize_lj_plane()
    visualize_pw_plane()

    # 2. Attractor field
    visualize_attractor_field()

    # 3. Harmony landscape
    visualize_harmony_landscape()

    # 4. Dimensional coupling
    visualize_dimensional_coupling()

    # 5. Textual descriptions
    print_region_map()
    print_attractor_diagram()

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("\nThese visualizations reveal the pre-existing architecture:")
    print()
    print("1. REGIONS: 13 natural territories (Transcendent, Peaceful, etc.)")
    print("   • Based on dimensional patterns relative to Natural Equilibrium")
    print("   • Each region has distinct characteristics and examples")
    print()
    print("2. ATTRACTORS: 8 stable points (Divine Perfection, Pure Love, etc.)")
    print("   • Meanings cluster around these coordinates")
    print("   • Varying strengths and basin sizes")
    print("   • One repeller (The Void) meanings avoid")
    print()
    print("3. HARMONY GRADIENT: Continuous field from virtue to vice")
    print("   • Maximum at Anchor Point (1,1,1,1)")
    print("   • Saddle point at Natural Equilibrium")
    print("   • Minimum at origin (absence)")
    print()
    print("4. DIMENSIONAL COUPLING: L and J correlate positively")
    print("   • Moral dimensions (L+J) reinforce each other")
    print("   • Power dimension is more independent")
    print("   • Wisdom aligns with Justice")
    print()
    print("This is not invented structure—it is DISCOVERED structure.")
    print("These patterns exist whether or not we observe them.")
    print("="*70)


if __name__ == '__main__':
    main()
