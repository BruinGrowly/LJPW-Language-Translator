"""
Test Simple Translator with Relationship Concepts
"""

import json
import numpy as np

def load_concepts():
    """Load concepts from relationships library."""
    with open("experiments/semantic_space_6594_RELATIONSHIPS.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # helper to extract concepts from a domain
    def extract_from_domain(domain_key):
        if domain_key in data['domains']:
             return [
                 {
                    'name': c['name'], 
                    'coords': np.array(c['coordinates'])
                 } 
                 for c in data['domains'][domain_key]['concepts'].values()
             ]
        return []

    concepts = []
    concepts.extend(extract_from_domain('spiritual_moral_enrichment'))
    concepts.extend(extract_from_domain('emotional_states'))
    concepts.extend(extract_from_domain('relationships'))
    
    return concepts

def detect_field_position(text):
    """Simple pattern detection for testing relationships."""
    text_lower = text.lower()
    
    # Defaults
    L, J, P, W = 0.5, 0.5, 0.5, 0.5
    
    if 'father' in text_lower:
        L=0.9; P=0.85; J=0.85; W=0.8
    elif 'friend' in text_lower:
        L=0.85; J=0.3; P=0.5
    elif 'king' in text_lower:
        J=0.9; P=0.95; W=0.8; L=0.5
    elif 'teacher' in text_lower:
        W=0.9; P=0.7; L=0.7; J=0.7
    elif 'enemy' in text_lower:
        L=0.1; P=0.7; J=0.2; W=0.4
    
    return np.array([np.clip(L, 0, 1), np.clip(J, 0, 1), 
                     np.clip(P, 0, 1), np.clip(W, 0, 1)])

def find_nearest(field_position, concepts, top_n=5):
    """Find nearest concepts."""
    distances = []
    for concept in concepts:
        distance = np.linalg.norm(field_position - concept['coords'])
        distances.append({'concept': concept, 'distance': distance})
    
    distances.sort(key=lambda x: x['distance'])
    return distances[:top_n]

def main():
    print("="*70)
    print("TESTING RELATIONSHIP CONCEPTS")
    print("="*70)
    
    concepts = load_concepts()
    print(f"\nLoaded {len(concepts)} concepts (Spiritual + Emotional + Relations)")
    
    tests = [
        ('My father', 'Father'),
        ('My friend', 'Friend'),
        ('The king', 'King'),
        ('My teacher', 'Teacher'),
        ('My enemy', 'Enemy')
    ]
    
    matches = 0
    print(f"\n{'='*70}")
    print("RESULTS")
    print(f"{'='*70}\n")
    
    for source, expected in tests:
        position = detect_field_position(source)
        nearest = find_nearest(position, concepts, top_n=5)
        
        top_name = nearest[0]['concept']['name']
        print(f"'{source}' -> {top_name}")
        
        # Check if expected is in top 3
        top_3 = [n['concept']['name'] for n in nearest[:3]]
        print(f"  Top 3: {', '.join(top_3)}")
        
        if expected in top_3:
            matches += 1
            print("  Result: [PASS]\n")
        else:
            print(f"  Result: [FAIL] (Expected {expected})\n")
            
    print(f"Success Rate: {matches}/{len(tests)}")

if __name__ == "__main__":
    main()
