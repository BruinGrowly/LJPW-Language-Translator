"""
10k Semantic Space Visualizer
=============================
Visualizes the density and distribution of 10,725 concepts
in 4D LJPW space using 2D ASCII heatmaps.
"""

import json
import numpy as np
from pathlib import Path
from collections import Counter

def load_concepts():
    # Construct path relative to this script file
    script_dir = Path(__file__).parent
    path = script_dir / "semantic_space_10000_MILESTONE.json"
    
    print(f"Loading {path}...")
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    concepts = []
    for domain_key, domain in data['domains'].items():
        domain_name = domain.get('name', domain_key)
        for name, c_data in domain.get('concepts', {}).items():
            c_data['id'] = name
            c_data['domain_name'] = domain_name
            concepts.append(c_data)
    return concepts

def render_heatmap(concepts, dim_x, dim_y, label_x, label_y, title):
    print(f"\n{title}")
    print("="*60)
    
    width, height = 60, 25
    grid = np.zeros((height, width))
    
    # Dimensions mapping
    # L=0, J=1, P=2, W=3
    d_map = {'L': 0, 'J': 1, 'P': 2, 'W': 3}
    idx_x = d_map[label_x[0]]
    idx_y = d_map[label_y[0]]
    
    # Populate grid
    for c in concepts:
        coords = c['coordinates']
        x_val = coords[idx_x]
        y_val = coords[idx_y]
        
        # Scale to grid
        gx = int(x_val * (width - 1))
        gy = int((1.0 - y_val) * (height - 1)) # Flip Y for visual "up"
        
        gx = max(0, min(width-1, gx))
        gy = max(0, min(height-1, gy))
        
        grid[gy, gx] += 1
        
    # ASCII Shading
    chars = " .:-=+*#%@"
    max_count = np.max(grid)
    if max_count == 0: max_count = 1
    
    print(f"  {label_y} ^")
    print("    +" + "-" * width + "+")
    
    for y in range(height):
        line = ""
        for x in range(width):
            val = grid[y, x]
            if val == 0:
                char = " "
            else:
                norm = val / max_count
                char_idx = int(norm * (len(chars) - 1))
                char = chars[char_idx]
            line += char
        print(f"    |{line}|")
        
    print("    +" + "-" * width + "+")
    print(f"     {' ' * (width // 2 - 2)} {label_x} >")
    print(f"Max Density: {int(max_count)} concepts per cell")

def main():
    try:
        concepts = load_concepts()
        print(f"Loaded {len(concepts)} concepts.")
        
        # 1. Love (Y) vs Justice (X)
        render_heatmap(concepts, 'J', 'L', "Justice (X)", "Love (Y)", 
                      "LOVE-JUSTICE PLANE (Moral Core)")
                      
        # 2. Power (X) vs Wisdom (Y) - Standard LJPW usually pairs P/W
        # Let's do Power (X) vs Wisdom (Y)
        render_heatmap(concepts, 'P', 'W', "Power (X)", "Wisdom (Y)", 
                      "WISDOM-POWER PLANE (Capability)")
                      
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
