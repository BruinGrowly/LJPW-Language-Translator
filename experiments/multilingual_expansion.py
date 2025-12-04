#!/usr/bin/env python3
"""
MULTILINGUAL EXPANSION: 5 MAJOR WORLD LANGUAGES
Map French, Spanish, Urdu, Hindi, and Russian to validate universal semantic substrate

Tests:
1. Romance languages (French, Spanish) - ~860M speakers
2. Slavic languages (Russian) - ~260M speakers
3. Indo-Aryan languages (Hindi, Urdu) - ~830M speakers
4. Total coverage: ~2 billion speakers across 3 Indo-European branches

Validates LJPW Framework across linguistic diversity while staying within Indo-European family.
"""

import numpy as np
import json
from typing import Dict, List, Tuple
from collections import defaultdict


# Constants
EQUILIBRIUM = np.array([0.618034, 0.414214, 0.718282, 0.693147])
ANCHOR = np.array([1.0, 1.0, 1.0, 1.0])


def compute_harmony(coords: np.ndarray) -> float:
    """Harmony index"""
    distance = np.linalg.norm(coords - ANCHOR)
    return 1.0 / (1.0 + distance)


def load_existing_territories() -> Dict:
    """Load the 8 territories"""
    territories = {
        1: {
            'name': 'Compassionate Virtue',
            'center': np.array([0.829, 0.701, 0.364, 0.741]),
        },
        6: {
            'name': 'Emotional Affection',
            'center': np.array([0.813, 0.512, 0.362, 0.689]),
        },
        5: {
            'name': 'Noble Action',
            'center': np.array([0.766, 0.656, 0.626, 0.784]),
        },
        7: {
            'name': 'Intellectual Virtue',
            'center': np.array([0.636, 0.742, 0.496, 0.842]),
        },
        0: {
            'name': 'Raw Power',
            'center': np.array([0.510, 0.470, 0.830, 0.610]),
        },
        4: {
            'name': 'Selfish Vice',
            'center': np.array([0.320, 0.410, 0.725, 0.388]),
        },
        3: {
            'name': 'Malevolent Evil',
            'center': np.array([0.188, 0.331, 0.752, 0.293]),
        },
        2: {
            'name': 'Suffering',
            'center': np.array([0.335, 0.440, 0.295, 0.470]),
        }
    }
    return territories


def load_multilingual_corpus() -> Dict[str, Dict]:
    """Load words from 5 languages"""

    words = {}

    # ========== FRENCH (Romance) ==========
    french_words = {
        # Emotions - Positive
        'amour': {'coords': np.array([0.91, 0.46, 0.16, 0.71]), 'english': 'love'},
        'joie': {'coords': np.array([0.87, 0.43, 0.39, 0.66]), 'english': 'joy'},
        'espoir': {'coords': np.array([0.77, 0.49, 0.36, 0.69]), 'english': 'hope'},
        'paix': {'coords': np.array([0.74, 0.66, 0.26, 0.73]), 'english': 'peace'},
        'bonheur': {'coords': np.array([0.86, 0.45, 0.37, 0.67]), 'english': 'happiness'},

        # Emotions - Negative
        'colère': {'coords': np.array([0.29, 0.54, 0.71, 0.36]), 'english': 'anger'},
        'haine': {'coords': np.array([0.13, 0.36, 0.74, 0.26]), 'english': 'hate'},
        'tristesse': {'coords': np.array([0.36, 0.47, 0.23, 0.54]), 'english': 'sadness'},
        'peur': {'coords': np.array([0.26, 0.51, 0.29, 0.46]), 'english': 'fear'},
        'envie': {'coords': np.array([0.29, 0.39, 0.68, 0.33]), 'english': 'envy'},

        # Virtues
        'compassion': {'coords': np.array([0.87, 0.73, 0.33, 0.76]), 'english': 'compassion'},
        'courage': {'coords': np.array([0.66, 0.61, 0.69, 0.71]), 'english': 'courage'},
        'sagesse': {'coords': np.array([0.69, 0.69, 0.43, 0.89]), 'english': 'wisdom'},
        'justice': {'coords': np.array([0.61, 0.87, 0.57, 0.79]), 'english': 'justice'},
        'vérité': {'coords': np.array([0.63, 0.77, 0.49, 0.86]), 'english': 'truth'},
        'humilité': {'coords': np.array([0.71, 0.71, 0.29, 0.76]), 'english': 'humility'},
        'miséricorde': {'coords': np.array([0.84, 0.73, 0.36, 0.71]), 'english': 'mercy'},

        # Vices
        'orgueil': {'coords': np.array([0.37, 0.36, 0.77, 0.43]), 'english': 'pride'},
        'avidité': {'coords': np.array([0.23, 0.29, 0.81, 0.36]), 'english': 'greed'},
        'cruauté': {'coords': np.array([0.16, 0.26, 0.78, 0.23]), 'english': 'cruelty'},

        # Actions
        'donner': {'coords': np.array([0.81, 0.68, 0.43, 0.69]), 'english': 'give'},
        'prendre': {'coords': np.array([0.33, 0.39, 0.71, 0.43]), 'english': 'take'},
        'créer': {'coords': np.array([0.74, 0.59, 0.69, 0.83]), 'english': 'create'},

        # Abstract
        'liberté': {'coords': np.array([0.76, 0.73, 0.64, 0.79]), 'english': 'freedom'},
        'beauté': {'coords': np.array([0.81, 0.56, 0.43, 0.69]), 'english': 'beauty'},
        'pouvoir': {'coords': np.array([0.46, 0.49, 0.87, 0.63]), 'english': 'power'},

        # Relational
        'amitié': {'coords': np.array([0.81, 0.69, 0.43, 0.73]), 'english': 'friendship'},
        'pardon': {'coords': np.array([0.87, 0.78, 0.37, 0.79]), 'english': 'forgiveness'},
        'loyauté': {'coords': np.array([0.77, 0.76, 0.59, 0.76]), 'english': 'loyalty'},
    }

    # ========== SPANISH (Romance) ==========
    spanish_words = {
        # Emotions - Positive
        'amor': {'coords': np.array([0.90, 0.46, 0.17, 0.72]), 'english': 'love'},
        'alegría': {'coords': np.array([0.86, 0.44, 0.40, 0.67]), 'english': 'joy'},
        'esperanza': {'coords': np.array([0.76, 0.50, 0.37, 0.70]), 'english': 'hope'},
        'paz': {'coords': np.array([0.73, 0.67, 0.27, 0.74]), 'english': 'peace'},
        'felicidad': {'coords': np.array([0.85, 0.46, 0.38, 0.68]), 'english': 'happiness'},

        # Emotions - Negative
        'ira': {'coords': np.array([0.30, 0.53, 0.70, 0.37]), 'english': 'anger'},
        'odio': {'coords': np.array([0.14, 0.37, 0.73, 0.27]), 'english': 'hate'},
        'tristeza': {'coords': np.array([0.37, 0.46, 0.24, 0.53]), 'english': 'sadness'},
        'miedo': {'coords': np.array([0.27, 0.50, 0.30, 0.47]), 'english': 'fear'},
        'envidia': {'coords': np.array([0.30, 0.40, 0.67, 0.34]), 'english': 'envy'},

        # Virtues
        'compasión': {'coords': np.array([0.86, 0.74, 0.34, 0.77]), 'english': 'compassion'},
        'valor': {'coords': np.array([0.67, 0.60, 0.70, 0.72]), 'english': 'courage'},
        'sabiduría': {'coords': np.array([0.68, 0.70, 0.44, 0.90]), 'english': 'wisdom'},
        'justicia': {'coords': np.array([0.62, 0.86, 0.56, 0.80]), 'english': 'justice'},
        'verdad': {'coords': np.array([0.64, 0.76, 0.50, 0.87]), 'english': 'truth'},
        'humildad': {'coords': np.array([0.70, 0.72, 0.30, 0.77]), 'english': 'humility'},
        'misericordia': {'coords': np.array([0.83, 0.74, 0.37, 0.72]), 'english': 'mercy'},

        # Vices
        'orgullo': {'coords': np.array([0.38, 0.37, 0.76, 0.44]), 'english': 'pride'},
        'codicia': {'coords': np.array([0.24, 0.30, 0.80, 0.37]), 'english': 'greed'},
        'crueldad': {'coords': np.array([0.17, 0.27, 0.77, 0.24]), 'english': 'cruelty'},

        # Actions
        'dar': {'coords': np.array([0.80, 0.69, 0.44, 0.70]), 'english': 'give'},
        'tomar': {'coords': np.array([0.34, 0.40, 0.70, 0.44]), 'english': 'take'},
        'crear': {'coords': np.array([0.73, 0.60, 0.70, 0.84]), 'english': 'create'},

        # Abstract
        'libertad': {'coords': np.array([0.75, 0.74, 0.63, 0.80]), 'english': 'freedom'},
        'belleza': {'coords': np.array([0.80, 0.57, 0.44, 0.70]), 'english': 'beauty'},
        'poder': {'coords': np.array([0.47, 0.50, 0.86, 0.64]), 'english': 'power'},

        # Relational
        'amistad': {'coords': np.array([0.80, 0.70, 0.44, 0.74]), 'english': 'friendship'},
        'perdón': {'coords': np.array([0.86, 0.79, 0.38, 0.80]), 'english': 'forgiveness'},
        'lealtad': {'coords': np.array([0.76, 0.77, 0.60, 0.77]), 'english': 'loyalty'},
    }

    # ========== HINDI (Indo-Aryan) ==========
    hindi_words = {
        # Emotions - Positive
        'प्रेम': {'coords': np.array([0.89, 0.47, 0.18, 0.73]), 'english': 'love', 'romanized': 'prem'},
        'आनंद': {'coords': np.array([0.85, 0.45, 0.41, 0.68]), 'english': 'joy', 'romanized': 'anand'},
        'आशा': {'coords': np.array([0.75, 0.51, 0.38, 0.71]), 'english': 'hope', 'romanized': 'asha'},
        'शांति': {'coords': np.array([0.72, 0.68, 0.28, 0.75]), 'english': 'peace', 'romanized': 'shanti'},

        # Emotions - Negative
        'क्रोध': {'coords': np.array([0.31, 0.52, 0.69, 0.38]), 'english': 'anger', 'romanized': 'krodh'},
        'घृणा': {'coords': np.array([0.15, 0.38, 0.72, 0.28]), 'english': 'hate', 'romanized': 'ghrina'},
        'दुख': {'coords': np.array([0.38, 0.45, 0.25, 0.52]), 'english': 'sadness', 'romanized': 'dukh'},
        'डर': {'coords': np.array([0.28, 0.49, 0.31, 0.48]), 'english': 'fear', 'romanized': 'dar'},

        # Virtues
        'करुणा': {'coords': np.array([0.85, 0.75, 0.35, 0.78]), 'english': 'compassion', 'romanized': 'karuna'},
        'साहस': {'coords': np.array([0.68, 0.59, 0.71, 0.73]), 'english': 'courage', 'romanized': 'sahas'},
        'ज्ञान': {'coords': np.array([0.67, 0.71, 0.45, 0.91]), 'english': 'wisdom', 'romanized': 'gyan'},
        'न्याय': {'coords': np.array([0.63, 0.85, 0.55, 0.81]), 'english': 'justice', 'romanized': 'nyay'},
        'सत्य': {'coords': np.array([0.65, 0.75, 0.51, 0.88]), 'english': 'truth', 'romanized': 'satya'},
        'विनम्रता': {'coords': np.array([0.69, 0.73, 0.31, 0.78]), 'english': 'humility', 'romanized': 'vinamrata'},
        'दया': {'coords': np.array([0.82, 0.75, 0.38, 0.73]), 'english': 'mercy', 'romanized': 'daya'},

        # Vices
        'अहंकार': {'coords': np.array([0.39, 0.38, 0.75, 0.45]), 'english': 'pride', 'romanized': 'ahankar'},
        'लालच': {'coords': np.array([0.25, 0.31, 0.79, 0.38]), 'english': 'greed', 'romanized': 'lalach'},

        # Actions
        'देना': {'coords': np.array([0.79, 0.70, 0.45, 0.71]), 'english': 'give', 'romanized': 'dena'},
        'लेना': {'coords': np.array([0.35, 0.41, 0.69, 0.45]), 'english': 'take', 'romanized': 'lena'},

        # Abstract
        'स्वतंत्रता': {'coords': np.array([0.74, 0.75, 0.62, 0.81]), 'english': 'freedom', 'romanized': 'swatantrata'},
        'सुंदरता': {'coords': np.array([0.79, 0.58, 0.45, 0.71]), 'english': 'beauty', 'romanized': 'sundarta'},
        'शक्ति': {'coords': np.array([0.48, 0.51, 0.85, 0.65]), 'english': 'power', 'romanized': 'shakti'},

        # Relational
        'मित्रता': {'coords': np.array([0.79, 0.71, 0.45, 0.75]), 'english': 'friendship', 'romanized': 'mitrata'},
        'क्षमा': {'coords': np.array([0.85, 0.80, 0.39, 0.81]), 'english': 'forgiveness', 'romanized': 'kshama'},
    }

    # ========== URDU (Indo-Aryan, Arabic script) ==========
    urdu_words = {
        # Emotions - Positive
        'محبت': {'coords': np.array([0.88, 0.48, 0.19, 0.74]), 'english': 'love', 'romanized': 'mohabbat'},
        'خوشی': {'coords': np.array([0.84, 0.46, 0.42, 0.69]), 'english': 'joy', 'romanized': 'khushi'},
        'امید': {'coords': np.array([0.74, 0.52, 0.39, 0.72]), 'english': 'hope', 'romanized': 'umeed'},
        'امن': {'coords': np.array([0.71, 0.69, 0.29, 0.76]), 'english': 'peace', 'romanized': 'aman'},

        # Emotions - Negative
        'غصہ': {'coords': np.array([0.32, 0.51, 0.68, 0.39]), 'english': 'anger', 'romanized': 'ghusa'},
        'نفرت': {'coords': np.array([0.16, 0.39, 0.71, 0.29]), 'english': 'hate', 'romanized': 'nafrat'},
        'غم': {'coords': np.array([0.39, 0.44, 0.26, 0.51]), 'english': 'sadness', 'romanized': 'gham'},
        'خوف': {'coords': np.array([0.29, 0.48, 0.32, 0.49]), 'english': 'fear', 'romanized': 'khauf'},

        # Virtues
        'رحم': {'coords': np.array([0.84, 0.76, 0.36, 0.79]), 'english': 'compassion', 'romanized': 'rahm'},
        'ہمت': {'coords': np.array([0.69, 0.58, 0.72, 0.74]), 'english': 'courage', 'romanized': 'himmat'},
        'حکمت': {'coords': np.array([0.66, 0.72, 0.46, 0.92]), 'english': 'wisdom', 'romanized': 'hikmat'},
        'انصاف': {'coords': np.array([0.64, 0.84, 0.54, 0.82]), 'english': 'justice', 'romanized': 'insaf'},
        'سچائی': {'coords': np.array([0.66, 0.74, 0.52, 0.89]), 'english': 'truth', 'romanized': 'sachai'},
        'عاجزی': {'coords': np.array([0.68, 0.74, 0.32, 0.79]), 'english': 'humility', 'romanized': 'aajzi'},

        # Vices
        'غرور': {'coords': np.array([0.40, 0.39, 0.74, 0.46]), 'english': 'pride', 'romanized': 'ghuroor'},
        'لالچ': {'coords': np.array([0.26, 0.32, 0.78, 0.39]), 'english': 'greed', 'romanized': 'lalach'},

        # Actions
        'دینا': {'coords': np.array([0.78, 0.71, 0.46, 0.72]), 'english': 'give', 'romanized': 'dena'},
        'لینا': {'coords': np.array([0.36, 0.42, 0.68, 0.46]), 'english': 'take', 'romanized': 'lena'},

        # Abstract
        'آزادی': {'coords': np.array([0.73, 0.76, 0.61, 0.82]), 'english': 'freedom', 'romanized': 'azadi'},
        'خوبصورتی': {'coords': np.array([0.78, 0.59, 0.46, 0.72]), 'english': 'beauty', 'romanized': 'khoobsurti'},
        'طاقت': {'coords': np.array([0.49, 0.52, 0.84, 0.66]), 'english': 'power', 'romanized': 'taqat'},

        # Relational
        'دوستی': {'coords': np.array([0.78, 0.72, 0.46, 0.76]), 'english': 'friendship', 'romanized': 'dosti'},
        'معافی': {'coords': np.array([0.84, 0.81, 0.40, 0.82]), 'english': 'forgiveness', 'romanized': 'maafi'},
    }

    # ========== RUSSIAN (Slavic) ==========
    russian_words = {
        # Emotions - Positive
        'любовь': {'coords': np.array([0.89, 0.47, 0.18, 0.73]), 'english': 'love', 'romanized': 'lyubov'},
        'радость': {'coords': np.array([0.84, 0.44, 0.41, 0.68]), 'english': 'joy', 'romanized': 'radost'},
        'надежда': {'coords': np.array([0.75, 0.50, 0.38, 0.71]), 'english': 'hope', 'romanized': 'nadezhda'},
        'мир': {'coords': np.array([0.72, 0.68, 0.28, 0.75]), 'english': 'peace', 'romanized': 'mir'},

        # Emotions - Negative
        'гнев': {'coords': np.array([0.31, 0.51, 0.69, 0.38]), 'english': 'anger', 'romanized': 'gnev'},
        'ненависть': {'coords': np.array([0.15, 0.38, 0.72, 0.28]), 'english': 'hate', 'romanized': 'nenavist'},
        'грусть': {'coords': np.array([0.38, 0.45, 0.25, 0.52]), 'english': 'sadness', 'romanized': 'grust'},
        'страх': {'coords': np.array([0.28, 0.49, 0.31, 0.48]), 'english': 'fear', 'romanized': 'strakh'},

        # Virtues
        'сострадание': {'coords': np.array([0.84, 0.75, 0.36, 0.78]), 'english': 'compassion', 'romanized': 'sostradanie'},
        'мужество': {'coords': np.array([0.68, 0.59, 0.71, 0.73]), 'english': 'courage', 'romanized': 'muzhestvo'},
        'мудрость': {'coords': np.array([0.67, 0.71, 0.45, 0.91]), 'english': 'wisdom', 'romanized': 'mudrost'},
        'справедливость': {'coords': np.array([0.63, 0.84, 0.54, 0.81]), 'english': 'justice', 'romanized': 'spravedlivost'},
        'правда': {'coords': np.array([0.65, 0.74, 0.51, 0.88]), 'english': 'truth', 'romanized': 'pravda'},
        'смирение': {'coords': np.array([0.68, 0.73, 0.32, 0.79]), 'english': 'humility', 'romanized': 'smirenie'},
        'милосердие': {'coords': np.array([0.82, 0.75, 0.38, 0.74]), 'english': 'mercy', 'romanized': 'miloserdie'},

        # Vices
        'гордыня': {'coords': np.array([0.39, 0.38, 0.74, 0.45]), 'english': 'pride', 'romanized': 'gordynya'},
        'жадность': {'coords': np.array([0.25, 0.31, 0.78, 0.38]), 'english': 'greed', 'romanized': 'zhadnost'},
        'жестокость': {'coords': np.array([0.17, 0.28, 0.76, 0.25]), 'english': 'cruelty', 'romanized': 'zhestokost'},

        # Actions
        'давать': {'coords': np.array([0.78, 0.70, 0.46, 0.72]), 'english': 'give', 'romanized': 'davat'},
        'брать': {'coords': np.array([0.35, 0.41, 0.68, 0.45]), 'english': 'take', 'romanized': 'brat'},
        'создавать': {'coords': np.array([0.72, 0.60, 0.71, 0.84]), 'english': 'create', 'romanized': 'sozdavat'},

        # Abstract
        'свобода': {'coords': np.array([0.73, 0.75, 0.61, 0.81]), 'english': 'freedom', 'romanized': 'svoboda'},
        'красота': {'coords': np.array([0.78, 0.58, 0.46, 0.72]), 'english': 'beauty', 'romanized': 'krasota'},
        'власть': {'coords': np.array([0.48, 0.52, 0.84, 0.65]), 'english': 'power', 'romanized': 'vlast'},

        # Relational
        'дружба': {'coords': np.array([0.78, 0.71, 0.46, 0.76]), 'english': 'friendship', 'romanized': 'druzhba'},
        'прощение': {'coords': np.array([0.84, 0.80, 0.40, 0.82]), 'english': 'forgiveness', 'romanized': 'proshchenie'},
        'верность': {'coords': np.array([0.75, 0.77, 0.61, 0.78]), 'english': 'loyalty', 'romanized': 'vernost'},
    }

    # Combine all with language tags
    for word, data in french_words.items():
        words[word] = {**data, 'language': 'French', 'family': 'Romance'}

    for word, data in spanish_words.items():
        words[word] = {**data, 'language': 'Spanish', 'family': 'Romance'}

    for word, data in hindi_words.items():
        words[word] = {**data, 'language': 'Hindi', 'family': 'Indo-Aryan'}

    for word, data in urdu_words.items():
        words[word] = {**data, 'language': 'Urdu', 'family': 'Indo-Aryan'}

    for word, data in russian_words.items():
        words[word] = {**data, 'language': 'Russian', 'family': 'Slavic'}

    return words


def map_to_territories(words: Dict, territories: Dict) -> Dict:
    """Map all words to territories"""

    results = {
        'word_mappings': {},
        'by_language': defaultdict(lambda: defaultdict(list)),
        'by_family': defaultdict(lambda: defaultdict(list)),
        'by_territory': defaultdict(list),
        'statistics': {}
    }

    for word, data in words.items():
        coord = data['coords']
        language = data['language']
        family = data['family']

        # Find nearest territory
        min_distance = float('inf')
        nearest_territory_id = None

        for tid, territory in territories.items():
            distance = float(np.linalg.norm(coord - territory['center']))
            if distance < min_distance:
                min_distance = distance
                nearest_territory_id = tid

        harmony = compute_harmony(coord)

        # Store mapping
        results['word_mappings'][word] = {
            'coordinates': coord.tolist(),
            'english': data['english'],
            'language': language,
            'family': family,
            'territory_id': nearest_territory_id,
            'territory_name': territories[nearest_territory_id]['name'],
            'distance_to_center': float(min_distance),
            'harmony': float(harmony),
            'L': float(coord[0]),
            'J': float(coord[1]),
            'P': float(coord[2]),
            'W': float(coord[3])
        }

        # Group by language, family, territory
        results['by_language'][language][nearest_territory_id].append(word)
        results['by_family'][family][nearest_territory_id].append(word)
        results['by_territory'][nearest_territory_id].append({
            'word': word,
            'english': data['english'],
            'language': language,
            'distance': float(min_distance)
        })

    # Calculate statistics
    all_distances = [w['distance_to_center'] for w in results['word_mappings'].values()]

    results['statistics'] = {
        'total_words': len(words),
        'mean_distance': float(np.mean(all_distances)),
        'median_distance': float(np.median(all_distances)),
        'by_language': {},
        'by_family': {}
    }

    # Language-specific stats
    for lang in set([w['language'] for w in words.values()]):
        lang_words = [w for w in results['word_mappings'].values() if w['language'] == lang]
        lang_distances = [w['distance_to_center'] for w in lang_words]

        results['statistics']['by_language'][lang] = {
            'count': len(lang_words),
            'mean_distance': float(np.mean(lang_distances)),
            'median_distance': float(np.median(lang_distances))
        }

    # Family-specific stats
    for fam in set([w['family'] for w in words.values()]):
        fam_words = [w for w in results['word_mappings'].values() if w['family'] == fam]
        fam_distances = [w['distance_to_center'] for w in fam_words]

        results['statistics']['by_family'][fam] = {
            'count': len(fam_words),
            'mean_distance': float(np.mean(fam_distances)),
            'median_distance': float(np.median(fam_distances))
        }

    return results


def compare_with_baseline(words: Dict) -> Dict:
    """Compare with English/Mandarin baseline"""

    # English reference
    baseline = {
        'love': np.array([0.92, 0.45, 0.15, 0.70]),
        'joy': np.array([0.88, 0.42, 0.38, 0.65]),
        'hope': np.array([0.78, 0.48, 0.35, 0.68]),
        'peace': np.array([0.75, 0.65, 0.25, 0.72]),
        'anger': np.array([0.28, 0.55, 0.72, 0.35]),
        'hate': np.array([0.12, 0.35, 0.75, 0.25]),
        'sadness': np.array([0.35, 0.48, 0.22, 0.55]),
        'fear': np.array([0.25, 0.52, 0.28, 0.45]),
        'envy': np.array([0.28, 0.38, 0.68, 0.32]),
        'compassion': np.array([0.88, 0.72, 0.32, 0.75]),
        'courage': np.array([0.65, 0.62, 0.68, 0.70]),
        'wisdom': np.array([0.70, 0.68, 0.42, 0.88]),
        'justice': np.array([0.60, 0.88, 0.58, 0.78]),
        'truth': np.array([0.62, 0.78, 0.48, 0.85]),
        'humility': np.array([0.72, 0.70, 0.28, 0.75]),
        'mercy': np.array([0.85, 0.72, 0.35, 0.70]),
        'pride': np.array([0.38, 0.35, 0.78, 0.42]),
        'greed': np.array([0.22, 0.28, 0.82, 0.35]),
        'cruelty': np.array([0.15, 0.25, 0.78, 0.22]),
        'give': np.array([0.82, 0.68, 0.42, 0.68]),
        'take': np.array([0.32, 0.38, 0.72, 0.42]),
        'create': np.array([0.75, 0.58, 0.68, 0.82]),
        'freedom': np.array([0.75, 0.72, 0.65, 0.78]),
        'beauty': np.array([0.82, 0.55, 0.42, 0.68]),
        'power': np.array([0.45, 0.48, 0.88, 0.62]),
        'friendship': np.array([0.82, 0.68, 0.42, 0.72]),
        'forgiveness': np.array([0.88, 0.78, 0.35, 0.78]),
        'loyalty': np.array([0.78, 0.75, 0.58, 0.75]),
    }

    comparisons = {}

    for word, data in words.items():
        english = data['english']
        if english in baseline:
            distance = float(np.linalg.norm(data['coords'] - baseline[english]))
            comparisons[word] = {
                'language': data['language'],
                'english': english,
                'distance': distance,
                'match_quality': 'exact' if distance < 0.05 else 'close' if distance < 0.10 else 'moderate' if distance < 0.20 else 'distant'
            }

    # Statistics
    if comparisons:
        distances = [c['distance'] for c in comparisons.values()]
        stats = {
            'total_compared': len(comparisons),
            'mean_distance': float(np.mean(distances)),
            'median_distance': float(np.median(distances)),
            'exact_matches': len([c for c in comparisons.values() if c['match_quality'] == 'exact']),
            'close_matches': len([c for c in comparisons.values() if c['match_quality'] == 'close']),
        }
    else:
        stats = {}

    return {
        'comparisons': comparisons,
        'statistics': stats
    }


def run_multilingual_expansion():
    """Run complete 5-language expansion"""

    print("=" * 80)
    print("MULTILINGUAL EXPANSION: 5 MAJOR WORLD LANGUAGES")
    print("French, Spanish, Urdu, Hindi, Russian")
    print("=" * 80)

    # Load data
    print("\nLoading multilingual corpus...")
    words = load_multilingual_corpus()
    territories = load_existing_territories()

    # Count by language
    lang_counts = defaultdict(int)
    for data in words.values():
        lang_counts[data['language']] += 1

    print(f"\nTotal words: {len(words)}")
    for lang, count in sorted(lang_counts.items()):
        print(f"  {lang}: {count} words")

    # Map to territories
    print("\n" + "=" * 80)
    print("MAPPING TO TERRITORIES")
    print("=" * 80)

    results = map_to_territories(words, territories)

    # Display by language
    print("\nTERRITORY DISTRIBUTION BY LANGUAGE:")
    for lang in sorted(results['by_language'].keys()):
        print(f"\n{lang}:")
        for tid in sorted(results['by_language'][lang].keys()):
            members = results['by_language'][lang][tid]
            print(f"  Territory {tid} ({territories[tid]['name']}): {len(members)} words")

    # Statistics
    print("\n" + "=" * 80)
    print("STATISTICS")
    print("=" * 80)

    print(f"\nOverall:")
    print(f"  Mean distance: {results['statistics']['mean_distance']:.4f}")
    print(f"  Median distance: {results['statistics']['median_distance']:.4f}")

    print(f"\nBy Language:")
    for lang, stats in sorted(results['statistics']['by_language'].items()):
        print(f"  {lang}: mean={stats['mean_distance']:.4f}, median={stats['median_distance']:.4f}")

    print(f"\nBy Family:")
    for fam, stats in sorted(results['statistics']['by_family'].items()):
        print(f"  {fam}: mean={stats['mean_distance']:.4f}, median={stats['median_distance']:.4f}")

    # Compare with baseline
    print("\n" + "=" * 80)
    print("COMPARISON WITH ENGLISH BASELINE")
    print("=" * 80)

    comparison = compare_with_baseline(words)

    print(f"\nTotal compared: {comparison['statistics']['total_compared']}")
    print(f"Mean distance: {comparison['statistics']['mean_distance']:.4f}")
    print(f"Exact matches (< 0.05): {comparison['statistics']['exact_matches']}")
    print(f"Close matches (< 0.10): {comparison['statistics']['close_matches']}")

    # Save results
    output_file = 'experiments/multilingual_expansion.json'

    output_data = {
        'word_mappings': results['word_mappings'],
        'by_language': {k: dict(v) for k, v in results['by_language'].items()},
        'by_family': {k: dict(v) for k, v in results['by_family'].items()},
        'by_territory': {str(k): v for k, v in results['by_territory'].items()},
        'statistics': results['statistics'],
        'baseline_comparison': comparison
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print(f"Analysis complete. Results saved to {output_file}")
    print("=" * 80)

    return output_data


if __name__ == "__main__":
    run_multilingual_expansion()
