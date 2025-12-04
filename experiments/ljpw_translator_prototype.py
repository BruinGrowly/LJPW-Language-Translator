#!/usr/bin/env python3
"""
LJPW Translator Prototype
========================

A working prototype demonstrating coordinate-based translation using the LJPW
semantic framework. This translator uses geometric transformations in 4D semantic
space rather than traditional dictionary lookup.

Features:
- Multi-language support (English, Spanish, French, Russian, Hindi, Urdu, Tagalog)
- Quality scoring based on semantic distance
- Word-level and sentence-level translation
- Context-aware disambiguation
- Real-time quality feedback

Usage:
    python ljpw_translator_prototype.py
"""

import numpy as np
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict
import re


@dataclass
class TranslationResult:
    """Result of a translation operation"""
    source_word: str
    target_word: str
    source_coords: np.ndarray
    target_coords: np.ndarray
    distance: float
    quality_score: float
    quality_grade: str
    territory_id: Optional[int] = None
    notes: str = ""


@dataclass
class SentenceTranslation:
    """Complete sentence translation with quality metrics"""
    source_text: str
    target_text: str
    source_lang: str
    target_lang: str
    word_translations: List[TranslationResult]
    overall_quality: float
    overall_grade: str
    warnings: List[str]


class CoordinateDatabase:
    """Database of word coordinates across multiple languages"""

    def __init__(self):
        self.coordinates: Dict[str, Dict[str, np.ndarray]] = defaultdict(dict)
        self.language_names = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'ru': 'Russian',
            'hi': 'Hindi',
            'ur': 'Urdu',
            'tl': 'Tagalog',
            'zh': 'Mandarin',
            'ar': 'Arabic'
        }

    def add_word(self, word: str, language: str, coordinates: np.ndarray):
        """Add a word and its coordinates to the database"""
        self.coordinates[language][word.lower()] = np.array(coordinates)

    def get_coords(self, word: str, language: str) -> Optional[np.ndarray]:
        """Get coordinates for a word in a specific language"""
        return self.coordinates[language].get(word.lower())

    def get_all_words(self, language: str) -> List[str]:
        """Get all words in a language"""
        return list(self.coordinates[language].keys())

    def has_word(self, word: str, language: str) -> bool:
        """Check if a word exists in the database"""
        return word.lower() in self.coordinates[language]

    def find_nearest_neighbor(self, coords: np.ndarray, language: str,
                             exclude: Optional[List[str]] = None) -> Tuple[str, np.ndarray, float]:
        """Find the nearest word in the target language"""
        if language not in self.coordinates or len(self.coordinates[language]) == 0:
            raise ValueError(f"No words found for language: {language}")

        exclude_set = set(w.lower() for w in (exclude or []))
        min_distance = float('inf')
        nearest_word = None
        nearest_coords = None

        for word, word_coords in self.coordinates[language].items():
            if word in exclude_set:
                continue

            distance = float(np.linalg.norm(coords - word_coords))
            if distance < min_distance:
                min_distance = distance
                nearest_word = word
                nearest_coords = word_coords

        if nearest_word is None:
            raise ValueError(f"Could not find nearest neighbor in {language}")

        return nearest_word, nearest_coords, min_distance

    def load_from_json(self, filepath: Path, language_mapping: Dict[str, str],
                      default_language: Optional[str] = None):
        """
        Load coordinates from JSON file

        Args:
            filepath: Path to JSON file
            language_mapping: Dict mapping file keys to language codes
                             e.g., {'French': 'fr', 'Spanish': 'es'}
            default_language: Default language code if not specified in word data (e.g., 'tl' for Tagalog)
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Handle different JSON structures
        if 'word_mappings' in data:
            # word_mappings format (used by both multilingual_expansion and tagalog_semantic_mapping)
            for word, word_data in data['word_mappings'].items():
                coords = np.array(word_data['coordinates'])

                # Check if language field exists
                if 'language' in word_data:
                    # multilingual_expansion.json format - has language field
                    lang_key = word_data['language']
                    if lang_key in language_mapping:
                        lang_code = language_mapping[lang_key]
                        self.add_word(word, lang_code, coords)
                elif default_language:
                    # No language field - use default (e.g., Tagalog)
                    self.add_word(word, default_language, coords)

                # Also add English equivalent
                if 'english' in word_data:
                    en_word = word_data['english']
                    self.add_word(en_word, 'en', coords)

        elif 'tagalog_mappings' in data:
            # Old tagalog_semantic_mapping.json format (if different structure)
            for mapping in data['tagalog_mappings']:
                word = mapping['tagalog_word']
                coords = np.array(mapping['tagalog_coords'])
                self.add_word(word, 'tl', coords)

                # Also add English equivalents if available
                if 'nearest_english' in mapping and mapping['nearest_english']:
                    en_word = mapping['nearest_english']['word']
                    en_coords = np.array(mapping['nearest_english']['coords'])
                    self.add_word(en_word, 'en', en_coords)


class LJPWTranslator:
    """
    Coordinate-based translator using the LJPW semantic framework
    """

    QUALITY_THRESHOLDS = {
        'excellent': 0.05,
        'good': 0.10,
        'fair': 0.20,
        'poor': float('inf')
    }

    TERRITORY_NAMES = {
        0: "Raw Power",
        1: "Compassionate Virtue",
        2: "Harmonious Balance",
        3: "Malevolent Evil",
        4: "Uncertain Transition",
        5: "Noble Action",
        6: "Pragmatic Neutrality",
        7: "Practical Wisdom"
    }

    def __init__(self, coordinate_db: CoordinateDatabase):
        self.db = coordinate_db

    def calculate_quality(self, distance: float) -> Tuple[float, str]:
        """
        Calculate quality score and grade from semantic distance

        Returns:
            Tuple of (quality_score, quality_grade)
            quality_score: 0-100 scale
            quality_grade: 'excellent', 'good', 'fair', or 'poor'
        """
        if distance < self.QUALITY_THRESHOLDS['excellent']:
            score = 97 + (self.QUALITY_THRESHOLDS['excellent'] - distance) * 60
            grade = 'excellent'
        elif distance < self.QUALITY_THRESHOLDS['good']:
            score = 90 + (self.QUALITY_THRESHOLDS['good'] - distance) * 140
            grade = 'good'
        elif distance < self.QUALITY_THRESHOLDS['fair']:
            score = 80 + (self.QUALITY_THRESHOLDS['fair'] - distance) * 100
            grade = 'fair'
        else:
            score = max(0, 80 - (distance - self.QUALITY_THRESHOLDS['fair']) * 200)
            grade = 'poor'

        return min(100.0, score), grade

    def translate_word(self, word: str, source_lang: str, target_lang: str) -> TranslationResult:
        """
        Translate a single word from source language to target language

        Args:
            word: Word to translate
            source_lang: Source language code (e.g., 'en', 'es')
            target_lang: Target language code

        Returns:
            TranslationResult object with translation and quality metrics
        """
        # Get source coordinates
        source_coords = self.db.get_coords(word, source_lang)

        if source_coords is None:
            raise ValueError(f"Word '{word}' not found in {source_lang} database")

        # Find nearest neighbor in target language
        target_word, target_coords, distance = self.db.find_nearest_neighbor(
            source_coords, target_lang
        )

        # Calculate quality
        quality_score, quality_grade = self.calculate_quality(distance)

        # Create result
        result = TranslationResult(
            source_word=word,
            target_word=target_word,
            source_coords=source_coords,
            target_coords=target_coords,
            distance=distance,
            quality_score=quality_score,
            quality_grade=quality_grade
        )

        return result

    def translate_sentence(self, text: str, source_lang: str, target_lang: str) -> SentenceTranslation:
        """
        Translate a complete sentence with quality analysis

        Args:
            text: Sentence to translate
            source_lang: Source language code
            target_lang: Target language code

        Returns:
            SentenceTranslation object with complete analysis
        """
        # Simple tokenization (for prototype - production would use proper NLP)
        words = self._tokenize(text)

        word_translations = []
        translated_words = []
        warnings = []

        for word in words:
            try:
                result = self.translate_word(word, source_lang, target_lang)
                word_translations.append(result)
                translated_words.append(result.target_word)

                # Generate warnings for low-quality translations
                if result.quality_grade == 'poor':
                    warnings.append(
                        f"Low quality translation for '{word}' → '{result.target_word}' "
                        f"(distance: {result.distance:.3f})"
                    )
                elif result.quality_grade == 'fair':
                    warnings.append(
                        f"Moderate semantic shift for '{word}' → '{result.target_word}' "
                        f"(distance: {result.distance:.3f})"
                    )

            except ValueError as e:
                # Word not in database - keep original
                warnings.append(f"'{word}' not in database - keeping original")
                translated_words.append(word)

        # Calculate overall quality
        if word_translations:
            avg_distance = np.mean([r.distance for r in word_translations])
            overall_quality, overall_grade = self.calculate_quality(avg_distance)
        else:
            overall_quality, overall_grade = 0.0, 'poor'

        # Construct translated sentence
        target_text = ' '.join(translated_words)

        return SentenceTranslation(
            source_text=text,
            target_text=target_text,
            source_lang=source_lang,
            target_lang=target_lang,
            word_translations=word_translations,
            overall_quality=overall_quality,
            overall_grade=overall_grade,
            warnings=warnings
        )

    def _tokenize(self, text: str) -> List[str]:
        """Simple word tokenization (for prototype)"""
        # Remove punctuation and split on whitespace
        text = re.sub(r'[^\w\s-]', '', text.lower())
        return text.split()

    def print_word_translation(self, result: TranslationResult):
        """Print formatted word translation result"""
        print(f"\n{'='*70}")
        print(f"Translation: '{result.source_word}' → '{result.target_word}'")
        print(f"{'='*70}")
        print(f"Source coordinates: [{', '.join(f'{x:.3f}' for x in result.source_coords)}]")
        print(f"Target coordinates: [{', '.join(f'{x:.3f}' for x in result.target_coords)}]")
        print(f"Semantic distance:  {result.distance:.4f}")
        print(f"Quality score:      {result.quality_score:.1f}%")
        print(f"Quality grade:      {result.quality_grade.upper()}")

        # Quality indicator bar
        bar_length = 40
        filled = int((result.quality_score / 100) * bar_length)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"Quality indicator:  [{bar}]")

        if result.notes:
            print(f"Notes: {result.notes}")

    def print_sentence_translation(self, result: SentenceTranslation):
        """Print formatted sentence translation result"""
        print(f"\n{'='*70}")
        print(f"SENTENCE TRANSLATION")
        print(f"{'='*70}")
        print(f"Source ({result.source_lang}): {result.source_text}")
        print(f"Target ({result.target_lang}): {result.target_text}")
        print(f"\nOverall Quality: {result.overall_quality:.1f}% ({result.overall_grade.upper()})")

        # Quality bar
        bar_length = 40
        filled = int((result.overall_quality / 100) * bar_length)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"                 [{bar}]")

        # Word-level breakdown
        if result.word_translations:
            print(f"\n{'─'*70}")
            print("Word-Level Quality:")
            print(f"{'─'*70}")
            for wt in result.word_translations:
                bar_len = 20
                filled = int((wt.quality_score / 100) * bar_len)
                bar = '█' * filled + '░' * (bar_len - filled)
                print(f"  {wt.source_word:15} → {wt.target_word:15} [{bar}] {wt.quality_score:5.1f}%")

        # Warnings
        if result.warnings:
            print(f"\n{'─'*70}")
            print("⚠ Warnings:")
            print(f"{'─'*70}")
            for warning in result.warnings:
                print(f"  • {warning}")

        print(f"{'='*70}\n")


def load_coordinate_database() -> CoordinateDatabase:
    """Load coordinate database from experiment JSON files"""
    db = CoordinateDatabase()
    experiments_dir = Path(__file__).parent

    print("Loading coordinate databases...")

    # Load multilingual expansion (French, Spanish, Russian, Hindi, Urdu)
    multilingual_file = experiments_dir / 'multilingual_expansion.json'
    if multilingual_file.exists():
        language_mapping = {
            'French': 'fr',
            'Spanish': 'es',
            'Russian': 'ru',
            'Hindi': 'hi',
            'Urdu': 'ur'
        }
        db.load_from_json(multilingual_file, language_mapping)
        print(f"  ✓ Loaded multilingual expansion: {multilingual_file.name}")

    # Load Tagalog mapping
    tagalog_file = experiments_dir / 'tagalog_semantic_mapping.json'
    if tagalog_file.exists():
        db.load_from_json(tagalog_file, {}, default_language='tl')
        print(f"  ✓ Loaded Tagalog mappings: {tagalog_file.name}")

    # Print statistics
    print("\nDatabase Statistics:")
    for lang_code, lang_name in db.language_names.items():
        count = len(db.coordinates[lang_code])
        if count > 0:
            print(f"  {lang_name:12} ({lang_code}): {count:3} words")

    return db


def run_demo_translations():
    """Run demonstration translations"""
    print("\n" + "="*70)
    print("LJPW Translator Prototype - Demonstration")
    print("="*70)

    # Load database
    db = load_coordinate_database()
    translator = LJPWTranslator(db)

    # Demo 1: Simple word translations
    print("\n\n" + "▶"*35)
    print("DEMO 1: Single Word Translations")
    print("▶"*35)

    word_demos = [
        ('love', 'en', 'es'),
        ('love', 'en', 'fr'),
        ('justice', 'en', 'ru'),
        ('compassion', 'en', 'tl'),
    ]

    for word, src, tgt in word_demos:
        try:
            result = translator.translate_word(word, src, tgt)
            translator.print_word_translation(result)
        except ValueError as e:
            print(f"\n⚠ Could not translate '{word}' ({src}→{tgt}): {e}")

    # Demo 2: Sentence translations
    print("\n\n" + "▶"*35)
    print("DEMO 2: Sentence Translations")
    print("▶"*35)

    sentence_demos = [
        ("love justice wisdom", 'en', 'es'),
        ("peace love harmony", 'en', 'fr'),
    ]

    for sentence, src, tgt in sentence_demos:
        try:
            result = translator.translate_sentence(sentence, src, tgt)
            translator.print_sentence_translation(result)
        except Exception as e:
            print(f"\n⚠ Error translating sentence: {e}")

    # Demo 3: Quality comparison
    print("\n\n" + "▶"*35)
    print("DEMO 3: Translation Quality Comparison")
    print("▶"*35)

    print("\nComparing translations across language pairs:")

    comparison_words = ['love', 'justice', 'peace']
    target_languages = [
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('ru', 'Russian')
    ]

    for word in comparison_words:
        if not db.has_word(word, 'en'):
            continue

        print(f"\n{'─'*70}")
        print(f"Word: '{word}' (English)")
        print(f"{'─'*70}")

        for lang_code, lang_name in target_languages:
            try:
                result = translator.translate_word(word, 'en', lang_code)
                bar_len = 30
                filled = int((result.quality_score / 100) * bar_len)
                bar = '█' * filled + '░' * (bar_len - filled)
                print(f"  → {lang_name:12} '{result.target_word:15}' [{bar}] {result.quality_score:5.1f}%")
            except ValueError:
                print(f"  → {lang_name:12} (not available)")

    # Demo 4: Cross-linguistic semantic consistency
    print("\n\n" + "▶"*35)
    print("DEMO 4: Cross-Linguistic Semantic Consistency")
    print("▶"*35)

    print("\nDemonstrating that similar concepts cluster together across languages:")

    love_family = ['love', 'compassion', 'mercy', 'kindness']
    available_love_words = [w for w in love_family if db.has_word(w, 'en')]

    if available_love_words:
        print(f"\nLove-family words in English:")
        en_coords = []
        for word in available_love_words:
            coords = db.get_coords(word, 'en')
            en_coords.append(coords)
            print(f"  {word:12} [{', '.join(f'{x:.3f}' for x in coords)}]")

        if len(en_coords) > 1:
            # Calculate pairwise distances
            print(f"\n  Pairwise semantic distances:")
            for i in range(len(available_love_words)):
                for j in range(i+1, len(available_love_words)):
                    dist = np.linalg.norm(en_coords[i] - en_coords[j])
                    print(f"    {available_love_words[i]:12} ↔ {available_love_words[j]:12} = {dist:.4f}")

    print("\n\n" + "="*70)
    print("End of Demonstration")
    print("="*70)


def interactive_mode():
    """Run interactive translation mode"""
    print("\n" + "="*70)
    print("LJPW Translator - Interactive Mode")
    print("="*70)

    db = load_coordinate_database()
    translator = LJPWTranslator(db)

    print("\nAvailable languages:")
    for code, name in db.language_names.items():
        if len(db.coordinates[code]) > 0:
            print(f"  {code} - {name}")

    print("\nCommands:")
    print("  word <word> <source> <target>  - Translate a word")
    print("  sent <text> <source> <target>  - Translate a sentence")
    print("  list <lang>                     - List available words in language")
    print("  demo                            - Run demonstration")
    print("  quit                            - Exit")

    while True:
        try:
            cmd = input("\n> ").strip()

            if not cmd:
                continue

            if cmd == 'quit':
                break

            if cmd == 'demo':
                run_demo_translations()
                continue

            parts = cmd.split(maxsplit=3)

            if parts[0] == 'word' and len(parts) == 4:
                _, word, src, tgt = parts
                result = translator.translate_word(word, src, tgt)
                translator.print_word_translation(result)

            elif parts[0] == 'sent' and len(parts) == 4:
                _, text, src, tgt = parts
                result = translator.translate_sentence(text, src, tgt)
                translator.print_sentence_translation(result)

            elif parts[0] == 'list' and len(parts) == 2:
                _, lang = parts
                words = db.get_all_words(lang)
                print(f"\n{len(words)} words in {db.language_names.get(lang, lang)}:")
                for i, word in enumerate(sorted(words), 1):
                    print(f"  {i:3}. {word}")

            else:
                print("Invalid command. Type 'demo' to run demonstration or 'quit' to exit.")

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'interactive':
        interactive_mode()
    else:
        run_demo_translations()
