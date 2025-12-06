"""
Context Integrator for Universal Translation System
Handles phrase-level and sentence-level semantic analysis with context awareness.
"""

import numpy as np
import re
from typing import Dict, List, Optional, Tuple, Any

# Natural constants for decay
PHI = (1 + np.sqrt(5)) / 2  # Golden ratio
PHI_INV = 1 / PHI


class ContextIntegrator:
    """Analyzes semantic relationships in multi-word phrases and sentences."""
    
    def __init__(self):
        """Initialize context integrator with compound concept patterns."""
        # Multi-word spiritual/theological compounds (EXPANDED)
        self.compound_patterns = {
            # Core Divine Concepts
            'kingdom_of_god': {
                'pattern': r'\b(kingdom|reign|rule)\s+(of|ana)\s+(god|heaven|divine)',
                'boost': {'L': 0.20, 'J': 0.25, 'P': 0.10, 'W': 0.30},
                'confidence': 1.0,
                'override_semantic': True
            },
            'holy_spirit': {
                'pattern': r'\b(holy|sacred|divine)\s+(spirit|ghost|breath)',
                'boost': {'L': 0.25, 'J': 0.20, 'P': 0.20, 'W': 0.35},
                'confidence': 1.0,
                'override_semantic': True
            },
            'son_of_god': {
                'pattern': r'\b(son|child)\s+(of|ana)\s+(god|divine|heaven)',
                'boost': {'L': 0.30, 'J': 0.25, 'P': 0.20, 'W': 0.30},
                'confidence': 1.0,
                'override_semantic': True
            },
            'word_of_god': {
                'pattern': r'\b(word|message|teaching|gospel)\s+(of|ana)\s+(god|lord)',
                'boost': {'L': 0.25, 'J': 0.30, 'P': 0.15, 'W': 0.40},
                'confidence': 1.0,
                'override_semantic': True
            },
            'love_of_god': {
                'pattern': r'\b(love|mercy|compassion)\s+(of|ana)\s+(god|divine)',
                'boost': {'L': 0.45, 'J': 0.20, 'P': 0.10, 'W': 0.30},
                'confidence': 1.0,
                'override_semantic': True
            },
            
            # Christ-Centered Concepts
            'love_of_christ': {
                'pattern': r'\b(love|grace|mercy)\s+(of|ana)\s+(christ|jesus|messiah)',
                'boost': {'L': 0.45, 'J': 0.20, 'P': 0.10, 'W': 0.30},
                'confidence': 1.0,
                'override_semantic': True
            },
            'body_of_christ': {
                'pattern': r'\b(body|church)\s+(of|ana)\s+(christ|jesus)',
                'boost': {'L': 0.35, 'J': 0.25, 'P': 0.20, 'W': 0.25},
                'confidence': 1.0,
                'override_semantic': True
            },
            'blood_of_christ': {
                'pattern': r'\b(blood|sacrifice)\s+(of|ana)\s+(christ|jesus|lamb)',
                'boost': {'L': 0.40, 'J': 0.30, 'P': 0.25, 'W': 0.30},
                'confidence': 1.0,
                'override_semantic': True
            },
            'lamb_of_god': {
                'pattern': r'\b(lamb|sacrifice)\s+(of|ana)\s+(god)',
                'boost': {'L': 0.40, 'J': 0.30, 'P': 0.20, 'W': 0.30},
                'confidence': 1.0,
                'override_semantic': True
            },
            
            # Divine Attributes
            'grace_of_god': {
                'pattern': r'\b(grace|favor|blessing)\s+(of|ana)\s+(god|lord)',
                'boost': {'L': 0.45, 'J': 0.25, 'P': 0.15, 'W': 0.30},
                'confidence': 1.0,
                'override_semantic': True
            },
            'will_of_god': {
                'pattern': r'\b(will|purpose|plan)\s+(of|ana)\s+(god|lord|heaven)',
                'boost': {'L': 0.30, 'J': 0.35, 'P': 0.25, 'W': 0.40},
                'confidence': 1.0,
                'override_semantic': True
            },
            'glory_of_god': {
                'pattern': r'\b(glory|splendor|majesty)\s+(of|ana)\s+(god|lord)',
                'boost': {'L': 0.35, 'J': 0.30, 'P': 0.35, 'W': 0.35},
                'confidence': 1.0,
                'override_semantic': True
            },
            'power_of_god': {
                'pattern': r'\b(power|might|strength)\s+(of|ana)\s+(god|lord)',
                'boost': {'L': 0.30, 'J': 0.30, 'P': 0.40, 'W': 0.35},
                'confidence': 1.0,
                'override_semantic': True
            },
            'wisdom_of_god': {
                'pattern': r'\b(wisdom|knowledge|understanding)\s+(of|ana)\s+(god|lord)',
                'boost': {'L': 0.30, 'J': 0.30, 'P': 0.20, 'W': 0.45},
                'confidence': 1.0,
                'override_semantic': True
            },
            'presence_of_god': {
                'pattern': r'\b(presence|face|dwelling)\s+(of|ana)\s+(god|lord)',
                'boost': {'L': 0.40, 'J': 0.25, 'P': 0.30, 'W': 0.35},
                'confidence': 1.0,
                'override_semantic': True
            },
            
            # Spiritual Entities & Concepts
            'spirit_of_truth': {
                'pattern': r'\b(spirit)\s+(of|ana)\s+(truth)',
                'boost': {'L': 0.30, 'J': 0.35, 'P': 0.25, 'W': 0.45},
                'confidence': 1.0,
                'override_semantic': True
            },
            'name_of_the_lord': {
                'pattern': r'\b(name)\s+(of|ana)\s+(the\s+)?(lord|god)',
                'boost': {'L': 0.30, 'J': 0.35, 'P': 0.30, 'W': 0.35},
                'confidence': 1.0,
                'override_semantic': True
            },
            'fear_of_the_lord': {
                'pattern': r'\b(fear|reverence|awe)\s+(of|ana)\s+(the\s+)?(lord|god)',
                'boost': {'L': 0.25, 'J': 0.40, 'P': 0.30, 'W': 0.40},
                'confidence': 1.0,
                'override_semantic': True
            },
            
            # Community Concepts
            'people_of_god': {
                'pattern': r'\b(people|children|nation)\s+(of|ana)\s+(god|lord)',
                'boost': {'L': 0.35, 'J': 0.30, 'P': 0.20, 'W': 0.25},
                'confidence': 1.0,
                'override_semantic': True
            },
            'church_of_god': {
                'pattern': r'\b(church|assembly|congregation)\s+(of|ana)\s+(god|lord|christ)',
                'boost': {'L': 0.35, 'J': 0.30, 'P': 0.25, 'W': 0.30},
                'confidence': 1.0,
                'override_semantic': True
            },
            'bride_of_christ': {
                'pattern': r'\b(bride)\s+(of|ana)\s+(christ|lamb)',
                'boost': {'L': 0.45, 'J': 0.25, 'P': 0.20, 'W': 0.30},
                'confidence': 1.0,
                'override_semantic': True
            }
        }
        
        # Relationship patterns (subject-verb-object)
        self.relationship_patterns = {
            'divine_action': r'\b(god|lord|divine)\s+(creates?|makes?|gives?|loves?|judges?)',
            'human_worship': r'\b(we|I|they|people)\s+(worship|praise|honor|glorify)',
            'moral_action': r'\b(we|I|they|people)\s+(sin|err|fail|transgress|repent)',
            'power_display': r'\b(god|lord|spirit)\s+(rules?|reigns?|commands?|destroys?)'
        }
    
    def detect_compound_concepts(self, text: str) -> List[Dict[str, Any]]:
        """
        Detect multi-word compound concepts in text.
        
        Returns:
            List of detected compounds with their boosts
        """
        text_lower = text.lower()
        detected = []
        
        for concept_name, config in self.compound_patterns.items():
            if re.search(config['pattern'], text_lower, re.IGNORECASE):
                detected.append({
                    'concept': concept_name,
                    'boost': config['boost'],
                    'confidence': config.get('confidence', 0.9),
                    'override_semantic': config.get('override_semantic', False)
                })
        
        return detected
    
    def analyze_phrase_structure(self, text: str) -> Dict[str, Any]:
        """
        Analyze the semantic structure of a phrase.
        
        Returns:
            Dictionary with phrase analysis results
        """
        words = text.split()
        word_count = len(words)
        
        # Detect compounds
        compounds = self.detect_compound_concepts(text)
        
        # Analyze word relationships
        relationships = self._detect_relationships(text)
        
        # Calculate phrase coherence (how well words fit together)
        coherence = self._calculate_phrase_coherence(words)
        
        return {
            'word_count': word_count,
            'compounds': compounds,
            'relationships': relationships,
            'coherence': coherence,
            'is_compound': len(compounds) > 0
        }
    
    def _detect_relationships(self, text: str) -> List[str]:
        """Detect semantic relationship patterns in text."""
        text_lower = text.lower()
        detected = []
        
        for rel_type, pattern in self.relationship_patterns.items():
            if re.search(pattern, text_lower, re.IGNORECASE):
                detected.append(rel_type)
        
        return detected
    
    def _calculate_phrase_coherence(self, words: List[str]) -> float:
        """
        Calculate how coherent a phrase is (0-1).
        Higher coherence means words likely form a semantic unit.
        """
        if len(words) <= 1:
            return 0.5  # Single words have neutral coherence (not a phrase)
        
        # Simple heuristic: shorter phrases with function words are more coherent
        function_words = {'of', 'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'with', 'by'}
        function_word_count = sum(1 for w in words if w.lower() in function_words)
        
        # Phrases with 2-4 words and function words are likely compounds
        if 2 <= len(words) <= 4 and function_word_count > 0:
            return 0.8
        
        # Simple 2-word phrases without function words are not coherent compounds
        if len(words) == 2 and function_word_count == 0:
            return 0.3
        
        # Longer phrases are less coherent as single units
        return max(0.3, 1.0 - (len(words) - 2) * 0.15)
    
    def calculate_semantic_flow(self, text: str) -> Dict[str, Any]:
        """
        Track semantic progression through a sentence.
        
        Analyzes how meaning builds from beginning to end.
        """
        words = text.split()
        if len(words) <= 1:
            return {
                'flow_detected': False,
                'progression': [],
                'narrative_arc': 'static'
            }
        
        # Detect narrative structure
        narrative_arc = self._detect_narrative_arc(text)
        
        # Track semantic shifts
        shifts = self._detect_semantic_shifts(words)
        
        return {
            'flow_detected': True,
            'word_count': len(words),
            'narrative_arc': narrative_arc,
            'semantic_shifts': shifts,
            'flow_strength': len(shifts) / max(len(words) - 1, 1)
        }
    
    def _detect_narrative_arc(self, text: str) -> str:
        """Detect the narrative structure of a sentence."""
        text_lower = text.lower()
        
        # Question
        if '?' in text or any(text_lower.startswith(q) for q in ['who', 'what', 'where', 'when', 'why', 'how']):
            return 'question'
        
        # Command
        command_verbs = ['go', 'come', 'do', 'make', 'give', 'take', 'see', 'hear', 'say', 'tell']
        if any(text_lower.startswith(v) for v in command_verbs):
            return 'command'
        
        # Conditional
        if 'if' in text_lower or 'when' in text_lower:
            return 'conditional'
        
        # Default: statement
        return 'statement'
    
    def _detect_semantic_shifts(self, words: List[str]) -> List[Dict[str, Any]]:
        """Detect points where semantic meaning shifts in a sentence."""
        shifts = []
        
        # Detect conjunctions and transitions
        transition_words = {
            'but': 'contrast',
            'however': 'contrast',
            'yet': 'contrast',
            'and': 'addition',
            'also': 'addition',
            'or': 'alternative',
            'because': 'causation',
            'therefore': 'conclusion',
            'thus': 'conclusion'
        }
        
        for i, word in enumerate(words):
            word_lower = word.lower()
            if word_lower in transition_words:
                shifts.append({
                    'position': i,
                    'word': word,
                    'type': transition_words[word_lower]
                })
        
        return shifts
    
    def apply_context_window(
        self, 
        target_word: str, 
        surrounding_words: List[str], 
        window_size: int = 5
    ) -> Dict[str, Any]:
        """
        Apply context window with golden ratio decay.
        
        Args:
            target_word: The word being analyzed
            surrounding_words: List of words in order (target word should be included)
            window_size: How many words on each side to consider
            
        Returns:
            Context influence scores
        """
        # Find target word position
        try:
            target_idx = surrounding_words.index(target_word)
        except ValueError:
            return {'influence': 0.0, 'context_words': []}
        
        context_influences = []
        
        # Look at words before and after
        for i, word in enumerate(surrounding_words):
            if i == target_idx:
                continue
            
            distance = abs(i - target_idx)
            if distance > window_size:
                continue
            
            # Golden ratio decay: closer words have more influence
            influence = PHI_INV ** distance
            
            context_influences.append({
                'word': word,
                'distance': distance,
                'influence': influence,
                'position': 'before' if i < target_idx else 'after'
            })
        
        # Sort by influence (strongest first)
        context_influences.sort(key=lambda x: x['influence'], reverse=True)
        
        total_influence = sum(c['influence'] for c in context_influences)
        
        return {
            'total_influence': total_influence,
            'context_words': context_influences,
            'window_size': window_size
        }
    
    def integrate_context_into_signature(
        self,
        base_signature: Dict[str, float],
        phrase_analysis: Dict[str, Any],
        flow_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Integrate context analysis into LJPW signature.
        
        Args:
            base_signature: Initial LJPW coordinates
            phrase_analysis: Results from analyze_phrase_structure
            flow_analysis: Results from calculate_semantic_flow
            
        Returns:
            Enhanced signature with context integration
        """
        enhanced = base_signature.copy()
        evidence = []
        context_conf = 0.0
        
        # Apply compound concept boosts
        if phrase_analysis.get('compounds'):
            for compound in phrase_analysis['compounds']:
                boost = compound['boost']
                confidence = compound['confidence']
                override_semantic = compound.get('override_semantic', False)
                
                for dimension, value in boost.items():
                    enhanced[dimension] = enhanced.get(dimension, 0.5) + (value * confidence)
                
                evidence.append(f"Compound: {compound['concept']} (conf: {confidence:.2f})")
                
                # If override_semantic is True, force high context confidence
                if override_semantic:
                    context_conf = max(context_conf, 1.0)
                else:
                    context_conf = max(context_conf, confidence * 0.8)
        
        # Apply relationship pattern boosts
        if phrase_analysis.get('relationships'):
            for rel_type in phrase_analysis['relationships']:
                if rel_type == 'divine_action':
                    enhanced['P'] = enhanced.get('P', 0.5) + 0.15
                    enhanced['W'] = enhanced.get('W', 0.5) + 0.10
                    evidence.append(f"Relationship: {rel_type}")
                elif rel_type == 'human_worship':
                    enhanced['L'] = enhanced.get('L', 0.5) + 0.20
                    enhanced['W'] = enhanced.get('W', 0.5) + 0.15
                    evidence.append(f"Relationship: {rel_type}")
                elif rel_type == 'moral_action':
                    enhanced['J'] = enhanced.get('J', 0.5) + 0.20
                    evidence.append(f"Relationship: {rel_type}")
            
            context_conf = max(context_conf, 0.6)
        
        # Apply coherence boost (high coherence = treat as single concept)
        coherence = phrase_analysis.get('coherence', 0.5)
        if coherence > 0.7:
            # High coherence means the phrase should be treated as a unified concept
            # Boost confidence in the signature
            evidence.append(f"High phrase coherence: {coherence:.2f}")
            context_conf = max(context_conf, coherence * 0.7)
        
        # Apply narrative arc influence
        if flow_analysis.get('flow_detected'):
            arc = flow_analysis.get('narrative_arc', 'statement')
            if arc == 'question':
                enhanced['W'] = enhanced.get('W', 0.5) + 0.10  # Questions seek wisdom
                evidence.append("Narrative: Question")
                context_conf = max(context_conf, 0.4)
            elif arc == 'command':
                enhanced['P'] = enhanced.get('P', 0.5) + 0.15  # Commands exert power
                enhanced['J'] = enhanced.get('J', 0.5) + 0.10  # Commands establish order
                evidence.append("Narrative: Command")
                context_conf = max(context_conf, 0.5)
        
        # Normalize to [0, 1]
        for dim in ['L', 'J', 'P', 'W']:
            enhanced[dim] = np.clip(enhanced.get(dim, 0.5), 0, 1)
        
        # Only return confidence if we actually found context evidence
        final_conf = context_conf if len(evidence) > 0 else 0.0
        
        return {
            'signature': enhanced,
            'evidence': evidence,
            'context_confidence': min(final_conf, 1.0)
        }


if __name__ == "__main__":
    # Test the context integrator
    integrator = ContextIntegrator()
    
    print("="*70)
    print("CONTEXT INTEGRATOR TEST")
    print("="*70)
    
    # Test 1: Compound concept detection
    print("\n1. Compound Concept Detection:")
    test_phrases = [
        "Kingdom of God",
        "Holy Spirit",
        "The love of God",
        "Simple word"
    ]
    
    for phrase in test_phrases:
        analysis = integrator.analyze_phrase_structure(phrase)
        print(f"\n  '{phrase}':")
        print(f"    Compounds: {len(analysis['compounds'])}")
        if analysis['compounds']:
            for c in analysis['compounds']:
                print(f"      - {c['concept']} (conf: {c['confidence']:.2f})")
        print(f"    Coherence: {analysis['coherence']:.2f}")
    
    # Test 2: Context window
    print("\n\n2. Context Window (Golden Ratio Decay):")
    sentence = "The king rules with justice and mercy"
    words = sentence.split()
    target = "rules"
    
    context = integrator.apply_context_window(target, words, window_size=3)
    print(f"\n  Sentence: '{sentence}'")
    print(f"  Target: '{target}'")
    print(f"  Total Influence: {context['total_influence']:.3f}")
    print(f"  Context words:")
    for cw in context['context_words'][:3]:
        print(f"    - '{cw['word']}' (distance={cw['distance']}, influence={cw['influence']:.3f})")
    
    # Test 3: Semantic flow
    print("\n\n3. Semantic Flow Analysis:")
    test_sentences = [
        "God creates the heavens and the earth",
        "If you believe, you will be saved",
        "Go and make disciples"
    ]
    
    for sentence in test_sentences:
        flow = integrator.calculate_semantic_flow(sentence)
        print(f"\n  '{sentence}':")
        print(f"    Arc: {flow['narrative_arc']}")
        print(f"    Shifts: {len(flow.get('semantic_shifts', []))}")
    
    print("\n" + "="*70)
    print("Context Integrator initialized successfully!")
    print("="*70)
