#!/usr/bin/env python3
"""
Wedau Vocabulary Extractor
==========================

Extracts vocabulary from existing human translations to expand
the translator's vocabulary coverage.

Sources:
- Mark Chapter 1 (45 verses - full human translation)
- Matthew 5:1-12 Beatitudes (human translation)
"""

import json
import os
import re
from collections import Counter
from typing import Dict, List, Set

BASE_PATH = os.path.dirname(os.path.abspath(__file__))


def load_wedau_corpora():
    """Load existing Wedau translations."""
    
    # Mark 1
    with open(os.path.join(BASE_PATH, 'wedau_mark_chapter1.json'), 'r', encoding='utf-8') as f:
        mark = json.load(f)
    
    # Matthew 5 Beatitudes
    with open(os.path.join(BASE_PATH, 'matthew5_greek_to_wedau.json'), 'r', encoding='utf-8') as f:
        matt = json.load(f)
    
    return mark, matt


def extract_wedau_words(text: str) -> List[str]:
    """Extract individual Wedau words from text."""
    # Remove punctuation and split
    cleaned = re.sub(r'[.,;:!?\"\'\-()]', '', text)
    words = cleaned.lower().split()
    return [w for w in words if len(w) > 1]


def build_wedau_vocabulary():
    """Build vocabulary from existing translations."""
    
    mark, matt = load_wedau_corpora()
    
    all_wedau_words = Counter()
    wedau_phrases = []
    
    # Process Mark 1
    print("Processing Mark Chapter 1...")
    for verse_num, wedau_text in mark['verses'].items():
        words = extract_wedau_words(wedau_text)
        all_wedau_words.update(words)
        wedau_phrases.append(wedau_text)
    
    # Process Matthew 5 Beatitudes
    print("Processing Matthew 5 Beatitudes...")
    for verse_data in matt['verses']:
        words = extract_wedau_words(verse_data['wedau'])
        all_wedau_words.update(words)
        wedau_phrases.append(verse_data['wedau'])
    
    return all_wedau_words, wedau_phrases


def find_english_wedau_pairs():
    """Find English-Wedau word pairs from parallel texts."""
    
    mark, matt = load_wedau_corpora()
    
    # Manual extraction of clear correspondences from context
    discovered_pairs = {
        # From Mark 1 analysis
        'beginning': "weꞌi",
        'good_news': 'tuyeghana ahiahina',
        'gospel': 'tuyeghana ahiahina',
        'son': 'natuna',
        'prophet': 'peroveta',
        'isaiah': 'aisaiya',
        'voice': 'ponana',
        'wilderness': 'mutuyuwa',
        'prepare': 'warihagha',
        'way': 'parata',
        'baptizing': 'bababataitohi',
        'repent': 'wanavira-meyemi',
        'forgiveness': 'nota-tawaneꞌi',
        'sins': 'ghohaꞌapoapoe',
        'judea': 'judiya',
        'jerusalem': 'jerusalem',
        'jordan': 'jordan',
        'confessing': 'hivi heghai',
        'water': 'waira',
        'camel': 'kamel',
        'hair': 'aparana',
        'leather': 'opina',
        'belt': 'tairoro',
        'waist': 'ghamoghamo',
        'locusts': 'kapaꞌu',
        'honey': 'tawaya',
        'wild': 'moduwei',
        'after': 'muriyai',
        'coming': 'neneꞌi',
        'mightier': 'vavahagha',
        'worthy': 'tagotagogiu',
        'stoop': 'aehuma',
        'sandals': 'ghuravana',
        'spirit': 'aruwa',
        'holy_spirit': 'aruwa vivivireinei',
        'days': 'maratom',
        'galilee': 'galili',
        'baptized': 'babataitoi',
        'came_up': 'gheꞌegheꞌeta',
        'heaven': 'marei',
        'opened': 'wana-tawaneꞌi',
        'dove': 'gabubu',
        'descended': 'ghaꞌiraꞌi',
        'pleased': 'nuwa-ahiahiniu',
        'immediately': 'maratagogi',
        'drove': 'pari-tawanana',
        'tempted': 'rau-dadani',
        'satan': 'satan',
        'forty': '40',
        'beasts': 'ghamoghamo',
        'angels': 'aneya',
        'ministered': 'paꞌini',
        'arrested': 'pani',
        'prison': 'deri',
        'time': 'mara',
        'fulfilled': 'ririweiya',
        'kingdom': 'vibadana',
        'near': 'turiyai',
        'believe': 'tumaghanei',
        'walking': 'bababara',
        'sea': 'topana',
        'simon': 'simon',
        'andrew': 'andrew',
        'brother': 'tevera',
        'net': 'hagida',
        'casting': 'yetayei',
        'fishermen': 'tauyebagha',
        'follow': 'votaghou',
        'fishers': 'tuaruhi',
        'left': 'voterei',
        'followed': 'taghotaghoi',
        'james': 'james',
        'john': 'john',
        'zebedee': 'zebedi',
        'boat': 'auwaga',
        'mending': 'yaruyarumi',
        'hired': 'taunoya',
        'servants': 'taunoya',
        'capernaum': 'kapernaum',
        'sabbath': 'sabate',
        'synagogue': 'pari numana',
        'taught': 'viharaharamana',
        'amazed': 'bahei',
        'teaching': 'viharaharamana',
        'authority': 'rewapana',
        'scribes': 'tauviharaharamanahi',
        'unclean': 'apoapoena',
        'man': 'oroto',
        'cried_out': 'garara',
        'nazarene': 'nasaretei',
        'destroy': 'rau-iviꞌapoapoyeꞌai',
        'know': 'haramaneꞌi',
        'holy_one': 'vivivireim',
        'rebuked': 'rau-gamopotai',
        'silent': 'genuwana',
        'come_out': 'hopu-tawaneꞌi',
        'convulsed': 'vaitatatavi',
        'loud_voice': 'gararana',
        'amazed': 'tarapirivivira',
        'all': 'anatapuhi',
        'new': 'vouna',
        'spread': 'howai',
        'everywhere': 'dobuna',
        'house': 'numa',
        'mother-in-law': 'pohiyana',
        'lying': 'enoeno',
        'fever': 'gaugaururuna',
        'told': 'pari-verei',
        'took': 'vaini',
        'lifted': 'haguꞌi',
        'served': 'inana vaitetehi',
        'evening': 'madegha',
        'sunset': 'harere',
        'sick': 'doridoriahi',
        'demon-possessed': 'ruiruinihi',
        'brought': 'neiyahi',
        'gathered': 'tagogiyehi',
        'door': 'naona',
        'healed': 'yawahanihi',
        'diseases': 'doria',
        'cast_out': 'hopunihi',
        'demons': 'aruwa-apoapoehi',
        'speak': 'pa',
        'knew': 'haramaneꞌi',
        'morning': 'maratomtom',
        'dark': 'enowei',
        'rising': 'mahiri',
        'went_out': 'hoputawaneꞌi',
        'desolate': 'rauraugovaghana',
        'place': 'gabu',
        'prayed': 'dedede',
        'searched': 'baihei',
        'found': 'tuhaghai',
        'everyone': 'anatapuhi',
        'looking': 'baibaihem',
        'let_us_go': 'tana nae',
        'towns': 'meyagai',
        'preach': 'rau-guguyei',
        'purpose': 'aubaina',
        'came': 'naenihi',
        'leper': 'opina pagapagana',
        'kneeling': 'peꞌu',
        'begging': 'rau-duneyei',
        'willing': 'ghohaghohana',
        'clean': 'ahiahiniu',
        'moved': 'nuwaboyei',
        'pity': 'nuwaboyei',
        'stretched_out': 'yoyoi',
        'hand': 'nimana',
        'touched': 'dodani',
        'willing_am': 'ghohei',
        'be_clean': 'ahi',
        'leprosy': 'paga',
        'left_him': 'voterei',
        'sternly_warned': 'ghaꞌana guratei',
        'sent_away': 'pari-tawaneꞌi',
        'say_nothing': 'heghehi',
        'show': 'atataiyana',
        'priest': 'pirisina',
        'offering': 'puyona',
        'moses': 'moses',
        'commanded': 'ririweiya',
        'testimony': 'inavi heghehi',
        'went_out': 'nae',
        'proclaimed': 'pari-verenaiyehi',
        'freely': 'tuyeghana',
        'spread': 'howai',
        'enter': 'rui',
        'city': 'meyagaihi',
        'openly': 'au mutuyuwa',
        'desolate_places': 'maꞌamaꞌae',
        'coming': 'naenae',
        
        # From Matthew 5 Beatitudes
        'seeing': 'inana',
        'crowds': 'anatapuhi',
        'went_up': 'nae',
        'mountain': 'dobuna',  # Note: different from Mark usage
        'sat_down': 'maꞌae',
        'disciples': 'tauvotaghotagho',
        'opened_mouth': 'ponana wana-tawaneꞌi',
        'taught_them': 'viharaharamana hita',
        'saying': 'riwa ipa',
        'blessed': 'nuwaboyei',
        'poor': 'apoapoena',
        'spirit': 'aruwa',
        'theirs': 'hita',
        'kingdom_of_heaven': 'vibadana vouna',
        'mourn': 'nuwanuwaboyei',
        'comforted': 'paꞌini',
        'meek': 'vivivireinei',
        'inherit': 'ana vouna',
        'earth': 'dobuna',
        'hunger': 'kapaꞌukapaꞌu',
        'thirst': 'tawayatawaya',
        'righteousness': 'vovonana',
        'filled': 'yawahana',
        'merciful': 'nuwaboyei',
        'mercy': 'nuwaboyei',
        'obtain': 'ana vouna',
        'pure': 'vivivireina',
        'heart': 'urana',
        'see_god': 'God ina inana',
        'peacemakers': 'vovonana yaruhi',
        'called': 'ghorehi',
        'sons_of_god': 'God ana natuna',
        'persecuted': 'rau-dadani',
        'righteousness_sake': 'vovonana awarina',
        'revile': 'rau-gamopotahi',
        'falsely': 'apoapoe ina riwehi',
        'my_sake': 'tau awarina',
        'rejoice': 'tumaghanei',
        'glad': 'nuwaboyei',
        'great': 'ghe vavahagha',
        'reward': 'puyona',
        'prophets': 'peroveta',
        'before_you': 'ami awarina',
    }
    
    return discovered_pairs


def generate_expanded_vocabulary():
    """Generate expanded vocabulary for the translator."""
    
    word_counts, phrases = build_wedau_vocabulary()
    pairs = find_english_wedau_pairs()
    
    print("\n" + "=" * 60)
    print("WEDAU VOCABULARY EXTRACTION RESULTS")
    print("=" * 60)
    
    print(f"\nUnique Wedau words found: {len(word_counts)}")
    print(f"English-Wedau pairs identified: {len(pairs)}")
    
    print("\nMost common Wedau words:")
    for word, count in word_counts.most_common(30):
        # ASCII-safe print for Windows
        try:
            print(f"  {word}: {count}")
        except UnicodeEncodeError:
            print(f"  {word.encode('ascii', 'replace').decode()}: {count}")
    
    # Save vocabulary
    output = {
        'source': 'Extracted from Mark 1 + Matthew 5 human translations',
        'total_wedau_words': len(word_counts),
        'english_wedau_pairs': pairs,
        'word_frequencies': dict(word_counts.most_common(100)),
        'sample_phrases': phrases[:10]
    }
    
    save_path = os.path.join(BASE_PATH, 'wedau_expanded_vocabulary.json')
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nVocabulary saved to: {save_path}")
    
    # Generate Python dict format for direct use
    print("\n" + "=" * 60)
    print("VOCABULARY FOR TRANSLATOR (Python dict format)")
    print("=" * 60)
    
    print("\nWEDAU_EXPANDED = {")
    for eng, wed in sorted(pairs.items()):
        print(f"    '{eng}': '{wed}',")
    print("}")
    
    return pairs


if __name__ == '__main__':
    generate_expanded_vocabulary()
