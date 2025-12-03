#!/usr/bin/env python3
"""
SEMANTIC SUBSTRATE ANALYSIS
Query the deep structure of semantic space itself

This explores:
1. Mathematical relationships (vector fields, curvature, topology)
2. Semantic Query Language (SQL for meaning)
3. Direct queries to meaning (vector calculus)
4. Semantic metadata (complexity, stability, richness)
5. Semantic resonance patterns (harmonics, entailment)
"""

import numpy as np
import json
from typing import Dict, List, Tuple, Callable, Any
from dataclasses import dataclass
from scipy.spatial.distance import pdist, squareform
from scipy.stats import entropy
from collections import defaultdict
import itertools


# Natural equilibrium point
EQUILIBRIUM = np.array([0.618034, 0.414214, 0.718282, 0.693147])  # φ⁻¹, √2-1, e-2, ln2


@dataclass
class SemanticMetadata:
    """Metadata about a semantic point"""
    complexity: float  # Entropy in local neighborhood
    stability: float  # Inverse of variance across contexts
    dimensionality: float  # Effective dimensionality
    concreteness: float  # Distance from sensory space
    polysemy: int  # Number of distinct semantic clusters
    richness: float  # Volume of semantic neighborhood


class SemanticVectorField:
    """Analyze vector fields in semantic space"""

    def __init__(self, semantic_points: Dict[str, np.ndarray]):
        self.points = semantic_points
        self.words = list(semantic_points.keys())
        self.coords = np.array(list(semantic_points.values()))

    def gradient(self, point: np.ndarray, scalar_field: Callable) -> np.ndarray:
        """Compute gradient: direction of steepest increase

        ∇f = (∂f/∂L, ∂f/∂J, ∂f/∂P, ∂f/∂W)
        """
        epsilon = 1e-5
        grad = np.zeros(4)

        for i in range(4):
            point_plus = point.copy()
            point_plus[i] += epsilon
            point_minus = point.copy()
            point_minus[i] -= epsilon

            grad[i] = (scalar_field(point_plus) - scalar_field(point_minus)) / (2 * epsilon)

        return grad

    def divergence(self, point: np.ndarray, vector_field: Callable) -> float:
        """Compute divergence: source/sink strength

        ∇·F = ∂F_L/∂L + ∂F_J/∂J + ∂F_P/∂P + ∂F_W/∂W

        Positive divergence = source (meaning emanates)
        Negative divergence = sink (meaning converges)
        """
        epsilon = 1e-5
        div = 0.0

        for i in range(4):
            point_plus = point.copy()
            point_plus[i] += epsilon
            point_minus = point.copy()
            point_minus[i] -= epsilon

            F_plus = vector_field(point_plus)[i]
            F_minus = vector_field(point_minus)[i]

            div += (F_plus - F_minus) / (2 * epsilon)

        return div

    def curl(self, point: np.ndarray, vector_field: Callable) -> np.ndarray:
        """Compute curl: rotational patterns (in 4D, returns 6 components)

        In 4D, curl is a bivector (6 components for 6 planes)
        Measures circular semantic flows
        """
        epsilon = 1e-5
        curl_components = []

        # All pairs of dimensions (6 combinations)
        pairs = [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]

        for i, j in pairs:
            # ∂F_j/∂x_i - ∂F_i/∂x_j
            point_plus_i = point.copy()
            point_plus_i[i] += epsilon
            point_minus_i = point.copy()
            point_minus_i[i] -= epsilon

            dFj_dxi = (vector_field(point_plus_i)[j] - vector_field(point_minus_i)[j]) / (2 * epsilon)

            point_plus_j = point.copy()
            point_plus_j[j] += epsilon
            point_minus_j = point.copy()
            point_minus_j[j] -= epsilon

            dFi_dxj = (vector_field(point_plus_j)[i] - vector_field(point_minus_j)[i]) / (2 * epsilon)

            curl_components.append(dFj_dxi - dFi_dxj)

        return np.array(curl_components)

    def laplacian(self, point: np.ndarray, scalar_field: Callable) -> float:
        """Compute Laplacian: semantic diffusion

        ∇²f = ∂²f/∂L² + ∂²f/∂J² + ∂²f/∂P² + ∂²f/∂W²

        Measures how much a point differs from its neighborhood average
        """
        epsilon = 1e-5
        laplacian = 0.0
        f_center = scalar_field(point)

        for i in range(4):
            point_plus = point.copy()
            point_plus[i] += epsilon
            point_minus = point.copy()
            point_minus[i] -= epsilon

            # Second derivative: (f(x+ε) - 2f(x) + f(x-ε)) / ε²
            laplacian += (scalar_field(point_plus) - 2*f_center + scalar_field(point_minus)) / (epsilon**2)

        return laplacian

    def semantic_flow_field(self, point: np.ndarray) -> np.ndarray:
        """Vector field pointing toward semantic equilibrium

        F(x) = direction from x toward equilibrium
        """
        return EQUILIBRIUM - point

    def meaning_gradient_field(self, point: np.ndarray) -> np.ndarray:
        """Vector field pointing toward nearest meaning

        F(x) = direction toward closest semantic point
        """
        distances = np.linalg.norm(self.coords - point, axis=1)
        nearest_idx = np.argmin(distances)
        return self.coords[nearest_idx] - point

    def analyze_vector_field(self, word: str) -> Dict:
        """Complete vector field analysis at a semantic point"""
        point = self.points[word]

        # Scalar field: distance to equilibrium
        def equilibrium_distance(p):
            return np.linalg.norm(p - EQUILIBRIUM)

        # Vector field: flow toward equilibrium
        flow_field = self.semantic_flow_field

        gradient = self.gradient(point, equilibrium_distance)
        div = self.divergence(point, flow_field)
        curl = self.curl(point, flow_field)
        laplacian = self.laplacian(point, equilibrium_distance)

        return {
            'word': word,
            'gradient': gradient.tolist(),
            'gradient_magnitude': float(np.linalg.norm(gradient)),
            'divergence': float(div),
            'curl': curl.tolist(),
            'curl_magnitude': float(np.linalg.norm(curl)),
            'laplacian': float(laplacian),
            'interpretation': {
                'gradient': 'Direction of increasing distance from equilibrium',
                'divergence': 'Source (+) or sink (-) of semantic flow',
                'curl': 'Rotational semantic patterns',
                'laplacian': 'Semantic diffusion rate'
            }
        }


class SemanticQueryLanguage:
    """SQL for meaning: query semantic space directly"""

    def __init__(self, semantic_points: Dict[str, np.ndarray]):
        self.points = semantic_points
        self.words = list(semantic_points.keys())
        self.coords = np.array(list(semantic_points.values()))

    def SELECT(self, *dimensions: str) -> 'SemanticQueryLanguage':
        """SELECT specific dimensions (L, J, P, W)"""
        self.selected_dims = dimensions
        return self

    def WHERE(self, condition: Callable[[str, np.ndarray], bool]) -> List[str]:
        """WHERE clause with semantic conditions"""
        results = []
        for word, coord in self.points.items():
            if condition(word, coord):
                results.append(word)
        return results

    def NEAR(self, target_word: str, max_distance: float = 0.3) -> List[Tuple[str, float]]:
        """Find meanings NEAR a target"""
        target = self.points[target_word]
        results = []

        for word, coord in self.points.items():
            if word != target_word:
                dist = np.linalg.norm(coord - target)
                if dist <= max_distance:
                    results.append((word, float(dist)))

        return sorted(results, key=lambda x: x[1])

    def FAR(self, target_word: str, min_distance: float = 0.5) -> List[Tuple[str, float]]:
        """Find meanings FAR from a target"""
        target = self.points[target_word]
        results = []

        for word, coord in self.points.items():
            if word != target_word:
                dist = np.linalg.norm(coord - target)
                if dist >= min_distance:
                    results.append((word, float(dist)))

        return sorted(results, key=lambda x: x[1], reverse=True)

    def BETWEEN(self, word1: str, word2: str, tolerance: float = 0.1) -> List[str]:
        """Find meanings geometrically BETWEEN two words"""
        p1 = self.points[word1]
        p2 = self.points[word2]

        results = []
        for word, coord in self.points.items():
            if word not in [word1, word2]:
                # Check if point is near the line segment
                # Project onto line
                line_vec = p2 - p1
                line_len = np.linalg.norm(line_vec)
                if line_len < 1e-10:
                    continue

                line_dir = line_vec / line_len
                point_vec = coord - p1
                projection_length = np.dot(point_vec, line_dir)

                # Check if projection is between p1 and p2
                if 0 <= projection_length <= line_len:
                    # Distance to line
                    projection = p1 + projection_length * line_dir
                    distance = np.linalg.norm(coord - projection)

                    if distance <= tolerance:
                        results.append(word)

        return results

    def ORTHOGONAL(self, word1: str, word2: str, tolerance: float = 0.2) -> List[str]:
        """Find meanings creating orthogonal relationships"""
        p1 = self.points[word1]
        p2 = self.points[word2]

        v1 = p2 - p1  # Vector from word1 to word2

        results = []
        for word, coord in self.points.items():
            if word not in [word1, word2]:
                v2 = coord - p1  # Vector from word1 to candidate

                # Check orthogonality: cos(θ) ≈ 0
                cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-10)

                if abs(cos_angle) <= tolerance:
                    results.append((word, float(abs(cos_angle))))

        return sorted(results, key=lambda x: x[1])

    def PARALLEL(self, word1: str, word2: str, tolerance: float = 0.2) -> List[Tuple[str, str, float]]:
        """Find meaning pairs that are PARALLEL to word1→word2 relationship"""
        p1 = self.points[word1]
        p2 = self.points[word2]

        v_ref = p2 - p1  # Reference vector

        results = []
        # Check all pairs
        for w1, w2 in itertools.combinations(self.words, 2):
            if w1 in [word1, word2] or w2 in [word1, word2]:
                continue

            v_test = self.points[w2] - self.points[w1]

            # Check parallelism: |cos(θ)| ≈ 1
            cos_angle = np.dot(v_ref, v_test) / (np.linalg.norm(v_ref) * np.linalg.norm(v_test) + 1e-10)

            if abs(abs(cos_angle) - 1.0) <= tolerance:
                results.append((w1, w2, float(cos_angle)))

        return sorted(results, key=lambda x: abs(abs(x[2]) - 1.0))

    def IN_REGION(self, L_range: Tuple[float, float], J_range: Tuple[float, float],
                  P_range: Tuple[float, float], W_range: Tuple[float, float]) -> List[str]:
        """Find meanings in a hypercube region"""
        results = []
        for word, coord in self.points.items():
            L, J, P, W = coord
            if (L_range[0] <= L <= L_range[1] and
                J_range[0] <= J <= J_range[1] and
                P_range[0] <= P <= P_range[1] and
                W_range[0] <= W <= W_range[1]):
                results.append(word)
        return results

    def JOIN(self, other_word: str, relationship: str = 'nearest') -> List[Tuple[str, str, float]]:
        """JOIN operation: connect semantically related meanings"""
        results = []

        if relationship == 'nearest':
            # For each word, find its nearest neighbor
            for word, coord in self.points.items():
                if word == other_word:
                    continue
                distances = []
                for w2, c2 in self.points.items():
                    if w2 != word:
                        distances.append((w2, np.linalg.norm(coord - c2)))
                nearest = min(distances, key=lambda x: x[1])
                results.append((word, nearest[0], float(nearest[1])))

        return sorted(results, key=lambda x: x[2])


class SemanticMetadataAnalyzer:
    """Measure metadata about meanings"""

    def __init__(self, semantic_points: Dict[str, np.ndarray]):
        self.points = semantic_points
        self.words = list(semantic_points.keys())
        self.coords = np.array(list(semantic_points.values()))

    def compute_complexity(self, word: str, k: int = 5) -> float:
        """Semantic complexity: entropy in local neighborhood

        High complexity = many diverse neighbors
        Low complexity = homogeneous neighborhood
        """
        coord = self.points[word]

        # Find k nearest neighbors
        distances = np.linalg.norm(self.coords - coord, axis=1)
        nearest_indices = np.argsort(distances)[1:k+1]  # Exclude self

        # Compute entropy of coordinate distributions
        neighbor_coords = self.coords[nearest_indices]

        # Discretize each dimension into bins
        entropies = []
        for dim in range(4):
            values = neighbor_coords[:, dim]
            hist, _ = np.histogram(values, bins=3, density=True)
            hist = hist + 1e-10  # Avoid log(0)
            entropies.append(entropy(hist))

        return float(np.mean(entropies))

    def compute_stability(self, word: str, k: int = 5) -> float:
        """Semantic stability: inverse of variance in neighborhood

        High stability = consistent local environment
        Low stability = volatile neighborhood
        """
        coord = self.points[word]

        # Find k nearest neighbors
        distances = np.linalg.norm(self.coords - coord, axis=1)
        nearest_indices = np.argsort(distances)[1:k+1]

        neighbor_coords = self.coords[nearest_indices]
        variance = np.mean(np.var(neighbor_coords, axis=0))

        # Return inverse (high variance = low stability)
        return float(1.0 / (variance + 0.01))

    def compute_dimensionality(self, word: str, k: int = 10) -> float:
        """Effective dimensionality: how many dimensions does meaning span?

        Use PCA on local neighborhood
        """
        coord = self.points[word]

        # Find k nearest neighbors
        distances = np.linalg.norm(self.coords - coord, axis=1)
        nearest_indices = np.argsort(distances)[1:k+1]

        neighbor_coords = self.coords[nearest_indices]

        # Center the data
        centered = neighbor_coords - np.mean(neighbor_coords, axis=0)

        # Compute covariance matrix
        cov_matrix = np.cov(centered.T)

        # Eigenvalues
        eigenvalues = np.linalg.eigvalsh(cov_matrix)
        eigenvalues = np.maximum(eigenvalues, 0)  # Ensure non-negative

        # Effective dimensionality: inverse participation ratio
        if np.sum(eigenvalues) < 1e-10:
            return 1.0

        normalized = eigenvalues / np.sum(eigenvalues)
        effective_dim = 1.0 / np.sum(normalized**2)

        return float(effective_dim)

    def compute_concreteness(self, word: str) -> float:
        """Concreteness: how sensory/physical is the meaning?

        Heuristic: distance from sensory anchor points
        Sensory space: high L (positive affect) + high P (physical)
        Abstract space: high W (cognitive) + high J (relational)
        """
        coord = self.points[word]
        L, J, P, W = coord

        # Sensory anchor: high physical presence
        sensory_score = L + P - W - J

        # Normalize to [0, 1]
        concreteness = (sensory_score + 2.0) / 4.0  # Range [-2, 2] → [0, 1]

        return float(np.clip(concreteness, 0, 1))

    def compute_richness(self, word: str, k: int = 10) -> float:
        """Semantic richness: volume of semantic neighborhood

        Measured by determinant of covariance matrix
        """
        coord = self.points[word]

        # Find k nearest neighbors
        distances = np.linalg.norm(self.coords - coord, axis=1)
        nearest_indices = np.argsort(distances)[1:k+1]

        neighbor_coords = self.coords[nearest_indices]

        # Covariance matrix
        centered = neighbor_coords - np.mean(neighbor_coords, axis=0)
        cov_matrix = np.cov(centered.T)

        # Volume = sqrt(determinant)
        det = np.linalg.det(cov_matrix)
        richness = np.sqrt(max(det, 0))

        return float(richness)

    def compute_polysemy(self, word: str) -> int:
        """Polysemy: number of distinct semantic clusters

        Simplified: count local maxima in neighborhood density
        """
        # For now, return 1 (single meaning)
        # Full implementation would require context-dependent embeddings
        return 1

    def analyze_metadata(self, word: str) -> SemanticMetadata:
        """Complete metadata analysis"""
        return SemanticMetadata(
            complexity=self.compute_complexity(word),
            stability=self.compute_stability(word),
            dimensionality=self.compute_dimensionality(word),
            concreteness=self.compute_concreteness(word),
            polysemy=self.compute_polysemy(word),
            richness=self.compute_richness(word)
        )


class SemanticResonancePatterns:
    """Discover semantic resonance patterns"""

    def __init__(self, semantic_points: Dict[str, np.ndarray]):
        self.points = semantic_points
        self.words = list(semantic_points.keys())
        self.coords = np.array(list(semantic_points.values()))

    def harmonic_resonance(self, word1: str, word2: str) -> float:
        """Harmonic resonance: do meanings oscillate together?

        Measured by correlation of deviations from equilibrium
        """
        c1 = self.points[word1] - EQUILIBRIUM
        c2 = self.points[word2] - EQUILIBRIUM

        # Correlation
        correlation = np.dot(c1, c2) / (np.linalg.norm(c1) * np.linalg.norm(c2) + 1e-10)

        return float(correlation)

    def entailment_strength(self, word1: str, word2: str) -> float:
        """Entailment: does word1 imply word2?

        word1 → word2 if word2 is "beyond" word1 toward equilibrium
        """
        c1 = self.points[word1]
        c2 = self.points[word2]

        # Direction from word1 to equilibrium
        to_equilibrium = EQUILIBRIUM - c1
        to_word2 = c2 - c1

        # Entailment if word2 is in same direction as equilibrium
        if np.linalg.norm(to_word2) < 1e-10:
            return 0.0

        cos_angle = np.dot(to_equilibrium, to_word2) / (
            np.linalg.norm(to_equilibrium) * np.linalg.norm(to_word2) + 1e-10
        )

        # Positive correlation = entailment
        return float(max(cos_angle, 0))

    def antonymy_score(self, word1: str, word2: str) -> float:
        """Antonymy: do meanings oppose each other?

        Measured by alignment with equilibrium as center
        """
        c1 = self.points[word1] - EQUILIBRIUM
        c2 = self.points[word2] - EQUILIBRIUM

        # Perfect antonyms: c2 = -c1 (opposite directions from equilibrium)
        similarity = np.dot(c1, c2) / (np.linalg.norm(c1) * np.linalg.norm(c2) + 1e-10)

        # Antonymy is negative similarity
        antonymy = -similarity

        return float(max(antonymy, 0))

    def find_harmonics(self, reference_word: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """Find words that resonate harmonically with reference"""
        results = []

        for word in self.words:
            if word != reference_word:
                resonance = self.harmonic_resonance(reference_word, word)
                results.append((word, resonance))

        return sorted(results, key=lambda x: abs(x[1]), reverse=True)[:top_k]

    def find_entailments(self, reference_word: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """Find words that are entailed by reference"""
        results = []

        for word in self.words:
            if word != reference_word:
                entailment = self.entailment_strength(reference_word, word)
                if entailment > 0.1:
                    results.append((word, entailment))

        return sorted(results, key=lambda x: x[1], reverse=True)[:top_k]

    def find_antonyms(self, reference_word: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """Find semantic antonyms"""
        results = []

        for word in self.words:
            if word != reference_word:
                antonymy = self.antonymy_score(reference_word, word)
                if antonymy > 0.3:
                    results.append((word, antonymy))

        return sorted(results, key=lambda x: x[1], reverse=True)[:top_k]


def run_complete_analysis():
    """Run complete semantic substrate analysis"""

    # Load semantic points from previous experiments
    print("=" * 80)
    print("SEMANTIC SUBSTRATE ANALYSIS")
    print("Querying the deep structure of meaning itself")
    print("=" * 80)

    # Use core vocabulary from previous experiments
    semantic_points = {
        # Core emotions
        'love': np.array([0.92, 0.45, 0.15, 0.70]),
        'hate': np.array([0.12, 0.35, 0.75, 0.25]),
        'joy': np.array([0.88, 0.42, 0.38, 0.65]),
        'sadness': np.array([0.35, 0.48, 0.22, 0.55]),
        'fear': np.array([0.25, 0.52, 0.28, 0.45]),
        'anger': np.array([0.28, 0.55, 0.72, 0.35]),
        'peace': np.array([0.75, 0.65, 0.25, 0.72]),
        'hope': np.array([0.78, 0.48, 0.35, 0.68]),

        # Virtues and vices
        'compassion': np.array([0.88, 0.72, 0.32, 0.75]),
        'courage': np.array([0.65, 0.62, 0.68, 0.70]),
        'wisdom': np.array([0.70, 0.68, 0.42, 0.88]),
        'justice': np.array([0.60, 0.88, 0.58, 0.78]),
        'mercy': np.array([0.85, 0.72, 0.35, 0.70]),
        'truth': np.array([0.62, 0.78, 0.48, 0.85]),
        'honesty': np.array([0.68, 0.82, 0.45, 0.80]),
        'humility': np.array([0.72, 0.70, 0.28, 0.75]),
        'pride': np.array([0.38, 0.35, 0.78, 0.42]),
        'greed': np.array([0.22, 0.28, 0.82, 0.35]),
        'envy': np.array([0.28, 0.38, 0.68, 0.32]),

        # Abstract concepts
        'freedom': np.array([0.75, 0.72, 0.65, 0.78]),
        'beauty': np.array([0.82, 0.55, 0.42, 0.68]),
        'faith': np.array([0.80, 0.58, 0.38, 0.72]),
        'knowledge': np.array([0.55, 0.58, 0.52, 0.85]),
        'power': np.array([0.45, 0.48, 0.88, 0.62]),
        'weakness': np.array([0.42, 0.45, 0.22, 0.48]),

        # Concrete concepts
        'light': np.array([0.85, 0.62, 0.55, 0.82]),
        'darkness': np.array([0.28, 0.35, 0.42, 0.38]),
        'fire': np.array([0.55, 0.48, 0.78, 0.58]),
        'water': np.array([0.68, 0.60, 0.45, 0.65]),
        'earth': np.array([0.58, 0.62, 0.68, 0.62]),
        'air': np.array([0.72, 0.58, 0.52, 0.70]),

        # Relational
        'friendship': np.array([0.82, 0.68, 0.42, 0.72]),
        'betrayal': np.array([0.18, 0.42, 0.65, 0.28]),
        'loyalty': np.array([0.78, 0.75, 0.58, 0.75]),
        'forgiveness': np.array([0.88, 0.78, 0.35, 0.78]),

        # Actions
        'give': np.array([0.82, 0.68, 0.42, 0.68]),
        'take': np.array([0.32, 0.38, 0.72, 0.42]),
        'create': np.array([0.75, 0.58, 0.68, 0.82]),
        'destroy': np.array([0.22, 0.35, 0.78, 0.32]),
        'heal': np.array([0.85, 0.72, 0.48, 0.75]),
        'harm': np.array([0.18, 0.32, 0.75, 0.28]),
    }

    results = {
        'vector_field_analysis': {},
        'semantic_queries': {},
        'metadata_analysis': {},
        'resonance_patterns': {}
    }

    # 1. VECTOR FIELD ANALYSIS
    print("\n" + "=" * 80)
    print("1. VECTOR FIELD ANALYSIS: Asking Meaning What It's Related To")
    print("=" * 80)

    vector_field = SemanticVectorField(semantic_points)

    test_words = ['love', 'hate', 'wisdom', 'power', 'peace']
    for word in test_words:
        analysis = vector_field.analyze_vector_field(word)
        results['vector_field_analysis'][word] = analysis

        print(f"\n{word.upper()} (coordinates: {semantic_points[word]})")
        print(f"  Gradient magnitude: {analysis['gradient_magnitude']:.4f}")
        print(f"    → Direction of steepest increase from equilibrium")
        print(f"  Divergence: {analysis['divergence']:.4f}")
        if analysis['divergence'] > 0:
            print(f"    → SOURCE: meaning emanates outward")
        else:
            print(f"    → SINK: meaning converges inward")
        print(f"  Curl magnitude: {analysis['curl_magnitude']:.4f}")
        print(f"    → Rotational semantic flow strength")
        print(f"  Laplacian: {analysis['laplacian']:.4f}")
        print(f"    → Semantic diffusion rate")

    # 2. SEMANTIC QUERY LANGUAGE
    print("\n" + "=" * 80)
    print("2. SEMANTIC QUERY LANGUAGE: SQL for Meaning")
    print("=" * 80)

    sql = SemanticQueryLanguage(semantic_points)

    # Query 1: NEAR love
    print("\nQUERY: SELECT * WHERE NEAR('love', distance < 0.3)")
    near_love = sql.NEAR('love', max_distance=0.3)
    for word, dist in near_love[:5]:
        print(f"  {word}: {dist:.4f}")
    results['semantic_queries']['near_love'] = near_love[:5]

    # Query 2: BETWEEN love and hate
    print("\nQUERY: SELECT * WHERE BETWEEN('love', 'hate')")
    between = sql.BETWEEN('love', 'hate', tolerance=0.15)
    print(f"  Found {len(between)} meanings between love and hate:")
    for word in between[:5]:
        print(f"    {word}")
    results['semantic_queries']['between_love_hate'] = between

    # Query 3: ORTHOGONAL to love→wisdom
    print("\nQUERY: SELECT * WHERE ORTHOGONAL('love', 'wisdom')")
    orthogonal = sql.ORTHOGONAL('love', 'wisdom', tolerance=0.2)
    for word, score in orthogonal[:5]:
        print(f"  {word}: {score:.4f} (cosine similarity)")
    results['semantic_queries']['orthogonal_love_wisdom'] = orthogonal[:5]

    # Query 4: PARALLEL relationships
    print("\nQUERY: SELECT * WHERE PARALLEL('love', 'hate') -- find similar oppositions")
    parallel = sql.PARALLEL('love', 'hate', tolerance=0.3)
    for w1, w2, score in parallel[:5]:
        print(f"  {w1} → {w2}: {score:.4f}")
    results['semantic_queries']['parallel_love_hate'] = parallel[:5]

    # Query 5: IN_REGION
    print("\nQUERY: SELECT * WHERE IN_REGION(L>0.8, J>0.6, P<0.5, W>0.7)")
    in_region = sql.IN_REGION((0.8, 1.0), (0.6, 1.0), (0.0, 0.5), (0.7, 1.0))
    print(f"  High Love, High Justice, Low Power, High Wisdom:")
    for word in in_region:
        print(f"    {word}: {semantic_points[word]}")
    results['semantic_queries']['high_wisdom_region'] = in_region

    # 3. SEMANTIC METADATA
    print("\n" + "=" * 80)
    print("3. SEMANTIC METADATA: Properties of Meaning")
    print("=" * 80)

    metadata_analyzer = SemanticMetadataAnalyzer(semantic_points)

    test_words = ['love', 'wisdom', 'peace', 'power', 'light', 'darkness']
    metadata_results = {}

    for word in test_words:
        metadata = metadata_analyzer.analyze_metadata(word)
        metadata_results[word] = {
            'complexity': metadata.complexity,
            'stability': metadata.stability,
            'dimensionality': metadata.dimensionality,
            'concreteness': metadata.concreteness,
            'richness': metadata.richness
        }

        print(f"\n{word.upper()}")
        print(f"  Complexity: {metadata.complexity:.4f} (entropy in neighborhood)")
        print(f"  Stability: {metadata.stability:.4f} (inverse variance)")
        print(f"  Dimensionality: {metadata.dimensionality:.2f} (effective dimensions)")
        print(f"  Concreteness: {metadata.concreteness:.4f} (0=abstract, 1=concrete)")
        print(f"  Richness: {metadata.richness:.6f} (semantic volume)")

    results['metadata_analysis'] = metadata_results

    # 4. SEMANTIC RESONANCE PATTERNS
    print("\n" + "=" * 80)
    print("4. SEMANTIC RESONANCE PATTERNS: Harmonic Relationships")
    print("=" * 80)

    resonance = SemanticResonancePatterns(semantic_points)

    test_words = ['love', 'wisdom', 'power', 'justice']

    for word in test_words:
        print(f"\n{word.upper()} resonance patterns:")

        # Harmonics
        harmonics = resonance.find_harmonics(word, top_k=5)
        print(f"  Harmonic resonance (oscillate together):")
        for w, score in harmonics:
            print(f"    {w}: {score:+.4f}")

        # Entailments
        entailments = resonance.find_entailments(word, top_k=5)
        if entailments:
            print(f"  Entailments ({word} implies...):")
            for w, score in entailments:
                print(f"    {w}: {score:.4f}")

        # Antonyms
        antonyms = resonance.find_antonyms(word, top_k=3)
        if antonyms:
            print(f"  Semantic antonyms:")
            for w, score in antonyms:
                print(f"    {w}: {score:.4f}")

        results['resonance_patterns'][word] = {
            'harmonics': [(w, float(s)) for w, s in harmonics],
            'entailments': [(w, float(s)) for w, s in entailments],
            'antonyms': [(w, float(s)) for w, s in antonyms]
        }

    # Save results
    output_file = 'experiments/semantic_substrate_analysis.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 80)
    print(f"Analysis complete. Results saved to {output_file}")
    print("=" * 80)

    return results


if __name__ == "__main__":
    run_complete_analysis()
