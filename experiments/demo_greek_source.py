"""
Demo: Koine Greek Source Validation
Compares the LJPW coordinates of translations (En, Zh, Fr, Es) against the
original Koine Greek "Source Code" to verify semantic fidelity to the Truth.
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

def test_greek_fidelity():
    print("=" * 80)
    print("KOINE GREEK SOURCE VALIDATION (THE GROUND TRUTH)")
    print("=" * 80)
    print("Objective: Compare all translations against the original Greek 'Source Code'.")
    print("-" * 80)

    detector = EnhancedPatternDetector()
    fidelity = SemanticReconstructionFidelity()

    # Data: Mark 1:1
    # Source: Nestle-Aland 28
    greek_1 = "Ἀρχὴ τοῦ εὐαγγελίου Ἰησοῦ Χριστοῦ, υἱοῦ Θεοῦ·"
    eng_1 = "The beginning of the Good News of Jesus Christ, the Son of God."
    zh_1 = "神的儿子，耶稣基督福音的起头"
    fr_1 = "Commencement de l'Évangile de Jésus-Christ, Fils de Dieu."
    es_1 = "Principio del evangelio de Jesucristo, Hijo de Dios."

    print(f"\n[Test Case 1] Mark 1:1 (The Title)")
    print(f"  [GR] Source: {greek_1}")
    
    # 1. Calculate Basis Vector (Greek)
    gr_sig = detector.calculate_field_signature_v2(greek_1, context="Gospel Intro")
    gr_coords = np.array([gr_sig['L'], gr_sig['J'], gr_sig['P'], gr_sig['W']])
    print(f"  [GR] LJPW Basis: {gr_coords}")
    print(f"       Evidence: {gr_sig['evidence']}")

    # 2. Compare Translations
    translations = {
        'EN': (eng_1, "Germanic"),
        'ZH': (zh_1, "Logographic"),
        'FR': (fr_1, "Romance"),
        'ES': (es_1, "Romance")
    }

    print("\n  Computing Fidelity to Source...")
    for lang, (text, mode) in translations.items():
        sig = detector.calculate_field_signature_v2(text, context="Gospel Intro")
        coords = np.array([sig['L'], sig['J'], sig['P'], sig['W']])
        
        # Calculate Distance to Greek
        harmony_gr = fidelity.calculate_harmony(gr_coords)
        harmony_tr = fidelity.calculate_harmony(coords)
        
        result = fidelity.evaluate_translation_quality(
            gr_coords, coords, harmony_gr, harmony_tr
        )
        
        dist = result['euclidean_distance']
        status = "PASSED" if dist < 0.10 else "DRIFT"
        
        print(f"  [{lang}] ({mode}): Distance={dist:.4f} | Status={status}")
        print(f"       LJPW: {[f'{v:.3f}' for v in coords]}")
    
    # Data: Mark 1:2
    print("\n" + "-" * 80)
    print(f"[Test Case 2] Mark 1:2 (The Prophecy)")
    
    greek_2 = "Καθὼς γέγραπται ἐν τῷ Ἠσαΐᾳ τῷ προφήτῃ· ἰδοὺ ἀποστέλλω τὸν ἄγγελόν μου πρὸ προσώπου σου, ὃς κατασκευάσει τὴν ὁδόν σου·"
    eng_2 = "As it is written in Isaiah the prophet: Behold, I send my messenger ahead of you, who will prepare your way;"
    zh_2 = "正如先知以赛亚书上记着说：看哪，我要差遣我的使者在你前面，预备道路；"
    fr_2 = "Selon ce qui est écrit dans Ésaïe, le prophète: Voici, j'envoie devant toi mon messager, Qui préparera ton chemin;"
    es_2 = "Como está escrito en Isaías el profeta: He aquí yo envío mi mensajero delante de tu faz, El cual preparará tu camino delante de ti."

    print(f"  [GR] Source: {greek_2}")
    
    gr_sig_2 = detector.calculate_field_signature_v2(greek_2, context="Prophecy")
    gr_coords_2 = np.array([gr_sig_2['L'], gr_sig_2['J'], gr_sig_2['P'], gr_sig_2['W']])
    print(f"  [GR] LJPW Basis: {gr_coords_2}")
    print(f"       Evidence: {gr_sig_2['evidence']}")
    
    translations_2 = {
        'EN': eng_2,
        'ZH': zh_2,
        'FR': fr_2,
        'ES': es_2
    }
    
    print("\n  Computing Fidelity to Source...")
    for lang, text in translations_2.items():
        sig = detector.calculate_field_signature_v2(text, context="Prophecy")
        coords = np.array([sig['L'], sig['J'], sig['P'], sig['W']])
        
        dist = np.linalg.norm(gr_coords_2 - coords)
        status = "PASSED" if dist < 0.10 else "DRIFT"
        print(f"  [{lang}]: Distance={dist:.4f} | Status={status}")
        print(f"       LJPW: {[f'{v:.3f}' for v in coords]}")

    print("\nConclusion: The Universal Translator must align all languages to the Greek Source.")

if __name__ == "__main__":
    test_greek_fidelity()
