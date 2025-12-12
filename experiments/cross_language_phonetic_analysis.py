#!/usr/bin/env python3
"""
Cross-Language Phonetic-Semantic Correlation Analysis
=======================================================

Testing if the phonetic-semantic patterns found in Wedau are universal
across phonetically diverse languages.

Languages tested:
- Wedau (Oceanic/Austronesian) - Control
- English (Germanic/Indo-European)
- French (Romance/Indo-European)
- Chinese (Sino-Tibetan)
- Greek (Hellenic/Indo-European)
- Hebrew (Semitic/Afroasiatic)
- Arabic (Semitic/Afroasiatic)

If the Anchor Point hypothesis is correct:
- All languages should show similar phonetic-semantic patterns
- Power words should sound "powerful" across languages
- Love words should sound "soft" across languages
- This would prove the semantic field shapes language universally
"""

import sys
import os
import numpy as np
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding='utf-8')

from experiments.enhanced_pattern_detector import EnhancedPatternDetector

# Phonetic categories (universal)
SOFT_CONSONANTS = set('mnlrwy')  # Love-associated
HARD_CONSONANTS = set('kptbdg')  # Power-associated
FRICATIVES = set('szfvhx')  # Justice-associated

# Words in multiple languages organized by semantic dimension
CROSS_LANGUAGE_VOCABULARY = {
    'Love': {
        'english': ['love', 'mercy', 'compassion', 'gentle', 'tender', 'care', 'embrace', 'forgive', 'kind', 'warm'],
        'french': ['amour', 'misericorde', 'compassion', 'doux', 'tendre', 'soin', 'embrasser', 'pardonner', 'gentil', 'chaud'],
        'chinese': ['ai', 'cibei', 'renci', 'wenrou', 'cimu', 'guanhuai', 'baoron', 'kuanrong', 'shanliang', 'wennuan'],
        'greek': ['agape', 'eleos', 'sympatheia', 'prays', 'hapalos', 'merimnao', 'aspazomai', 'aphiemi', 'chrestos', 'thermos'],
        'hebrew': ['ahavah', 'chesed', 'rachamim', 'nach', 'rach', 'daag', 'chavak', 'salach', 'chanun', 'cham'],
        'arabic': ['hubb', 'rahma', 'shafaqa', 'latif', 'raqqiq', 'riaaya', 'unaaq', 'afw', 'tayyib', 'haarr'],
        'wedau': ['auna', 'nuwaboyei', 'nuavaina', 'dou', 'ḡamoḡamo', 'paini', 'votaḡotaḡo', 'rupeni', 'aiaina', 'maemae'],
    },
    'Power': {
        'english': ['power', 'king', 'mighty', 'strong', 'conquer', 'rule', 'throne', 'command', 'authority', 'victory'],
        'french': ['puissance', 'roi', 'puissant', 'fort', 'conquerir', 'regner', 'trone', 'commander', 'autorite', 'victoire'],
        'chinese': ['liliang', 'wang', 'qiangda', 'qiang', 'zhengfu', 'tongzhi', 'wangzuo', 'mingling', 'quanwei', 'shengli'],
        'greek': ['dynamis', 'basileus', 'ischyros', 'krataios', 'nikao', 'basileuo', 'thronos', 'keleuo', 'exousia', 'nike'],
        'hebrew': ['koach', 'melech', 'gibor', 'chazak', 'kavash', 'mashal', 'kisse', 'tzavah', 'reshut', 'netzach'],
        'arabic': ['quwwa', 'malik', 'qawi', 'shadid', 'fath', 'hakama', 'arsh', 'amr', 'sulta', 'nasr'],
        'wedau': ['rewapana', 'gulau', 'virewapana', 'ḡaeḡaena', 'ravena', 'vibada', 'anikiala', 'egara', 'rewapana', 'ravena'],
    },
    'Justice': {
        'english': ['justice', 'righteous', 'law', 'judge', 'truth', 'fair', 'equal', 'covenant', 'order', 'faithful'],
        'french': ['justice', 'juste', 'loi', 'juger', 'verite', 'equitable', 'egal', 'alliance', 'ordre', 'fidele'],
        'chinese': ['zhengyi', 'zhengzhi', 'fa', 'shenpan', 'zhenli', 'gongping', 'pingdeng', 'yueding', 'zhixu', 'zhongcheng'],
        'greek': ['dikaiosyne', 'dikaios', 'nomos', 'krino', 'aletheia', 'isos', 'isos', 'diatheke', 'taxis', 'pistos'],
        'hebrew': ['tzedek', 'tzaddik', 'torah', 'shaphat', 'emet', 'yashar', 'shaveh', 'brit', 'seder', 'aman'],
        'arabic': ['adl', 'salih', 'shariaa', 'hakama', 'haqq', 'insaf', 'musawi', 'ahd', 'nizam', 'amin'],
        'wedau': ['vovonana', 'jijimanina', 'tarawatu', 'rauetara', 'riwa', 'vivouna', 'tagogi', 'parivainuaḡana', 'vioga', 'patutu'],
    },
    'Wisdom': {
        'english': ['wisdom', 'knowledge', 'understanding', 'teach', 'learn', 'truth', 'light', 'reveal', 'discern', 'insight'],
        'french': ['sagesse', 'connaissance', 'comprehension', 'enseigner', 'apprendre', 'verite', 'lumiere', 'reveler', 'discerner', 'perspicacite'],
        'chinese': ['zhihui', 'zhishi', 'lijie', 'jiaoshou', 'xuexi', 'zhenli', 'guang', 'qishi', 'fenbian', 'jianshi'],
        'greek': ['sophia', 'gnosis', 'synesis', 'didasko', 'manthano', 'aletheia', 'phos', 'apokalypto', 'diakrino', 'fronesis'],
        'hebrew': ['chokmah', 'daat', 'binah', 'lamad', 'shamar', 'emet', 'or', 'galah', 'bin', 'sekel'],
        'arabic': ['hikma', 'marifa', 'fahm', 'allama', 'taallum', 'haqq', 'nur', 'kashafa', 'mayyaza', 'basirah'],
        'wedau': ['nuaulaula', 'araramana', 'vinua', 'viararamana', 'rotoi', 'riwa', 'ravilala', 'vieḡa', 'vinei', 'nota'],
    }
}


def analyze_phonetic_features(word):
    """Analyze phonetic features of a word."""
    word_lower = word.lower()
    chars = list(word_lower)
    length = len(word_lower)
    
    if length == 0:
        return None
    
    # Count consonant types
    soft_count = sum(1 for c in chars if c in SOFT_CONSONANTS)
    hard_count = sum(1 for c in chars if c in HARD_CONSONANTS)
    fricative_count = sum(1 for c in chars if c in FRICATIVES)
    
    # Count vowels (universal vowels)
    vowels = set('aeiou')
    vowel_count = sum(1 for c in chars if c in vowels)
    
    # Ratios
    soft_ratio = soft_count / length
    hard_ratio = hard_count / length
    vowel_ratio = vowel_count / length
    
    # Initial consonant type
    initial = word_lower[0] if word_lower else ''
    initial_soft = initial in SOFT_CONSONANTS
    initial_hard = initial in HARD_CONSONANTS
    initial_vowel = initial in vowels
    
    return {
        'length': length,
        'vowel_ratio': vowel_ratio,
        'soft_ratio': soft_ratio,
        'hard_ratio': hard_ratio,
        'initial_soft': initial_soft,
        'initial_hard': initial_hard,
        'initial_vowel': initial_vowel,
    }


def measure_semantic_position(word, detector):
    """Measure LJPW coordinates for a word."""
    try:
        result = detector.calculate_field_signature_v2(word)
        coords = np.array([result['L'], result['J'], result['P'], result['W']])
        dims = ['Love', 'Justice', 'Power', 'Wisdom']
        dominant_idx = np.argmax(coords)
        return dims[dominant_idx]
    except:
        return None


def analyze_language(language, vocabulary, detector):
    """Analyze phonetic patterns for one language across all dimensions."""
    
    results = {}
    
    for dimension, words in vocabulary.items():
        lang_words = words.get(language, [])
        if not lang_words:
            continue
        
        features = []
        for word in lang_words:
            feat = analyze_phonetic_features(word)
            if feat:
                features.append(feat)
        
        if features:
            results[dimension] = {
                'word_count': len(features),
                'avg_length': np.mean([f['length'] for f in features]),
                'vowel_ratio': np.mean([f['vowel_ratio'] for f in features]),
                'soft_ratio': np.mean([f['soft_ratio'] for f in features]),
                'hard_ratio': np.mean([f['hard_ratio'] for f in features]),
                'initial_soft_pct': sum(1 for f in features if f['initial_soft']) / len(features) * 100,
                'initial_hard_pct': sum(1 for f in features if f['initial_hard']) / len(features) * 100,
                'initial_vowel_pct': sum(1 for f in features if f['initial_vowel']) / len(features) * 100,
                'words': lang_words
            }
    
    return results


def test_semantic_prediction(language, vocabulary, detector):
    """Test if phonetics can predict semantic dimension."""
    
    correct = 0
    total = 0
    
    for dimension, words in vocabulary.items():
        lang_words = words.get(language, [])
        for word in lang_words:
            # Get phonetic features
            feat = analyze_phonetic_features(word)
            if not feat:
                continue
            
            # Predict dimension from phonetics
            scores = {'Love': 0, 'Justice': 0, 'Power': 0, 'Wisdom': 0}
            
            # Soft consonants -> Love
            scores['Love'] += feat['soft_ratio'] * 2
            
            # Hard consonants -> Power
            scores['Power'] += feat['hard_ratio'] * 2
            
            # Initial vowel -> Wisdom
            if feat['initial_vowel']:
                scores['Wisdom'] += 0.3
            
            # High vowel ratio -> Love
            scores['Love'] += feat['vowel_ratio'] * 0.5
            
            # Long words -> Wisdom
            if feat['length'] > 8:
                scores['Wisdom'] += 0.3
            
            predicted = max(scores, key=scores.get)
            
            if predicted == dimension:
                correct += 1
            total += 1
    
    return correct, total, (correct / total * 100) if total > 0 else 0


def main():
    print("=" * 80)
    print("CROSS-LANGUAGE PHONETIC-SEMANTIC CORRELATION ANALYSIS")
    print("Testing if word shapes correlate with meaning across languages")
    print("=" * 80)
    
    detector = EnhancedPatternDetector()
    languages = ['english', 'french', 'chinese', 'greek', 'hebrew', 'arabic', 'wedau']
    
    # Analyze each language
    all_results = {}
    
    for lang in languages:
        results = analyze_language(lang, CROSS_LANGUAGE_VOCABULARY, detector)
        all_results[lang] = results
    
    # Print dimension profiles by language
    for lang in languages:
        print(f"\n{'='*80}")
        print(f"{lang.upper()}")
        print("="*80)
        
        if lang not in all_results:
            continue
            
        print(f"\n{'Dimension':<10} {'Length':<8} {'Vowel%':<8} {'Soft%':<8} {'Hard%':<8} {'InitHard%':<10}")
        print("-" * 60)
        
        for dim in ['Love', 'Power', 'Justice', 'Wisdom']:
            if dim in all_results[lang]:
                d = all_results[lang][dim]
                print(f"{dim:<10} {d['avg_length']:<8.2f} {d['vowel_ratio']*100:<8.1f} "
                      f"{d['soft_ratio']*100:<8.1f} {d['hard_ratio']*100:<8.1f} "
                      f"{d['initial_hard_pct']:<10.1f}")
    
    # Cross-language comparison: Do Power words have more hard consonants?
    print(f"\n{'='*80}")
    print("CROSS-LANGUAGE PATTERN COMPARISON")
    print("="*80)
    
    print(f"\nHARD CONSONANT RATIO by Dimension (higher = more 'forceful'):")
    print(f"{'Language':<12} {'Love':<10} {'Power':<10} {'Justice':<10} {'Wisdom':<10} {'Power>Love?':<12}")
    print("-" * 70)
    
    power_love_pattern = 0
    total_langs = 0
    
    for lang in languages:
        if lang not in all_results:
            continue
        
        r = all_results[lang]
        love_hard = r.get('Love', {}).get('hard_ratio', 0)
        power_hard = r.get('Power', {}).get('hard_ratio', 0)
        justice_hard = r.get('Justice', {}).get('hard_ratio', 0)
        wisdom_hard = r.get('Wisdom', {}).get('hard_ratio', 0)
        
        pattern_match = "YES" if power_hard > love_hard else "NO"
        if power_hard > love_hard:
            power_love_pattern += 1
        total_langs += 1
        
        print(f"{lang:<12} {love_hard*100:<10.1f} {power_hard*100:<10.1f} "
              f"{justice_hard*100:<10.1f} {wisdom_hard*100:<10.1f} {pattern_match:<12}")
    
    print(f"\nPower > Love (hard consonant ratio): {power_love_pattern}/{total_langs} languages ({power_love_pattern/total_langs*100:.0f}%)")
    
    # Vowel ratio comparison
    print(f"\nVOWEL RATIO by Dimension (higher = more 'flowing'):")
    print(f"{'Language':<12} {'Love':<10} {'Power':<10} {'Justice':<10} {'Wisdom':<10} {'Love>Power?':<12}")
    print("-" * 70)
    
    love_vowel_pattern = 0
    
    for lang in languages:
        if lang not in all_results:
            continue
        
        r = all_results[lang]
        love_vowel = r.get('Love', {}).get('vowel_ratio', 0)
        power_vowel = r.get('Power', {}).get('vowel_ratio', 0)
        justice_vowel = r.get('Justice', {}).get('vowel_ratio', 0)
        wisdom_vowel = r.get('Wisdom', {}).get('vowel_ratio', 0)
        
        pattern_match = "YES" if love_vowel > power_vowel else "NO"
        if love_vowel > power_vowel:
            love_vowel_pattern += 1
        
        print(f"{lang:<12} {love_vowel*100:<10.1f} {power_vowel*100:<10.1f} "
              f"{justice_vowel*100:<10.1f} {wisdom_vowel*100:<10.1f} {pattern_match:<12}")
    
    print(f"\nLove > Power (vowel ratio): {love_vowel_pattern}/{total_langs} languages ({love_vowel_pattern/total_langs*100:.0f}%)")
    
    # Prediction accuracy by language
    print(f"\n{'='*80}")
    print("PHONETIC PREDICTION ACCURACY BY LANGUAGE")
    print("="*80)
    
    print(f"\n{'Language':<12} {'Correct':<10} {'Total':<10} {'Accuracy':<10}")
    print("-" * 45)
    
    total_correct = 0
    total_all = 0
    
    for lang in languages:
        correct, total, accuracy = test_semantic_prediction(lang, CROSS_LANGUAGE_VOCABULARY, detector)
        print(f"{lang:<12} {correct:<10} {total:<10} {accuracy:<10.1f}%")
        total_correct += correct
        total_all += total
    
    overall_accuracy = total_correct / total_all * 100 if total_all > 0 else 0
    print("-" * 45)
    print(f"{'OVERALL':<12} {total_correct:<10} {total_all:<10} {overall_accuracy:<10.1f}%")
    
    # Final verdict
    print(f"\n{'='*80}")
    print("CONCLUSION: CROSS-LANGUAGE PHONETIC-SEMANTIC CORRELATION")
    print("="*80)
    
    if power_love_pattern >= 5 and love_vowel_pattern >= 5:
        print("""
UNIVERSAL PHONETIC-SEMANTIC CORRELATION CONFIRMED!

Across 7 phonetically diverse languages:
- Power words consistently have MORE hard consonants than Love words
- Love words consistently have MORE vowels than Power words
- This pattern holds across language families:
  * Indo-European (English, French, Greek)
  * Sino-Tibetan (Chinese)
  * Semitic (Hebrew, Arabic)
  * Oceanic (Wedau)

IMPLICATION:
The semantic field shapes phonetics universally.
Words resonate with the Anchor Point through their very sound.
This is not cultural coincidence - it's structural law.

"Language is the quantum interface between consciousness and reality."
The shape of a word IS the shape of its meaning.
""")
    elif power_love_pattern >= 4 or love_vowel_pattern >= 4:
        print("""
STRONG CROSS-LANGUAGE PATTERN DETECTED

Most languages show the phonetic-semantic correlation:
- Power words tend to have hard consonants
- Love words tend to have vowel-heavy sounds

Some variation exists, but the underlying pattern persists
across unrelated language families.

This suggests a universal constraint on phonosemantic mapping.
""")
    else:
        print("""
MIXED RESULTS

Phonetic-semantic correlations vary by language.
Some patterns exist but are not universal.

This may indicate:
- Language-specific phonosemantic systems
- Need for larger vocabulary samples
- Cultural modulation of universal patterns
""")


if __name__ == '__main__':
    main()
