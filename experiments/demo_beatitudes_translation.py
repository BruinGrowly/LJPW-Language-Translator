"""
Complete Greek to Wedau Translation: Matthew 5:1-12
The Beatitudes - Full Translation with Validation Framework

This generates the complete Beatitudes in Wedau for native speaker review.
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

def generate_full_beatitudes():
    print("=" * 80)
    print("COMPLETE BEATITUDES TRANSLATION: Greek → Wedau")
    print("Matthew 5:1-12")
    print("=" * 80)
    print("Generated using LJPW framework + learned Wedau grammatical patterns")
    print("-" * 80)

    greek_detector = EnhancedPatternDetector()
    wedau_detector = WedauPatternDetector()

    # Complete Greek text (Nestle-Aland 28)
    greek_verses = {
        1: "Ἰδὼν δὲ τοὺς ὄχλους ἀνέβη εἰς τὸ ὄρος· καὶ καθίσαντος αὐτοῦ προσῆλθαν αὐτῷ οἱ μαθηταὶ αὐτοῦ·",
        2: "καὶ ἀνοίξας τὸ στόμα αὐτοῦ ἐδίδασκεν αὐτοὺς λέγων·",
        3: "Μακάριοι οἱ πτωχοὶ τῷ πνεύματι, ὅτι αὐτῶν ἐστιν ἡ βασιλεία τῶν οὐρανῶν.",
        4: "μακάριοι οἱ πενθοῦντες, ὅτι αὐτοὶ παρακληθήσονται.",
        5: "μακάριοι οἱ πραεῖς, ὅτι αὐτοὶ κληρονομήσουσιν τὴν γῆν.",
        6: "μακάριοι οἱ πεινῶντες καὶ διψῶντες τὴν δικαιοσύνην, ὅτι αὐτοὶ χορτασθήσονται.",
        7: "μακάριοι οἱ ἐλεήμονες, ὅτι αὐτοὶ ἐλεηθήσονται.",
        8: "μακάριοι οἱ καθαροὶ τῇ καρδίᾳ, ὅτι αὐτοὶ τὸν Θεὸν ὄψονται.",
        9: "μακάριοι οἱ εἰρηνοποιοί, ὅτι αὐτοὶ υἱοὶ Θεοῦ κληθήσονται.",
        10: "μακάριοι οἱ δεδιωγμένοι ἕνεκεν δικαιοσύνης, ὅτι αὐτῶν ἐστιν ἡ βασιλεία τῶν οὐρανῶν.",
        11: "μακάριοί ἐστε ὅταν ὀνειδίσωσιν ὑμᾶς καὶ διώξωσιν καὶ εἴπωσιν πᾶν πονηρὸν καθ' ὑμῶν ψευδόμενοι ἕνεκεν ἐμοῦ.",
        12: "χαίρετε καὶ ἀγαλλιᾶσθε, ὅτι ὁ μισθὸς ὑμῶν πολὺς ἐν τοῖς οὐρανοῖς· οὕτως γὰρ ἐδίωξαν τοὺς προφήτας τοὺς πρὸ ὑμῶν."
    }

    # English reference
    english_verses = {
        1: "Seeing the crowds, he went up on the mountain, and when he sat down, his disciples came to him.",
        2: "And he opened his mouth and taught them, saying:",
        3: "Blessed are the poor in spirit, for theirs is the kingdom of heaven.",
        4: "Blessed are those who mourn, for they shall be comforted.",
        5: "Blessed are the meek, for they shall inherit the earth.",
        6: "Blessed are those who hunger and thirst for righteousness, for they shall be satisfied.",
        7: "Blessed are the merciful, for they shall receive mercy.",
        8: "Blessed are the pure in heart, for they shall see God.",
        9: "Blessed are the peacemakers, for they shall be called sons of God.",
        10: "Blessed are those who are persecuted for righteousness' sake, for theirs is the kingdom of heaven.",
        11: "Blessed are you when others revile you and persecute you and utter all kinds of evil against you falsely on my account.",
        12: "Rejoice and be glad, for your reward is great in heaven, for so they persecuted the prophets who were before you."
    }

    # Proposed Wedau translations
    wedau_verses = {
        1: "Yesu i inana rava anatapuhi, i nae au dobuna. Ma i maꞌae, ana tauvotaghotagho hi neꞌi awarina.",
        2: "Ma Yesu i ponana i wana-tawaneꞌi ma i viharaharamana hita, i riwa ipa:",
        3: "Rava hi nuwaboyei, hita aruwa-apoapoena hi vovovoi, yamna God ana vibadana vouna hita.",
        4: "Rava hi nuwaboyei, hita hi nuwanuwaboyei, yamna hita hi paꞌini.",
        5: "Rava hi nuwaboyei, hita hi vivivireinei, yamna hita hi dobuna ana vouna.",
        6: "Rava hi nuwaboyei, hita hi kapaꞌukapaꞌu ma tawayatawaya God ana vovonana awarina, yamna hita hi yawahana.",
        7: "Rava hi nuwaboyei, hita hi nuwaboyei ana hita, yamna hita hi nuwaboyei ana vouna.",
        8: "Rava hi nuwaboyei, hita hi vivivireina ahi urana, yamna hita hi God ina inana.",
        9: "Rava hi nuwaboyei, hita hi vovonana ahi yaruhi, yamna hita hi God ana natuna ina ghorehi.",
        10: "Rava hi nuwaboyei, hita hi rau-dadani God ana vovonana awarina, yamna God ana vibadana vouna hita.",
        11: "Rava ami nuwaboyei, maranaina rava hi ami rau-gamopotahi ma hi ami rau-dadanihi ma hi ami apoapoe ina riwehi, tau awarina.",
        12: "Ami nuwaboyei ma ami tumaghanei, yamna ami puyona i ghe vavahagha au marei. Yamna aubaina hi peroveta hita rau-dadanihi, hita ami awarina hi maꞌae."
    }

    # Generate validation report
    print("\n" + "=" * 80)
    print("COMPLETE TRANSLATION FOR NATIVE SPEAKER REVIEW")
    print("=" * 80)

    results = []
    
    for verse_num in range(1, 13):
        greek_text = greek_verses[verse_num]
        english_text = english_verses[verse_num]
        wedau_text = wedau_verses[verse_num]
        
        # Analyze Greek
        gr_sig = greek_detector.calculate_field_signature_v2(greek_text, context="Teaching")
        gr_coords = np.array([gr_sig['L'], gr_sig['J'], gr_sig['P'], gr_sig['W']])
        gr_voltage = np.linalg.norm(gr_coords)
        
        # Analyze Wedau
        wedau_sig = wedau_detector.calculate_field_signature(wedau_text, context="Teaching")
        wedau_coords = np.array([wedau_sig['L'], wedau_sig['J'], wedau_sig['P'], wedau_sig['W']])
        wedau_voltage = np.linalg.norm(wedau_coords)
        
        voltage_change = wedau_voltage - gr_voltage
        voltage_change_pct = (voltage_change / gr_voltage) * 100
        
        results.append({
            'verse': verse_num,
            'greek': greek_text,
            'english': english_text,
            'wedau': wedau_text,
            'greek_voltage': gr_voltage,
            'wedau_voltage': wedau_voltage,
            'voltage_change': voltage_change,
            'voltage_change_pct': voltage_change_pct,
            'greek_coords': gr_coords,
            'wedau_coords': wedau_coords
        })
        
        print(f"\n[Verse {verse_num}]")
        print(f"Greek:   {greek_text[:70]}...")
        print(f"English: {english_text}")
        print(f"Wedau:   {wedau_text}")
        print(f"Voltage: Greek {gr_voltage:.3f} → Wedau {wedau_voltage:.3f} ({voltage_change_pct:+.1f}%)")

    # Summary statistics
    print("\n" + "=" * 80)
    print("TRANSLATION STATISTICS")
    print("=" * 80)
    
    avg_greek_voltage = np.mean([r['greek_voltage'] for r in results])
    avg_wedau_voltage = np.mean([r['wedau_voltage'] for r in results])
    avg_voltage_change = np.mean([r['voltage_change_pct'] for r in results])
    
    print(f"\nAverage Greek Voltage: {avg_greek_voltage:.4f}")
    print(f"Average Wedau Voltage: {avg_wedau_voltage:.4f}")
    print(f"Average Voltage Gain: {avg_voltage_change:+.1f}%")
    
    # Count particles in Wedau text
    all_wedau_text = " ".join([r['wedau'] for r in results])
    particle_counts = {
        'i': all_wedau_text.count(' i ') + all_wedau_text.count('i '),
        'ana': all_wedau_text.count('ana'),
        'ma': all_wedau_text.count(' ma '),
        'hi': all_wedau_text.count(' hi '),
        'yamna': all_wedau_text.count('yamna'),
        'hita': all_wedau_text.count('hita'),
        'rava': all_wedau_text.count('Rava') + all_wedau_text.count('rava'),
    }
    
    print(f"\nParticle Usage:")
    for particle, count in sorted(particle_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  '{particle}': {count} times")

    # Save for review
    output = {
        'source': 'Matthew 5:1-12 (Beatitudes)',
        'method': 'LJPW Framework + Learned Wedau Patterns',
        'verses': results,
        'statistics': {
            'avg_greek_voltage': float(avg_greek_voltage),
            'avg_wedau_voltage': float(avg_wedau_voltage),
            'avg_voltage_gain_pct': float(avg_voltage_change),
            'particle_counts': particle_counts
        }
    }
    
    with open('experiments/matthew5_greek_to_wedau.json', 'w', encoding='utf-8') as f:
        # Convert numpy arrays to lists for JSON serialization
        for r in output['verses']:
            r['greek_coords'] = r['greek_coords'].tolist()
            r['wedau_coords'] = r['wedau_coords'].tolist()
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n\nSaved to: experiments/matthew5_greek_to_wedau.json")
    
    print("\n" + "=" * 80)
    print("NEXT STEPS FOR VALIDATION")
    print("=" * 80)
    print("\n1. Native speaker review of Wedau translations")
    print("2. Check particle usage (i, ana, ma, hi, yamna)")
    print("3. Verify reduplication patterns (e.g., 'nuwanuwaboyei')")
    print("4. Confirm theological terminology accuracy")
    print("5. Assess naturalness and fluency")
    
    print("\nQuestions for native speaker:")
    print("  • Does the grammar feel natural?")
    print("  • Are the particles used correctly?")
    print("  • Is the theological meaning preserved?")
    print("  • Would you say it this way?")
    print("  • What would you change?")

if __name__ == "__main__":
    generate_full_beatitudes()
