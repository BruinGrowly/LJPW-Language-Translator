"""
Generate Abstract Concepts
Expands the library with 60 concepts related to intellectual, philosophical, and intangible ideas.
Target: 380 -> 440 concepts.
"""

import json
import numpy as np

def generate_abstract_concepts():
    """Generate 60 abstract concepts with LJPW coordinates."""
    
    # L = Value/Worth (High: Good/Beauty, Low: Evil/Ugly)
    # J = Justice/Truth (High: Fact/Logic, Low: Lie/Chaos)
    # P = Power/Impact (High: Cause/Force, Low: Effect/Potential)
    # W = Wisdom/Meaning (High: Idea/Theory, Low: Noise/Data)

    concepts = {
        # --- PHILOSOPHY / EXISTENCE ---
        'truth': {
            'name': 'Truth',
            'definition': 'That which is true or in accordance with fact or reality',
            'coordinates': [0.85, 0.95, 0.70, 0.90] # High J, W
        },
        'reality': {
            'name': 'Reality',
            'definition': 'The world or the state of things as they actually exist',
            'coordinates': [0.70, 0.90, 0.80, 0.80]
        },
        'existence': {
            'name': 'Existence',
            'definition': 'The fact or state of living or having objective reality',
            'coordinates': [0.80, 0.80, 0.70, 0.80]
        },
        'being': {
            'name': 'Being',
            'definition': 'The nature or essence of a person',
            'coordinates': [0.90, 0.70, 0.60, 0.90]
        },
        'nothingness': {
            'name': 'Nothingness',
            'definition': 'The absence or cessation of life or existence',
            'coordinates': [0.20, 0.20, 0.10, 0.20] # Low everything
        },
        'time': {
            'name': 'Time',
            'definition': 'The indefinite continued progress of existence',
            'coordinates': [0.50, 0.90, 0.60, 0.90] # High J (Order), W
        },
        'space': {
            'name': 'Space',
            'definition': 'Continuous area or expanse which is free',
            'coordinates': [0.60, 0.70, 0.50, 0.80]
        },
        'eternity': {
            'name': 'Eternity',
            'definition': 'Infinite or unending time',
            'coordinates': [0.90, 0.90, 0.80, 1.00] # Max W
        },
        'infinity': {
            'name': 'Infinity',
            'definition': 'The state or quality of being infinite',
            'coordinates': [0.85, 0.85, 0.85, 1.00]
        },
        'void': {
            'name': 'Void',
            'definition': 'A completely empty space',
            'coordinates': [0.30, 0.30, 0.20, 0.30]
        },

        # --- LOGIC / CAUSALITY ---
        'cause': {
            'name': 'Cause',
            'definition': 'A person or thing that gives rise to an action',
            'coordinates': [0.50, 0.80, 0.90, 0.70] # High P
        },
        'effect': {
            'name': 'Effect',
            'definition': 'A change which is a result or consequence of an action',
            'coordinates': [0.50, 0.70, 0.50, 0.60]
        },
        'reason': {
            'name': 'Reason',
            'definition': 'A cause, explanation, or justification',
            'coordinates': [0.60, 0.90, 0.50, 0.90] # High J, W
        },
        'logic': {
            'name': 'Logic',
            'definition': 'Reasoning conducted or assessed according to strict principles',
            'coordinates': [0.50, 0.95, 0.60, 0.90] # Very High J
        },
        'proof': {
            'name': 'Proof',
            'definition': 'Evidence or argument establishing or helping to establish a fact',
            'coordinates': [0.60, 0.95, 0.70, 0.85]
        },
        'theory': {
            'name': 'Theory',
            'definition': 'Supposition or a system of ideas intended to explain something',
            'coordinates': [0.60, 0.70, 0.50, 0.95] # High W
        },
        'hypothesis': {
            'name': 'Hypothesis',
            'definition': 'Proposed explanation made on the basis of limited evidence',
            'coordinates': [0.50, 0.60, 0.40, 0.90]
        },
        'conclusion': {
            'name': 'Conclusion',
            'definition': 'A judgment or decision reached by reasoning',
            'coordinates': [0.60, 0.90, 0.60, 0.80]
        },
        'paradox': {
            'name': 'Paradox',
            'definition': 'Situation/Statement that contradicts itself',
            'coordinates': [0.50, 0.30, 0.60, 0.95] # High W, Low J (Confusion)
        },
        'chance': {
            'name': 'Chance',
            'definition': 'The occurrence of events in the absence of any obvious intention',
            'coordinates': [0.50, 0.20, 0.60, 0.50] # Low J (Random)
        },

        # --- VALUES / ETHICS ---
        'good': {
            'name': 'Good',
            'definition': 'To be desired or approved of',
            'coordinates': [0.95, 0.90, 0.70, 0.90] # High L, J
        },
        'evil': {
            'name': 'Evil',
            'definition': 'Profoundly immoral and malevolent',
            'coordinates': [0.05, 0.10, 0.80, 0.20] # Very Low L, J
        },
        'right': {
            'name': 'Right',
            'definition': 'Morally good, justified, or acceptable',
            'coordinates': [0.80, 0.95, 0.60, 0.85] # High J
        },
        'wrong': {
            'name': 'Wrong',
            'definition': 'Unjust, dishonest, or immoral',
            'coordinates': [0.20, 0.10, 0.50, 0.30] # Low J
        },
        'justice': {
            'name': 'Justice',
            'definition': 'Just behavior or treatment',
            'coordinates': [0.80, 0.98, 0.75, 0.90] # Max J
        },
        'virtue': {
            'name': 'Virtue',
            'definition': 'Behavior showing high moral standards',
            'coordinates': [0.90, 0.90, 0.60, 0.90]
        },
        'vice': {
            'name': 'Vice',
            'definition': 'Immoral or wicked behavior',
            'coordinates': [0.20, 0.20, 0.50, 0.30]
        },
        'freedom_concept': { # Renamed to avoid collision with emotional 'Freedom'
            'name': 'Liberty', 
            'definition': 'The state of being free within society',
            'coordinates': [0.80, 0.85, 0.70, 0.80]
        },
        'duty': {
            'name': 'Duty',
            'definition': 'Moral or legal obligation',
            'coordinates': [0.60, 0.90, 0.70, 0.75] # High J
        },
        'honor': {
            'name': 'Honor',
            'definition': 'High respect; great esteem',
            'coordinates': [0.80, 0.85, 0.75, 0.80]
        },

        # --- KNOWLEDGE / DOMAINS ---
        'knowledge': {
            'name': 'Knowledge',
            'definition': 'Facts, information, and skills acquired by a person',
            'coordinates': [0.60, 0.70, 0.60, 0.95] # High W
        },
        'science': {
            'name': 'Science',
            'definition': 'Systematic study of the structure and behavior of the physical world',
            'coordinates': [0.50, 0.90, 0.70, 0.95] # High J, W
        },
        'art': {
            'name': 'Art',
            'definition': 'Expression of human creative skill and imagination',
            'coordinates': [0.90, 0.40, 0.60, 0.90] # High L, W, Low J (Creative/Free)
        },
        'history': {
            'name': 'History',
            'definition': 'Study of past events',
            'coordinates': [0.60, 0.80, 0.50, 0.85]
        },
        'math': {
            'name': 'Mathematics',
            'definition': 'Abstract science of number, quantity, and space',
            'coordinates': [0.50, 0.95, 0.60, 0.95] # High J, W
        },
        'language': {
            'name': 'Language',
            'definition': 'Method of human communication',
            'coordinates': [0.80, 0.70, 0.60, 0.90]
        },
        'music': {
            'name': 'Music',
            'definition': 'Vocal or instrumental sounds',
            'coordinates': [0.90, 0.50, 0.50, 0.80] # High L
        },
        'law': {
            'name': 'Law',
            'definition': 'System of rules',
            'coordinates': [0.50, 0.95, 0.80, 0.80] # High J
        },
        'politics': {
            'name': 'Politics',
            'definition': 'Activities associated with the governance of a country',
            'coordinates': [0.40, 0.60, 0.90, 0.70] # High P
        },
        'economics': {
            'name': 'Economics',
            'definition': 'Production, consumption, and transfer of wealth',
            'coordinates': [0.50, 0.70, 0.80, 0.80]
        },

        # --- QUALITIES / ATTRIBUTES ---
        'strength': {
            'name': 'Strength',
            'definition': 'Quality or state of being physically strong',
            'coordinates': [0.60, 0.70, 0.95, 0.60] # High P
        },
        'weakness': {
            'name': 'Weakness',
            'definition': 'State or condition of lacking strength',
            'coordinates': [0.40, 0.30, 0.20, 0.40] # Low P
        },
        'beauty': {
            'name': 'Beauty',
            'definition': 'Quality that gives pleasure to the senses',
            'coordinates': [0.95, 0.60, 0.50, 0.80] # High L
        },
        'wisdom': {
            'name': 'Wisdom',
            'definition': 'Quality of having experience, knowledge, and good judgment',
            'coordinates': [0.85, 0.90, 0.60, 0.98] # Max W
        },
        'power': {
            'name': 'Power',
            'definition': 'Ability to do something or act in a particular way',
            'coordinates': [0.50, 0.70, 0.98, 0.70] # Max P
        },
        'peace': {
            'name': 'Peace',
            'definition': 'Freedom from disturbance; tranquility',
            'coordinates': [0.90, 0.95, 0.30, 0.80] # High L, J
        },
        'chaos': {
            'name': 'Chaos',
            'definition': 'Complete disorder and confusion',
            'coordinates': [0.20, 0.10, 0.80, 0.20] # Very Low J
        },
        'balance': {
            'name': 'Balance',
            'definition': 'Even distribution of weight enabling someone or something to remain upright',
            'coordinates': [0.70, 0.90, 0.50, 0.80] # High J
        },
        'potential': {
            'name': 'Potential',
            'definition': 'Latent qualities or abilities that may be developed',
            'coordinates': [0.60, 0.50, 0.80, 0.80] # High P, W
        },
        'value': {
            'name': 'Value',
            'definition': 'Importance, worth, or usefulness of something',
            'coordinates': [0.80, 0.80, 0.70, 0.80]
        },

        # --- METAPHYSICAL ---
        'spirit': {
            'name': 'Spirit',
            'definition': 'Non-physical part of a person',
            'coordinates': [0.90, 0.70, 0.60, 0.95]
        },
        'soul': {
            'name': 'Soul',
            'definition': 'Spiritual or immaterial part of a human being',
            'coordinates': [0.95, 0.75, 0.50, 0.90]
        },
        'mind': {
            'name': 'Mind',
            'definition': 'Element of a person that enables them to be aware',
            'coordinates': [0.60, 0.70, 0.60, 0.95] # High W
        },
        'body': {
            'name': 'Body',
            'definition': 'Physical structure of a person or an animal',
            'coordinates': [0.60, 0.60, 0.60, 0.50]
        },
        'consciousness': {
            'name': 'Consciousness',
            'definition': 'State of being awake and aware of one\'s surroundings',
            'coordinates': [0.80, 0.70, 0.50, 0.98] # Very High W
        },
        'dream': {
            'name': 'Dream',
            'definition': 'Series of thoughts, images, and sensations occurring in a person\'s mind during sleep',
            'coordinates': [0.70, 0.30, 0.40, 0.90] # Low J (Illogical), High W
        },
        'vision': {
            'name': 'Vision',
            'definition': 'Experience of seeing someone or something in a dream or trance',
            'coordinates': [0.80, 0.60, 0.60, 0.95]
        },
        'idea': {
            'name': 'Idea',
            'definition': 'Thought or suggestion as to a possible course of action',
            'coordinates': [0.60, 0.60, 0.50, 0.90]
        },
        'symbol': {
            'name': 'Symbol',
            'definition': 'Mark or character used as a conventional representation',
            'coordinates': [0.50, 0.70, 0.40, 0.90]
        },
        'meaning': {
            'name': 'Meaning',
            'definition': 'What is meant by a word, text, concept, or action',
            'coordinates': [0.70, 0.80, 0.50, 0.95]
        }
    }
    
    return concepts

def add_to_semantic_space():
    """Add abstract concepts to semantic space."""
    print("="*70)
    print("EXPANDING CONCEPT LIBRARY: ABSTRACT CONCEPTS")
    print("="*70)
    
    # Input file
    input_file = "experiments/semantic_space_6734_NATURE.json"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Add new domain
    if 'abstract_concepts' not in data['domains']:
        data['domains']['abstract_concepts'] = {
            'name': 'Abstract and Philosophical Concepts',
            'description': 'Ideas, values, logic, and metaphysics',
            'concepts': {}
        }
    
    domain = data['domains']['abstract_concepts']['concepts']
    
    # Generate new concepts
    new_concepts = generate_abstract_concepts()
    print(f"\nGenerating: {len(new_concepts)} new concepts")
    
    # Add to domain
    for key, concept in new_concepts.items():
        domain[key] = concept
    
    # Update metadata
    current_total = data['metadata']['total_concepts']
    new_total = current_total + len(new_concepts)
    data['metadata']['total_concepts'] = new_total
    data['metadata']['version'] = "23.0-ABSTRACT"
    
    # Save
    output_file = "experiments/semantic_space_6794_ABSTRACT.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*70}")
    print("SUCCESS")
    print(f"{'='*70}")
    print(f"Output: {output_file}")
    print(f"Previous total: {current_total:,}")
    print(f"New total: {new_total:,}")
    
    # Show samples
    print(f"\n{'='*70}")
    print("SAMPLE NEW CONCEPTS")
    print(f"{'='*70}\n")
    
    samples = ['truth', 'time', 'justice', 'science', 'chaos']
    for key in samples:
        if key in new_concepts:
            c = new_concepts[key]
            print(f"{c['name']}:")
            print(f"  {c['definition']}")
            print(f"  L={c['coordinates'][0]:.2f}, J={c['coordinates'][1]:.2f}, "
                  f"P={c['coordinates'][2]:.2f}, W={c['coordinates'][3]:.2f}\n")


if __name__ == "__main__":
    add_to_semantic_space()
