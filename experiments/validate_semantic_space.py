"""
LJPW Comprehensive Validation Suite
Tests semantic completeness, quality, and integrity of the LJPW space.
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
DIMENSION_NAMES = ['Love', 'Justice', 'Power', 'Wisdom']


def load_semantic_space(filepath):
    """Load semantic space."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_all_concepts(semantic_space):
    """Extract all concepts."""
    concepts = []
    for domain_data in semantic_space['domains'].values():
        for concept_data in domain_data['concepts'].values():
            concepts.append({
                'coordinates': np.array(concept_data['coordinates']),
                'definition': concept_data.get('definition', '')
            })
    return concepts


class ValidationTest:
    """Base class for validation tests."""
    def __init__(self, name):
        self.name = name
        self.passed = False
        self.message = ""
        self.details = {}
    
    def run(self, semantic_space, concepts):
        """Override this method."""
        raise NotImplementedError


class CoordinateValidityTest(ValidationTest):
    """Test that all coordinates are in [0,1] range."""
    def __init__(self):
        super().__init__("Coordinate Validity")
    
    def run(self, semantic_space, concepts):
        invalid = []
        for i, concept in enumerate(concepts):
            coords = concept['coordinates']
            if not all(0 <= c <= 1 for c in coords):
                invalid.append(i)
        
        self.passed = len(invalid) == 0
        self.message = f"All {len(concepts)} concepts have valid coordinates" if self.passed else f"Found {len(invalid)} invalid coordinates"
        self.details = {'invalid_count': len(invalid), 'total': len(concepts)}
        return self.passed


class CompletenessTest(ValidationTest):
    """Test that all concepts have required fields."""
    def __init__(self):
        super().__init__("Completeness")
    
    def run(self, semantic_space, concepts):
        incomplete = 0
        for concept in concepts:
            if not concept.get('definition') or len(concept.get('definition', '')) < 5:
                incomplete += 1
        
        self.passed = incomplete == 0
        self.message = f"All concepts complete" if self.passed else f"{incomplete} concepts missing definitions"
        self.details = {'incomplete_count': incomplete, 'total': len(concepts)}
        return self.passed


class DimensionalCoverageTest(ValidationTest):
    """Test coverage across all dimensions."""
    def __init__(self):
        super().__init__("Dimensional Coverage")
    
    def run(self, semantic_space, concepts):
        coords = np.array([c['coordinates'] for c in concepts])
        
        coverage_scores = []
        for i, dim_name in enumerate(DIMENSION_NAMES):
            dim_values = coords[:, i]
            range_coverage = (np.max(dim_values) - np.min(dim_values))
            coverage_scores.append(range_coverage)
        
        avg_coverage = np.mean(coverage_scores)
        self.passed = avg_coverage > 0.85
        self.message = f"Average dimensional coverage: {avg_coverage:.2%}"
        self.details = {
            'coverage_scores': {DIMENSION_NAMES[i]: coverage_scores[i] for i in range(4)},
            'average': avg_coverage
        }
        return self.passed


class EquilibriumAlignmentTest(ValidationTest):
    """Test alignment with natural equilibrium."""
    def __init__(self):
        super().__init__("Equilibrium Alignment")
    
    def run(self, semantic_space, concepts):
        coords = np.array([c['coordinates'] for c in concepts])
        centroid = np.mean(coords, axis=0)
        distance = np.linalg.norm(centroid - EQUILIBRIUM)
        
        self.passed = distance < 0.5
        self.message = f"Distance from equilibrium: {distance:.4f}"
        self.details = {
            'centroid': centroid.tolist(),
            'equilibrium': EQUILIBRIUM.tolist(),
            'distance': distance
        }
        return self.passed


class DensityUniformityTest(ValidationTest):
    """Test that density is reasonably uniform."""
    def __init__(self):
        super().__init__("Density Uniformity")
    
    def run(self, semantic_space, concepts):
        coords = np.array([c['coordinates'] for c in concepts])
        
        # Check 2D projections
        grid_size = 10
        sparse_count = 0
        total_cells = 0
        
        projections = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
        
        for dim1, dim2 in projections:
            proj_coords = coords[:, [dim1, dim2]]
            hist, _, _ = np.histogram2d(proj_coords[:, 0], proj_coords[:, 1], 
                                       bins=grid_size)
            
            avg_density = len(coords) / (grid_size * grid_size)
            sparse_threshold = avg_density * 0.01
            sparse_cells = np.sum(hist < sparse_threshold)
            
            sparse_count += sparse_cells
            total_cells += grid_size * grid_size
        
        uniformity_score = 1 - (sparse_count / total_cells)
        self.passed = uniformity_score > 0.7
        self.message = f"Density uniformity: {uniformity_score:.2%}"
        self.details = {
            'sparse_cells': sparse_count,
            'total_cells': total_cells,
            'uniformity_score': uniformity_score
        }
        return self.passed


class RelationshipRichnessTest(ValidationTest):
    """Test that concepts are well-connected."""
    def __init__(self):
        super().__init__("Relationship Richness")
    
    def run(self, semantic_space, concepts):
        # Sample for performance
        sample_size = min(1000, len(concepts))
        sample_indices = np.random.choice(len(concepts), sample_size, replace=False)
        sample_coords = np.array([concepts[i]['coordinates'] for i in sample_indices])
        
        # Calculate nearest neighbor distances
        nearest_distances = []
        for i in range(len(sample_coords)):
            distances = np.linalg.norm(sample_coords - sample_coords[i], axis=1)
            distances[i] = np.inf
            nearest_distances.append(np.min(distances))
        
        mean_distance = np.mean(nearest_distances)
        self.passed = mean_distance < 0.1
        self.message = f"Mean nearest neighbor distance: {mean_distance:.4f}"
        self.details = {
            'mean_nn_distance': mean_distance,
            'sample_size': sample_size
        }
        return self.passed


class AnchorCoverageTest(ValidationTest):
    """Test that critical anchors are present."""
    def __init__(self):
        super().__init__("Anchor Coverage")
    
    def run(self, semantic_space, concepts):
        coords = np.array([c['coordinates'] for c in concepts])
        
        # Check for low-dimensional extremes
        anchors_found = {}
        for i, dim_name in enumerate(DIMENSION_NAMES):
            dim_values = coords[:, i]
            anchors_found[f'low_{dim_name}'] = np.sum(dim_values < 0.1)
            anchors_found[f'high_{dim_name}'] = np.sum(dim_values > 0.9)
        
        # Check equilibrium-adjacent
        eq_distances = np.linalg.norm(coords - EQUILIBRIUM, axis=1)
        anchors_found['near_equilibrium'] = np.sum(eq_distances < 0.1)
        
        # All categories should have at least 5 concepts
        missing = [k for k, v in anchors_found.items() if v < 5]
        
        self.passed = len(missing) == 0
        self.message = f"All anchor categories covered" if self.passed else f"Missing anchors: {', '.join(missing)}"
        self.details = anchors_found
        return self.passed


def run_validation_suite(filepath):
    """Run all validation tests."""
    print("="*60)
    print("LJPW COMPREHENSIVE VALIDATION SUITE")
    print("="*60)
    
    # Load semantic space
    print(f"\nLoading: {filepath}")
    semantic_space = load_semantic_space(filepath)
    concepts = extract_all_concepts(semantic_space)
    
    print(f"Concepts: {len(concepts):,}")
    print(f"Domains: {len(semantic_space['domains'])}")
    
    # Define tests
    tests = [
        CoordinateValidityTest(),
        CompletenessTest(),
        DimensionalCoverageTest(),
        EquilibriumAlignmentTest(),
        DensityUniformityTest(),
        RelationshipRichnessTest(),
        AnchorCoverageTest(),
    ]
    
    # Run tests
    print(f"\n{'='*60}")
    print("RUNNING VALIDATION TESTS")
    print(f"{'='*60}\n")
    
    results = []
    for test in tests:
        print(f"Running: {test.name}...")
        passed = test.run(semantic_space, concepts)
        results.append(test)
        
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status} {test.message}")
    
    # Summary
    passed_count = sum(1 for t in results if t.passed)
    total_count = len(results)
    
    print(f"\n{'='*60}")
    print("VALIDATION SUMMARY")
    print(f"{'='*60}\n")
    print(f"Tests Passed: {passed_count}/{total_count}")
    print(f"Success Rate: {passed_count/total_count:.1%}\n")
    
    if passed_count == total_count:
        print("[SUCCESS] All validation tests passed!")
    else:
        print("[WARNING] Some tests failed. Review details above.")
    
    # Detailed results
    print(f"\n{'='*60}")
    print("DETAILED RESULTS")
    print(f"{'='*60}\n")
    
    for test in results:
        print(f"{test.name}:")
        print(f"  Status: {'PASS' if test.passed else 'FAIL'}")
        print(f"  Message: {test.message}")
        if test.details:
            print(f"  Details: {test.details}")
        print()
    
    return passed_count == total_count


def main():
    """Main validation function."""
    # Test the final semantic space
    filepath = "experiments/semantic_space_6353_VALIDATED.json"
    all_passed = run_validation_suite(filepath)
    
    if all_passed:
        print("\n" + "="*60)
        print("SEMANTIC SPACE VALIDATED SUCCESSFULLY!")
        print("="*60)
        return 0
    else:
        print("\n" + "="*60)
        print("VALIDATION FAILED - REVIEW REQUIRED")
        print("="*60)
        return 1


if __name__ == "__main__":
    np.random.seed(42)
    exit(main())
