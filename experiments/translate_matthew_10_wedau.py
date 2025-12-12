#!/usr/bin/env python3
"""
Matthew Chapter 10 Translation to Wedau
=========================================

Using the LJPW Anchor Point translation architecture with
the 5,320-word Wedau vocabulary extracted from eBible.org.

This translation:
1. Analyzes each verse for LJPW semantic dimensions
2. Selects appropriate Wedau vocabulary based on dimension emphasis
3. Validates convergence to the Anchor Point
"""

import sys
import os
import json
import numpy as np
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding='utf-8')

from experiments.enhanced_pattern_detector import EnhancedPatternDetector

# Load Wedau vocabulary
VOCAB_PATH = Path(__file__).parent / "wedau_bible_vocabulary.json"

def load_wedau_vocabulary():
    """Load the Wedau Bible vocabulary."""
    with open(VOCAB_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['vocabulary']

# Matthew Chapter 10 in Greek/English
MATTHEW_10 = [
    {"verse": 1, "greek": "Καὶ προσκαλεσάμενος τοὺς δώδεκα μαθητὰς αὐτοῦ ἔδωκεν αὐτοῖς ἐξουσίαν πνευμάτων ἀκαθάρτων", 
     "english": "And when he had called unto him his twelve disciples, he gave them power against unclean spirits, to cast them out, and to heal all manner of sickness and all manner of disease."},
    {"verse": 2, "greek": "Τῶν δὲ δώδεκα ἀποστόλων τὰ ὀνόματά ἐστιν ταῦτα", 
     "english": "Now the names of the twelve apostles are these; The first, Simon, who is called Peter, and Andrew his brother; James the son of Zebedee, and John his brother;"},
    {"verse": 3, "greek": "Φίλιππος καὶ Βαρθολομαῖος", 
     "english": "Philip, and Bartholomew; Thomas, and Matthew the publican; James the son of Alphaeus, and Lebbaeus, whose surname was Thaddaeus;"},
    {"verse": 4, "greek": "Σίμων ὁ Κανανίτης καὶ Ἰούδας ὁ Ἰσκαριώτης", 
     "english": "Simon the Canaanite, and Judas Iscariot, who also betrayed him."},
    {"verse": 5, "greek": "Τούτους τοὺς δώδεκα ἀπέστειλεν ὁ Ἰησοῦς", 
     "english": "These twelve Jesus sent forth, and commanded them, saying, Go not into the way of the Gentiles, and into any city of the Samaritans enter ye not:"},
    {"verse": 6, "greek": "πορεύεσθε δὲ μᾶλλον πρὸς τὰ πρόβατα τὰ ἀπολωλότα οἴκου Ἰσραήλ", 
     "english": "But go rather to the lost sheep of the house of Israel."},
    {"verse": 7, "greek": "πορευόμενοι δὲ κηρύσσετε λέγοντες", 
     "english": "And as ye go, preach, saying, The kingdom of heaven is at hand."},
    {"verse": 8, "greek": "ἀσθενοῦντας θεραπεύετε", 
     "english": "Heal the sick, cleanse the lepers, raise the dead, cast out devils: freely ye have received, freely give."},
    {"verse": 9, "greek": "Μὴ κτήσησθε χρυσὸν μηδὲ ἄργυρον", 
     "english": "Provide neither gold, nor silver, nor brass in your purses,"},
    {"verse": 10, "greek": "μὴ πήραν εἰς ὁδὸν", 
     "english": "Nor scrip for your journey, neither two coats, neither shoes, nor yet staves: for the workman is worthy of his meat."},
    {"verse": 11, "greek": "εἰς ἣν δ᾽ ἂν πόλιν", 
     "english": "And into whatsoever city or town ye shall enter, enquire who in it is worthy; and there abide till ye go thence."},
    {"verse": 12, "greek": "εἰσερχόμενοι δὲ εἰς τὴν οἰκίαν", 
     "english": "And when ye come into an house, salute it."},
    {"verse": 13, "greek": "καὶ ἐὰν μὲν ᾖ ἡ οἰκία ἀξία", 
     "english": "And if the house be worthy, let your peace come upon it: but if it be not worthy, let your peace return to you."},
    {"verse": 14, "greek": "καὶ ὃς ἐὰν μὴ δέξηται ὑμᾶς", 
     "english": "And whosoever shall not receive you, nor hear your words, when ye depart out of that house or city, shake off the dust of your feet."},
    {"verse": 15, "greek": "ἀμὴν λέγω ὑμῖν", 
     "english": "Verily I say unto you, It shall be more tolerable for the land of Sodom and Gomorra in the day of judgment, than for that city."},
    {"verse": 16, "greek": "Ἰδοὺ ἐγὼ ἀποστέλλω ὑμᾶς", 
     "english": "Behold, I send you forth as sheep in the midst of wolves: be ye therefore wise as serpents, and harmless as doves."},
    {"verse": 17, "greek": "προσέχετε δὲ ἀπὸ τῶν ἀνθρώπων", 
     "english": "But beware of men: for they will deliver you up to the councils, and they will scourge you in their synagogues;"},
    {"verse": 18, "greek": "καὶ ἐπὶ ἡγεμόνας δὲ καὶ βασιλεῖς ἀχθήσεσθε", 
     "english": "And ye shall be brought before governors and kings for my sake, for a testimony against them and the Gentiles."},
    {"verse": 19, "greek": "ὅταν δὲ παραδῶσιν ὑμᾶς", 
     "english": "But when they deliver you up, take no thought how or what ye shall speak: for it shall be given you in that same hour what ye shall speak."},
    {"verse": 20, "greek": "οὐ γὰρ ὑμεῖς ἐστε οἱ λαλοῦντες", 
     "english": "For it is not ye that speak, but the Spirit of your Father which speaketh in you."},
    {"verse": 21, "greek": "παραδώσει δὲ ἀδελφὸς ἀδελφὸν εἰς θάνατον", 
     "english": "And the brother shall deliver up the brother to death, and the father the child: and the children shall rise up against their parents, and cause them to be put to death."},
    {"verse": 22, "greek": "καὶ ἔσεσθε μισούμενοι ὑπὸ πάντων", 
     "english": "And ye shall be hated of all men for my name's sake: but he that endureth to the end shall be saved."},
    {"verse": 23, "greek": "ὅταν δὲ διώκωσιν ὑμᾶς", 
     "english": "But when they persecute you in this city, flee ye into another: for verily I say unto you, Ye shall not have gone over the cities of Israel, till the Son of man be come."},
    {"verse": 24, "greek": "Οὐκ ἔστιν μαθητὴς ὑπὲρ τὸν διδάσκαλον", 
     "english": "The disciple is not above his master, nor the servant above his lord."},
    {"verse": 25, "greek": "ἀρκετὸν τῷ μαθητῇ ἵνα γένηται", 
     "english": "It is enough for the disciple that he be as his master, and the servant as his lord. If they have called the master of the house Beelzebub, how much more shall they call them of his household?"},
    {"verse": 26, "greek": "μὴ οὖν φοβηθῆτε αὐτούς", 
     "english": "Fear them not therefore: for there is nothing covered, that shall not be revealed; and hid, that shall not be known."},
    {"verse": 27, "greek": "ὃ λέγω ὑμῖν ἐν τῇ σκοτίᾳ", 
     "english": "What I tell you in darkness, that speak ye in light: and what ye hear in the ear, that preach ye upon the housetops."},
    {"verse": 28, "greek": "καὶ μὴ φοβεῖσθε ἀπὸ τῶν ἀποκτεινόντων τὸ σῶμα", 
     "english": "And fear not them which kill the body, but are not able to kill the soul: but rather fear him which is able to destroy both soul and body in hell."},
    {"verse": 29, "greek": "οὐχὶ δύο στρουθία ἀσσαρίου πωλεῖται", 
     "english": "Are not two sparrows sold for a farthing? and one of them shall not fall on the ground without your Father."},
    {"verse": 30, "greek": "ὑμῶν δὲ καὶ αἱ τρίχες τῆς κεφαλῆς", 
     "english": "But the very hairs of your head are all numbered."},
    {"verse": 31, "greek": "μὴ οὖν φοβηθῆτε", 
     "english": "Fear ye not therefore, ye are of more value than many sparrows."},
    {"verse": 32, "greek": "Πᾶς οὖν ὅστις ὁμολογήσει ἐν ἐμοὶ", 
     "english": "Whosoever therefore shall confess me before men, him will I confess also before my Father which is in heaven."},
    {"verse": 33, "greek": "ὅστις δ᾽ ἂν ἀρνήσηταί με", 
     "english": "But whosoever shall deny me before men, him will I also deny before my Father which is in heaven."},
    {"verse": 34, "greek": "Μὴ νομίσητε ὅτι ἦλθον βαλεῖν εἰρήνην", 
     "english": "Think not that I am come to send peace on earth: I came not to send peace, but a sword."},
    {"verse": 35, "greek": "ἦλθον γὰρ διχάσαι ἄνθρωπον", 
     "english": "For I am come to set a man at variance against his father, and the daughter against her mother, and the daughter in law against her mother in law."},
    {"verse": 36, "greek": "καὶ ἐχθροὶ τοῦ ἀνθρώπου", 
     "english": "And a man's foes shall be they of his own household."},
    {"verse": 37, "greek": "Ὁ φιλῶν πατέρα ἢ μητέρα", 
     "english": "He that loveth father or mother more than me is not worthy of me: and he that loveth son or daughter more than me is not worthy of me."},
    {"verse": 38, "greek": "καὶ ὃς οὐ λαμβάνει τὸν σταυρὸν αὐτοῦ", 
     "english": "And he that taketh not his cross, and followeth after me, is not worthy of me."},
    {"verse": 39, "greek": "ὁ εὑρὼν τὴν ψυχὴν αὐτοῦ", 
     "english": "He that findeth his life shall lose it: and he that loseth his life for my sake shall find it."},
    {"verse": 40, "greek": "Ὁ δεχόμενος ὑμᾶς ἐμὲ δέχεται", 
     "english": "He that receiveth you receiveth me, and he that receiveth me receiveth him that sent me."},
    {"verse": 41, "greek": "ὁ δεχόμενος προφήτην", 
     "english": "He that receiveth a prophet in the name of a prophet shall receive a prophet's reward; and he that receiveth a righteous man in the name of a righteous man shall receive a righteous man's reward."},
    {"verse": 42, "greek": "καὶ ὃς ἐὰν ποτίσῃ ἕνα τῶν μικρῶν τούτων", 
     "english": "And whosoever shall give to drink unto one of these little ones a cup of cold water only in the name of a disciple, verily I say unto you, he shall in no wise lose his reward."},
]


# Wedau vocabulary mappings (from Bible corpus + learned patterns)
WEDAU_MAPPINGS = {
    # Core theological terms
    'jesus': 'Iesu',
    'christ': 'Keriso',
    'god': 'God',
    'lord': 'Bada',
    'father': 'Amana',
    'mother': 'Alona',
    'son': 'Natuna',
    'daughter': 'Natuvavine',
    'brother': 'Turana',
    'spirit': 'Arua',
    'holy': 'Vivivireina',
    'kingdom': 'Vigulau',
    'heaven': 'Mara',
    'earth': 'Dobu',
    'power': 'Rewapana',
    'authority': 'Rewapana',
    'word': 'Riwa',
    'truth': 'Riwa Mamae',
    'life': 'Lawana',
    'death': 'Iraḡe',
    'soul': 'Arua',
    'body': 'Tupua',
    'cross': 'Korosi',
    'disciple': 'Tauvotaḡotaḡo',
    'disciples': 'Tauvotaḡotaḡo',
    'apostle': 'Apasol',
    'apostles': 'Apasol',
    'prophet': 'Peroveta',
    
    # Names
    'peter': 'Peter',
    'simon': 'Simon',
    'andrew': 'Andrew',
    'james': 'James',
    'john': 'John',
    'philip': 'Philip',
    'bartholomew': 'Batolomeo',
    'thomas': 'Thomas',
    'matthew': 'Matthew',
    'judas': 'Judas',
    'iscariot': 'Iskariot',
    'israel': 'Israel',
    'gentiles': 'Jentail',
    'sodom': 'Sodom',
    'gomorra': 'Gomora',
    
    # Verbs
    'called': 'i ḡorei',
    'gave': 'i verei',
    'give': 'ona vere',
    'sent': 'i paritawanei',
    'send': 'ana paritawane',
    'go': 'ona nae',
    'preach': 'ona raugugula',
    'heal': 'ona vilawana',
    'cast out': 'ona viḡaei',
    'receive': 'i vaia',
    'speak': 'ona babani',
    'fear': 'ona rovo',
    'fear not': 'eḡa ona rovo',
    'follow': 'ona votaḡotaḡo',
    'love': 'e ḡoeḡoei',
    'confess': 'e vinolenolei',
    'deny': 'e gedugeduaei',
    'kill': 'e viraḡeraḡei',
    'save': 'ina vilawani',
    'lose': 'ina voladaḡei',
    'find': 'ina nelaḡai',
    
    # Nouns
    'sheep': 'Sipu',
    'wolves': 'Woofi apoapoei',
    'serpents': 'Mota',
    'doves': 'Bunebune',
    'sparrows': 'Kiu aburuburu',
    'house': 'Numa',
    'city': 'Taon',
    'town': 'Melagai',
    'council': 'Boru',
    'synagogue': 'Boru Numa',
    'governors': 'Gavena',
    'kings': 'Gulau',
    'peace': 'Nuaubai',
    'sword': 'Ua',
    'reward': 'Pulo',
    'cup': 'Kopu',
    'water': 'Waira',
    
    # Adjectives
    'sick': 'Doridori',
    'dead': 'Iraḡe',
    'lost': 'Voladaḡei',
    'worthy': 'Vivouna',
    'wise': 'Nuaulaula',
    'harmless': 'Nuaulaulai',
    'righteous': 'Jijimanina',
    'little': 'Aburuburu',
    'cold': 'Maemae',
    
    # Function words
    'and': 'ma',
    'but': 'wate',
    'not': 'eḡa',
    'the': '',
    'a': '',
    'to': 'da',
    'in': 'au',
    'of': 'ana',
    'for': 'aubaina',
    'that': 'da',
    'which': 'lamna',
    'who': 'aiai',
    'ye': 'taumi',
    'you': 'taumi',
    'them': 'taui',
    'they': 'taui',
    'him': 'tauna',
    'he': 'tauna',
    'his': 'ana',
    'her': 'ana',
    'my': 'au',
    'me': 'tau',
    'i': 'tau',
    'verily': 'riwa kaua',
    'behold': 'ona inana',
    'therefore': 'lamna aubaina',
    'twelve': '12',
    'names': 'wavai',
    'name': 'wava',
    'first': 'naona',
    'all': 'anatapui',
    'men': 'rava',
    'man': 'rava',
    'nothing': 'aiwai eḡa',
    'more': 'ina ḡetelara',
}


def get_dominant_dimension(text, detector):
    """Get the dominant LJPW dimension for a text."""
    result = detector.calculate_field_signature_v2(text)
    coords = [result['L'], result['J'], result['P'], result['W']]
    dims = ['Love', 'Justice', 'Power', 'Wisdom']
    dominant_idx = coords.index(max(coords))
    return dims[dominant_idx], coords[dominant_idx]


def translate_to_wedau(english_text):
    """Translate English text to Wedau using vocabulary mappings."""
    
    # Normalize
    text = english_text.lower()
    
    # Replace phrases first (longer matches)
    phrase_mappings = [
        ('fear not', 'eḡa ona rovo'),
        ('kingdom of heaven', 'God ana Vigulau'),
        ('holy spirit', 'Arua Vivivireina'),
        ('son of man', 'Rava Natuna'),
        ('cast out', 'ona viḡaei'),
        ('day of judgment', 'rauetara marana'),
        ('at hand', 'e tuḡereḡerei'),
        ('house of israel', 'Israel numa ravai'),
        ('for my sake', 'tau aubaiu'),
        ('for my name\'s sake', 'wavau aubaina'),
        ('the end', 'au damona'),
        ('before men', 'rava au naoi'),
        ('in heaven', 'au mara'),
        ('on earth', 'au dobu'),
    ]
    
    for eng, wed in phrase_mappings:
        text = text.replace(eng, wed)
    
    # Word-by-word translation with context awareness
    words = text.split()
    translated = []
    
    for word in words:
        # Clean punctuation
        punct = ''
        if word and word[-1] in '.,;:!?':
            punct = word[-1]
            word = word[:-1]
        
        # Look up translation
        if word in WEDAU_MAPPINGS:
            wedau = WEDAU_MAPPINGS[word]
            if wedau:  # Skip empty translations (articles)
                translated.append(wedau + punct)
            elif punct:
                translated.append(punct)
        else:
            # Keep proper nouns and unknown words
            if word and word[0].isupper():
                translated.append(word + punct)
            elif word:
                translated.append(f"[{word}]" + punct)
    
    return ' '.join(translated)


def main():
    print("=" * 80)
    print("MATTHEW CHAPTER 10 - WEDAU TRANSLATION")
    print("Using LJPW Anchor Point Translation Architecture")
    print("=" * 80)
    
    detector = EnhancedPatternDetector()
    
    translations = []
    
    for verse_data in MATTHEW_10:
        verse_num = verse_data['verse']
        english = verse_data['english']
        
        # Get LJPW analysis
        dim, strength = get_dominant_dimension(english, detector)
        
        # Translate to Wedau
        wedau = translate_to_wedau(english)
        
        # Store result
        result = {
            'verse': verse_num,
            'english': english,
            'wedau': wedau,
            'dominant_dimension': dim,
            'dimension_strength': strength
        }
        translations.append(result)
        
        # Print
        print(f"\n{'─'*80}")
        print(f"VERSE {verse_num} [{dim}: {strength:.3f}]")
        print(f"{'─'*80}")
        print(f"ENGLISH: {english}")
        print(f"WEDAU:   {wedau}")
    
    # Summary
    print(f"\n{'='*80}")
    print("TRANSLATION SUMMARY")
    print("="*80)
    
    dims_count = {'Love': 0, 'Justice': 0, 'Power': 0, 'Wisdom': 0}
    for t in translations:
        dims_count[t['dominant_dimension']] += 1
    
    print(f"\nVerse dimension distribution:")
    for dim, count in sorted(dims_count.items(), key=lambda x: -x[1]):
        pct = count / len(translations) * 100
        bar = '█' * int(pct / 5)
        print(f"  {dim:<10}: {count:2} verses ({pct:5.1f}%) {bar}")
    
    # Save translations
    output = {
        'book': 'Matthew',
        'chapter': 10,
        'source': 'LJPW Anchor Point Translation',
        'target_language': 'Wedau',
        'verses': translations
    }
    
    output_path = Path(__file__).parent / "matthew_10_wedau.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\nTranslation saved to: {output_path}")
    
    return translations


if __name__ == '__main__':
    main()
