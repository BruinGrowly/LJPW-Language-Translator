"""
Test Simple Translator with Emotional Concepts
"""

import json
import numpy as np

def load_concepts():
    """Load concepts including emotional domain."""
    with open("experiments/semantic_space_6534_EMOTIONAL.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Load spiritual + emotional
    spiritual = data['domains']['spiritual_moral_enrichment']['concepts']
    emotional = data['domains']['emotional_states']['concepts']
    
    concepts = []
    
    # Helper to clean keys
    for domain in [spiritual, emotional]:
        for key, concept in domain.items():
            concepts.append({
                'name': concept['name'],
                'coords': np.array(concept['coordinates']),
                'definition': concept.get('definition', '')
            })
    
    return concepts

def detect_field_position(text):
    """Simple pattern detection for testing emotions."""
    text_lower = text.lower()
    
    # Defaults
    L, J, P, W = 0.5, 0.5, 0.5, 0.5
    
    # Mock detector logic for emotions (simplified for this test)
    if 'happy' in text_lower or 'good' in text_lower:
        L += 0.35; P += 0.2
    elif 'sad' in text_lower or 'heavy' in text_lower:
        L -= 0.2; P -= 0.3; J -= 0.1
    elif 'lost' in text_lower or 'confused' in text_lower:
        W -= 0.4; J -= 0.3
    elif 'angry' in text_lower or 'mad' in text_lower:
        P += 0.4; L -= 0.3
    elif 'fear' in text_lower or 'scared' in text_lower:
        P += 0.3; L -= 0.3; J -= 0.3
    
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
    print("TESTING EMOTIONAL CONCEPTS")
    print("="*70)
    
    concepts = load_concepts()
    print(f"\nLoaded {len(concepts)} concepts (Spiritual + Emotional)")
    
    tests = [
        ('I am happy', 'Joy'),
        ('I feel lost', 'Confusion'),
        ('My heart is heavy', 'Sadness'),
        ('I am so mad', 'Anger'),
        ('I am scared', 'Fear')
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
