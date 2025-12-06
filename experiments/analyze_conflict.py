"""
Analyze Conflict: Kingdom vs Science
Compares specific coordinates to determine separation strategy.
"""
import numpy as np
import sys
import os

sys.path.append(os.getcwd())
try:
    from experiments.universal_translator_core import UniversalTranslator
except ImportError:
    # Fallback if run from experiments dir
    sys.path.append(os.path.dirname(os.getcwd()))
    from experiments.universal_translator_core import UniversalTranslator

def analyze():
    ut = UniversalTranslator()
    
    # 1. Get current detection for "Kingdom of God"
    text = "God ana vibadana vouna" 
    context = "Kingdom of God"
    
    print(f"\nAnalyzing Input: '{text}' ({context})")
    sig = ut.detector.calculate_field_signature(text, context)
    target_coords = sig['coordinates']
    
    print(f"Detected Signature: L={sig['L']:.3f} J={sig['J']:.3f} P={sig['P']:.3f} W={sig['W']:.3f}")
    
    # 2. Get concept coordinates
    concepts_of_interest = [
        'Kingdom', 
        'Genetic Engineering',
        'Natural Selection',
        'Trial',
        'Determinism'
    ]
    
    print("\nConcept Coordinates & Distances:")
    print(f"{'Concept':<25} | {'L':<5} {'J':<5} {'P':<5} {'W':<5} | {'Dist':<6} | {'Diff L'}")
    print("-" * 75)
    
    found_concepts = []
    
    for c in ut.concepts:
        if c['name'] in concepts_of_interest:
            coords = c['coordinates']
            dist = np.linalg.norm(coords - target_coords)
            diff_l = coords[0] - target_coords[0]
            found_concepts.append(c)
            
            print(f"{c['name']:<25} | {coords[0]:.2f} {coords[1]:.2f} {coords[2]:.2f} {coords[3]:.2f} | {dist:.4f} | {diff_l:+.2f}")

    # 3. Suggest Strategy
    print("\nAnalysis:")
    kingdom = next((c for c in found_concepts if c['name'] == 'Kingdom'), None)
    genetic = next((c for c in found_concepts if c['name'] == 'Genetic Engineering'), None)
    
    if kingdom and genetic:
        l_diff = kingdom['coordinates'][0] - genetic['coordinates'][0]
        print(f"Kingdom L - Genetic L = {l_diff:.2f}")
        
        if sig['L'] < kingdom['coordinates'][0]:
            print("Recommendation: Boost L in Detector for Divine+Power contexts to match Kingdom's L.")
        elif sig['L'] > genetic['coordinates'][0]:
             print("Observation: Detected L is already higher than Genetic Engineering.")
             
if __name__ == "__main__":
    analyze()
