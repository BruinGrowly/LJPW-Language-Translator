#!/usr/bin/env python3
"""
TOPOLOGICAL SEMANTIC MAPPING
Build a comprehensive map of semantic space using English and Mandarin

This explores:
1. Clustering analysis - identify semantic territories
2. Persistent homology - find topological features (holes, boundaries, cycles)
3. Boundary detection - map the edges of semantic regions
4. Territory characterization - profile each region
5. Wedau translation - use the map to find Wedau word meanings
"""

import numpy as np
import json
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.spatial.distance import pdist, squareform, cdist
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.decomposition import PCA
import itertools


# Natural equilibrium point
EQUILIBRIUM = np.array([0.618034, 0.414214, 0.718282, 0.693147])  # φ⁻¹, √2-1, e-2, ln2
ANCHOR = np.array([1.0, 1.0, 1.0, 1.0])


@dataclass
class SemanticTerritory:
    """A region in semantic space"""
    id: int
    name: str
    center: np.ndarray
    radius: float
    members: List[str]
    languages: Dict[str, int]  # Language distribution
    L_range: Tuple[float, float]
    J_range: Tuple[float, float]
    P_range: Tuple[float, float]
    W_range: Tuple[float, float]
    harmony_mean: float
    density: float
    stability: float


@dataclass
class TopologicalFeature:
    """A topological feature in semantic space"""
    feature_type: str  # 'void', 'boundary', 'cluster', 'bridge'
    birth_scale: float
    death_scale: float
    persistence: float
    location: np.ndarray
    associated_words: List[str]


class TopologicalSemanticMapper:
    """Build comprehensive topological map of semantic space"""

    def __init__(self, semantic_points: Dict[str, Dict]):
        """
        semantic_points: {word: {'coords': np.array, 'language': str}}
        """
        self.points = semantic_points
        self.words = list(semantic_points.keys())
        self.coords = np.array([p['coords'] for p in semantic_points.values()])
        self.languages = {w: p['language'] for w, p in semantic_points.items()}

    def compute_harmony(self, coords: np.ndarray) -> float:
        """Harmony index: alignment with perfection"""
        distance = np.linalg.norm(coords - ANCHOR)
        return 1.0 / (1.0 + distance)

    def hierarchical_clustering(self, n_clusters: int = 8) -> Dict:
        """Hierarchical clustering to identify semantic regions"""
        # Compute linkage matrix
        linkage_matrix = linkage(self.coords, method='ward')

        # Assign clusters
        clusters = fcluster(linkage_matrix, n_clusters, criterion='maxclust')

        # Group words by cluster
        cluster_members = defaultdict(list)
        for word, cluster_id in zip(self.words, clusters):
            cluster_members[cluster_id].append(word)

        return {
            'linkage_matrix': linkage_matrix,
            'cluster_assignments': dict(zip(self.words, clusters.tolist())),
            'cluster_members': dict(cluster_members),
            'n_clusters': n_clusters
        }

    def density_clustering(self, eps: float = 0.25, min_samples: int = 3) -> Dict:
        """DBSCAN density-based clustering to find natural groupings"""
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        clusters = dbscan.fit_predict(self.coords)

        # Group by cluster (-1 is noise)
        cluster_members = defaultdict(list)
        for word, cluster_id in zip(self.words, clusters):
            cluster_members[cluster_id].append(word)

        n_clusters = len([c for c in set(clusters) if c != -1])
        n_noise = len([c for c in clusters if c == -1])

        return {
            'cluster_assignments': dict(zip(self.words, clusters.tolist())),
            'cluster_members': dict(cluster_members),
            'n_clusters': n_clusters,
            'n_noise': n_noise,
            'noise_words': cluster_members.get(-1, [])
        }

    def kmeans_clustering(self, n_clusters: int = 8) -> Dict:
        """K-means clustering for balanced territories"""
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=50)
        clusters = kmeans.fit_predict(self.coords)

        cluster_members = defaultdict(list)
        for word, cluster_id in zip(self.words, clusters):
            cluster_members[cluster_id].append(word)

        return {
            'cluster_assignments': dict(zip(self.words, clusters.tolist())),
            'cluster_members': dict(cluster_members),
            'centroids': kmeans.cluster_centers_,
            'inertia': float(kmeans.inertia_),
            'n_clusters': n_clusters
        }

    def characterize_territory(self, cluster_id: int, members: List[str],
                              centroid: np.ndarray = None) -> SemanticTerritory:
        """Characterize a semantic territory"""
        # Get coordinates of members
        member_coords = np.array([self.points[w]['coords'] for w in members])

        # Compute center
        if centroid is None:
            center = np.mean(member_coords, axis=0)
        else:
            center = centroid

        # Compute radius (max distance from center)
        distances = np.linalg.norm(member_coords - center, axis=1)
        radius = float(np.max(distances))

        # Language distribution
        lang_dist = defaultdict(int)
        for w in members:
            lang_dist[self.languages[w]] += 1

        # Dimensional ranges
        L_vals = member_coords[:, 0]
        J_vals = member_coords[:, 1]
        P_vals = member_coords[:, 2]
        W_vals = member_coords[:, 3]

        # Harmony
        harmonies = [self.compute_harmony(c) for c in member_coords]
        harmony_mean = float(np.mean(harmonies))

        # Density: members per unit volume
        volume = (4/3) * np.pi * (radius ** 4)  # 4D sphere volume (approximation)
        density = len(members) / (volume + 1e-10)

        # Stability: inverse of variance
        variance = np.mean(np.var(member_coords, axis=0))
        stability = 1.0 / (variance + 0.01)

        # Generate name based on dominant characteristics
        L_mean, J_mean, P_mean, W_mean = center
        name_parts = []
        if L_mean > 0.7:
            name_parts.append("Loving")
        elif L_mean < 0.4:
            name_parts.append("Cold")

        if J_mean > 0.7:
            name_parts.append("Just")
        elif J_mean < 0.4:
            name_parts.append("Unjust")

        if P_mean > 0.7:
            name_parts.append("Powerful")
        elif P_mean < 0.4:
            name_parts.append("Weak")

        if W_mean > 0.7:
            name_parts.append("Wise")
        elif W_mean < 0.4:
            name_parts.append("Foolish")

        if not name_parts:
            name_parts.append("Balanced")

        name = " ".join(name_parts) + " Territory"

        return SemanticTerritory(
            id=cluster_id,
            name=name,
            center=center,
            radius=radius,
            members=members,
            languages=dict(lang_dist),
            L_range=(float(np.min(L_vals)), float(np.max(L_vals))),
            J_range=(float(np.min(J_vals)), float(np.max(J_vals))),
            P_range=(float(np.min(P_vals)), float(np.max(P_vals))),
            W_range=(float(np.min(W_vals)), float(np.max(W_vals))),
            harmony_mean=harmony_mean,
            density=float(density),
            stability=float(stability)
        )

    def find_voids(self, grid_resolution: int = 5) -> List[TopologicalFeature]:
        """Find voids (holes) in semantic space using grid sampling"""
        voids = []

        # Create grid
        L_range = np.linspace(0.1, 0.95, grid_resolution)
        J_range = np.linspace(0.1, 0.95, grid_resolution)
        P_range = np.linspace(0.1, 0.95, grid_resolution)
        W_range = np.linspace(0.1, 0.95, grid_resolution)

        # Sample grid points
        for L in L_range:
            for J in J_range:
                for P in P_range:
                    for W in W_range:
                        point = np.array([L, J, P, W])

                        # Find distance to nearest semantic point
                        distances = np.linalg.norm(self.coords - point, axis=1)
                        min_dist = np.min(distances)

                        # If far from all points, this is a void
                        if min_dist > 0.3:  # Threshold for void
                            # Find nearest words for context
                            nearest_indices = np.argsort(distances)[:3]
                            nearest_words = [self.words[i] for i in nearest_indices]

                            voids.append(TopologicalFeature(
                                feature_type='void',
                                birth_scale=min_dist - 0.1,
                                death_scale=min_dist,
                                persistence=0.1,
                                location=point,
                                associated_words=nearest_words
                            ))

        return voids

    def find_boundaries(self, threshold: float = 0.35) -> List[Tuple[str, str, float]]:
        """Find boundary words - words at the edge of clusters"""
        boundaries = []

        for i, word in enumerate(self.words):
            coord = self.coords[i]

            # Find k nearest neighbors
            distances = np.linalg.norm(self.coords - coord, axis=1)
            sorted_indices = np.argsort(distances)[1:11]  # Exclude self, take 10

            # Check if neighbors are diverse (boundary indicator)
            neighbor_coords = self.coords[sorted_indices]
            neighbor_distances = distances[sorted_indices]

            # Variance in neighbor coordinates
            variance = np.mean(np.var(neighbor_coords, axis=0))

            # If high variance and some distant neighbors, it's a boundary
            if variance > threshold and np.max(neighbor_distances[:5]) > 0.25:
                boundaries.append((
                    word,
                    float(variance),
                    float(np.max(neighbor_distances[:5]))
                ))

        return sorted(boundaries, key=lambda x: x[1], reverse=True)

    def find_bridges(self, min_gap: float = 0.4) -> List[TopologicalFeature]:
        """Find bridge words - words connecting distant clusters"""
        bridges = []

        for i, word in enumerate(self.words):
            coord = self.coords[i]

            # Find all distances
            distances = np.linalg.norm(self.coords - coord, axis=1)
            sorted_indices = np.argsort(distances)[1:]  # Exclude self

            # Check if there's a gap in distances (bridge indicator)
            sorted_distances = distances[sorted_indices]

            for j in range(len(sorted_distances) - 1):
                gap = sorted_distances[j+1] - sorted_distances[j]

                if gap > min_gap:
                    # This word bridges two groups
                    near_group = [self.words[idx] for idx in sorted_indices[:j+1] if distances[idx] < 0.3]
                    far_group = [self.words[idx] for idx in sorted_indices[j+1:] if distances[idx] < 0.5]

                    if near_group and far_group:
                        bridges.append(TopologicalFeature(
                            feature_type='bridge',
                            birth_scale=sorted_distances[j],
                            death_scale=sorted_distances[j+1],
                            persistence=gap,
                            location=coord,
                            associated_words=[word] + near_group[:2] + far_group[:2]
                        ))
                        break

        return bridges

    def simplified_persistent_homology(self, max_scale: float = 0.8,
                                      n_steps: int = 20) -> List[TopologicalFeature]:
        """Simplified persistent homology: track connected components"""
        features = []
        scales = np.linspace(0.05, max_scale, n_steps)

        # Track connected components at each scale
        for scale in scales:
            # Build adjacency at this scale
            distances = squareform(pdist(self.coords))
            adjacency = distances < scale

            # Find connected components (simplified)
            visited = set()
            components = []

            for i in range(len(self.words)):
                if i in visited:
                    continue

                # BFS to find component
                component = set()
                queue = [i]

                while queue:
                    node = queue.pop(0)
                    if node in visited:
                        continue
                    visited.add(node)
                    component.add(node)

                    # Add neighbors
                    neighbors = np.where(adjacency[node])[0]
                    for neighbor in neighbors:
                        if neighbor not in visited:
                            queue.append(neighbor)

                if len(component) > 1:
                    components.append(component)

            # Record number of components at this scale
            if len(components) > 0:
                for comp in components:
                    comp_words = [self.words[i] for i in comp]
                    comp_coords = self.coords[list(comp)]
                    center = np.mean(comp_coords, axis=0)

                    features.append(TopologicalFeature(
                        feature_type='cluster',
                        birth_scale=scale,
                        death_scale=scale + (max_scale - scale) / n_steps,
                        persistence=(max_scale - scale) / n_steps,
                        location=center,
                        associated_words=comp_words[:5]
                    ))

        return features

    def map_territory(self, wedau_words: Dict[str, np.ndarray] = None) -> Dict:
        """Complete topological mapping of semantic space"""
        print("=" * 80)
        print("TOPOLOGICAL SEMANTIC MAPPING")
        print("Building comprehensive map of meaning space")
        print("=" * 80)

        results = {
            'clustering': {},
            'territories': {},
            'topological_features': {},
            'wedau_predictions': {}
        }

        # 1. Multiple clustering approaches
        print("\n1. CLUSTERING ANALYSIS")
        print("-" * 80)

        # Hierarchical
        print("Running hierarchical clustering...")
        hierarchical = self.hierarchical_clustering(n_clusters=8)
        results['clustering']['hierarchical'] = hierarchical
        print(f"  ✓ Identified {hierarchical['n_clusters']} hierarchical clusters")

        # Density-based
        print("Running density-based clustering (DBSCAN)...")
        density = self.density_clustering(eps=0.25, min_samples=3)
        results['clustering']['density'] = density
        print(f"  ✓ Found {density['n_clusters']} dense clusters, {density['n_noise']} noise points")

        # K-means
        print("Running K-means clustering...")
        kmeans = self.kmeans_clustering(n_clusters=8)
        results['clustering']['kmeans'] = kmeans
        print(f"  ✓ Created {kmeans['n_clusters']} balanced territories")

        # 2. Characterize territories (use K-means as primary)
        print("\n2. TERRITORY CHARACTERIZATION")
        print("-" * 80)

        territories = {}
        for cluster_id, members in kmeans['cluster_members'].items():
            cluster_id = int(cluster_id)  # Ensure integer keys
            territory = self.characterize_territory(
                cluster_id,
                members,
                kmeans['centroids'][cluster_id]
            )
            territories[cluster_id] = territory

            print(f"\n{territory.name} (Territory {cluster_id})")
            print(f"  Center: L={territory.center[0]:.3f} J={territory.center[1]:.3f} " +
                  f"P={territory.center[2]:.3f} W={territory.center[3]:.3f}")
            print(f"  Members: {len(territory.members)} words")
            print(f"  Languages: {territory.languages}")
            print(f"  Harmony: {territory.harmony_mean:.3f}")
            print(f"  Stability: {territory.stability:.2f}")
            print(f"  Sample words: {', '.join(territory.members[:5])}")

        results['territories'] = {
            k: {
                'id': v.id,
                'name': v.name,
                'center': v.center.tolist(),
                'radius': v.radius,
                'members': v.members,
                'languages': v.languages,
                'L_range': v.L_range,
                'J_range': v.J_range,
                'P_range': v.P_range,
                'W_range': v.W_range,
                'harmony_mean': v.harmony_mean,
                'density': v.density,
                'stability': v.stability
            }
            for k, v in territories.items()
        }

        # 3. Topological features
        print("\n3. TOPOLOGICAL FEATURES")
        print("-" * 80)

        # Find voids
        print("Searching for voids (holes in semantic space)...")
        voids = self.find_voids(grid_resolution=4)
        print(f"  ✓ Found {len(voids)} potential voids")

        # Find boundaries
        print("Identifying boundary words...")
        boundaries = self.find_boundaries(threshold=0.3)
        print(f"  ✓ Found {len(boundaries)} boundary words")

        # Find bridges
        print("Locating bridge words...")
        bridges = self.find_bridges(min_gap=0.35)
        print(f"  ✓ Found {len(bridges)} bridge words")

        results['topological_features'] = {
            'voids': [{
                'type': v.feature_type,
                'location': v.location.tolist(),
                'min_distance': v.death_scale,
                'nearest_words': v.associated_words
            } for v in voids[:10]],  # Limit to top 10
            'boundaries': [{
                'word': b[0],
                'variance': b[1],
                'max_neighbor_distance': b[2]
            } for b in boundaries[:15]],
            'bridges': [{
                'type': b.feature_type,
                'word': b.associated_words[0] if b.associated_words else None,
                'connects': b.associated_words,
                'gap': b.persistence
            } for b in bridges]
        }

        # 4. Wedau word prediction
        if wedau_words:
            print("\n4. WEDAU WORD TRANSLATION")
            print("-" * 80)

            for wedau_word, wedau_coord in wedau_words.items():
                # Find nearest territory
                min_distance = float('inf')
                nearest_territory_id = None
                nearest_territory = None

                for tid, t in territories.items():
                    distance = float(np.linalg.norm(wedau_coord - t.center))
                    if distance < min_distance:
                        min_distance = distance
                        nearest_territory_id = int(tid)
                        nearest_territory = t

                territory_distance = min_distance

                # Find nearest words overall
                all_distances = {
                    word: float(np.linalg.norm(wedau_coord - self.points[word]['coords']))
                    for word in self.words
                }
                sorted_words = sorted(all_distances.items(), key=lambda x: x[1])

                # Find nearest words in same territory
                territory_words = nearest_territory.members
                territory_distances = {
                    word: all_distances[word]
                    for word in territory_words
                }
                sorted_territory_words = sorted(territory_distances.items(), key=lambda x: x[1])

                print(f"\n{wedau_word.upper()}")
                print(f"  Coordinates: L={wedau_coord[0]:.3f} J={wedau_coord[1]:.3f} " +
                      f"P={wedau_coord[2]:.3f} W={wedau_coord[3]:.3f}")
                print(f"  Territory: {nearest_territory.name}")
                print(f"  Nearest words (global):")
                for word, dist in sorted_words[:5]:
                    lang = self.languages[word]
                    print(f"    {word} ({lang}): {dist:.4f}")
                print(f"  Nearest in territory:")
                for word, dist in sorted_territory_words[:5]:
                    lang = self.languages[word]
                    print(f"    {word} ({lang}): {dist:.4f}")

                results['wedau_predictions'][wedau_word] = {
                    'coordinates': wedau_coord.tolist(),
                    'territory_id': nearest_territory_id,
                    'territory_name': nearest_territory.name,
                    'territory_distance': territory_distance,
                    'nearest_global': [(w, d) for w, d in sorted_words[:10]],
                    'nearest_in_territory': [(w, d) for w, d in sorted_territory_words[:10]]
                }

        return results


def load_bilingual_corpus() -> Dict[str, Dict]:
    """Load English and Mandarin semantic coordinates"""

    semantic_points = {
        # ENGLISH - Core emotions
        'love': {'coords': np.array([0.92, 0.45, 0.15, 0.70]), 'language': 'English'},
        'hate': {'coords': np.array([0.12, 0.35, 0.75, 0.25]), 'language': 'English'},
        'joy': {'coords': np.array([0.88, 0.42, 0.38, 0.65]), 'language': 'English'},
        'sadness': {'coords': np.array([0.35, 0.48, 0.22, 0.55]), 'language': 'English'},
        'fear': {'coords': np.array([0.25, 0.52, 0.28, 0.45]), 'language': 'English'},
        'anger': {'coords': np.array([0.28, 0.55, 0.72, 0.35]), 'language': 'English'},
        'peace': {'coords': np.array([0.75, 0.65, 0.25, 0.72]), 'language': 'English'},
        'hope': {'coords': np.array([0.78, 0.48, 0.35, 0.68]), 'language': 'English'},

        # ENGLISH - Virtues
        'compassion': {'coords': np.array([0.88, 0.72, 0.32, 0.75]), 'language': 'English'},
        'courage': {'coords': np.array([0.65, 0.62, 0.68, 0.70]), 'language': 'English'},
        'wisdom': {'coords': np.array([0.70, 0.68, 0.42, 0.88]), 'language': 'English'},
        'justice': {'coords': np.array([0.60, 0.88, 0.58, 0.78]), 'language': 'English'},
        'mercy': {'coords': np.array([0.85, 0.72, 0.35, 0.70]), 'language': 'English'},
        'truth': {'coords': np.array([0.62, 0.78, 0.48, 0.85]), 'language': 'English'},
        'honesty': {'coords': np.array([0.68, 0.82, 0.45, 0.80]), 'language': 'English'},
        'humility': {'coords': np.array([0.72, 0.70, 0.28, 0.75]), 'language': 'English'},

        # ENGLISH - Vices
        'pride': {'coords': np.array([0.38, 0.35, 0.78, 0.42]), 'language': 'English'},
        'greed': {'coords': np.array([0.22, 0.28, 0.82, 0.35]), 'language': 'English'},
        'envy': {'coords': np.array([0.28, 0.38, 0.68, 0.32]), 'language': 'English'},
        'cruelty': {'coords': np.array([0.15, 0.25, 0.78, 0.22]), 'language': 'English'},

        # ENGLISH - Abstract concepts
        'freedom': {'coords': np.array([0.75, 0.72, 0.65, 0.78]), 'language': 'English'},
        'beauty': {'coords': np.array([0.82, 0.55, 0.42, 0.68]), 'language': 'English'},
        'faith': {'coords': np.array([0.80, 0.58, 0.38, 0.72]), 'language': 'English'},
        'knowledge': {'coords': np.array([0.55, 0.58, 0.52, 0.85]), 'language': 'English'},
        'power': {'coords': np.array([0.45, 0.48, 0.88, 0.62]), 'language': 'English'},
        'weakness': {'coords': np.array([0.42, 0.45, 0.22, 0.48]), 'language': 'English'},

        # ENGLISH - Concrete/elemental
        'light': {'coords': np.array([0.85, 0.62, 0.55, 0.82]), 'language': 'English'},
        'darkness': {'coords': np.array([0.28, 0.35, 0.42, 0.38]), 'language': 'English'},
        'fire': {'coords': np.array([0.55, 0.48, 0.78, 0.58]), 'language': 'English'},
        'water': {'coords': np.array([0.68, 0.60, 0.45, 0.65]), 'language': 'English'},

        # ENGLISH - Relational
        'friendship': {'coords': np.array([0.82, 0.68, 0.42, 0.72]), 'language': 'English'},
        'betrayal': {'coords': np.array([0.18, 0.42, 0.65, 0.28]), 'language': 'English'},
        'loyalty': {'coords': np.array([0.78, 0.75, 0.58, 0.75]), 'language': 'English'},
        'forgiveness': {'coords': np.array([0.88, 0.78, 0.35, 0.78]), 'language': 'English'},

        # ENGLISH - Actions
        'give': {'coords': np.array([0.82, 0.68, 0.42, 0.68]), 'language': 'English'},
        'take': {'coords': np.array([0.32, 0.38, 0.72, 0.42]), 'language': 'English'},
        'create': {'coords': np.array([0.75, 0.58, 0.68, 0.82]), 'language': 'English'},
        'destroy': {'coords': np.array([0.22, 0.35, 0.78, 0.32]), 'language': 'English'},
        'heal': {'coords': np.array([0.85, 0.72, 0.48, 0.75]), 'language': 'English'},
        'harm': {'coords': np.array([0.18, 0.32, 0.75, 0.28]), 'language': 'English'},

        # MANDARIN (爱 = love, 恨 = hate, etc.) - Core emotions
        '爱': {'coords': np.array([0.90, 0.46, 0.17, 0.71]), 'language': 'Mandarin'},  # ài - love
        '恨': {'coords': np.array([0.14, 0.36, 0.73, 0.27]), 'language': 'Mandarin'},  # hèn - hate
        '喜': {'coords': np.array([0.86, 0.44, 0.40, 0.67]), 'language': 'Mandarin'},  # xǐ - joy
        '悲': {'coords': np.array([0.37, 0.46, 0.24, 0.53]), 'language': 'Mandarin'},  # bēi - sadness
        '恐': {'coords': np.array([0.27, 0.50, 0.30, 0.47]), 'language': 'Mandarin'},  # kǒng - fear
        '怒': {'coords': np.array([0.30, 0.53, 0.70, 0.37]), 'language': 'Mandarin'},  # nù - anger
        '和': {'coords': np.array([0.73, 0.67, 0.27, 0.74]), 'language': 'Mandarin'},  # hé - peace
        '望': {'coords': np.array([0.76, 0.50, 0.37, 0.70]), 'language': 'Mandarin'},  # wàng - hope

        # MANDARIN - Virtues
        '仁': {'coords': np.array([0.90, 0.70, 0.30, 0.77]), 'language': 'Mandarin'},  # rén - benevolence/compassion
        '勇': {'coords': np.array([0.67, 0.60, 0.70, 0.72]), 'language': 'Mandarin'},  # yǒng - courage
        '智': {'coords': np.array([0.68, 0.70, 0.44, 0.90]), 'language': 'Mandarin'},  # zhì - wisdom
        '义': {'coords': np.array([0.62, 0.86, 0.56, 0.80]), 'language': 'Mandarin'},  # yì - righteousness/justice
        '慈': {'coords': np.array([0.87, 0.74, 0.33, 0.72]), 'language': 'Mandarin'},  # cí - mercy
        '真': {'coords': np.array([0.64, 0.76, 0.50, 0.87]), 'language': 'Mandarin'},  # zhēn - truth
        '诚': {'coords': np.array([0.70, 0.80, 0.47, 0.82]), 'language': 'Mandarin'},  # chéng - honesty/sincerity
        '谦': {'coords': np.array([0.74, 0.68, 0.30, 0.77]), 'language': 'Mandarin'},  # qiān - humility

        # MANDARIN - Vices
        '傲': {'coords': np.array([0.36, 0.37, 0.76, 0.44]), 'language': 'Mandarin'},  # ào - pride/arrogance
        '贪': {'coords': np.array([0.24, 0.30, 0.80, 0.37]), 'language': 'Mandarin'},  # tān - greed
        '妒': {'coords': np.array([0.30, 0.36, 0.70, 0.34]), 'language': 'Mandarin'},  # dù - envy
        '恶': {'coords': np.array([0.17, 0.27, 0.76, 0.24]), 'language': 'Mandarin'},  # è - evil/cruelty

        # MANDARIN - Abstract concepts
        '自由': {'coords': np.array([0.77, 0.74, 0.63, 0.80]), 'language': 'Mandarin'},  # zìyóu - freedom
        '美': {'coords': np.array([0.84, 0.53, 0.44, 0.70]), 'language': 'Mandarin'},  # měi - beauty
        '信': {'coords': np.array([0.82, 0.56, 0.36, 0.74]), 'language': 'Mandarin'},  # xìn - faith/trust
        '知': {'coords': np.array([0.57, 0.56, 0.54, 0.87]), 'language': 'Mandarin'},  # zhī - knowledge
        '力': {'coords': np.array([0.47, 0.46, 0.86, 0.64]), 'language': 'Mandarin'},  # lì - power/strength
        '弱': {'coords': np.array([0.44, 0.43, 0.24, 0.50]), 'language': 'Mandarin'},  # ruò - weakness

        # MANDARIN - Concrete/elemental
        '光': {'coords': np.array([0.87, 0.64, 0.53, 0.84]), 'language': 'Mandarin'},  # guāng - light
        '暗': {'coords': np.array([0.30, 0.33, 0.44, 0.40]), 'language': 'Mandarin'},  # àn - darkness
        '火': {'coords': np.array([0.57, 0.46, 0.80, 0.60]), 'language': 'Mandarin'},  # huǒ - fire
        '水': {'coords': np.array([0.70, 0.58, 0.47, 0.67]), 'language': 'Mandarin'},  # shuǐ - water

        # MANDARIN - Relational
        '友': {'coords': np.array([0.84, 0.66, 0.44, 0.74]), 'language': 'Mandarin'},  # yǒu - friendship
        '叛': {'coords': np.array([0.20, 0.40, 0.67, 0.30]), 'language': 'Mandarin'},  # pàn - betrayal
        '忠': {'coords': np.array([0.80, 0.73, 0.56, 0.77]), 'language': 'Mandarin'},  # zhōng - loyalty
        '恕': {'coords': np.array([0.90, 0.76, 0.37, 0.80]), 'language': 'Mandarin'},  # shù - forgiveness

        # MANDARIN - Actions
        '施': {'coords': np.array([0.84, 0.66, 0.44, 0.70]), 'language': 'Mandarin'},  # shī - give/bestow
        '夺': {'coords': np.array([0.34, 0.36, 0.74, 0.44]), 'language': 'Mandarin'},  # duó - take/seize
        '造': {'coords': np.array([0.77, 0.56, 0.70, 0.84]), 'language': 'Mandarin'},  # zào - create
        '毁': {'coords': np.array([0.24, 0.33, 0.80, 0.34]), 'language': 'Mandarin'},  # huǐ - destroy
        '疗': {'coords': np.array([0.87, 0.70, 0.50, 0.77]), 'language': 'Mandarin'},  # liáo - heal
        '伤': {'coords': np.array([0.20, 0.34, 0.73, 0.30]), 'language': 'Mandarin'},  # shāng - harm/wound
    }

    return semantic_points


def load_wedau_test_words() -> Dict[str, np.ndarray]:
    """Load Wedau words with estimated coordinates from previous experiments"""

    # From wedau_rigorous_geometric_translation.json
    wedau_words = {
        'bada': np.array([0.88, 0.72, 0.35, 0.75]),  # Predicted: compassion/mercy
        'gabu': np.array([0.65, 0.62, 0.68, 0.70]),  # Predicted: courage/strength
        'nuahai': np.array([0.85, 0.45, 0.18, 0.72]),  # Predicted: love/affection
        'wesawe': np.array([0.32, 0.38, 0.72, 0.42]),  # Predicted: take/seize
        'matana': np.array([0.82, 0.68, 0.42, 0.68]),  # Predicted: give/gift
        'yawa': np.array([0.75, 0.65, 0.25, 0.72]),  # Predicted: peace/calm
    }

    return wedau_words


def run_topological_mapping():
    """Run complete topological semantic mapping"""

    # Load bilingual corpus
    semantic_points = load_bilingual_corpus()

    print(f"\nLoaded {len(semantic_points)} words:")
    english_words = [w for w in semantic_points if semantic_points[w]['language'] == 'English']
    mandarin_words = [w for w in semantic_points if semantic_points[w]['language'] == 'Mandarin']
    print(f"  English: {len(english_words)} words")
    print(f"  Mandarin: {len(mandarin_words)} words")

    # Create mapper
    mapper = TopologicalSemanticMapper(semantic_points)

    # Load Wedau test words
    wedau_words = load_wedau_test_words()

    # Run complete mapping
    results = mapper.map_territory(wedau_words=wedau_words)

    # Save results
    output_file = 'experiments/topological_semantic_map.json'

    # Convert numpy arrays to lists for JSON serialization
    def convert_to_serializable(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, dict):
            return {str(k) if isinstance(k, (np.integer, np.floating)) else k:
                    convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_serializable(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(convert_to_serializable(item) for item in obj)
        else:
            return obj

    serializable_results = convert_to_serializable(results)

    with open(output_file, 'w') as f:
        json.dump(serializable_results, f, indent=2)

    print("\n" + "=" * 80)
    print(f"Topological mapping complete. Results saved to {output_file}")
    print("=" * 80)

    return results


if __name__ == "__main__":
    run_topological_mapping()
