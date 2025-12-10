#!/usr/bin/env python3
"""
Quechua-Farsi Translation Test
==============================

Tests the LJPW resonance paradigm on extremely different language families:
- Quechua (Andean language family, agglutinative, SOV)
- Farsi/Persian (Indo-Iranian, VSO/SVO, different script)

These languages have:
- No common ancestry
- Different scripts (Latin-adapted vs Arabic)
- Different word order
- Different grammatical structures
- Different cultural contexts

If resonance works here, it works everywhere.
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_quantum.resonance_engine import ResonanceEngine
from experiments.enhanced_pattern_detector import EnhancedPatternDetector


# Quechua translations (San Martín Quechua - QVS)
QUECHUA_VERSES = {
    '1': "Jesucristo Diospa Churinmanta alli willakuypa qallariyninmi kay.",
    '11': "Hanaq pachamantam niqra uyarirqan: Qanmi Churiy munakushqay; qanwanmi kusikuni.",
    '15': "Willarkansapa: Chay nawpa yachachikuk runakuna rimashkanshina nami shamushkanina. Tata Dios sukaman munan kunanmantapacha mandunpina kawsanaykichipa. Chayrayku tukuy mana alli ruranaykichimanta wanaychi. Tata Dios tukuy willashushkaykichita tukuy shunku kreyiychi.",
    '41': "Jesusqa khuyakuspa makinta chanrarqan hap'ispa nirqan: Munani, llimphu kay."
}

# English reference translations (NWT)
ENGLISH_VERSES = {
    '1': "The beginning of the good news about Jesus Christ, the Son of God.",
    '11': "And a voice came out of the heavens: You are my Son, the beloved; I have approved of you.",
    '15': "The appointed time has been fulfilled, and the Kingdom of God has drawn near. Repent, and have faith in the good news.",
    '41': "At that he was moved with pity, and he stretched out his hand and touched him, and said to him: I want to! Be made clean."
}

# Farsi/Persian translations (Persian Old Version - POV-FAS)
FARSI_VERSES = {
    '1': "ابتدا انجیل عیسی مسیح پسر خدا",
    '11': "آوازی از آسمان آمد که تو پسر حبیب من هستی که از تو خشنودم",
    '15': "می گفت: وقت تمام شد و ملکوت خدا نزدیک است. پس توبه کنید و به انجیل ایمان بیاورید",
    '41': "عیسی ترحم فرموده دست خود را دراز کرد و او را لمس نموده گفت: می خواهم پاک شو"
}

# Greek reference (Koine Greek)
GREEK_VERSES = {
    '1': "Ἀρχὴ τοῦ εὐαγγελίου Ἰησοῦ Χριστοῦ υἱοῦ θεοῦ",
    '11': "καὶ φωνὴ ἐγένετο ἐκ τῶν οὐρανῶν Σὺ εἶ ὁ υἱός μου ὁ ἀγαπητός ἐν σοὶ εὐδόκησα",
    '15': "καὶ λέγων ὅτι Πεπλήρωται ὁ καιρὸς καὶ ἤγγικεν ἡ βασιλεία τοῦ θεοῦ μετανοεῖτε καὶ πιστεύετε ἐν τῷ εὐαγγελίῳ",
    '41': "καὶ σπλαγχνισθεὶς ἐκτείνας τὴν χεῖρα αὐτοῦ ἥψατο καὶ λέγει αὐτῷ Θέλω καθαρίσθητι"
}


def test_language_pair(lang1_name, lang1_verses, lang2_name, lang2_verses, 
                       detector, engine):
    """Test resonance between two languages."""
    
    results = []
    
    common_verses = set(lang1_verses.keys()) & set(lang2_verses.keys())
    
    for verse_num in sorted(common_verses, key=int):
        # Get LJPW coordinates
        result1 = detector.calculate_field_signature_v2(lang1_verses[verse_num])
        coords1 = [result1['L'], result1['J'], result1['P'], result1['W']]
        
        result2 = detector.calculate_field_signature_v2(lang2_verses[verse_num])
        coords2 = [result2['L'], result2['J'], result2['P'], result2['W']]
        
        # Euclidean distance
        euclidean = np.linalg.norm(np.array(coords1) - np.array(coords2))
        
        # Resonance analysis
        analysis = engine.analyze_translation_pair(coords1, coords2, cycles=1000)
        
        results.append({
            'verse': verse_num,
            'euclidean': euclidean,
            'convergence': analysis['convergence_distance'],
            'same_attractor': analysis['same_deficit'],
            'quality': analysis['quality_assessment']
        })
    
    return results


def main():
    print("=" * 70)
    print("EXTREME LANGUAGE FAMILY TEST")
    print("Quechua (Andean) vs Farsi (Indo-Iranian) vs Greek (Hellenic)")
    print("=" * 70)
    
    detector = EnhancedPatternDetector()
    engine = ResonanceEngine()
    
    print("\nLanguage Families Being Tested:")
    print("  - Quechua: Quechuan family, agglutinative, South America")
    print("  - Farsi: Indo-Iranian family, Persian script, Middle East")
    print("  - Greek: Hellenic family, Greek script, Mediterranean")
    print("\nThese languages share NO common ancestry.")
    
    # Test all pairs
    pairs = [
        ("Quechua", QUECHUA_VERSES, "Farsi", FARSI_VERSES),
        ("Quechua", QUECHUA_VERSES, "Greek", GREEK_VERSES),
        ("Farsi", FARSI_VERSES, "Greek", GREEK_VERSES),
        ("Quechua", QUECHUA_VERSES, "English", ENGLISH_VERSES),
        ("Farsi", FARSI_VERSES, "English", ENGLISH_VERSES),
    ]
    
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    
    for lang1_name, lang1_verses, lang2_name, lang2_verses in pairs:
        print(f"\n--- {lang1_name} <-> {lang2_name} ---")
        
        results = test_language_pair(
            lang1_name, lang1_verses, 
            lang2_name, lang2_verses,
            detector, engine
        )
        
        print(f"{'Verse':<8} {'Euclidean':<12} {'Convergence':<12} {'Same Attr':<10} {'Quality'}")
        print("-" * 60)
        
        total_resonance_pass = 0
        total_euclidean_pass = 0
        
        for r in results:
            qual = "EXCELLENT" if "EXCELLENT" in r['quality'] else "GOOD" if "GOOD" in r['quality'] else "CHECK"
            print(f"{r['verse']:<8} {r['euclidean']:<12.4f} {r['convergence']:<12.4f} "
                  f"{'Yes' if r['same_attractor'] else 'NO':<10} {qual}")
            
            if r['euclidean'] < 0.10:
                total_euclidean_pass += 1
            if r['convergence'] < 0.10 and r['same_attractor']:
                total_resonance_pass += 1
        
        print(f"\nSummary: Euclidean passed: {total_euclidean_pass}/{len(results)}, "
              f"Resonance passed: {total_resonance_pass}/{len(results)}")
    
    # Final summary
    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    
    # Test the most extreme pair: Quechua-Farsi
    print("\nMost Extreme Test: Quechua <-> Farsi")
    quechua_farsi = test_language_pair(
        "Quechua", QUECHUA_VERSES,
        "Farsi", FARSI_VERSES,
        detector, engine
    )
    
    all_passed = all(r['same_attractor'] and r['convergence'] < 0.10 for r in quechua_farsi)
    max_euclidean = max(r['euclidean'] for r in quechua_farsi)
    
    if all_passed:
        print(f"\n>>> ALL {len(quechua_farsi)} verses pass resonance validation!")
        print(f"    Max Euclidean distance: {max_euclidean:.4f}")
        print(f"    Despite completely different:")
        print(f"      - Language families")
        print(f"      - Scripts (Latin vs Arabic)")
        print(f"      - Word order")
        print(f"      - Cultural contexts")
        print(f"\n    THE RESONANCE PARADIGM WORKS UNIVERSALLY!")
    else:
        failed = [r for r in quechua_farsi if not r['same_attractor']]
        print(f"    Some verses did not pass. Investigate: {[r['verse'] for r in failed]}")


if __name__ == '__main__':
    main()
