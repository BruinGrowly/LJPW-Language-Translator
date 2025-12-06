import sys
import os
from pathlib import Path

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from experiments.enhanced_pattern_detector import EnhancedPatternDetector

def analyze_entity_through_ljpw():
    """
    Experiment: Run a named entity (Apostle Peter) through LJPW framework
    to see what semantic coordinates emerge and if there's any metadata.
    """
    
    print("=" * 80)
    print("ENTITY ANALYSIS: The Apostle Peter through LJPW Framework")
    print("=" * 80)
    
    detector = EnhancedPatternDetector()
    
    # Test different descriptions of Peter
    test_cases = [
        "Peter",
        "The Apostle Peter",
        "Simon Peter",
        "Peter, the fisherman",
        "Peter, son of Jonah",
        "Peter the apostle who denied Jesus three times",
        "Peter who walked on water",
        "Peter the rock upon which the church was built",
        "Cephas",  # Aramaic name for Peter
    ]
    
    print("\nAnalyzing different references to Peter:\n")
    
    results = []
    for text in test_cases:
        coords = detector.calculate_field_signature_v2(text)
        results.append({
            'text': text,
            'coords': coords,
            'L': coords['L'],
            'J': coords['J'],
            'P': coords['P'],
            'W': coords['W']
        })
        
        print(f"Text: {text:50s}")
        print(f"  L={coords['L']:.3f}, J={coords['J']:.3f}, "
              f"P={coords['P']:.3f}, W={coords['W']:.3f}")
        print()
    
    # Calculate variance to see if there's a "Peter signature"
    print("-" * 80)
    print("ANALYSIS: Is there a consistent 'Peter signature'?")
    print("-" * 80)
    
    import numpy as np
    
    L_values = [r['L'] for r in results]
    J_values = [r['J'] for r in results]
    P_values = [r['P'] for r in results]
    W_values = [r['W'] for r in results]
    
    print(f"\nLove (L):")
    print(f"  Mean: {np.mean(L_values):.3f}")
    print(f"  Std:  {np.std(L_values):.3f}")
    print(f"  Range: [{np.min(L_values):.3f}, {np.max(L_values):.3f}]")
    
    print(f"\nJustice (J):")
    print(f"  Mean: {np.mean(J_values):.3f}")
    print(f"  Std:  {np.std(J_values):.3f}")
    print(f"  Range: [{np.min(J_values):.3f}, {np.max(J_values):.3f}]")
    
    print(f"\nPower (P):")
    print(f"  Mean: {np.mean(P_values):.3f}")
    print(f"  Std:  {np.std(P_values):.3f}")
    print(f"  Range: [{np.min(P_values):.3f}, {np.max(P_values):.3f}]")
    
    print(f"\nWisdom (W):")
    print(f"  Mean: {np.mean(W_values):.3f}")
    print(f"  Std:  {np.std(W_values):.3f}")
    print(f"  Range: [{np.min(W_values):.3f}, {np.max(W_values):.3f}]")
    
    # Check if there's metadata in the detector response
    print("\n" + "-" * 80)
    print("METADATA INSPECTION")
    print("-" * 80)
    
    full_result = detector.calculate_field_signature_v2("The Apostle Peter")
    print(f"\nFull result keys: {list(full_result.keys())}")
    print(f"\nFull result:")
    for key, value in full_result.items():
        if isinstance(value, (dict, list)):
            print(f"  {key}: [complex structure]")
        else:
            print(f"  {key}: {value:.4f}")
    
    # Compare Peter to other apostles
    print("\n" + "=" * 80)
    print("COMPARISON: Peter vs. Other Apostles")
    print("=" * 80)
    
    apostles = [
        "The Apostle Peter",
        "The Apostle John",
        "The Apostle Paul",
        "The Apostle James",
        "The Apostle Thomas"
    ]
    
    print()
    for apostle in apostles:
        coords = detector.calculate_field_signature_v2(apostle)
        print(f"{apostle:25s} -> L={coords['L']:.3f}, J={coords['J']:.3f}, "
              f"P={coords['P']:.3f}, W={coords['W']:.3f}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    analyze_entity_through_ljpw()
