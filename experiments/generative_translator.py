"""
Generative Translator
Generates actual translations from LJPW coordinates using template-based composition
"""

import sys
sys.path.append('experiments')

from enhanced_pattern_detector import EnhancedPatternDetector
from theological_dictionary import TheologicalDictionary
import numpy as np
import json


class GenerativeTranslator:
    """
    Generate translations from LJPW coordinates.
    
    Approach:
    1. Find nearest theological terms
    2. Use template-based composition
    3. Validate semantic preservation
    """
    
    def __init__(self):
        self.detector = EnhancedPatternDetector()
        self.dictionary = TheologicalDictionary()
        
        # Load verse corpus for templates
        self.corpus = self._load_corpus()
        
        # Translation templates
        self.templates = self._build_templates()
    
    def _load_corpus(self) -> dict:
        """Load verse corpus."""
        with open('experiments/nwt_mark_chapter1.json', 'r', encoding='utf-8') as f:
            return json.load(f)['verses']
    
    def _build_templates(self) -> dict:
        """Build translation templates."""
        return {
            'divine_declaration': [
                "You are {subject}, {descriptor}",
                "{subject} is {descriptor}",
                "This is {subject}, {descriptor}"
            ],
            'action_statement': [
                "{subject} {action} {object}",
                "{subject} will {action} {object}",
                "And {subject} {action} {object}"
            ],
            'teaching': [
                "{subject} said: {message}",
                "{subject} taught them, saying: {message}",
                "He proclaimed: {message}"
            ],
            'prophecy': [
                "The {concept} has {state}",
                "{concept} is {state}",
                "Behold, {concept} {state}"
            ]
        }
    
    def find_nearest_terms(self, coords: list, top_n: int = 5) -> list:
        """Find nearest theological terms to coordinates."""
        return self.dictionary.search_similar(coords, threshold=0.30)[:top_n]
    
    def classify_semantic_type(self, coords: list) -> str:
        """
        Classify the semantic type based on coordinates.
        
        High L, High J, Low P = Divine declaration
        Moderate L, Moderate J, High P = Action statement
        High W, Moderate J = Teaching
        High J, High W, Moderate P = Prophecy
        """
        L, J, P, W = coords
        
        if L > 0.80 and J > 0.80 and P < 0.60:
            return 'divine_declaration'
        elif P > 0.70:
            return 'action_statement'
        elif W > 0.85 and J > 0.70:
            return 'teaching'
        elif J > 0.80 and W > 0.80:
            return 'prophecy'
        else:
            return 'action_statement'  # Default
    
    def generate_from_coordinates(self, coords: list, language: str = 'english') -> dict:
        """
        Generate translation from LJPW coordinates.
        
        Returns multiple candidates with confidence scores.
        """
        # Find nearest terms
        nearest_terms = self.find_nearest_terms(coords)
        
        # Classify semantic type
        semantic_type = self.classify_semantic_type(coords)
        
        # Get templates
        templates = self.templates.get(semantic_type, self.templates['action_statement'])
        
        # Generate candidates
        candidates = []
        
        # Strategy 1: Use nearest corpus verse
        nearest_verse = self._find_nearest_corpus_verse(coords)
        candidates.append({
            'text': nearest_verse['text'],
            'method': 'nearest_corpus',
            'distance': nearest_verse['distance'],
            'confidence': 1.0 - (nearest_verse['distance'] / 2.0)
        })
        
        # Strategy 2: Template-based with theological terms
        if nearest_terms:
            for template in templates[:2]:  # Use top 2 templates
                # Simple template filling (proof of concept)
                filled = template.format(
                    subject=nearest_terms[0]['term'] if len(nearest_terms) > 0 else "He",
                    descriptor=nearest_terms[1]['term'] if len(nearest_terms) > 1 else "blessed",
                    action="proclaimed" if coords[2] > 0.6 else "spoke",
                    object=nearest_terms[2]['term'] if len(nearest_terms) > 2 else "truth",
                    message=nearest_terms[0]['term'] if len(nearest_terms) > 0 else "the word",
                    concept=nearest_terms[0]['term'] if len(nearest_terms) > 0 else "kingdom",
                    state="near" if coords[2] < 0.6 else "come"
                )
                
                # Calculate how well generated text matches target coords
                gen_sig = self.detector.calculate_field_signature(filled)
                gen_coords = [gen_sig['L'], gen_sig['J'], gen_sig['P'], gen_sig['W']]
                distance = np.linalg.norm(np.array(coords) - np.array(gen_coords))
                
                candidates.append({
                    'text': filled,
                    'method': 'template',
                    'template': template,
                    'distance': float(distance),
                    'confidence': 1.0 - (distance / 2.0)
                })
        
        # Sort by confidence
        candidates.sort(key=lambda x: x['confidence'], reverse=True)
        
        return {
            'target_coords': coords,
            'semantic_type': semantic_type,
            'nearest_terms': [t['term'] for t in nearest_terms],
            'candidates': candidates,
            'best_candidate': candidates[0] if candidates else None
        }
    
    def _find_nearest_corpus_verse(self, coords: list) -> dict:
        """Find nearest verse in corpus."""
        min_distance = float('inf')
        nearest_verse = None
        
        for verse_num, text in self.corpus.items():
            sig = self.detector.calculate_field_signature(text)
            verse_coords = [sig['L'], sig['J'], sig['P'], sig['W']]
            distance = np.linalg.norm(np.array(coords) - np.array(verse_coords))
            
            if distance < min_distance:
                min_distance = distance
                nearest_verse = {
                    'verse': verse_num,
                    'text': text,
                    'coords': verse_coords,
                    'distance': float(distance)
                }
        
        return nearest_verse


def test_generative_translator():
    """Test generative translation."""
    translator = GenerativeTranslator()
    
    print("="*80)
    print("GENERATIVE TRANSLATOR TEST")
    print("="*80)
    print("\nGenerating translations from LJPW coordinates\n")
    
    # Test cases: specific coordinate patterns
    test_cases = [
        {
            'name': 'Divine Declaration',
            'coords': [0.90, 0.90, 0.50, 0.95],  # High L, High J, Low P, High W
            'description': 'God speaking about His nature'
        },
        {
            'name': 'Action Statement',
            'coords': [0.70, 0.70, 0.85, 0.75],  # Moderate L/J, High P
            'description': 'Physical action or event'
        },
        {
            'name': 'Teaching/Wisdom',
            'coords': [0.75, 0.80, 0.60, 0.92],  # High W, Moderate others
            'description': 'Instructional content'
        },
        {
            'name': 'Prophecy',
            'coords': [0.70, 0.88, 0.75, 0.90],  # High J, High W
            'description': 'Prophetic declaration'
        }
    ]
    
    results = []
    
    for test in test_cases:
        print(f"\n{'='*80}")
        print(f"Test: {test['name']}")
        print(f"Description: {test['description']}")
        print(f"Target Coords: {test['coords']}")
        print('='*80)
        
        result = translator.generate_from_coordinates(test['coords'])
        results.append(result)
        
        print(f"\nSemantic Type: {result['semantic_type']}")
        print(f"Nearest Terms: {', '.join(result['nearest_terms'][:3])}")
        
        print(f"\nGenerated Candidates:")
        for i, candidate in enumerate(result['candidates'][:3], 1):
            print(f"\n{i}. [{candidate['method'].upper()}] (confidence: {candidate['confidence']:.2f})")
            print(f"   {candidate['text'][:80]}...")
            print(f"   Distance: {candidate['distance']:.3f}")
    
    # Overall statistics
    print(f"\n{'='*80}")
    print("OVERALL STATISTICS")
    print('='*80)
    
    avg_best_confidence = np.mean([r['best_candidate']['confidence'] for r in results])
    avg_best_distance = np.mean([r['best_candidate']['distance'] for r in results])
    
    print(f"\nAverage Best Candidate:")
    print(f"  Confidence: {avg_best_confidence:.2f}")
    print(f"  Distance: {avg_best_distance:.3f}")
    
    # Save results
    with open('experiments/generative_translation_results.json', 'w', encoding='utf-8') as f:
        json.dump({
            'test_cases': test_cases,
            'results': results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved to: experiments/generative_translation_results.json")
    
    # Recommendations
    print(f"\n{'='*80}")
    print("NEXT STEPS FOR GENERATIVE TRANSLATION")
    print('='*80)
    print("\nCurrent Approach (Proof of Concept):")
    print("  - Template-based composition")
    print("  - Nearest corpus verse")
    print("  - Theological term insertion")
    
    print(f"\nFuture Enhancements:")
    print("  1. Neural generation (GPT-style with LJPW guidance)")
    print("  2. Syntax-aware composition")
    print("  3. Multi-word phrase templates")
    print("  4. Language-specific generation")
    print("  5. Context-aware generation (surrounding verses)")
    
    print(f"\n{'='*80}")
    print("GENERATIVE TRANSLATOR TEST COMPLETE")
    print("="*80)


if __name__ == "__main__":
    test_generative_translator()
