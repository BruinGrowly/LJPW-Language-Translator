"""
Demo: English-Chinese Cross-Lingual Fidelity Test
Validates that the Universal Translation System assigns the same LJPW coordinates
to the same meaning in different languages.
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
    print("CROSS-LINGUAL SEMANTIC FIDELITY TEST (ENGLISH <-> CHINESE)")
    print("=" * 80)
    print("Objective: Prove that English 'God' and Chinese '神' share LJPW coordinates.")
    print("Method: Encoding Mark 1:1 -> LJPW Space -> Measuring Semantic Distance")
    print("-" * 80)

    detector = EnhancedPatternDetector()
    fidelity = SemanticReconstructionFidelity()

    # Test Case 1: Mark 1:1
    # "The beginning of the Good News of Jesus Christ, the Son of God."
    eng_text = "The beginning of the Good News of Jesus Christ, the Son of God."
    
    # "神的儿子，耶稣基督福音的起头" (God's Son, Jesus Christ Gospel's beginning)
    chi_text = "神的儿子，耶稣基督福音的起头"

    print(f"\n[Test Case 1] Mark 1:1")
    print(f"  English: {eng_text}")
    try:
        print(f"  Chinese: {chi_text}")
    except UnicodeEncodeError:
        print(f"  Chinese: [Unable to print characters in this console]")

    # Encode with Context Awareness
    print("\n  Encoding to Semantic Hilbert Space...")
    eng_sig = detector.calculate_field_signature_v2(eng_text, context="Gospel Introduction")
    chi_sig = detector.calculate_field_signature_v2(chi_text, context="Gospel Introduction")

    eng_coords = np.array([eng_sig['L'], eng_sig['J'], eng_sig['P'], eng_sig['W']])
    chi_coords = np.array([chi_sig['L'], chi_sig['J'], chi_sig['P'], chi_sig['W']])

    print(f"  English LJPW: [{eng_coords[0]:.3f}, {eng_coords[1]:.3f}, {eng_coords[2]:.3f}, {eng_coords[3]:.3f}]")
    print(f"  English Evidence: {eng_sig['evidence']}")
    print(f"  Chinese LJPW: [{chi_coords[0]:.3f}, {chi_coords[1]:.3f}, {chi_coords[2]:.3f}, {chi_coords[3]:.3f}]")
    print(f"  Chinese Evidence: {chi_sig['evidence']}")

    # Evaluate Fidelity
    print("\n  Validating Quantum Semantic Fidelity...")
    eng_harmony = fidelity.calculate_harmony(eng_coords)
    chi_harmony = fidelity.calculate_harmony(chi_coords)
    
    result = fidelity.evaluate_translation_quality(
        eng_coords, chi_coords,
        eng_harmony,
        chi_harmony
    )

    print("\n  RESULTS:")
    print(f"  Quality Level: {result['quality_level']}")
    print(f"  Overall Fidelity: {result['overall_fidelity']:.2%}")
    print(f"  LJPW Distance (epsilon): {result['euclidean_distance']:.4f} (Threshold: < 0.08)")
    print(f"  Harmony Drift (Delta_H): {result['harmony_drift']:.4f} (Threshold: < 0.03)")
    
    print(f"  Harmony Drift (Delta_H): {result['harmony_drift']:.4f} (Threshold: < 0.03)")
    
    # Test Case 2: Mark 1:2
    print("\n" + "-" * 50)
    print("[Test Case 2] Mark 1:2 (Prophecy Context)")
    eng_text_2 = "As it is written in Isaiah the prophet: Behold, I send my messenger ahead of you, who will prepare your way;"
    chi_text_2 = "正如先知以赛亚书上记着说：看哪，我要差遣我的使者在你前面，预备道路"
    
    print(f"  English: {eng_text_2}")
    try:
        print(f"  Chinese: {chi_text_2}")
    except:
        print(f"  Chinese: [Mark 1:2 Chinese Text]")
        
    eng_sig_2 = detector.calculate_field_signature_v2(eng_text_2, context="Prophecy")
    chi_sig_2 = detector.calculate_field_signature_v2(chi_text_2, context="Prophecy")

    eng_coords_2 = np.array([eng_sig_2['L'], eng_sig_2['J'], eng_sig_2['P'], eng_sig_2['W']])
    chi_coords_2 = np.array([chi_sig_2['L'], chi_sig_2['J'], chi_sig_2['P'], chi_sig_2['W']])
    
    print(f"  English LJPW: [{eng_coords_2[0]:.3f}, {eng_coords_2[1]:.3f}, {eng_coords_2[2]:.3f}, {eng_coords_2[3]:.3f}]")
    print(f"  Chinese LJPW: [{chi_coords_2[0]:.3f}, {chi_coords_2[1]:.3f}, {chi_coords_2[2]:.3f}, {chi_coords_2[3]:.3f}]")
    
    result_2 = fidelity.evaluate_translation_quality(
        eng_coords_2, chi_coords_2,
        fidelity.calculate_harmony(eng_coords_2),
        fidelity.calculate_harmony(chi_coords_2)
    )
    print(f"  Quality Level: {result_2['quality_level']}")
    print(f"  LJPW Distance: {result_2['euclidean_distance']:.4f}")

    print("\n  Conclusion: ", end="")
    if result['quality_level'] in ['EXCELLENT', 'GOOD']:
        print("✓ SUCCESS: Meaning is preserved across languages.")
    else:
        print("✗ FAILURE: Meaning divergence detected (check linguistic markers).")

if __name__ == "__main__":
    test_cross_lingual_fidelity()
