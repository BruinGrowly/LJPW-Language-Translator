"""
Debug Kingdom Match
Inspects the coordinates of 'Kingdom' and the unexpected match 'Food Cooking Concept 42'.
"""
import json
import numpy as np
import sys
import os

sys.path.append(os.getcwd())
from experiments.universal_translator_core import UniversalTranslator

def analyze_mismatch():
    ut = UniversalTranslator()
    
    concepts_to_find = ['Kingdom', 'Surgeon', 'Elevator', 'Genetic Engineering']
    found_concepts = {name: None for name in concepts_to_find}
    
    print("\nSearching for concepts...")
    for c in ut.concepts:
        # Check exact names or partial matches
        for name in concepts_to_find:
            if name.lower() in c['name'].lower():
                print(f"Found: {c['name']}")
                found_concepts[name] = c
                
    # Print comparison
    print("\nCoordinate Comparison:")
    header = f"{'Name':<30} | {'L':<5} {'J':<5} {'P':<5} {'W':<5} | {'Dist from Sig':<10}"
    print(header)
    print("-" * len(header))
    
    # Signature from the failing test: L=0.61 J=0.75 P=0.77 W=0.70
    target_sig = np.array([0.61, 0.75, 0.77, 0.70])
    
    for name, concept in found_concepts.items():
        if concept:
            coords = concept['coordinates']
            dist = np.linalg.norm(coords - target_sig)
            print(f"{concept['name']:<30} | {coords[0]:.2f} {coords[1]:.2f} {coords[2]:.2f} {coords[3]:.2f} | {dist:.4f}")
        else:
            print(f"{name:<30} | NOT FOUND")

if __name__ == "__main__":
    analyze_mismatch()
