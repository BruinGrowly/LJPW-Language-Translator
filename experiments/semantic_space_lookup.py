"""
Semantic Space Lookup
Provides fast concept retrieval from the semantic space.
"""

import json
import numpy as np
from typing import Dict, Optional, List, Tuple
from pathlib import Path


class SemanticSpaceLookup:
    """Fast lookup of concepts in the semantic space."""
    
    def __init__(self, semantic_space_path: str):
        """Initialize lookup from semantic space JSON."""
        self.semantic_space_path = semantic_space_path
        self.concepts = {}
        self.index = {}
        self.load_semantic_space()
    
    def load_semantic_space(self):
        """Load all concepts from semantic space."""
        with open(self.semantic_space_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract all concepts from all domains
        for domain_name, domain_data in data.get('domains', {}).items():
            for concept_key, concept_data in domain_data.get('concepts', {}).items():
                name = concept_data.get('name', concept_key)
                coords = concept_data.get('coordinates', [0.5, 0.5, 0.5, 0.5])
                
                # Store concept
                self.concepts[concept_key] = {
                    'name': name,
                    'coordinates': np.array(coords),
                    'domain': domain_name,
                    'definition': concept_data.get('definition', '')
                }
                
                # Build index (lowercase name -> concept_key)
                self.index[name.lower()] = concept_key
                
                # Also index by key
                self.index[concept_key.lower()] = concept_key
    
    def find_concept(self, word: str) -> Optional[Dict]:
        """
        Find concept by name.
        
        Args:
            word: Word to look up (case-insensitive)
            
        Returns:
            Concept dict with 'name', 'coordinates', 'domain', 'definition'
            or None if not found
        """
        word_lower = word.lower().strip()
        
        # Exact match
        if word_lower in self.index:
            concept_key = self.index[word_lower]
            return self.concepts[concept_key]
        
        # Try with underscores (e.g., "holy spirit" -> "holy_spirit")
        word_underscore = word_lower.replace(' ', '_')
        if word_underscore in self.index:
            concept_key = self.index[word_underscore]
            return self.concepts[concept_key]
        
        return None
    
    def find_multiple(self, words: List[str]) -> List[Tuple[str, Optional[Dict]]]:
        """
        Find multiple concepts.
        
        Returns:
            List of (word, concept) tuples
        """
        results = []
        for word in words:
            concept = self.find_concept(word)
            results.append((word, concept))
        return results
    
    def get_all_concepts(self) -> Dict[str, Dict]:
        """Get all concepts."""
        return self.concepts
    
    def search_by_coordinates(
        self,
        target_coords: np.ndarray,
        top_n: int = 5
    ) -> List[Tuple[str, Dict, float]]:
        """
        Find concepts nearest to target coordinates.
        
        Returns:
            List of (name, concept, distance) tuples
        """
        distances = []
        
        for key, concept in self.concepts.items():
            coords = concept['coordinates']
            distance = np.linalg.norm(coords - target_coords)
            distances.append((concept['name'], concept, distance))
        
        # Sort by distance
        distances.sort(key=lambda x: x[2])
        
        return distances[:top_n]


if __name__ == "__main__":
    # Test the lookup
    lookup = SemanticSpaceLookup('experiments/semantic_space_6854_SOCIAL.json')
    
    print("="*70)
    print("SEMANTIC SPACE LOOKUP TEST")
    print("="*70)
    
    # Test 1: Find specific concepts
    print("\n1. Finding Concepts:")
    test_words = ['Kingdom', 'God', 'Love', 'Spirit', 'Holy']
    
    for word in test_words:
        concept = lookup.find_concept(word)
        if concept:
            print(f"\n  '{word}':")
            print(f"    Coordinates: {concept['coordinates']}")
            print(f"    Domain: {concept['domain']}")
        else:
            print(f"\n  '{word}': NOT FOUND")
    
    # Test 2: Search by coordinates
    print("\n\n2. Search by Coordinates:")
    target = np.array([0.9, 0.9, 0.5, 0.9])  # High L, J, W
    print(f"  Target: {target}")
    print(f"  Nearest concepts:")
    
    nearest = lookup.search_by_coordinates(target, top_n=5)
    for name, concept, distance in nearest:
        print(f"    {name}: distance={distance:.3f}")
    
    print("\n" + "="*70)
    print(f"Loaded {len(lookup.concepts)} concepts from semantic space")
    print("="*70)
