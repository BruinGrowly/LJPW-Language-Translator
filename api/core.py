"""
LJPW API Core Logic
Handles data loading and semantic operations.
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class LJPWEngine:
    _instance = None
    
    def __init__(self):
        self.concepts: Dict[str, dict] = {}
        self.vectors: Optional[np.ndarray] = None
        self.ids: List[str] = []
        self.load_data()
            
    def load_data(self):
        # Locate data file relative to this script
        # Assumes /api/core.py -> /experiments/semantic_space...
        root_dir = Path(__file__).parent.parent
        data_path = root_dir / "experiments" / "semantic_space_10000_MILESTONE.json"
        
        print(f"Loading semantic space from {data_path}...")
        if not data_path.exists():
            raise FileNotFoundError(f"Could not find data at {data_path}")
            
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Flatten concepts
        concept_list = []
        vectors_list = []
        ids_list = []
        
        for domain_key, domain in data['domains'].items():
            domain_name = domain.get('name', domain_key)
            for name, c_data in domain.get('concepts', {}).items():
                c_data['id'] = name
                c_data['domain'] = domain_name # Ensure domain name is clean
                
                # Normalize key to lowercase
                lower_name = name.lower()
                self.concepts[lower_name] = c_data
                ids_list.append(lower_name)
                vectors_list.append(c_data['coordinates'])
                
        # MANUAL PATCH: Restore Love if missing
        if "love" not in self.concepts:
            print("Patching 'Love' into semantic space...")
            love_data = {
                "name": "Love",
                "definition": "The fundamental force of unity and affection.",
                "coordinates": [1.0, 0.0, 0.0, 0.0],
                "domain": "Universal Constants",
                "id": "love"
            }
            self.concepts["love"] = love_data
            ids_list.append("love")
            vectors_list.append([1.0, 0.0, 0.0, 0.0])

        self.ids = ids_list
        self.vectors = np.array(vectors_list)
        print(f"Loaded {len(self.concepts)} concepts.")

    def get_concept(self, name: str) -> Optional[dict]:
        return self.concepts.get(name.lower())

    def get_vector(self, name: str) -> Optional[np.ndarray]:
        c = self.concepts.get(name.lower())
        if c:
            return np.array(c['coordinates'])
        return None

    def search_nearest(self, vector: List[float], n: int = 10) -> List[dict]:
        """Find N nearest concepts to the given 4D vector."""
        if self.vectors is None:
            return []
            
        target = np.array(vector)
        dists = np.linalg.norm(self.vectors - target, axis=1)
        sorted_indices = np.argsort(dists)[:n]
        
        results = []
        for idx in sorted_indices:
            concept_id = self.ids[idx]
            concept = self.concepts[concept_id].copy()
            concept['distance'] = float(dists[idx])
            results.append(concept)
            
        return results

    def analyze_text(self, text: str) -> dict:
        """Analyze text by averaging vectors of recognized words."""
        words = text.lower().replace('.', '').replace(',', '').split()
        vectors = []
        found_words = []
        
        for w in words:
            # Direct match
            v = self.get_vector(w)
            if v is not None:
                vectors.append(v)
                found_words.append(w)
        
        if not vectors:
            return {"coordinates": [0.0, 0.0, 0.0, 0.0], "dominant": "None"}
            
        # Average
        avg_vec = np.mean(vectors, axis=0)
        
        # Find dominant dimension
        dims = ["Love", "Justice", "Power", "Wisdom"]
        dominant_idx = np.argmax(avg_vec)
        
        return {
            "coordinates": avg_vec.tolist(),
            "dominant": dims[dominant_idx],
            "words_found": found_words
        }

# Singleton accessor
_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = LJPWEngine()
    return _engine
