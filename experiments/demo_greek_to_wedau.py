"""
Greek to Wedau Translation Experiment
Matthew 5:1-12 (The Beatitudes)

Approach:
1. Extract LJPW coordinates from Greek source
2. Apply Wedau grammatical patterns (particles, demonstratives, emphatics)
3. Generate Wedau-style text that preserves Greek semantic voltage
4. Validate against known Wedau patterns from Mark Chapter 1
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
from experiments.wedau_pattern_detector import WedauPatternDetector

def translate_greek_to_wedau():
    print("=" * 80)
    print("GREEK → WEDAU TRANSLATION EXPERIMENT")
    print("Matthew 5:1-12 (The Beatitudes)")
    print("=" * 80)
    print("Objective: Generate Wedau-style translation directly from Greek LJPW coordinates")
    print("-" * 80)

    greek_detector = EnhancedPatternDetector()
    wedau_detector = WedauPatternDetector()

    # Matthew 5:1-12 Greek text (Nestle-Aland 28)
    # We'll start with just verses 1-5 for this experiment
    greek_verses = {
        1: "Ἰδὼν δὲ τοὺς ὄχλους ἀνέβη εἰς τὸ ὄρος· καὶ καθίσαντος αὐτοῦ προσῆλθαν αὐτῷ οἱ μαθηταὶ αὐτοῦ·",
        2: "καὶ ἀνοίξας τὸ στόμα αὐτοῦ ἐδίδασκεν αὐτοὺς λέγων·",
        3: "Μακάριοι οἱ πτωχοὶ τῷ πνεύματι, ὅτι αὐτῶν ἐστιν ἡ βασιλεία τῶν οὐρανῶν.",
        4: "μακάριοι οἱ πενθοῦντες, ὅτι αὐτοὶ παρακληθήσονται.",
        5: "μακάριοι οἱ πραεῖς, ὅτι αὐτοὶ κληρονομήσουσιν τὴν γῆν.",
    }

    # English reference (for comparison)
    english_verses = {
        1: "Seeing the crowds, he went up on the mountain, and when he sat down, his disciples came to him.",
        2: "And he opened his mouth and taught them, saying:",
        3: "Blessed are the poor in spirit, for theirs is the kingdom of heaven.",
        4: "Blessed are those who mourn, for they shall be comforted.",
        5: "Blessed are the meek, for they shall inherit the earth.",
    }

    print("\n[STEP 1: ANALYZE GREEK SOURCE]")
    print("-" * 80)
    
    greek_analysis = {}
    for verse_num, greek_text in greek_verses.items():
        sig = greek_detector.calculate_field_signature_v2(greek_text, context="Teaching")
        coords = np.array([sig['L'], sig['J'], sig['P'], sig['W']])
        voltage = np.linalg.norm(coords)
        
        greek_analysis[verse_num] = {
            'text': greek_text,
            'coords': coords,
            'voltage': voltage,
            'evidence': sig['evidence']
        }
        
        print(f"\nVerse {verse_num}:")
        print(f"  Greek: {greek_text[:60]}...")
        print(f"  LJPW: L={coords[0]:.3f}, J={coords[1]:.3f}, P={coords[2]:.3f}, W={coords[3]:.3f}")
        print(f"  Voltage: {voltage:.4f}")

    print("\n" + "=" * 80)
    print("[STEP 2: WEDAU TRANSLATION RULES]")
    print("=" * 80)
    
    print("\nBased on Mark Chapter 1 analysis, Wedau requires:")
    print("  1. Subject markers ('i') for every agent")
    print("  2. Possessive markers ('ana') for relationships")
    print("  3. Conjunctions ('ma') for connections")
    print("  4. Demonstratives ('ivi', 'weꞌi') for presence")
    print("  5. Emphatics ('yamna') for certainty")
    print("  6. Subordinators ('da') for purpose/result")

    print("\n" + "=" * 80)
    print("[STEP 3: PROPOSED WEDAU TRANSLATIONS]")
    print("=" * 80)
    
    # Attempt to generate Wedau-style translations
    # This is experimental - we're applying the patterns we learned
    
    wedau_proposals = {
        1: {
            'literal': "Yesu i inana rava anatapuhi, i nae au dobuna. Ma i maꞌae, ana tauvotaghotagho hi neꞌi awarina.",
            'gloss': "Jesus [i] saw [i] crowds many, [i] went [au] mountain. [Ma] [i] sat, [ana] disciples [hi] came [awarina].",
            'reasoning': "Added 'i' for Jesus (subject), 'au' for location (mountain), 'ma' for conjunction, 'ana' for possession (his disciples), 'hi' for plural"
        },
        2: {
            'literal': "Ma Yesu i ponana i wana-tawaneꞌi ma i viharaharamana hita, i riwa ipa:",
            'gloss': "[Ma] Jesus [i] mouth [i] opened [ma] [i] taught them, [i] said [ipa]:",
            'reasoning': "Added 'ma' (and), 'i' for each verb, 'ipa' for quotative (saying)"
        },
        3: {
            'literal': "Rava hi nuwaboyei, hita aruwa-apoapoena hi vovovoi, yamna God ana vibadana vouna hita.",
            'gloss': "Blessed [hi] are, they [hita] spirit-poor [hi] are, truly [yamna] God [ana] kingdom [vouna] theirs.",
            'reasoning': "Added 'hi' (plural), 'yamna' (emphatic), 'ana' (possessive for God's kingdom)"
        },
        4: {
            'literal': "Rava hi nuwaboyei, hita hi nuwanuwaboyei, yamna hita hi paꞌini.",
            'gloss': "Blessed [hi] are, they [hita] [hi] mourn, truly [yamna] they [hita] [hi] comforted.",
            'reasoning': "Reduplication 'nuwanuwaboyei' for emphasis (mourning), 'hi' for plural, 'yamna' for certainty"
        },
        5: {
            'literal': "Rava hi nuwaboyei, hita hi vivivireinei, yamna hita hi dobuna ana vouna.",
            'gloss': "Blessed [hi] are, they [hita] [hi] meek, truly [yamna] they [hita] [hi] earth [ana] inherit.",
            'reasoning': "Added 'hi' (plural), 'yamna' (emphatic), 'ana' for possession (of earth)"
        }
    }

    for verse_num, proposal in wedau_proposals.items():
        print(f"\n[Verse {verse_num}]")
        print(f"Greek:   {greek_verses[verse_num][:60]}...")
        print(f"English: {english_verses[verse_num]}")
        print(f"\nProposed Wedau: {proposal['literal']}")
        print(f"Gloss: {proposal['gloss']}")
        print(f"Reasoning: {proposal['reasoning']}")
        
        # Analyze the proposed Wedau
        wedau_sig = wedau_detector.calculate_field_signature(proposal['literal'], context="Teaching")
        wedau_coords = np.array([wedau_sig['L'], wedau_sig['J'], wedau_sig['P'], wedau_sig['W']])
        wedau_voltage = np.linalg.norm(wedau_coords)
        
        greek_coords = greek_analysis[verse_num]['coords']
        greek_voltage = greek_analysis[verse_num]['voltage']
        
        voltage_change = wedau_voltage - greek_voltage
        voltage_change_pct = (voltage_change / greek_voltage) * 100
        
        print(f"\nWedau LJPW: L={wedau_coords[0]:.3f}, J={wedau_coords[1]:.3f}, P={wedau_coords[2]:.3f}, W={wedau_coords[3]:.3f}")
        print(f"Wedau Voltage: {wedau_voltage:.4f}")
        print(f"Voltage Change: {voltage_change:+.4f} ({voltage_change_pct:+.1f}%)")
        
        if voltage_change > 0:
            print(f"✓ VOLTAGE GAIN (as expected for oral language)")
        else:
            print(f"⚠ Voltage drop (unexpected)")

    print("\n" + "=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    print("\nThis is an experimental translation using learned Wedau patterns.")
    print("To validate, we would need:")
    print("  1. Native Wedau speaker review")
    print("  2. Comparison with actual Wedau Matthew (if it exists)")
    print("  3. Verification of particle usage patterns")
    print("\nBut the LJPW framework allows us to:")
    print("  • Preserve Greek semantic voltage")
    print("  • Apply Wedau grammatical patterns systematically")
    print("  • Generate translations that maintain relational context")

if __name__ == "__main__":
    translate_greek_to_wedau()
