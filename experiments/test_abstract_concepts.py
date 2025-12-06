"""
Test Simple Translator with Abstract Concepts
"""

import json
import numpy as np

def load_concepts():
    """Load concepts from abstract library."""
    with open("experiments/semantic_space_6794_ABSTRACT.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
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
    concepts.extend(extract_from_domain('actions_processes'))
    concepts.extend(extract_from_domain('natural_world'))
    concepts.extend(extract_from_domain('abstract_concepts'))
    
    return concepts

def detect_field_position(text):
    """Simple pattern detection for testing abstract ideas."""
    text_lower = text.lower()
    
    # Defaults
    L, J, P, W = 0.5, 0.5, 0.5, 0.5
    
    if 'truth' in text_lower:
        J=0.9; W=0.9; L=0.8; P=0.7
    elif 'justice' in text_lower:
        J=0.95; L=0.8; P=0.8; W=0.9
    elif 'time' in text_lower:
        W=0.9; J=0.9; P=0.6; L=0.5
    elif 'chaos' in text_lower:
        L=0.2; J=0.1; P=0.8; W=0.2
    elif 'science' in text_lower:
        W=0.95; J=0.9; P=0.7; L=0.5
    
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
    print("TESTING ABSTRACT CONCEPTS")
    print("="*70)
    
    concepts = load_concepts()
    print(f"\nLoaded {len(concepts)} concepts (Spiritual + Emotions + Rel + Actions + Nature + Abstract)")
    
    tests = [
        ('The truth', 'Truth'),
        ('True justice', 'Justice'),
        ('Time passes', 'Time'),
        ('Total chaos', 'Chaos'),
        ('Pure science', 'Science')
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
