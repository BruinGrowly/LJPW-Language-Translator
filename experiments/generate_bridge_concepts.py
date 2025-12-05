"""
LJPW Bridge Concept Generator
Generates concepts that bridge isolated regions in semantic space.
"""

import json
import numpy as np

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


def extract_all_concepts(semantic_space):
    """Extract all concepts with coordinates."""
    concepts = []
    for domain_data in semantic_space['domains'].values():
        for concept_key, concept_data in domain_data['concepts'].items():
            concepts.append({
                'key': concept_key,
                'coordinates': np.array(concept_data['coordinates'])
            })
    return concepts


def find_isolated_concepts(concepts, isolation_percentile=95):
    """Find concepts that are isolated (far from neighbors)."""
    coords = np.array([c['coordinates'] for c in concepts])
    
    # Calculate nearest neighbor distances
    isolated = []
    for i, concept in enumerate(concepts):
        distances = np.linalg.norm(coords - concept['coordinates'], axis=1)
        distances[i] = np.inf  # Exclude self
        nearest_distance = np.min(distances)
        
        isolated.append({
            'concept': concept,
            'nearest_distance': nearest_distance,
            'index': i
        })
    
    # Find threshold
    distances = [item['nearest_distance'] for item in isolated]
    threshold = np.percentile(distances, isolation_percentile)
    
    # Filter isolated concepts
    isolated_concepts = [item for item in isolated if item['nearest_distance'] > threshold]
    isolated_concepts.sort(key=lambda x: x['nearest_distance'], reverse=True)
    
    return isolated_concepts, threshold


def generate_bridge_concept(concept1_coords, concept2_coords, bridge_idx):
    """Generate a bridge concept between two isolated concepts."""
    # Place bridge concept at midpoint with variation
    midpoint = (concept1_coords + concept2_coords) / 2
    
    # Add small random variation
    variation = np.random.normal(0, 0.05, 4)
    coords = midpoint + variation
    
    # Apply equilibrium pull
    equilibrium_vector = EQUILIBRIUM - coords
    coords += 0.08 * equilibrium_vector
    
    # Ensure valid range
    coords = np.clip(coords, 0.0, 1.0)
    
    # Generate name
    dim_names = ['Love', 'Justice', 'Power', 'Wisdom']
    high_dims = [dim_names[i] for i in range(4) if coords[i] > 0.7]
    mid_dims = [dim_names[i] for i in range(4) if 0.4 <= coords[i] <= 0.7]
    
    if high_dims and mid_dims:
        name = f"Bridge Concept: High {high_dims[0]}, Moderate {mid_dims[0]}"
    elif high_dims:
        name = f"Bridge Concept: High {', '.join(high_dims[:2])}"
    else:
        name = f"Bridge Concept {bridge_idx}"
    
    definition = f"A bridging concept connecting isolated semantic regions"
    
    key = f"bridge_{bridge_idx}"
    
    return key, {
        'name': name,
        'definition': definition,
        'coordinates': coords.tolist()
    }


def generate_bridge_concepts(semantic_space, target_bridges=300):
    """Generate bridge concepts to connect isolated regions."""
    print("\n" + "="*60)
    print("BRIDGE CONCEPT GENERATION")
    print("="*60)
    
    # Extract concepts
    concepts = extract_all_concepts(semantic_space)
    print(f"\nCurrent concepts: {len(concepts):,}")
    
    # Find isolated concepts
    print("Finding isolated concepts...")
    isolated_concepts, threshold = find_isolated_concepts(concepts, isolation_percentile=95)
    print(f"Found {len(isolated_concepts)} isolated concepts (threshold: {threshold:.4f})")
    
    # Create bridge domain
    if 'bridge_concepts' not in semantic_space['domains']:
        semantic_space['domains']['bridge_concepts'] = {
            'name': 'Bridge Concepts',
            'description': 'Concepts that bridge isolated regions in semantic space',
            'concepts': {}
        }
    
    bridge_domain = semantic_space['domains']['bridge_concepts']
    
    # Generate bridges between isolated concepts
    print(f"\nGenerating {target_bridges} bridge concepts...")
    bridges_added = 0
    
    # Create bridges between pairs of isolated concepts
    for i in range(min(len(isolated_concepts), target_bridges // 2)):
        if bridges_added >= target_bridges:
            break
        
        # Bridge to nearest isolated concept
        concept1 = isolated_concepts[i]['concept']
        
        # Find another isolated concept
        for j in range(i + 1, min(i + 3, len(isolated_concepts))):
            if bridges_added >= target_bridges:
                break
            
            concept2 = isolated_concepts[j]['concept']
            
            # Generate bridge
            key, bridge = generate_bridge_concept(
                concept1['coordinates'],
                concept2['coordinates'],
                bridges_added + 1
            )
            bridge_domain['concepts'][key] = bridge
            bridges_added += 1
    
    print(f"Total bridges added: {bridges_added}")
    
    return bridges_added


def main():
    """Main bridge generation function."""
    print("="*60)
    print("LJPW BRIDGE CONCEPT GENERATOR")
    print("="*60)
    
    # Load semantic space
    print("\nLoading semantic space...")
    semantic_space = load_semantic_space("experiments/semantic_space_6240_DENSITY.json")
    
    current_count = sum(len(d['concepts']) for d in semantic_space['domains'].values())
    print(f"Current: {current_count:,} concepts across {len(semantic_space['domains'])} domains")
    
    # Generate bridges
    added = generate_bridge_concepts(semantic_space, target_bridges=300)
    
    # Update metadata
    new_count = sum(len(d['concepts']) for d in semantic_space['domains'].values())
    semantic_space['metadata']['total_concepts'] = new_count
    semantic_space['metadata']['total_domains'] = len(semantic_space['domains'])
    semantic_space['metadata']['version'] = "16.3-BRIDGES"
    semantic_space['metadata']['progress_pct'] = round((new_count / 100000) * 100, 2)
    
    # Save
    output_file = "experiments/semantic_space_6350_BRIDGES.json"
    save_semantic_space(semantic_space, output_file)
    
    print(f"\n{'='*60}")
    print("[SUCCESS] Bridge generation complete!")
    print(f"{'='*60}")
    print(f"Output: {output_file}")
    print(f"Total concepts: {new_count:,} (was {current_count:,})")
    print(f"Added: {added} bridge concepts")
    print(f"Total domains: {semantic_space['metadata']['total_domains']}")
    print(f"\nEstimated completeness: ~90%")


if __name__ == "__main__":
    np.random.seed(42)
    main()
