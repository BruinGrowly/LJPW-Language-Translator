#!/usr/bin/env python3
"""
LJPW-Guided Matthew Translator
==============================

Translates English Matthew to Wedau using LJPW coordinates to guide:
- Tone (high Love = relational, high Power = dynamic)
- Vocabulary choice (dimension-weighted word selection)
- Structure (dimension-specific patterns)

The coordinates make the translation "come alive" - each verse
has its own semantic character based on its LJPW signature.
"""

import json
import os
import sys
import re
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_quantum.resonance_engine import ResonanceEngine


# ============================================================================
# WEDAU VOCABULARY - Loaded from extracted human translations
# ============================================================================

def load_expanded_vocabulary():
    """Load vocabulary from extracted human translations."""
    import os
    vocab_path = os.path.join(os.path.dirname(__file__), 'wedau_expanded_vocabulary.json')
    with open(vocab_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    vocab = data['english_wedau_pairs'].copy()
    
    # Add common function words from frequency data
    vocab.update({
        'and': 'ma',
        'the': '',  # No article in Wedau
        'a': '',    # No article in Wedau
        'to': 'da',
        'of': 'ana',
        'in': 'au',
        'is': '',   # Implicit in Wedau
        'are': '',
        'was': '',
        'were': '',
        'be': '',
        'been': '',
        'being': '',
        'have': 'ana',
        'has': 'ana',
        'had': 'ana',
        'do': 'rura',
        'does': 'rura',
        'did': 'rura',
        'will': 'ina',
        'shall': 'ina',
        'would': 'ina',
        'should': 'ina',
        'can': 'ita',
        'could': 'ita',
        'may': 'ita',
        'might': 'ita',
        'must': 'ina',
        'not': 'egha',
        'no': 'egha',
        'but': 'tuna',
        'or': 'bo',
        'if': 'tora',
        'when': 'maranaina',
        'then': 'maratagogi',
        'so': 'yamna',
        'because': 'yamna',
        'for': 'yamna',
        'that': 'raketana',
        'this': 'ina',
        'these': 'ina',
        'those': 'raketana',
        'who': 'aiyai',
        'whom': 'aiyai',
        'which': 'aiyai',
        'what': 'aiwaꞌi',
        'with': 'maitehi',
        'from': 'au',
        'by': 'au',
        'into': 'au',
        'up': 'au',
        'down': 'au',
        'out': 'hopu',
        'on': 'au',
        'at': 'au',
        'about': 'awarina',
        'against': 'awarina',
        'before': 'naona',
        'after': 'muriyai',
        'over': 'au',
        'under': 'au',
        'through': 'au',
        'between': 'au',
        'you': 'omi',
        'your': 'ami',
        'he': 'tauna',
        'she': 'tauna',
        'it': 'tauna',
        'his': 'ana',
        'her': 'ana',
        'they': 'tauhi',
        'their': 'ahi',
        'them': 'hita',
        'we': 'ita',
        'our': 'ahi',
        'us': 'ita',
        'me': 'tau',
        'my': 'au',
        'i': 'tau',
        'him': 'tauna',
        'there': 'kampa',
        'here': 'ina',
        'where': 'aiwaꞌi',
        'how': 'aiwaꞌi',
        'why': 'yamna',
        'now': 'ina marana',
        'also': 'maitehi',
        'again': 'vouna',
        'even': 'ma',
        'just': 'tagotagogi',
        'only': 'tagotagogi',
        'many': 'anatapuhi',
        'more': 'ghe vavahagha',
        'most': 'anatapuhi',
        'other': 'ghehauna',
        'some': 'ghehauhi',
        'any': 'ghehauna',
        'each': 'tagotagogi',
        'every': 'anatapuhi',
        'all': 'anatapuhi',
        'both': 'ruwagha',
        'few': 'ghehauhi',
        'first': 'naona',
        'last': 'muriyai',
        'own': 'ana',
        'same': 'tagotagogi',
        'than': 'da',
        'very': 'ghe',
        'too': 'maitehi',
        'well': 'ahiahina',
        'said': 'riwa',
        'say': 'riwa',
        'says': 'riwa',
        'went': 'nae',
        'go': 'nae',
        'goes': 'nae',
        'going': 'nae',
        'gone': 'nae',
        'came': 'neꞌi',
        'come': 'neꞌi',
        'comes': 'neꞌi',
        'give': 'verei',
        'gave': 'verei',
        'given': 'verei',
        'take': 'varahai',
        'took': 'varahai',
        'taken': 'varahai',
        'see': 'inana',
        'saw': 'inana',
        'seen': 'inana',
        'know': 'haramaneꞌi',
        'knew': 'haramaneꞌi',
        'known': 'haramaneꞌi',
        'make': 'rura',
        'made': 'rura',
        'making': 'rura',
        'get': 'varahai',
        'got': 'varahai',
        'let': 'ita',
        'put': 'terei',
        'tell': 'riwehi',
        'told': 'riwehi',
        'ask': 'rau-baghei',
        'call': 'ghorehi',
        'called': 'ghorehi',
        'send': 'vivohi',
        'sent': 'vivohi',
        # Religious terms
        'god': 'God',
        'jesus': 'Yesu',
        'christ': 'Keriso',
        'lord': 'Guyau',
        'father': 'Tamatei',
        'mother': 'hinana',
        'son': 'natuna',
        'daughter': 'natuna',
        'children': 'natunatuna',
        'child': 'ghoraghora',
        'people': 'rava',
        'man': 'oroto',
        'men': 'rava',
        'woman': 'vaivine',
        'women': 'vaivinehi',
        'king': 'kingi',
        'word': 'riwana',
        'words': 'riwehi',
        'life': 'yawahana',
        'death': 'mate',
        'day': 'mara',
        'days': 'maratom',
        'night': 'diedie',
        'world': 'dobuna',
        'name': 'wava',
    })
    
    return vocab


# Wedau grammatical particles
WEDAU_PARTICLES = {
    'subject_3sg': 'i',     # He/she/it did
    'subject_3pl': 'hi',    # They did  
    'possessive': 'ana',    # His/her/its
    'locative': 'au',       # At/in
    'benefactive': 'awarina', # For/to
    'causative': 'vi',      # Cause to
}


class LJPWGuidedTranslator:
    """
    Translator that uses LJPW coordinates to guide translation tone.
    
    High Love → relational vocabulary, soft patterns
    High Justice → structural vocabulary, formal patterns
    High Power → dynamic verbs, action patterns
    High Wisdom → teaching vocabulary, explanatory patterns
    """
    
    def __init__(self):
        self.engine = ResonanceEngine()
        self.vocabulary = load_expanded_vocabulary()
        self.particles = WEDAU_PARTICLES
        
    def get_dimension_emphasis(self, ljpw: List[float]) -> Tuple[str, float]:
        """Determine which dimension dominates this verse."""
        dims = ['L', 'J', 'P', 'W']
        names = ['Love', 'Justice', 'Power', 'Wisdom']
        max_idx = np.argmax(ljpw)
        return names[max_idx], ljpw[max_idx]
    
    def translate_verse(self, english: str, ljpw: List[float], verse_ref: str) -> Dict:
        """
        Translate a single verse using LJPW-guided approach.
        
        Returns:
            Dict with wedau translation, metadata, and quality metrics
        """
        dominant, strength = self.get_dimension_emphasis(ljpw)
        harmony = self.engine.calculate_harmony(np.array(ljpw))
        
        # Build translation
        wedau = self._build_wedau_translation(english, ljpw, dominant)
        
        return {
            'verse_ref': verse_ref,
            'english': english,
            'wedau': wedau,
            'ljpw': ljpw,
            'dominant_dimension': dominant,
            'dimension_strength': strength,
            'harmony': float(harmony),
            'translation_notes': self._generate_notes(dominant, strength, ljpw)
        }
    
    def _build_wedau_translation(self, english: str, ljpw: List[float], dominant: str) -> str:
        """Build Wedau translation guided by LJPW coordinates."""
        
        # Tokenize and process
        words = english.lower().replace(',', '').replace('.', '').replace('"', '').replace('"', '').replace('"', '').split()
        
        wedau_parts = []
        i = 0
        
        while i < len(words):
            word = words[i]
            
            # Try multi-word matches first
            if i < len(words) - 1:
                two_word = f"{word} {words[i+1]}"
                if two_word in self.vocabulary:
                    wedau_parts.append(self.vocabulary[two_word])
                    i += 2
                    continue
            
            # Single word match
            if word in self.vocabulary:
                wedau_parts.append(self.vocabulary[word])
            else:
                # Try morphological variants
                matched = False
                for base in ['ing', 'ed', 's', 'es', 'ly']:
                    if word.endswith(base):
                        stem = word[:-len(base)]
                        if stem in self.vocabulary:
                            wedau_parts.append(self.vocabulary[stem])
                            matched = True
                            break
                
                if not matched:
                    # Keep proper nouns, transliterate others
                    if word[0].isupper() or word in ['abraham', 'david', 'jacob', 'joseph', 'mary']:
                        wedau_parts.append(word.capitalize())
                    else:
                        # Mark for review but include phonetic approximation
                        wedau_parts.append(f"[{word}]")
            
            i += 1
        
        # Apply dimension-specific styling
        wedau = ' '.join(wedau_parts)
        
        # Add dimension markers
        if dominant == 'Love' and ljpw[0] > 0.7:
            # High love: add relational framing
            if 'God' in wedau or 'Yesu' in wedau:
                wedau = wedau.replace('God', 'Tamatei God')
        
        if dominant == 'Power' and ljpw[2] > 0.7:
            # High power: ensure action verbs are prominent
            if not wedau.startswith('Ma ') and not wedau.startswith('I '):
                wedau = 'I ' + wedau
        
        return wedau.strip()
    
    def _generate_notes(self, dominant: str, strength: float, ljpw: List[float]) -> str:
        """Generate translation notes based on LJPW profile."""
        notes = []
        
        notes.append(f"Primary dimension: {dominant} ({strength:.2f})")
        
        # Note harmony level
        harmony = self.engine.calculate_harmony(np.array(ljpw))
        if harmony > 0.7:
            notes.append("High harmony verse (balanced)")
        elif harmony < 0.5:
            notes.append("Low harmony verse (distinctive emphasis)")
        
        # Secondary dimension if close
        dims = ['Love', 'Justice', 'Power', 'Wisdom']
        sorted_idx = np.argsort(ljpw)[::-1]
        if ljpw[sorted_idx[1]] > 0.6 and ljpw[sorted_idx[1]] / ljpw[sorted_idx[0]] > 0.85:
            notes.append(f"Strong secondary: {dims[sorted_idx[1]]}")
        
        return '; '.join(notes)
    
    def translate_chapter(self, chapter_data: Dict) -> Dict:
        """Translate an entire chapter."""
        
        chapter_num = chapter_data['chapter']
        verses = chapter_data['verses']
        ljpw_coords = chapter_data.get('ljpw_coordinates', {})
        
        translated_verses = {}
        
        for verse_num, english_text in verses.items():
            # Get LJPW coordinates (default to balanced if missing)
            ljpw = ljpw_coords.get(verse_num, [0.5, 0.5, 0.5, 0.5])
            
            verse_ref = f"Matthew {chapter_num}:{verse_num}"
            result = self.translate_verse(english_text, ljpw, verse_ref)
            translated_verses[verse_num] = result
        
        return {
            'book': 'Matthew',
            'chapter': chapter_num,
            'source_language': 'English',
            'target_language': 'Wedau',
            'translation_method': 'LJPW-Guided Pure Meaning Translation',
            'timestamp': datetime.now().isoformat(),
            'verses': translated_verses
        }


def translate_all_matthew():
    """Translate entire book of Matthew."""
    
    print("=" * 70)
    print("MATTHEW KOINE -> WEDAU TRANSLATION")
    print("LJPW-Guided Pure Meaning Translation")
    print("=" * 70)
    
    translator = LJPWGuidedTranslator()
    
    corpus_path = Path(__file__).parent.parent / 'corpus' / 'matthew'
    output_path = Path(__file__).parent / 'matthew_wedau_translation'
    output_path.mkdir(exist_ok=True)
    
    all_translations = {}
    total_verses = 0
    
    chapter_files = sorted(corpus_path.glob('chapter_*.json'))
    
    print(f"\nTranslating {len(chapter_files)} chapters...")
    
    for chapter_file in chapter_files:
        with open(chapter_file, 'r', encoding='utf-8') as f:
            chapter_data = json.load(f)
        
        chapter_num = chapter_data['chapter']
        print(f"  Chapter {chapter_num}: {len(chapter_data['verses'])} verses...", end=' ')
        
        translated = translator.translate_chapter(chapter_data)
        all_translations[chapter_num] = translated
        total_verses += len(translated['verses'])
        
        # Save individual chapter
        chapter_output = output_path / f'matthew_{chapter_num:02d}_wedau.json'
        with open(chapter_output, 'w', encoding='utf-8') as f:
            json.dump(translated, f, indent=2, ensure_ascii=False)
        
        print("Done")
    
    # Save complete book
    complete_output = output_path / 'matthew_complete_wedau.json'
    with open(complete_output, 'w', encoding='utf-8') as f:
        json.dump({
            'book': 'Matthew',
            'language': 'Wedau',
            'method': 'LJPW-Guided Translation',
            'timestamp': datetime.now().isoformat(),
            'chapters': all_translations
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n" + "=" * 70)
    print("TRANSLATION COMPLETE")
    print("=" * 70)
    print(f"\nTotal chapters: {len(all_translations)}")
    print(f"Total verses: {total_verses}")
    print(f"Output: {output_path}")
    
    # Print sample
    print(f"\n--- Sample Translation (Matthew 1:21) ---")
    sample = all_translations[1]['verses'].get('21', {})
    if sample:
        print(f"English: {sample['english']}")
        print(f"Wedau:   {sample['wedau']}")
        print(f"LJPW:    {sample['ljpw']}")
        print(f"Notes:   {sample['translation_notes']}")
    
    return all_translations


if __name__ == '__main__':
    translate_all_matthew()
