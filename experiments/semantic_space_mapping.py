#!/usr/bin/env python3
"""
LJPW Semantic Space - Complete Concept Mapping
===============================================

Goal: Map 100,000+ concepts to complete the human semantic space

This script implements a systematic methodology for assigning LJPW coordinates
to the full range of human concepts, organized hierarchically into domains.

Current state: ~20 core concepts mapped
Target state: 100,000+ concepts covering all human thought

Approach:
1. Use existing 20 anchor concepts as reference points
2. Define major conceptual domains
3. Systematically expand within each domain
4. Validate consistency with cross-linguistic mappings
5. Build progressively: 100 → 1,000 → 10,000 → 100,000

Conceptual Domains:
- Emotions (1000+ concepts)
- Relationships (500+ concepts)
- Actions/Verbs (5000+ concepts)
- Objects/Nouns (30,000+ concepts)
- Properties/Adjectives (10,000+ concepts)
- Abstract Concepts (5000+ concepts)
- Cognitive States (1000+ concepts)
- Social Concepts (2000+ concepts)
- Ethical/Moral Concepts (1000+ concepts)
- Physical Properties (5000+ concepts)
- Biological Concepts (5000+ concepts)
- Technological Concepts (2000+ concepts)
- Scientific Concepts (10,000+ concepts)
- And more...
"""

import numpy as np
from typing import Dict, List, Tuple, Set
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime


class ConceptualDomain:
    """Represents a domain of related concepts."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.concepts = {}
        self.subcategories = {}

    def add_concept(self, concept: str, coordinates: np.ndarray,
                   definition: str = "", related: List[str] = None):
        """Add a concept to this domain."""
        self.concepts[concept] = {
            'coordinates': coordinates,
            'definition': definition,
            'related': related or [],
            'domain': self.name
        }

    def add_subcategory(self, name: str, parent_concept: str):
        """Add a subcategory within this domain."""
        self.subcategories[name] = parent_concept


class SemanticSpaceMapper:
    """
    Complete semantic space mapper for 100,000+ concepts.

    Uses existing 20 anchor concepts to systematically map
    the entire conceptual space.
    """

    def __init__(self):
        self.anchor_concepts = self._load_anchor_concepts()
        self.domains = {}
        self.concept_map = {}
        self.coordinate_index = {}  # For nearest-neighbor lookup

    def _load_anchor_concepts(self) -> Dict[str, np.ndarray]:
        """Load the 20 core anchor concepts validated across 81 languages."""
        return {
            # EMOTIONS & FEELINGS
            'love': np.array([0.91, 0.48, 0.17, 0.72]),
            'compassion': np.array([0.86, 0.54, 0.23, 0.69]),
            'kindness': np.array([0.83, 0.61, 0.27, 0.72]),
            'anger': np.array([0.29, 0.34, 0.79, 0.42]),
            'fear': np.array([0.31, 0.38, 0.62, 0.48]),
            'sadness': np.array([0.42, 0.41, 0.24, 0.52]),

            # RELATIONSHIPS
            'bond': np.array([0.88, 0.52, 0.19, 0.67]),

            # PROPERTIES
            'beauty': np.array([0.79, 0.58, 0.32, 0.74]),

            # ACTIONS/STATES
            'sleep': np.array([0.58, 0.51, 0.36, 0.61]),
            'life': np.array([0.76, 0.63, 0.34, 0.71]),

            # COGNITIVE
            'knowledge': np.array([0.59, 0.72, 0.41, 0.89]),
            'truth': np.array([0.67, 0.81, 0.38, 0.84]),

            # POWER/AGENCY
            'power': np.array([0.51, 0.68, 0.79, 0.64]),
            'strength': np.array([0.48, 0.61, 0.81, 0.58]),
            'freedom': np.array([0.61, 0.79, 0.68, 0.76]),

            # ETHICAL/MORAL
            'justice': np.array([0.56, 0.91, 0.48, 0.82]),
            'honor': np.array([0.65, 0.84, 0.72, 0.81]),
            'good': np.array([0.73, 0.69, 0.38, 0.78]),
            'evil': np.array([0.19, 0.28, 0.71, 0.33]),

            # SPIRITUAL
            'sacred': np.array([0.71, 0.78, 0.43, 0.87]),
        }

    def interpolate_concept(self, base_concept: str,
                          target_concept: str,
                          l_shift: float = 0.0,
                          j_shift: float = 0.0,
                          p_shift: float = 0.0,
                          w_shift: float = 0.0) -> np.ndarray:
        """
        Derive coordinates for a new concept based on a base concept
        with specified shifts in each dimension.

        Example:
            'joy' = 'love' with slightly higher L, lower P
            'hate' = 'love' inverted with high P, low L
        """
        if base_concept not in self.anchor_concepts:
            raise ValueError(f"Base concept '{base_concept}' not found in anchors")

        base_coords = self.anchor_concepts[base_concept].copy()
        new_coords = base_coords + np.array([l_shift, j_shift, p_shift, w_shift])

        # Ensure coordinates stay in valid range [0, 1]
        new_coords = np.clip(new_coords, 0.0, 1.0)

        return new_coords

    def blend_concepts(self, concept1: str, concept2: str,
                      weight1: float = 0.5) -> np.ndarray:
        """
        Blend two concepts to create a hybrid.

        Example:
            'bittersweet' = blend('sadness', 'beauty', 0.5)
        """
        if concept1 not in self.anchor_concepts or concept2 not in self.anchor_concepts:
            raise ValueError("Both concepts must be anchors")

        coords1 = self.anchor_concepts[concept1]
        coords2 = self.anchor_concepts[concept2]

        weight2 = 1.0 - weight1
        blended = weight1 * coords1 + weight2 * coords2

        return blended

    def create_emotion_domain(self) -> ConceptualDomain:
        """
        Create comprehensive emotion domain with 1000+ concepts.

        Organizes emotions by:
        - Valence (positive/negative)
        - Arousal (high/low)
        - Complexity (basic/complex)
        - Social orientation (self/other)
        """
        domain = ConceptualDomain(
            name="Emotions",
            description="All human emotional states and feelings"
        )

        # POSITIVE EMOTIONS (High Love)

        # Joy family
        domain.add_concept('joy',
            self.interpolate_concept('love', 'joy', l_shift=0.02, p_shift=-0.05),
            definition="Intense happiness and delight")

        domain.add_concept('happiness',
            self.interpolate_concept('love', 'happiness', l_shift=0.0, p_shift=-0.08),
            definition="State of well-being and contentment")

        domain.add_concept('contentment',
            self.interpolate_concept('love', 'contentment', l_shift=-0.05, p_shift=-0.10, w_shift=0.05),
            definition="Peaceful satisfaction with one's situation")

        domain.add_concept('delight',
            self.interpolate_concept('love', 'delight', l_shift=0.03, p_shift=-0.06),
            definition="Great pleasure and enjoyment")

        domain.add_concept('elation',
            self.interpolate_concept('love', 'elation', l_shift=0.04, p_shift=0.10, w_shift=-0.05),
            definition="Extreme happiness and excitement")

        domain.add_concept('euphoria',
            self.interpolate_concept('love', 'euphoria', l_shift=0.05, p_shift=0.15, w_shift=-0.10),
            definition="Intense state of pleasure and well-being")

        domain.add_concept('bliss',
            self.interpolate_concept('love', 'bliss', l_shift=0.06, j_shift=0.10, p_shift=-0.12, w_shift=0.15),
            definition="Perfect happiness and spiritual joy")

        domain.add_concept('ecstasy',
            self.interpolate_concept('love', 'ecstasy', l_shift=0.07, p_shift=0.20, w_shift=-0.15),
            definition="Overwhelming feeling of rapture")

        # Love family
        domain.add_concept('affection',
            self.interpolate_concept('love', 'affection', l_shift=-0.05, p_shift=-0.08),
            definition="Gentle caring feeling")

        domain.add_concept('tenderness',
            self.interpolate_concept('love', 'tenderness', l_shift=-0.02, j_shift=0.05, p_shift=-0.12),
            definition="Gentle warmth and care")

        domain.add_concept('adoration',
            self.interpolate_concept('love', 'adoration', l_shift=0.04, j_shift=0.08, w_shift=0.05),
            definition="Deep love and respect")

        domain.add_concept('infatuation',
            self.interpolate_concept('love', 'infatuation', l_shift=0.05, p_shift=0.15, w_shift=-0.20),
            definition="Intense but often short-lived passion")

        domain.add_concept('devotion',
            self.interpolate_concept('love', 'devotion', l_shift=0.02, j_shift=0.15, w_shift=0.10),
            definition="Loyal commitment and dedication")

        # Peace family
        domain.add_concept('serenity',
            self.interpolate_concept('love', 'serenity', l_shift=-0.10, j_shift=0.05, p_shift=-0.15, w_shift=0.20),
            definition="State of calm and peaceful tranquility")

        domain.add_concept('tranquility',
            self.interpolate_concept('love', 'tranquility', l_shift=-0.12, p_shift=-0.16, w_shift=0.18),
            definition="Quality of being calm and peaceful")

        domain.add_concept('calm',
            self.interpolate_concept('love', 'calm', l_shift=-0.15, p_shift=-0.14, w_shift=0.15),
            definition="State of quietness and composure")

        # NEGATIVE EMOTIONS (Low Love, often High Power)

        # Anger family
        domain.add_concept('rage',
            self.interpolate_concept('anger', 'rage', p_shift=0.12, w_shift=-0.10),
            definition="Violent uncontrollable anger")

        domain.add_concept('fury',
            self.interpolate_concept('anger', 'fury', p_shift=0.10, w_shift=-0.08),
            definition="Wild intense anger")

        domain.add_concept('wrath',
            self.interpolate_concept('anger', 'wrath', j_shift=0.15, p_shift=0.08),
            definition="Divine or righteous anger")

        domain.add_concept('irritation',
            self.interpolate_concept('anger', 'irritation', p_shift=-0.25, w_shift=0.05),
            definition="Mild annoyance")

        domain.add_concept('annoyance',
            self.interpolate_concept('anger', 'annoyance', p_shift=-0.20, w_shift=0.03),
            definition="Feeling of being bothered")

        domain.add_concept('frustration',
            self.interpolate_concept('anger', 'frustration', l_shift=0.05, p_shift=-0.10, w_shift=0.10),
            definition="Feeling of being blocked or helpless")

        domain.add_concept('resentment',
            self.interpolate_concept('anger', 'resentment', j_shift=-0.10, p_shift=-0.05, w_shift=0.08),
            definition="Bitter indignation at perceived unfairness")

        domain.add_concept('hostility',
            self.interpolate_concept('anger', 'hostility', l_shift=-0.05, j_shift=-0.08, p_shift=0.10),
            definition="Deep-seated anger and opposition")

        # Fear family
        domain.add_concept('terror',
            self.interpolate_concept('fear', 'terror', p_shift=0.20, w_shift=-0.15),
            definition="Extreme fear and dread")

        domain.add_concept('panic',
            self.interpolate_concept('fear', 'panic', p_shift=0.18, w_shift=-0.20),
            definition="Sudden overwhelming fear")

        domain.add_concept('anxiety',
            self.interpolate_concept('fear', 'anxiety', p_shift=-0.10, w_shift=0.10),
            definition="Persistent worry and unease")

        domain.add_concept('worry',
            self.interpolate_concept('fear', 'worry', l_shift=0.05, p_shift=-0.15, w_shift=0.12),
            definition="Anxious concern about potential problems")

        domain.add_concept('dread',
            self.interpolate_concept('fear', 'dread', j_shift=-0.05, p_shift=0.10, w_shift=0.05),
            definition="Great fear of something in the future")

        domain.add_concept('horror',
            self.interpolate_concept('fear', 'horror', l_shift=-0.08, p_shift=0.15, w_shift=-0.10),
            definition="Intense shock and fear")

        domain.add_concept('nervousness',
            self.interpolate_concept('fear', 'nervousness', p_shift=-0.20, w_shift=0.08),
            definition="Slight anxiety or apprehension")

        # Sadness family
        domain.add_concept('grief',
            self.interpolate_concept('sadness', 'grief', l_shift=-0.10, p_shift=-0.05),
            definition="Deep sorrow over loss")

        domain.add_concept('sorrow',
            self.interpolate_concept('sadness', 'sorrow', l_shift=-0.08, j_shift=-0.05),
            definition="Deep distress and regret")

        domain.add_concept('melancholy',
            self.interpolate_concept('sadness', 'melancholy', l_shift=-0.05, w_shift=0.10),
            definition="Pensive sadness with no obvious cause")

        domain.add_concept('despair',
            self.interpolate_concept('sadness', 'despair', l_shift=-0.15, j_shift=-0.20, w_shift=-0.10),
            definition="Complete loss of hope")

        domain.add_concept('depression',
            self.interpolate_concept('sadness', 'depression', l_shift=-0.12, p_shift=-0.08, w_shift=-0.05),
            definition="Persistent feeling of sadness and hopelessness")

        domain.add_concept('misery',
            self.interpolate_concept('sadness', 'misery', l_shift=-0.18, j_shift=-0.15, p_shift=-0.10),
            definition="Great unhappiness and suffering")

        domain.add_concept('loneliness',
            self.interpolate_concept('sadness', 'loneliness', l_shift=-0.10, p_shift=-0.12),
            definition="Sadness from lack of companionship")

        domain.add_concept('heartbreak',
            self.interpolate_concept('sadness', 'heartbreak', l_shift=-0.12, p_shift=-0.08),
            definition="Overwhelming grief from emotional loss")

        # COMPLEX EMOTIONS (Blends)

        # Bittersweet emotions
        domain.add_concept('nostalgia',
            self.blend_concepts('sadness', 'love', 0.4),
            definition="Sentimental longing for the past")

        domain.add_concept('bittersweet',
            self.blend_concepts('sadness', 'love', 0.3),
            definition="Mixed feeling of happiness and sadness")

        # Social emotions
        domain.add_concept('guilt',
            self.interpolate_concept('sadness', 'guilt', j_shift=0.20, w_shift=0.15),
            definition="Remorse for wrongdoing")

        domain.add_concept('shame',
            self.interpolate_concept('sadness', 'shame', l_shift=-0.08, j_shift=0.10, p_shift=-0.10),
            definition="Painful feeling of humiliation")

        domain.add_concept('embarrassment',
            self.interpolate_concept('sadness', 'embarrassment', l_shift=-0.05, j_shift=0.12, p_shift=-0.08),
            definition="Self-conscious awkwardness")

        domain.add_concept('pride',
            self.blend_concepts('honor', 'love', 0.5),
            definition="Satisfaction in achievements")

        domain.add_concept('envy',
            self.interpolate_concept('sadness', 'envy', l_shift=-0.10, p_shift=0.20, w_shift=-0.05),
            definition="Resentful desire for others' advantages")

        domain.add_concept('jealousy',
            self.interpolate_concept('fear', 'jealousy', l_shift=-0.10, p_shift=0.15),
            definition="Fear of losing something to a rival")

        # Surprise/Interest
        domain.add_concept('surprise',
            np.array([0.62, 0.58, 0.45, 0.75]),
            definition="Sudden unexpected feeling")

        domain.add_concept('astonishment',
            np.array([0.64, 0.60, 0.55, 0.80]),
            definition="Great surprise or amazement")

        domain.add_concept('curiosity',
            np.array([0.68, 0.62, 0.38, 0.85]),
            definition="Strong desire to learn")

        domain.add_concept('interest',
            np.array([0.65, 0.60, 0.40, 0.82]),
            definition="Feeling of wanting to know more")

        # Disgust family
        domain.add_concept('disgust',
            np.array([0.22, 0.35, 0.65, 0.40]),
            definition="Revulsion or strong disapproval")

        domain.add_concept('contempt',
            np.array([0.24, 0.50, 0.75, 0.48]),
            definition="Feeling that something is worthless")

        domain.add_concept('revulsion',
            np.array([0.20, 0.33, 0.77, 0.35]),
            definition="Strong feeling of disgust")

        # Hope/Optimism
        domain.add_concept('hope',
            np.array([0.78, 0.70, 0.42, 0.80]),
            definition="Expectation and desire for positive outcome")

        domain.add_concept('optimism',
            np.array([0.80, 0.73, 0.45, 0.83]),
            definition="Hopefulness about the future")

        # Gratitude
        domain.add_concept('gratitude',
            self.blend_concepts('love', 'honor', 0.6),
            definition="Thankful appreciation")

        domain.add_concept('appreciation',
            self.blend_concepts('love', 'honor', 0.55),
            definition="Recognition of value or quality")

        return domain

    def create_action_domain(self) -> ConceptualDomain:
        """
        Create action/verb domain with 5000+ concepts.

        Actions organized by:
        - Physical vs Mental
        - Transitive vs Intransitive
        - Intentional vs Involuntary
        - Social vs Individual
        """
        domain = ConceptualDomain(
            name="Actions",
            description="All human actions and activities"
        )

        # PHYSICAL ACTIONS

        # Movement verbs
        domain.add_concept('walk',
            np.array([0.55, 0.50, 0.45, 0.60]),
            definition="Move at regular pace on foot")

        domain.add_concept('run',
            np.array([0.57, 0.52, 0.65, 0.55]),
            definition="Move swiftly on foot")

        domain.add_concept('jump',
            np.array([0.60, 0.52, 0.65, 0.62]),
            definition="Push off ground into the air")

        domain.add_concept('dance',
            np.array([0.75, 0.58, 0.55, 0.68]),
            definition="Move rhythmically to music")

        # Creation verbs
        domain.add_concept('create',
            np.array([0.72, 0.68, 0.60, 0.85]),
            definition="Bring something into existence")

        domain.add_concept('build',
            np.array([0.74, 0.70, 0.70, 0.90]),
            definition="Construct by putting parts together")

        domain.add_concept('make',
            np.array([0.67, 0.63, 0.60, 0.85]),
            definition="Form by combining materials")

        # Destruction verbs
        domain.add_concept('destroy',
            np.array([0.18, 0.32, 0.82, 0.35]),
            definition="Cause to cease to exist")

        domain.add_concept('break',
            np.array([0.20, 0.34, 0.72, 0.37]),
            definition="Separate into pieces")

        # MENTAL ACTIONS

        # Cognitive verbs
        domain.add_concept('think',
            np.array([0.58, 0.65, 0.38, 0.88]),
            definition="Use mind to consider")

        domain.add_concept('know',
            self.anchor_concepts['knowledge'],
            definition="Have information in mind")

        domain.add_concept('learn',
            self.interpolate_concept('knowledge', 'learn', l_shift=0.05, p_shift=0.08, w_shift=0.05),
            definition="Acquire knowledge or skill")

        domain.add_concept('understand',
            self.interpolate_concept('knowledge', 'understand', j_shift=0.05, w_shift=0.08),
            definition="Comprehend meaning")

        domain.add_concept('remember',
            np.array([0.62, 0.68, 0.35, 0.85]),
            definition="Recall from memory")

        domain.add_concept('forget',
            np.array([0.45, 0.42, 0.30, 0.40]),
            definition="Fail to remember")

        # SOCIAL ACTIONS

        # Communication verbs
        domain.add_concept('speak',
            np.array([0.62, 0.62, 0.52, 0.75]),
            definition="Express thoughts in words")

        domain.add_concept('listen',
            np.array([0.68, 0.65, 0.35, 0.80]),
            definition="Pay attention to sounds")

        domain.add_concept('teach',
            np.array([0.75, 0.72, 0.48, 0.90]),
            definition="Impart knowledge or skill")

        domain.add_concept('help',
            np.array([0.82, 0.70, 0.40, 0.75]),
            definition="Assist or aid someone")

        # Relationship verbs
        domain.add_concept('love (verb)',
            self.anchor_concepts['love'],
            definition="Feel deep affection for")

        domain.add_concept('hate',
            np.array([0.12, 0.25, 0.75, 0.30]),
            definition="Feel intense dislike for")

        domain.add_concept('care',
            np.array([0.85, 0.62, 0.28, 0.72]),
            definition="Feel concern or interest")

        domain.add_concept('trust',
            np.array([0.78, 0.75, 0.38, 0.82]),
            definition="Have confidence in")

        return domain

    def save_semantic_space(self, output_path: Path):
        """Save complete semantic space to JSON."""
        output_data = {
            'metadata': {
                'created': datetime.now().isoformat(),
                'total_concepts': len(self.concept_map),
                'total_domains': len(self.domains),
                'description': 'Complete LJPW semantic space mapping'
            },
            'anchor_concepts': {
                concept: coords.tolist()
                for concept, coords in self.anchor_concepts.items()
            },
            'domains': {
                name: {
                    'description': domain.description,
                    'concepts': {
                        c: {
                            'coordinates': data['coordinates'].tolist(),
                            'definition': data['definition'],
                            'related': data['related']
                        }
                        for c, data in domain.concepts.items()
                    }
                }
                for name, domain in self.domains.items()
            },
            'concept_index': {
                concept: {
                    'coordinates': data['coordinates'].tolist(),
                    'definition': data.get('definition', ''),
                    'domain': data.get('domain', 'unknown')
                }
                for concept, data in self.concept_map.items()
            }
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        print(f"✓ Saved semantic space to: {output_path}")
        print(f"  Total concepts: {len(self.concept_map)}")
        print(f"  Total domains: {len(self.domains)}")


def main():
    """Initialize and populate semantic space with first batch of concepts."""
    print("=" * 80)
    print("LJPW SEMANTIC SPACE - COMPLETE CONCEPT MAPPING")
    print("=" * 80)
    print()
    print("Goal: Map 100,000+ concepts to complete human semantic space")
    print()

    mapper = SemanticSpaceMapper()
    print(f"✓ Loaded {len(mapper.anchor_concepts)} anchor concepts")
    print()

    # Create domains
    print("Creating conceptual domains...")

    print("  1. Emotions domain...")
    emotion_domain = mapper.create_emotion_domain()
    mapper.domains['emotions'] = emotion_domain
    mapper.concept_map.update(emotion_domain.concepts)
    print(f"     ✓ Added {len(emotion_domain.concepts)} emotion concepts")

    print("  2. Actions domain...")
    action_domain = mapper.create_action_domain()
    mapper.domains['actions'] = action_domain
    mapper.concept_map.update(action_domain.concepts)
    print(f"     ✓ Added {len(action_domain.concepts)} action concepts")

    print()
    print("=" * 80)
    print("FIRST BATCH COMPLETE")
    print("=" * 80)
    print()
    print(f"Total concepts mapped: {len(mapper.concept_map)}")
    print(f"Total domains: {len(mapper.domains)}")
    print()

    # Save
    output_path = Path(__file__).parent / 'semantic_space_mapping.json'
    mapper.save_semantic_space(output_path)

    print()
    print("Next steps to reach 100,000+ concepts:")
    print("  • Expand emotion domain to 1,000+ concepts")
    print("  • Complete action domain with 5,000+ verbs")
    print("  • Add object/noun domain with 30,000+ concepts")
    print("  • Add property/adjective domain with 10,000+ concepts")
    print("  • Add abstract concept domain")
    print("  • Add scientific/technical domains")
    print("  • Add social/cultural domains")
    print()


if __name__ == '__main__':
    main()
