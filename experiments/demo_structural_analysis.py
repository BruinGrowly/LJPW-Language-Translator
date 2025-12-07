"""
Demo: Deep Structural Analysis of Voltage Drop
Investigates WHY simple lexical substitution fails to recover semantic voltage.

Hypothesis: The voltage drop is caused by STRUCTURAL differences between Greek
and English, not just word choice.
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

def deep_structural_analysis():
    print("=" * 80)
    print("DEEP STRUCTURAL ANALYSIS: Why Lexical Changes Fail")
    print("=" * 80)
    print("Question: Why does 'messenger' → 'angel' only recover 0.1% of voltage?")
    print("-" * 80)

    detector = EnhancedPatternDetector()

    # Let's analyze the FULL sentence structure
    greek = "ἰδοὺ ἀποστέλλω τὸν ἄγγελόν μου πρὸ προσώπου σου"
    english_messenger = "Behold, I send my messenger ahead of you"
    english_angel = "Behold, I send my angel ahead of you"

    print("\n[GREEK STRUCTURE]")
    print(f"Text: {greek}")
    print("\nWord-by-word breakdown:")
    print("  ἰδοὺ (idou) = Behold [Attention marker - High Power]")
    print("  ἀποστέλλω (apostello) = I send [Divine commission - High Power + Wisdom]")
    print("  τὸν ἄγγελόν (ton angelon) = the angel/messenger [Divine + Power superposition]")
    print("  μου (mou) = my [Relational - High Love]")
    print("  πρὸ προσώπου (pro prosopou) = before face [Intimate presence - High Love]")
    print("  σου (sou) = your [Relational - High Love]")

    gr_sig = detector.calculate_field_signature_v2(greek, context="Divine Commission")
    gr_coords = np.array([gr_sig['L'], gr_sig['J'], gr_sig['P'], gr_sig['W']])
    
    print(f"\nGreek LJPW: L={gr_coords[0]:.3f}, J={gr_coords[1]:.3f}, P={gr_coords[2]:.3f}, W={gr_coords[3]:.3f}")
    print(f"Evidence: {gr_sig['evidence']}")

    print("\n" + "=" * 80)
    print("[ENGLISH STRUCTURE - 'messenger']")
    print(f"Text: {english_messenger}")
    print("\nWord-by-word breakdown:")
    print("  Behold = Attention marker [Power]")
    print("  I send = Simple action [Power]")
    print("  my messenger = Functional role [Power only - Divine dimension LOST]")
    print("  ahead of you = Spatial/temporal [Justice - structural]")

    en_msg_sig = detector.calculate_field_signature_v2(english_messenger, context="Divine Commission")
    en_msg_coords = np.array([en_msg_sig['L'], en_msg_sig['J'], en_msg_sig['P'], en_msg_sig['W']])
    
    print(f"\nEnglish (messenger) LJPW: L={en_msg_coords[0]:.3f}, J={en_msg_coords[1]:.3f}, P={en_msg_coords[2]:.3f}, W={en_msg_coords[3]:.3f}")
    print(f"Evidence: {en_msg_sig['evidence']}")

    print("\n" + "=" * 80)
    print("[ENGLISH STRUCTURE - 'angel']")
    print(f"Text: {english_angel}")
    
    en_ang_sig = detector.calculate_field_signature_v2(english_angel, context="Divine Commission")
    en_ang_coords = np.array([en_ang_sig['L'], en_ang_sig['J'], en_ang_sig['P'], en_ang_sig['W']])
    
    print(f"\nEnglish (angel) LJPW: L={en_ang_coords[0]:.3f}, J={en_ang_coords[1]:.3f}, P={en_ang_coords[2]:.3f}, W={en_ang_coords[3]:.3f}")
    print(f"Evidence: {en_ang_sig['evidence']}")

    # Calculate the difference
    lexical_change = en_ang_coords - en_msg_coords
    print(f"\nLexical Change Impact: ΔL={lexical_change[0]:+.3f}, ΔJ={lexical_change[1]:+.3f}, ΔP={lexical_change[2]:+.3f}, ΔW={lexical_change[3]:+.3f}")

    print("\n" + "=" * 80)
    print("THE STRUCTURAL LOSS PROBLEM")
    print("=" * 80)
    print("\nGreek has THREE relational markers that English loses:")
    print("  1. μου (mou) = 'my' - possessive intimacy")
    print("  2. πρὸ προσώπου (pro prosopou) = 'before [your] face' - physical presence")
    print("  3. σου (sou) = 'your' - relational bond")
    print("\nEnglish reduces this to:")
    print("  'ahead of you' - mere spatial positioning")
    print("\nThis is a STRUCTURAL difference, not lexical.")

    # Test: Can we recover voltage by restoring the relational structure?
    enhanced_english = "Behold, I send my angel before your face"
    
    print("\n" + "=" * 80)
    print("STRUCTURAL RECOVERY EXPERIMENT")
    print("=" * 80)
    print(f"\nOriginal: {english_messenger}")
    print(f"Enhanced: {enhanced_english}")
    print("  Changes:")
    print("    1. 'messenger' → 'angel' (Divine dimension)")
    print("    2. 'ahead of you' → 'before your face' (Relational intimacy)")

    enh_sig = detector.calculate_field_signature_v2(enhanced_english, context="Divine Commission")
    enh_coords = np.array([enh_sig['L'], enh_sig['J'], enh_sig['P'], enh_sig['W']])
    
    print(f"\nEnhanced LJPW: L={enh_coords[0]:.3f}, J={enh_coords[1]:.3f}, P={enh_coords[2]:.3f}, W={enh_coords[3]:.3f}")
    print(f"Evidence: {enh_sig['evidence']}")

    # Calculate recovery
    original_gap = gr_coords - en_msg_coords
    enhanced_gap = gr_coords - enh_coords
    recovery = original_gap - enhanced_gap
    recovery_pct = (np.linalg.norm(recovery) / np.linalg.norm(original_gap)) * 100

    print(f"\nRecovery Analysis:")
    print(f"  Original Gap: ||Δ|| = {np.linalg.norm(original_gap):.4f}")
    print(f"  Enhanced Gap: ||Δ|| = {np.linalg.norm(enhanced_gap):.4f}")
    print(f"  Recovery: {recovery_pct:.1f}% of gap closed")
    print(f"  Per-dimension recovery: ΔL={recovery[0]:+.3f}, ΔJ={recovery[1]:+.3f}, ΔP={recovery[2]:+.3f}, ΔW={recovery[3]:+.3f}")

    if recovery_pct > 20:
        print("\n✅ SIGNIFICANT RECOVERY: Structural changes matter more than lexical!")
    else:
        print("\n⚠️  LIMITED RECOVERY: Even structural changes can't fully bridge the gap.")

    print("\n" + "=" * 80)
    print("FUNDAMENTAL INSIGHT")
    print("=" * 80)
    print("\nThe 'Voltage Drop' has THREE sources:")
    print("\n1. LEXICAL COLLAPSE")
    print("   Greek: ἄγγελον (angel/messenger superposition)")
    print("   English: 'messenger' (single state)")
    print("   → Loses Divine dimension")
    print("\n2. STRUCTURAL SIMPLIFICATION")
    print("   Greek: πρὸ προσώπου σου (before your face)")
    print("   English: 'ahead of you' (spatial only)")
    print("   → Loses relational intimacy (Love dimension)")
    print("\n3. MORPHOLOGICAL DENSITY")
    print("   Greek: Inflected forms carry grammatical + semantic info")
    print("   English: Word order + prepositions (less dense)")
    print("   → Loses information compression (Wisdom dimension)")
    print("\nConclusion: Full voltage recovery requires:")
    print("  • Better lexical choices (angel vs messenger)")
    print("  • Structural preservation (before your face)")
    print("  • Possibly even syntactic restructuring")

if __name__ == "__main__":
    deep_structural_analysis()
