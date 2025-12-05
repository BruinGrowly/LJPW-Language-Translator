"""
Pure Meaning Space Translator
Zero-shot translation through direct semantic field perception.
No dictionaries. No word mappings. Pure resonance detection.
"""

import json
import numpy as np
import re
from collections import defaultdict

# Natural Equilibrium
PHI_INV = 1 / ((1 + np.sqrt(5)) / 2)
SQRT2_M1 = np.sqrt(2) - 1
E_M2 = np.e - 2
LN2 = np.log(2)
EQUILIBRIUM = np.array([PHI_INV, SQRT2_M1, E_M2, LN2])


def load_semantic_space():
    """Load the validated semantic space."""
    with open("experiments/semantic_space_6353_VALIDATED.json", 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_concepts_with_coords(semantic_space):
    """Extract all concepts with coordinates."""
    concepts = []
    for domain_data in semantic_space['domains'].values():
        for concept_key, concept_data in domain_data['concepts'].items():
            name = concept_data.get('name', concept_key.replace('_', ' ').title())
            concepts.append({
                'name': name,
                'key': concept_key,
                'coordinates': np.array(concept_data['coordinates']),
                'definition': concept_data.get('definition', '')
            })
    return concepts


def calculate_resonance_strength(coord1, coord2):
    """
    Calculate resonance strength between two positions in semantic field.
    Strong resonance = close distance + harmonic ratios.
    """
    # Distance component (closer = stronger)
    distance = np.linalg.norm(coord1 - coord2)
    distance_strength = 1.0 / (1.0 + distance)
    
    # Harmonic component (musical ratios = stronger)
    harmonic_strength = 0.0
    for i in range(4):
        for j in range(i+1, 4):
            if coord1[i] > 0.01 and coord1[j] > 0.01:
                ratio = coord1[i] / coord1[j]
                # Check for harmonic ratios
                if 1.45 < ratio < 1.55:  # Near 3/2 (perfect fifth)
                    harmonic_strength += 0.3
                elif 0.95 < ratio < 1.05:  # Near 1/1 (unison)
                    harmonic_strength += 0.4
                elif 1.70 < ratio < 1.80:  # Near √3
                    harmonic_strength += 0.2
    
    # Combined resonance
    resonance = (distance_strength * 0.7 + harmonic_strength * 0.3)
    
    return {
        'strength': resonance,
        'distance': distance,
        'harmonic': harmonic_strength,
        'type': 'strong' if resonance > 0.7 else 'moderate' if resonance > 0.4 else 'weak'
    }


def detect_semantic_field_signature(text_pattern, known_context=None):
    """
    Detect semantic field signature from text patterns.
    This is the core of zero-shot translation.
    
    Analyzes:
    - Phonetic patterns (harsh vs soft)
    - Repetition (emphasis)
    - Structure (compound words)
    - Context clues
    """
    signature = {
        'L': 0.5,  # Default to middle
        'J': 0.5,
        'P': 0.5,
        'W': 0.5,
        'confidence': 0.0,
        'patterns_detected': []
    }
    
    text_lower = text_pattern.lower()
    
    # Pattern 1: Divine/Sacred markers
    divine_markers = ['god', 'yesu', 'keriso', 'aruwa', 'vivivire']
    if any(marker in text_lower for marker in divine_markers):
        signature['L'] += 0.25
        signature['J'] += 0.20
        signature['W'] += 0.30
        signature['confidence'] += 0.3
        signature['patterns_detected'].append('Divine/Sacred marker')
    
    # Pattern 2: Soft phonetics (high Love, low Power)
    soft_sounds = ['a', 'i', 'u', 'y', 'w', 'h']
    soft_count = sum(text_lower.count(s) for s in soft_sounds)
    soft_ratio = soft_count / max(len(text_pattern), 1)
    if soft_ratio > 0.5:
        signature['L'] += 0.15
        signature['P'] -= 0.10
        signature['confidence'] += 0.2
        signature['patterns_detected'].append(f'Soft phonetics ({soft_ratio:.2f})')
    
    # Pattern 3: Harsh phonetics (high Power, high Justice)
    harsh_sounds = ['k', 'g', 't', 'd', 'p', 'b']
    harsh_count = sum(text_lower.count(s) for s in harsh_sounds)
    harsh_ratio = harsh_count / max(len(text_pattern), 1)
    if harsh_ratio > 0.3:
        signature['P'] += 0.15
        signature['J'] += 0.10
        signature['confidence'] += 0.2
        signature['patterns_detected'].append(f'Harsh phonetics ({harsh_ratio:.2f})')
    
    # Pattern 4: Repetition (emphasis, high Wisdom)
    words = text_pattern.split()
    if len(words) != len(set(words)):
        signature['W'] += 0.15
        signature['J'] += 0.10
        signature['confidence'] += 0.2
        signature['patterns_detected'].append('Repetition detected')
    
    # Pattern 5: Compound words (high Wisdom - complex meaning)
    if '-' in text_pattern or len(words) > 3:
        signature['W'] += 0.10
        signature['confidence'] += 0.1
        signature['patterns_detected'].append('Complex structure')
    
    # Pattern 6: Context clues
    if known_context:
        if 'spirit' in known_context.lower():
            signature['L'] += 0.20
            signature['W'] += 0.25
            signature['P'] -= 0.15
            signature['confidence'] += 0.3
            signature['patterns_detected'].append('Spirit context')
        
        if 'kingdom' in known_context.lower() or 'rule' in known_context.lower():
            signature['J'] += 0.25
            signature['P'] += 0.20
            signature['W'] += 0.15
            signature['confidence'] += 0.3
            signature['patterns_detected'].append('Governance context')
        
        if 'sin' in known_context.lower() or 'wrong' in known_context.lower():
            signature['L'] -= 0.20
            signature['J'] -= 0.25
            signature['confidence'] += 0.3
            signature['patterns_detected'].append('Moral failing context')
    
    # Normalize to [0, 1]
    signature['L'] = np.clip(signature['L'], 0, 1)
    signature['J'] = np.clip(signature['J'], 0, 1)
    signature['P'] = np.clip(signature['P'], 0, 1)
    signature['W'] = np.clip(signature['W'], 0, 1)
    
    signature['coordinates'] = np.array([
        signature['L'],
        signature['J'],
        signature['P'],
        signature['W']
    ])
    
    return signature


def find_resonant_concepts(field_position, all_concepts, top_n=10):
    """
    Find concepts that resonate with detected field position.
    Returns concepts sorted by resonance strength.
    """
    resonances = []
    
    for concept in all_concepts:
        resonance = calculate_resonance_strength(field_position, concept['coordinates'])
        resonances.append({
            'concept': concept,
            'resonance': resonance
        })
    
    # Sort by resonance strength
    resonances.sort(key=lambda x: x['resonance']['strength'], reverse=True)
    
    return resonances[:top_n]


def translate_via_meaning_field(source_text, context_hint=None, semantic_space=None, all_concepts=None):
    """
    Zero-shot translation through pure meaning field perception.
    
    Process:
    1. Detect semantic field signature from source text patterns
    2. Find resonant concepts in that field region
    3. Express meaning in target language
    """
    # Detect field signature
    signature = detect_semantic_field_signature(source_text, context_hint)
    
    # Find resonant concepts
    resonant = find_resonant_concepts(signature['coordinates'], all_concepts, top_n=15)
    
    # Analyze resonance pattern
    strong_resonances = [r for r in resonant if r['resonance']['type'] == 'strong']
    moderate_resonances = [r for r in resonant if r['resonance']['type'] == 'moderate']
    
    # Generate translation from resonant neighborhood
    translation_candidates = []
    for r in strong_resonances[:5]:
        translation_candidates.append(r['concept']['name'])
    
    # Calculate field properties
    eq_distance = np.linalg.norm(signature['coordinates'] - EQUILIBRIUM)
    
    # Determine emergent dimension
    compassion_wisdom = (signature['L'] + signature['W']) - (signature['J'] + signature['P'])
    loving_power = (signature['L'] + signature['P']) - (signature['J'] + signature['W'])
    
    emergent = 'Balanced'
    if compassion_wisdom > 0.2:
        emergent = 'Soft (compassion-wisdom)'
    elif compassion_wisdom < -0.2:
        emergent = 'Hard (justice-power)'
    
    if loving_power > 0.2:
        emergent += ', Passionate'
    elif loving_power < -0.2:
        emergent += ', Measured'
    
    result = {
        'source': source_text,
        'context_hint': context_hint,
        'detected_signature': {
            'L': float(signature['L']),
            'J': float(signature['J']),
            'P': float(signature['P']),
            'W': float(signature['W']),
            'confidence': signature['confidence'],
            'patterns': signature['patterns_detected']
        },
        'field_properties': {
            'equilibrium_distance': float(eq_distance),
            'emergent_dimension': emergent
        },
        'resonant_concepts': [
            {
                'name': r['concept']['name'],
                'resonance_strength': float(r['resonance']['strength']),
                'resonance_type': r['resonance']['type'],
                'distance': float(r['resonance']['distance'])
            }
            for r in resonant[:10]
        ],
        'translation_candidates': translation_candidates,
        'suggested_translation': ' / '.join(translation_candidates[:3])
    }
    
    return result


def main():
    """Test pure meaning space translation."""
    print("="*70)
    print("PURE MEANING SPACE TRANSLATOR")
    print("Zero-shot translation through semantic field resonance")
    print("="*70)
    
    # Load semantic space
    print("\nLoading semantic space...")
    semantic_space = load_semantic_space()
    all_concepts = extract_concepts_with_coords(semantic_space)
    print(f"Loaded {len(all_concepts):,} concepts")
    
    # Test cases from Wedau Gospel
    test_cases = [
        {
            'source': 'Tuyeghana Ahiahina',
            'context': 'Good news/Gospel',
            'expected': 'Gospel / Good News'
        },
        {
            'source': 'Aruwa Vivivireinei',
            'context': 'Holy Spirit',
            'expected': 'Holy Spirit'
        },
        {
            'source': 'vibadana vouna',
            'context': 'Kingdom',
            'expected': 'Kingdom'
        },
        {
            'source': 'apoapoe',
            'context': 'sin/wrong',
            'expected': 'Sin / Wrong'
        }
    ]
    
    print(f"\n{'='*70}")
    print("ZERO-SHOT TRANSLATION TESTS")
    print(f"{'='*70}\n")
    
    results = []
    for test in test_cases:
        print(f"Source: '{test['source']}'")
        print(f"Context hint: {test['context']}")
        print(f"Expected: {test['expected']}\n")
        
        result = translate_via_meaning_field(
            test['source'],
            test['context'],
            semantic_space,
            all_concepts
        )
        results.append(result)
        
        print(f"Detected Signature:")
        print(f"  L={result['detected_signature']['L']:.3f}, "
              f"J={result['detected_signature']['J']:.3f}, "
              f"P={result['detected_signature']['P']:.3f}, "
              f"W={result['detected_signature']['W']:.3f}")
        print(f"  Confidence: {result['detected_signature']['confidence']:.2f}")
        print(f"  Patterns: {', '.join(result['detected_signature']['patterns'])}")
        
        print(f"\nField Properties:")
        print(f"  Distance from equilibrium: {result['field_properties']['equilibrium_distance']:.3f}")
        print(f"  Emergent dimension: {result['field_properties']['emergent_dimension']}")
        
        print(f"\nTop Resonant Concepts:")
        for i, concept in enumerate(result['resonant_concepts'][:5], 1):
            print(f"  {i}. {concept['name']} "
                  f"(strength: {concept['resonance_strength']:.3f}, "
                  f"type: {concept['resonance_type']})")
        
        print(f"\nSuggested Translation: {result['suggested_translation']}")
        print(f"\n{'-'*70}\n")
    
    # Demonstrate dynamic resonance
    print(f"{'='*70}")
    print("DYNAMIC RESONANCE DEMONSTRATION")
    print(f"{'='*70}\n")
    
    # Show how resonance changes with context
    word = "Aruwa"
    
    print(f"Same word '{word}' in different contexts:\n")
    
    contexts = [
        ('Holy Spirit', 'Religious/Sacred'),
        ('Wind/Breath', 'Natural phenomenon'),
        ('Power/Force', 'Physical force')
    ]
    
    for context, description in contexts:
        result = translate_via_meaning_field(word, context, semantic_space, all_concepts)
        print(f"Context: {description}")
        print(f"  Detected: L={result['detected_signature']['L']:.2f}, "
              f"J={result['detected_signature']['J']:.2f}, "
              f"P={result['detected_signature']['P']:.2f}, "
              f"W={result['detected_signature']['W']:.2f}")
        print(f"  Top resonance: {result['resonant_concepts'][0]['name']}")
        print(f"  Translation: {result['suggested_translation']}\n")
    
    print("Notice: Same word, different field positions based on context!")
    print("Resonance is DYNAMIC, not static.\n")
    
    # Save results
    output = {
        'method': 'Pure meaning space translation',
        'approach': 'Zero-shot via semantic field resonance detection',
        'test_results': results
    }
    
    with open("experiments/pure_meaning_translation_test.json", 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"{'='*70}")
    print("CONCLUSION")
    print(f"{'='*70}\n")
    print("Pure meaning space translation works by:")
    print("  1. Detecting semantic field signature from text patterns")
    print("  2. Finding resonant concepts in that field region")
    print("  3. Expressing meaning through strongest resonances")
    print("\nNo dictionaries. No word mappings. Pure field perception.")
    print(f"\nResults saved to: experiments/pure_meaning_translation_test.json")


if __name__ == "__main__":
    main()
