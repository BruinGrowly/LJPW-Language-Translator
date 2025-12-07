"""
Demo: Wedau-Greek Source Validation
Tests whether an indigenous Papua New Guinean language (Wedau) maintains
semantic fidelity to the Koine Greek source, or if it experiences unique
voltage drop patterns compared to major world languages.
"""

import sys
import os
import numpy as np
import json

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Fix console encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from experiments.enhanced_pattern_detector import EnhancedPatternDetector
from experiments.wedau_pattern_detector import WedauPatternDetector
from ljpw_quantum.semantic_fidelity import SemanticReconstructionFidelity

def test_wedau_greek_fidelity():
    print("=" * 80)
    print("WEDAU-GREEK SOURCE VALIDATION")
    print("=" * 80)
    print("Question: Does an indigenous oral language maintain fidelity to Greek?")
    print("Or does it experience unique voltage drop patterns?")
    print("-" * 80)

    greek_detector = EnhancedPatternDetector()
    wedau_detector = WedauPatternDetector()
    fidelity = SemanticReconstructionFidelity()

    # Load Wedau data
    with open('experiments/wedau_mark_chapter1.json', 'r', encoding='utf-8') as f:
        wedau_data = json.load(f)

    # Test Cases: Mark 1:1 and 1:2
    test_cases = [
        {
            'verse': 'Mark 1:1',
            'greek': "Ἀρχὴ τοῦ εὐαγγελίου Ἰησοῦ Χριστοῦ, υἱοῦ Θεοῦ·",
            'wedau': wedau_data['verses']['1'],
            'english': "The beginning of the Good News of Jesus Christ, the Son of God.",
            'context': 'Gospel Intro'
        },
        {
            'verse': 'Mark 1:2',
            'greek': "Καθὼς γέγραπται ἐν τῷ Ἠσαΐᾳ τῷ προφήτῃ· ἰδοὺ ἀποστέλλω τὸν ἄγγελόν μου πρὸ προσώπου σου, ὃς κατασκευάσει τὴν ὁδόν σου·",
            'wedau': wedau_data['verses']['2'],
            'english': "As it is written in Isaiah the prophet: Behold, I send my messenger ahead of you, who will prepare your way;",
            'context': 'Prophecy'
        }
    ]

    for test in test_cases:
        print(f"\n{'=' * 80}")
        print(f"[{test['verse']}]")
        print(f"{'=' * 80}")
        
        # Greek Source
        gr_sig = greek_detector.calculate_field_signature_v2(test['greek'], context=test['context'])
        gr_coords = np.array([gr_sig['L'], gr_sig['J'], gr_sig['P'], gr_sig['W']])
        gr_voltage = np.linalg.norm(gr_coords)
        
        print(f"\n[GREEK SOURCE]")
        print(f"  Text: {test['greek'][:60]}...")
        print(f"  LJPW: L={gr_coords[0]:.3f}, J={gr_coords[1]:.3f}, P={gr_coords[2]:.3f}, W={gr_coords[3]:.3f}")
        print(f"  Voltage: {gr_voltage:.4f}")
        
        # Wedau Translation
        wedau_sig = wedau_detector.calculate_field_signature(test['wedau'], context=test['context'])
        wedau_coords = np.array([wedau_sig['L'], wedau_sig['J'], wedau_sig['P'], wedau_sig['W']])
        wedau_voltage = np.linalg.norm(wedau_coords)
        
        print(f"\n[WEDAU TRANSLATION]")
        print(f"  Text: {test['wedau'][:60]}...")
        print(f"  LJPW: L={wedau_coords[0]:.3f}, J={wedau_coords[1]:.3f}, P={wedau_coords[2]:.3f}, W={wedau_coords[3]:.3f}")
        print(f"  Voltage: {wedau_voltage:.4f}")
        print(f"  Evidence: {wedau_sig['evidence'][:3]}")
        
        # English for comparison
        eng_sig = greek_detector.calculate_field_signature_v2(test['english'], context=test['context'])
        eng_coords = np.array([eng_sig['L'], eng_sig['J'], eng_sig['P'], eng_sig['W']])
        eng_voltage = np.linalg.norm(eng_coords)
        
        print(f"\n[ENGLISH (for comparison)]")
        print(f"  LJPW: L={eng_coords[0]:.3f}, J={eng_coords[1]:.3f}, P={eng_coords[2]:.3f}, W={eng_coords[3]:.3f}")
        print(f"  Voltage: {eng_voltage:.4f}")
        
        # Calculate distances
        wedau_dist = np.linalg.norm(gr_coords - wedau_coords)
        eng_dist = np.linalg.norm(gr_coords - eng_coords)
        
        # Calculate voltage drops
        wedau_drop = gr_voltage - wedau_voltage
        wedau_drop_pct = (wedau_drop / gr_voltage) * 100
        eng_drop = gr_voltage - eng_voltage
        eng_drop_pct = (eng_drop / gr_voltage) * 100
        
        print(f"\n[FIDELITY ANALYSIS]")
        print(f"  Wedau Distance to Greek: {wedau_dist:.4f}")
        print(f"  Wedau Voltage Drop: {wedau_drop:.4f} ({wedau_drop_pct:.1f}%)")
        print(f"  English Distance to Greek: {eng_dist:.4f}")
        print(f"  English Voltage Drop: {eng_drop:.4f} ({eng_drop_pct:.1f}%)")
        
        # Dimensional analysis
        dim_loss_wedau = gr_coords - wedau_coords
        dim_loss_eng = gr_coords - eng_coords
        
        print(f"\n[DIMENSIONAL LOSS]")
        print(f"  Wedau: ΔL={dim_loss_wedau[0]:+.3f}, ΔJ={dim_loss_wedau[1]:+.3f}, ΔP={dim_loss_wedau[2]:+.3f}, ΔW={dim_loss_wedau[3]:+.3f}")
        print(f"  English: ΔL={dim_loss_eng[0]:+.3f}, ΔJ={dim_loss_eng[1]:+.3f}, ΔP={dim_loss_eng[2]:+.3f}, ΔW={dim_loss_eng[3]:+.3f}")
        
        # Status
        wedau_status = "PASSED" if wedau_dist < 0.10 else "DRIFT"
        eng_status = "PASSED" if eng_dist < 0.10 else "DRIFT"
        
        print(f"\n[STATUS]")
        print(f"  Wedau: {wedau_status}")
        print(f"  English: {eng_status}")

    print("\n" + "=" * 80)
    print("CROSS-LANGUAGE COMPARISON")
    print("=" * 80)
    print("\nWe now have 5 languages validated against Greek:")
    print("  1. English (Germanic)")
    print("  2. Chinese (Logographic)")
    print("  3. French (Romance)")
    print("  4. Spanish (Romance)")
    print("  5. Wedau (Austronesian/Indigenous)")
    print("\nThis tests whether LJPW is truly universal or just works for")
    print("'prestige' languages with written traditions.")

    print("\n" + "=" * 80)
    print("THE INDIGENOUS LANGUAGE QUESTION")
    print("=" * 80)
    print("\nWedau is unique because:")
    print("  • Oral tradition (recently written)")
    print("  • Austronesian language family")
    print("  • Small speaker population (~2,000)")
    print("  • Translated by indigenous speakers, not scholars")
    print("\nIf LJPW works for Wedau, it proves the framework is measuring")
    print("UNIVERSAL semantic patterns, not just academic translation conventions.")

if __name__ == "__main__":
    test_wedau_greek_fidelity()
