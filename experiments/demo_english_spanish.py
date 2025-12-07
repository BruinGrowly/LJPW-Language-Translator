"""
Demo: English-Spanish Cross-Lingual Fidelity Test
Validates that the Universal Translation System assigns the same LJPW coordinates
to the same meaning in different languages (Germanic vs Spanish Romance).
"""

import sys
import os
import numpy as np

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Fix console encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from experiments.enhanced_pattern_detector import EnhancedPatternDetector
from ljpw_quantum.semantic_fidelity import SemanticReconstructionFidelity

def test_cross_lingual_fidelity():
    print("=" * 80)
    print("CROSS-LINGUAL SEMANTIC FIDELITY TEST (ENGLISH <-> SPANISH)")
    print("=" * 80)
    print("Objective: Prove that English 'God' and Spanish 'Dios' share LJPW coordinates.")
    print("Hypothesis: Spanish should benefit from the 'Romance Flow' calibration.")
    print("-" * 80)

    detector = EnhancedPatternDetector()
    fidelity = SemanticReconstructionFidelity()

    # Test Case 1: Mark 1:1
    # Spanish (RVR1960): "Principio del evangelio de Jesucristo, Hijo de Dios."
    eng_text = "The beginning of the Good News of Jesus Christ, the Son of God."
    spa_text = "Principio del evangelio de Jesucristo, Hijo de Dios."

    print(f"\n[Test Case 1] Mark 1:1")
    print(f"  English: {eng_text}")
    print(f"  Spanish: {spa_text}")

    # Encode with Context Awareness
    print("\n  Encoding to Semantic Hilbert Space...")
    eng_sig = detector.calculate_field_signature_v2(eng_text, context="Gospel Introduction")
    spa_sig = detector.calculate_field_signature_v2(spa_text, context="Gospel Introduction")

    eng_coords = np.array([eng_sig['L'], eng_sig['J'], eng_sig['P'], eng_sig['W']])
    spa_coords = np.array([spa_sig['L'], spa_sig['J'], spa_sig['P'], spa_sig['W']])

    print(f"  English LJPW: [{eng_coords[0]:.3f}, {eng_coords[1]:.3f}, {eng_coords[2]:.3f}, {eng_coords[3]:.3f}]")
    print(f"  English Evidence: {eng_sig['evidence']}")
    print(f"  Spanish LJPW: [{spa_coords[0]:.3f}, {spa_coords[1]:.3f}, {spa_coords[2]:.3f}, {spa_coords[3]:.3f}]")
    print(f"  Spanish Evidence: {spa_sig['evidence']}")

    # Evaluate Fidelity
    print("\n  Validating Quantum Semantic Fidelity...")
    eng_harmony = fidelity.calculate_harmony(eng_coords)
    spa_harmony = fidelity.calculate_harmony(spa_coords)
    
    result = fidelity.evaluate_translation_quality(
        eng_coords, spa_coords,
        eng_harmony,
        spa_harmony
    )

    print("\n  RESULTS:")
    print(f"  Quality Level: {result['quality_level']}")
    print(f"  Overall Fidelity: {result['overall_fidelity']:.2%}")
    print(f"  LJPW Distance (epsilon): {result['euclidean_distance']:.4f} (Threshold: < 0.08)")
    print(f"  Harmony Drift (Delta_H): {result['harmony_drift']:.4f} (Threshold: < 0.03)")
    
    # Test Case 2: Mark 1:2
    # Spanish (RVR1960): "Como está escrito en Isaías el profeta: He aquí yo envío mi mensajero delante de tu faz, El cual preparará tu camino delante de ti."
    print("\n" + "-" * 50)
    print("[Test Case 2] Mark 1:2 (Prophecy Context)")
    eng_text_2 = "As it is written in Isaiah the prophet: Behold, I send my messenger ahead of you, who will prepare your way;"
    spa_text_2 = "Como está escrito en Isaías el profeta: He aquí yo envío mi mensajero delante de tu faz, El cual preparará tu camino delante de ti."
    
    print(f"  English: {eng_text_2}")
    print(f"  Spanish: {spa_text_2}")
        
    eng_sig_2 = detector.calculate_field_signature_v2(eng_text_2, context="Prophecy")
    spa_sig_2 = detector.calculate_field_signature_v2(spa_text_2, context="Prophecy")

    eng_coords_2 = np.array([eng_sig_2['L'], eng_sig_2['J'], eng_sig_2['P'], eng_sig_2['W']])
    spa_coords_2 = np.array([spa_sig_2['L'], spa_sig_2['J'], spa_sig_2['P'], spa_sig_2['W']])
    
    print(f"  English LJPW: [{eng_coords_2[0]:.3f}, {eng_coords_2[1]:.3f}, {eng_coords_2[2]:.3f}, {eng_coords_2[3]:.3f}]")
    print(f"  Spanish LJPW: [{spa_coords_2[0]:.3f}, {spa_coords_2[1]:.3f}, {spa_coords_2[2]:.3f}, {spa_coords_2[3]:.3f}]")
    print(f"  English Evidence: {eng_sig_2['evidence']}")
    print(f"  Spanish Evidence: {spa_sig_2['evidence']}")
    
    result_2 = fidelity.evaluate_translation_quality(
        eng_coords_2, spa_coords_2,
        fidelity.calculate_harmony(eng_coords_2),
        fidelity.calculate_harmony(spa_coords_2)
    )
    print(f"  Quality Level: {result_2['quality_level']}")
    print(f"  LJPW Distance: {result_2['euclidean_distance']:.4f}")

    print("\n  Conclusion: ", end="")
    if result['quality_level'] in ['EXCELLENT', 'GOOD']:
        print("✓ SUCCESS: Meaning is preserved across languages.")
    else:
        print("✗ FAILURE: Meaning divergence detected.")

if __name__ == "__main__":
    test_cross_lingual_fidelity()
