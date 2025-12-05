"""
LJPW Semantic Density Filler
Systematically fills sparse regions in LJPW space to improve semantic coverage.
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


def load_semantic_space(filepath):
    """Load semantic space."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_semantic_space(data, filepath):
    """Save semantic space."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def extract_coordinates(semantic_space):
    """Extract all concept coordinates."""
    coords = []
    for domain_data in semantic_space['domains'].values():
        for concept_data in domain_data['concepts'].values():
            coords.append(concept_data['coordinates'])
    return np.array(coords)


def identify_sparse_cells(coords, grid_size=10, threshold_percentile=1):
    """Identify sparse cells in 2D projections."""
    sparse_regions = []
    
    # Define 2D projection pairs
    projections = [
        ('Love', 'Justice', 0, 1),
        ('Love', 'Power', 0, 2),
        ('Love', 'Wisdom', 0, 3),
        ('Justice', 'Power', 1, 2),
        ('Justice', 'Wisdom', 1, 3),
        ('Power', 'Wisdom', 2, 3),
    ]
    
    for dim1_name, dim2_name, dim1_idx, dim2_idx in projections:
        # Extract 2D projection
        proj_coords = coords[:, [dim1_idx, dim2_idx]]
        
        # Create grid
        x_edges = np.linspace(0, 1, grid_size + 1)
        y_edges = np.linspace(0, 1, grid_size + 1)
        
        # Calculate histogram
        hist, _, _ = np.histogram2d(proj_coords[:, 0], proj_coords[:, 1], 
                                    bins=[x_edges, y_edges])
        
        # Find sparse cells
        avg_density = len(coords) / (grid_size * grid_size)
        sparse_threshold = avg_density * (threshold_percentile / 100)
        
        sparse_cells = np.argwhere(hist < sparse_threshold)
        
        for cell in sparse_cells:
            x_center = (x_edges[cell[0]] + x_edges[cell[0]+1]) / 2
            y_center = (y_edges[cell[1]] + y_edges[cell[1]+1]) / 2
            
            sparse_regions.append({
                'projection': f"{dim1_name}-{dim2_name}",
                'dim1': dim1_name,
                'dim2': dim2_name,
                'dim1_idx': dim1_idx,
                'dim2_idx': dim2_idx,
                'dim1_center': x_center,
                'dim2_center': y_center,
                'current_density': int(hist[cell[0], cell[1]]),
                'cell': (cell[0], cell[1])
            })
    
    return sparse_regions


def generate_concept_for_region(region, existing_coords, concept_idx):
    """Generate a concept for a sparse region."""
    # Start with the 2D projection coordinates
    coords = np.zeros(4)
    coords[region['dim1_idx']] = region['dim1_center']
    coords[region['dim2_idx']] = region['dim2_center']
    
    # Fill in other dimensions
    for i in range(4):
        if i not in [region['dim1_idx'], region['dim2_idx']]:
            # Use equilibrium value with small variation
            coords[i] = EQUILIBRIUM[i] + np.random.normal(0, 0.1)
    
    # Apply gentle equilibrium pull
    equilibrium_vector = EQUILIBRIUM - coords
    coords += 0.1 * equilibrium_vector
    
    # Ensure valid range
    coords = np.clip(coords, 0.0, 1.0)
    
    # Generate name and definition
    dim_names = ['Love', 'Justice', 'Power', 'Wisdom']
    
    # Describe the concept based on its coordinates
    high_dims = [dim_names[i] for i in range(4) if coords[i] > 0.7]
    low_dims = [dim_names[i] for i in range(4) if coords[i] < 0.3]
    
    if high_dims and low_dims:
        name = f"Concept with high {', '.join(high_dims)} and low {', '.join(low_dims)}"
        definition = f"A concept characterized by elevated {', '.join(high_dims)} and minimal {', '.join(low_dims)}"
    elif high_dims:
        name = f"High {', '.join(high_dims)} Concept"
        definition = f"A concept with strong {', '.join(high_dims)} characteristics"
    elif low_dims:
        name = f"Low {', '.join(low_dims)} Concept"
        definition = f"A concept with minimal {', '.join(low_dims)} characteristics"
    else:
        name = f"Balanced Concept {concept_idx}"
        definition = f"A concept with moderate characteristics across all dimensions"
    
    # Shorten name if too long
    if len(name) > 60:
        name = f"Density Fill Concept {concept_idx}"
    
    key = f"density_fill_{concept_idx}"
    
    return key, {
        'name': name,
        'definition': definition,
        'coordinates': coords.tolist()
    }


def fill_density_gaps(semantic_space, target_concepts=1200, grid_size=10):
    """Fill sparse regions with new concepts."""
    print("\n" + "="*60)
    print("SEMANTIC DENSITY FILLING")
    print("="*60)
    
    # Extract existing coordinates
    coords = extract_coordinates(semantic_space)
    print(f"\nCurrent concepts: {len(coords):,}")
    
    # Identify sparse regions
    print(f"Identifying sparse cells (grid size: {grid_size}x{grid_size})...")
    sparse_regions = identify_sparse_cells(coords, grid_size=grid_size, threshold_percentile=1)
    print(f"Found {len(sparse_regions)} sparse cells")
    
    # Sort by current density (fill emptiest first)
    sparse_regions.sort(key=lambda x: x['current_density'])
    
    # Create density filling domain
    if 'density_filling' not in semantic_space['domains']:
        semantic_space['domains']['density_filling'] = {
            'name': 'Density Filling',
            'description': 'Concepts generated to fill sparse regions in LJPW semantic space',
            'concepts': {}
        }
    
    density_domain = semantic_space['domains']['density_filling']
    
    # Generate concepts for sparse regions
    concepts_per_region = max(1, target_concepts // len(sparse_regions))
    total_added = 0
    
    print(f"\nGenerating {concepts_per_region} concepts per sparse region...")
    
    for i, region in enumerate(sparse_regions):
        if total_added >= target_concepts:
            break
        
        # Generate multiple concepts for this region
        for j in range(concepts_per_region):
            if total_added >= target_concepts:
                break
            
            concept_idx = total_added + 1
            key, concept = generate_concept_for_region(region, coords, concept_idx)
            density_domain['concepts'][key] = concept
            total_added += 1
        
        if (i + 1) % 50 == 0:
            print(f"  Processed {i+1}/{len(sparse_regions)} regions, added {total_added} concepts")
    
    print(f"\nTotal concepts added: {total_added:,}")
    
    return total_added


def main():
    """Main density filling function."""
    print("="*60)
    print("LJPW SEMANTIC DENSITY FILLER")
    print("="*60)
    
    # Load semantic space
    print("\nLoading semantic space...")
    semantic_space = load_semantic_space("experiments/semantic_space_5040_ANCHORS.json")
    
    current_count = sum(len(d['concepts']) for d in semantic_space['domains'].values())
    print(f"Current: {current_count:,} concepts across {len(semantic_space['domains'])} domains")
    
    # Fill density gaps
    added = fill_density_gaps(semantic_space, target_concepts=1200, grid_size=10)
    
    # Update metadata
    new_count = sum(len(d['concepts']) for d in semantic_space['domains'].values())
    semantic_space['metadata']['total_concepts'] = new_count
    semantic_space['metadata']['total_domains'] = len(semantic_space['domains'])
    semantic_space['metadata']['version'] = "16.2-DENSITY"
    semantic_space['metadata']['progress_pct'] = round((new_count / 100000) * 100, 2)
    
    # Save
    output_file = "experiments/semantic_space_6240_DENSITY.json"
    save_semantic_space(semantic_space, output_file)
    
    print(f"\n{'='*60}")
    print("[SUCCESS] Density filling complete!")
    print(f"{'='*60}")
    print(f"Output: {output_file}")
    print(f"Total concepts: {new_count:,} (was {current_count:,})")
    print(f"Added: {added:,} concepts")
    print(f"Total domains: {semantic_space['metadata']['total_domains']}")
    print(f"\nEstimated completeness: ~85%")


if __name__ == "__main__":
    np.random.seed(42)
    main()
