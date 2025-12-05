"""
LJPW Semantic Density Analyzer
Analyzes the semantic density and coverage of the LJPW space
to identify gaps and high-weight concepts needed for completeness.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from scipy.spatial import distance_matrix
from scipy.stats import gaussian_kde

# Natural Equilibrium Constants
PHI_INV = 1 / ((1 + np.sqrt(5)) / 2)  # φ⁻¹ ≈ 0.618 (Love)
SQRT2_M1 = np.sqrt(2) - 1              # √2-1 ≈ 0.414 (Justice)
E_M2 = np.e - 2                         # e-2 ≈ 0.718 (Power)
LN2 = np.log(2)                         # ln2 ≈ 0.693 (Wisdom)

EQUILIBRIUM = np.array([PHI_INV, SQRT2_M1, E_M2, LN2])
DIMENSION_NAMES = ['Love', 'Justice', 'Power', 'Wisdom']


def load_semantic_space(filepath):
    """Load semantic space from JSON."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_all_concepts(semantic_space):
    """Extract all concepts with their coordinates and metadata."""
    concepts = []
    for domain_key, domain_data in semantic_space['domains'].items():
        domain_name = domain_data.get('domain_name') or domain_data.get('name', domain_key)
        for concept_key, concept_data in domain_data['concepts'].items():
            # Use concept_key as name if 'name' field doesn't exist
            concept_name = concept_data.get('name', concept_key.replace('_', ' ').title())
            concepts.append({
                'key': concept_key,
                'name': concept_name,
                'definition': concept_data.get('definition', ''),
                'coordinates': np.array(concept_data['coordinates']),
                'domain': domain_name,
                'domain_key': domain_key
            })
    return concepts


def analyze_dimensional_coverage(concepts):
    """Analyze coverage across each LJPW dimension."""
    print("\n" + "="*60)
    print("DIMENSIONAL COVERAGE ANALYSIS")
    print("="*60)
    
    coords = np.array([c['coordinates'] for c in concepts])
    
    coverage = {}
    for i, dim_name in enumerate(DIMENSION_NAMES):
        dim_values = coords[:, i]
        
        coverage[dim_name] = {
            'min': float(np.min(dim_values)),
            'max': float(np.max(dim_values)),
            'mean': float(np.mean(dim_values)),
            'std': float(np.std(dim_values)),
            'median': float(np.median(dim_values)),
            'range': float(np.max(dim_values) - np.min(dim_values)),
            'equilibrium': float(EQUILIBRIUM[i]),
            'distance_from_eq': float(abs(np.mean(dim_values) - EQUILIBRIUM[i]))
        }
        
        print(f"\n{dim_name} Dimension:")
        print(f"  Range: [{coverage[dim_name]['min']:.3f}, {coverage[dim_name]['max']:.3f}] (span: {coverage[dim_name]['range']:.3f})")
        print(f"  Mean: {coverage[dim_name]['mean']:.3f} (Equilibrium: {coverage[dim_name]['equilibrium']:.3f})")
        print(f"  Median: {coverage[dim_name]['median']:.3f}")
        print(f"  Std Dev: {coverage[dim_name]['std']:.3f}")
        print(f"  Distance from Equilibrium: {coverage[dim_name]['distance_from_eq']:.3f}")
        
        # Identify sparse regions
        bins = np.linspace(0, 1, 11)  # 10 bins
        hist, _ = np.histogram(dim_values, bins=bins)
        sparse_bins = np.where(hist < len(concepts) * 0.02)[0]  # Less than 2% of concepts
        
        if len(sparse_bins) > 0:
            print(f"  Sparse regions (< 2% density):")
            for bin_idx in sparse_bins:
                print(f"    [{bins[bin_idx]:.1f}, {bins[bin_idx+1]:.1f}]: {hist[bin_idx]} concepts")
    
    return coverage


def calculate_semantic_density(concepts, grid_size=10):
    """Calculate semantic density in different regions of LJPW space."""
    print("\n" + "="*60)
    print("SEMANTIC DENSITY ANALYSIS")
    print("="*60)
    
    coords = np.array([c['coordinates'] for c in concepts])
    
    # Create 4D grid (simplified to 2D projections for visualization)
    density_maps = {}
    
    # Analyze L-J plane
    print("\nLove-Justice Plane:")
    lj_coords = coords[:, [0, 1]]
    lj_density = analyze_2d_density(lj_coords, "Love", "Justice", grid_size)
    density_maps['LJ'] = lj_density
    
    # Analyze P-W plane
    print("\nPower-Wisdom Plane:")
    pw_coords = coords[:, [2, 3]]
    pw_density = analyze_2d_density(pw_coords, "Power", "Wisdom", grid_size)
    density_maps['PW'] = pw_density
    
    # Analyze L-P plane
    print("\nLove-Power Plane:")
    lp_coords = coords[:, [0, 2]]
    lp_density = analyze_2d_density(lp_coords, "Love", "Power", grid_size)
    density_maps['LP'] = lp_density
    
    # Analyze J-W plane
    print("\nJustice-Wisdom Plane:")
    jw_coords = coords[:, [1, 3]]
    jw_density = analyze_2d_density(jw_coords, "Justice", "Wisdom", grid_size)
    density_maps['JW'] = jw_density
    
    return density_maps


def analyze_2d_density(coords, dim1, dim2, grid_size):
    """Analyze density in a 2D projection."""
    # Create grid
    x_edges = np.linspace(0, 1, grid_size + 1)
    y_edges = np.linspace(0, 1, grid_size + 1)
    
    # Calculate histogram
    hist, _, _ = np.histogram2d(coords[:, 0], coords[:, 1], bins=[x_edges, y_edges])
    
    # Find sparse cells (< 1% of average density)
    avg_density = len(coords) / (grid_size * grid_size)
    sparse_threshold = avg_density * 0.01
    sparse_cells = np.argwhere(hist < sparse_threshold)
    
    print(f"  Average density per cell: {avg_density:.1f} concepts")
    print(f"  Sparse cells (< 1% avg): {len(sparse_cells)} / {grid_size*grid_size}")
    
    if len(sparse_cells) > 0 and len(sparse_cells) <= 10:
        print(f"  Sparse regions:")
        for cell in sparse_cells[:10]:
            x_range = f"[{x_edges[cell[0]]:.2f}, {x_edges[cell[0]+1]:.2f}]"
            y_range = f"[{y_edges[cell[1]]:.2f}, {y_edges[cell[1]+1]:.2f}]"
            print(f"    {dim1}: {x_range}, {dim2}: {y_range} - {int(hist[cell[0], cell[1]])} concepts")
    
    return {
        'histogram': hist,
        'x_edges': x_edges,
        'y_edges': y_edges,
        'sparse_cells': sparse_cells,
        'avg_density': avg_density
    }


def identify_semantic_anchors(concepts, top_n=50):
    """Identify high-weight semantic anchor concepts."""
    print("\n" + "="*60)
    print("HIGH-WEIGHT SEMANTIC ANCHORS")
    print("="*60)
    
    coords = np.array([c['coordinates'] for c in concepts])
    
    # Calculate semantic weight based on multiple factors
    weights = []
    for i, concept in enumerate(concepts):
        # Factor 1: Distance from equilibrium (closer = higher weight)
        eq_distance = np.linalg.norm(concept['coordinates'] - EQUILIBRIUM)
        eq_weight = 1.0 / (1.0 + eq_distance)
        
        # Factor 2: Average distance to all other concepts (central = higher weight)
        distances = np.linalg.norm(coords - concept['coordinates'], axis=1)
        avg_distance = np.mean(distances)
        centrality_weight = 1.0 / (1.0 + avg_distance)
        
        # Factor 3: Extremity in any dimension (extreme = higher weight as anchor)
        extremity = max([
            abs(concept['coordinates'][j] - 0.5) for j in range(4)
        ])
        extremity_weight = extremity * 2  # Scale to [0, 1]
        
        # Combined weight
        total_weight = (eq_weight * 0.4 + centrality_weight * 0.3 + extremity_weight * 0.3)
        
        weights.append({
            'concept': concept,
            'weight': total_weight,
            'eq_weight': eq_weight,
            'centrality_weight': centrality_weight,
            'extremity_weight': extremity_weight
        })
    
    # Sort by weight
    weights.sort(key=lambda x: x['weight'], reverse=True)
    
    print(f"\nTop {top_n} Semantic Anchors:")
    print(f"{'Rank':<6} {'Concept':<40} {'Weight':<8} {'Domain':<30}")
    print("-" * 90)
    
    for i, item in enumerate(weights[:top_n]):
        concept = item['concept']
        print(f"{i+1:<6} {concept['name'][:39]:<40} {item['weight']:.4f}   {concept['domain'][:29]}")
    
    return weights


def identify_missing_anchors(concepts, coverage, density_maps):
    """Identify missing high-weight concepts based on gaps."""
    print("\n" + "="*60)
    print("MISSING SEMANTIC ANCHORS")
    print("="*60)
    
    missing_anchors = []
    
    # Check for dimensional extremes
    coords = np.array([c['coordinates'] for c in concepts])
    
    for i, dim_name in enumerate(DIMENSION_NAMES):
        dim_values = coords[:, i]
        
        # Check low extreme (< 0.1)
        low_count = np.sum(dim_values < 0.1)
        if low_count < 10:
            missing_anchors.append({
                'type': 'dimensional_extreme',
                'dimension': dim_name,
                'region': 'low',
                'range': [0.0, 0.1],
                'current_count': low_count,
                'priority': 'HIGH',
                'description': f'Very low {dim_name} concepts (minimal {dim_name.lower()})'
            })
        
        # Check high extreme (> 0.9)
        high_count = np.sum(dim_values > 0.9)
        if high_count < 10:
            missing_anchors.append({
                'type': 'dimensional_extreme',
                'dimension': dim_name,
                'region': 'high',
                'range': [0.9, 1.0],
                'current_count': high_count,
                'priority': 'HIGH',
                'description': f'Very high {dim_name} concepts (maximal {dim_name.lower()})'
            })
    
    # Check for equilibrium-adjacent concepts
    eq_distances = np.linalg.norm(coords - EQUILIBRIUM, axis=1)
    near_eq_count = np.sum(eq_distances < 0.1)
    if near_eq_count < 20:
        missing_anchors.append({
            'type': 'equilibrium',
            'region': 'near_equilibrium',
            'current_count': near_eq_count,
            'priority': 'CRITICAL',
            'description': 'Concepts near natural equilibrium point (balanced across all dimensions)'
        })
    
    # Check for cross-dimensional bridges
    # Concepts that are high in multiple dimensions
    multi_high = np.sum(coords > 0.8, axis=1)
    bridge_count = np.sum(multi_high >= 3)
    if bridge_count < 15:
        missing_anchors.append({
            'type': 'bridge',
            'region': 'multi_dimensional_high',
            'current_count': bridge_count,
            'priority': 'HIGH',
            'description': 'Concepts high in 3+ dimensions (universal qualities)'
        })
    
    print(f"\nIdentified {len(missing_anchors)} missing anchor types:\n")
    for i, anchor in enumerate(missing_anchors, 1):
        print(f"{i}. [{anchor['priority']}] {anchor['description']}")
        print(f"   Current count: {anchor['current_count']}")
        if 'dimension' in anchor:
            print(f"   Dimension: {anchor['dimension']} ({anchor['region']})")
        print()
    
    return missing_anchors


def calculate_relationship_richness(concepts, sample_size=1000):
    """Calculate how interconnected concepts are."""
    print("\n" + "="*60)
    print("RELATIONSHIP RICHNESS ANALYSIS")
    print("="*60)
    
    # Sample for performance
    if len(concepts) > sample_size:
        sample_indices = np.random.choice(len(concepts), sample_size, replace=False)
        sample_concepts = [concepts[i] for i in sample_indices]
    else:
        sample_concepts = concepts
    
    coords = np.array([c['coordinates'] for c in sample_concepts])
    
    # Calculate pairwise distances
    distances = distance_matrix(coords, coords)
    
    # Exclude self-distances
    np.fill_diagonal(distances, np.inf)
    
    # Find nearest neighbors
    nearest_distances = np.min(distances, axis=1)
    
    print(f"\nNearest Neighbor Analysis (sample size: {len(sample_concepts)}):")
    print(f"  Mean nearest neighbor distance: {np.mean(nearest_distances):.4f}")
    print(f"  Median nearest neighbor distance: {np.median(nearest_distances):.4f}")
    print(f"  Min nearest neighbor distance: {np.min(nearest_distances):.4f}")
    print(f"  Max nearest neighbor distance: {np.max(nearest_distances):.4f}")
    
    # Identify isolated concepts (far from neighbors)
    isolation_threshold = np.percentile(nearest_distances, 95)
    isolated_indices = np.where(nearest_distances > isolation_threshold)[0]
    
    print(f"\nIsolated Concepts (top 5% by distance):")
    print(f"  Count: {len(isolated_indices)}")
    print(f"  Threshold distance: {isolation_threshold:.4f}")
    
    if len(isolated_indices) > 0:
        print(f"\n  Most isolated concepts:")
        isolated_sorted = sorted(isolated_indices, key=lambda i: nearest_distances[i], reverse=True)
        for idx in isolated_sorted[:10]:
            concept = sample_concepts[idx]
            print(f"    {concept['name'][:50]} (distance: {nearest_distances[idx]:.4f})")
    
    return {
        'mean_nn_distance': float(np.mean(nearest_distances)),
        'median_nn_distance': float(np.median(nearest_distances)),
        'isolated_count': len(isolated_indices),
        'isolation_threshold': float(isolation_threshold)
    }


def generate_completeness_report(semantic_space, concepts, coverage, density_maps, anchors, missing_anchors, richness):
    """Generate comprehensive semantic completeness report."""
    print("\n" + "="*60)
    print("SEMANTIC COMPLETENESS REPORT")
    print("="*60)
    
    total_concepts = len(concepts)
    total_domains = len(semantic_space['domains'])
    
    # Calculate completeness scores
    scores = {}
    
    # 1. Dimensional Coverage Score (0-100)
    dim_coverage_scores = []
    for dim_name in DIMENSION_NAMES:
        range_score = coverage[dim_name]['range'] * 100  # How much of [0,1] is covered
        balance_score = (1 - coverage[dim_name]['distance_from_eq']) * 100  # How close to equilibrium
        dim_coverage_scores.append((range_score + balance_score) / 2)
    scores['dimensional_coverage'] = np.mean(dim_coverage_scores)
    
    # 2. Density Score (0-100)
    # Based on how few sparse regions exist
    total_sparse = sum(len(dm['sparse_cells']) for dm in density_maps.values())
    max_sparse = 10 * 10 * len(density_maps)  # 10x10 grid per map
    scores['density'] = (1 - total_sparse / max_sparse) * 100
    
    # 3. Anchor Coverage Score (0-100)
    # Based on how many missing anchor types we have
    max_missing = 10  # Assume max 10 critical missing types
    scores['anchor_coverage'] = (1 - min(len(missing_anchors), max_missing) / max_missing) * 100
    
    # 4. Relationship Richness Score (0-100)
    # Based on nearest neighbor distances (closer = better connected)
    max_expected_distance = 0.5  # In 4D space
    scores['relationship_richness'] = (1 - min(richness['mean_nn_distance'] / max_expected_distance, 1)) * 100
    
    # Overall Completeness Score
    overall_score = np.mean(list(scores.values()))
    
    print(f"\nCompleteness Metrics:")
    print(f"  Total Concepts: {total_concepts:,}")
    print(f"  Total Domains: {total_domains}")
    print(f"\nScores (0-100):")
    print(f"  Dimensional Coverage: {scores['dimensional_coverage']:.1f}")
    print(f"  Semantic Density: {scores['density']:.1f}")
    print(f"  Anchor Coverage: {scores['anchor_coverage']:.1f}")
    print(f"  Relationship Richness: {scores['relationship_richness']:.1f}")
    print(f"\n  OVERALL COMPLETENESS: {overall_score:.1f}/100")
    
    # Recommendations
    print(f"\nRecommendations for Semantic Completeness:")
    
    if scores['dimensional_coverage'] < 80:
        print(f"  1. Improve dimensional coverage (current: {scores['dimensional_coverage']:.1f})")
        print(f"     - Add concepts in sparse dimensional regions")
        print(f"     - Balance toward equilibrium in over/under-represented dimensions")
    
    if scores['density'] < 80:
        print(f"  2. Fill semantic density gaps (current: {scores['density']:.1f})")
        print(f"     - Add concepts in sparse 2D projections")
        print(f"     - Ensure even distribution across LJPW space")
    
    if scores['anchor_coverage'] < 80:
        print(f"  3. Add missing semantic anchors (current: {scores['anchor_coverage']:.1f})")
        print(f"     - {len(missing_anchors)} critical anchor types missing")
        print(f"     - Focus on high-priority missing anchors first")
    
    if scores['relationship_richness'] < 80:
        print(f"  4. Improve relationship richness (current: {scores['relationship_richness']:.1f})")
        print(f"     - Add bridge concepts between isolated regions")
        print(f"     - Reduce isolated concepts")
    
    # Estimated concepts needed
    if overall_score < 90:
        concepts_needed = int((90 - overall_score) * 100)  # Rough estimate
        print(f"\nEstimated concepts needed for 90% completeness: ~{concepts_needed:,}")
    else:
        print(f"\nSemantic space is highly complete! Focus on refinement.")
    
    return {
        'scores': scores,
        'overall_score': overall_score,
        'total_concepts': total_concepts,
        'total_domains': total_domains
    }


def main():
    """Main analysis function."""
    print("="*60)
    print("LJPW SEMANTIC DENSITY ANALYZER")
    print("="*60)
    
    # Load semantic space
    print("\nLoading semantic space...")
    semantic_space = load_semantic_space("experiments/semantic_space_5000_FINAL.json")
    
    # Extract concepts
    print("Extracting concepts...")
    concepts = extract_all_concepts(semantic_space)
    print(f"Loaded {len(concepts):,} concepts from {len(semantic_space['domains'])} domains")
    
    # Run analyses
    coverage = analyze_dimensional_coverage(concepts)
    density_maps = calculate_semantic_density(concepts, grid_size=10)
    anchors = identify_semantic_anchors(concepts, top_n=50)
    missing_anchors = identify_missing_anchors(concepts, coverage, density_maps)
    richness = calculate_relationship_richness(concepts, sample_size=1000)
    
    # Generate completeness report
    report = generate_completeness_report(
        semantic_space, concepts, coverage, density_maps, 
        anchors, missing_anchors, richness
    )
    
    # Save analysis results
    output = {
        'metadata': {
            'total_concepts': len(concepts),
            'total_domains': len(semantic_space['domains']),
            'analysis_date': '2025-12-05'
        },
        'coverage': coverage,
        'missing_anchors': missing_anchors,
        'relationship_richness': richness,
        'completeness_scores': report['scores'],
        'overall_completeness': report['overall_score']
    }
    
    with open("experiments/semantic_density_analysis.json", 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print("[SUCCESS] Analysis complete!")
    print(f"Results saved to: experiments/semantic_density_analysis.json")
    print(f"{'='*60}")


if __name__ == "__main__":
    np.random.seed(42)
    main()
