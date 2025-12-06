"""
Generate Emotional & State Concepts
Expands the library with 80 concepts related to human emotions, psychological states, and moods.
Target: 100 -> 180 concepts.
"""

import json
import numpy as np

def generate_emotional_concepts():
    """Generate 80 emotional and state concepts with LJPW coordinates."""
    
    # L = Love/Connection/Affect (High: Love/Joy, Low: Hate/Isolation)
    # J = Justice/Stability/Order (High: Calm/Peace, Low: Chaos/Panic)
    # P = Power/Intensity/Arousal (High: Rage/Ecstasy, Low: Depression/Apathy)
    # W = Wisdom/Clarity/Awareness (High: Insight, Low: Confusion)

    concepts = {
        # --- BASIC EMOTIONS (High Intensity) ---
        'joy': {
            'name': 'Joy',
            'definition': 'A feeling of great pleasure and happiness',
            'coordinates': [0.90, 0.75, 0.80, 0.70] # High L, High P
        },
        'sadness': {
            'name': 'Sadness',
            'definition': 'Emotional pain associated with loss or despair',
            'coordinates': [0.30, 0.40, 0.20, 0.60] # Low L, Low P
        },
        'anger': {
            'name': 'Anger',
            'definition': 'Strong feeling of annoyance, displeasure, or hostility',
            'coordinates': [0.20, 0.30, 0.90, 0.40] # Low L, Very High P, Low J
        },
        'fear': {
            'name': 'Fear',
            'definition': 'Unpleasant emotion caused by belief that someone or something is dangerous',
            'coordinates': [0.20, 0.20, 0.85, 0.50] # Low L, High P, Low J
        },
        'disgust': {
            'name': 'Disgust',
            'definition': 'Feeling of revulsion or strong disapproval',
            'coordinates': [0.15, 0.60, 0.60, 0.50] # Very Low L
        },
        'surprise': {
            'name': 'Surprise',
            'definition': 'Feeling caused by something unexpected',
            'coordinates': [0.50, 0.40, 0.85, 0.60] # Neutral L, High P
        },
        'anticipation': {
            'name': 'Anticipation',
            'definition': 'Excitement about something that is going to happen',
            'coordinates': [0.65, 0.60, 0.75, 0.70]
        },
        'trust': {
            'name': 'Trust',
            'definition': 'Firm belief in reliability or truth',
            'coordinates': [0.85, 0.80, 0.50, 0.75] # High L, High J
        },

        # --- POSITIVE STATES ---
        'happiness': {
            'name': 'Happiness',
            'definition': 'State of being happy',
            'coordinates': [0.85, 0.70, 0.60, 0.60]
        },
        'gratitude': {
            'name': 'Gratitude',
            'definition': 'Quality of being thankful',
            'coordinates': [0.88, 0.75, 0.40, 0.80] # High L/W
        },
        'hope': {
            'name': 'Hope',
            'definition': 'Feeling of expectation and desire for a certain thing to happen',
            'coordinates': [0.80, 0.60, 0.65, 0.70]
        },
        'relief': {
            'name': 'Relief',
            'definition': 'Reassurance and relaxation following release from anxiety',
            'coordinates': [0.70, 0.85, 0.20, 0.60] # High J (Stable), Low P
        },
        'pride': {
            'name': 'Pride',
            'definition': 'Deep pleasure or satisfaction derived from achievements',
            'coordinates': [0.60, 0.65, 0.75, 0.60] # Moderate L, High P
        },
        'affection': {
            'name': 'Affection',
            'definition': 'Gentle feeling of fondness or liking',
            'coordinates': [0.90, 0.60, 0.30, 0.50] # High L, Low P
        },
        'contentment': {
            'name': 'Contentment',
            'definition': 'State of happiness and satisfaction',
            'coordinates': [0.75, 0.80, 0.20, 0.65] # High J, Low P
        },
        'enthusiasm': {
            'name': 'Enthusiasm',
            'definition': 'Intense and eager enjoyment',
            'coordinates': [0.70, 0.50, 0.85, 0.60] # High P
        },
        'euphoria': {
            'name': 'Euphoria',
            'definition': 'Feeling or state of intense excitement and happiness',
            'coordinates': [0.85, 0.40, 0.95, 0.40] # High P+L, Low J/W
        },
        'optimism': {
            'name': 'Optimism',
            'definition': 'Hopefulness and confidence about the future',
            'coordinates': [0.75, 0.70, 0.60, 0.75]
        },

        # --- NEGATIVE STATES ---
        'grief': {
            'name': 'Grief',
            'definition': 'Deep sorrow, especially caused by someone\'s death',
            'coordinates': [0.40, 0.30, 0.30, 0.50]
        },
        'loneliness': {
            'name': 'Loneliness',
            'definition': 'Sadness because one has no friends or company',
            'coordinates': [0.10, 0.40, 0.20, 0.50] # Very Low L
        },
        'shame': {
            'name': 'Shame',
            'definition': 'Humiliating feeling of guilt or foolishness',
            'coordinates': [0.20, 0.30, 0.40, 0.40]
        },
        'guilt': {
            'name': 'Guilt',
            'definition': 'Feeling of having done wrong or failed',
            'coordinates': [0.30, 0.60, 0.40, 0.50] # Moderate J (judging self), Low L
        },
        'envy': {
            'name': 'Envy',
            'definition': 'Feeling of discontented or resentful longing',
            'coordinates': [0.20, 0.40, 0.60, 0.40] # Low L, Med P
        },
        'jealousy': {
            'name': 'Jealousy',
            'definition': 'Feeling or showing envy of someone',
            'coordinates': [0.15, 0.30, 0.70, 0.30] # Low L, High P
        },
        'despair': {
            'name': 'Despair',
            'definition': 'Complete loss or absence of hope',
            'coordinates': [0.10, 0.20, 0.10, 0.30] # Low everything
        },
        'anxiety': {
            'name': 'Anxiety',
            'definition': 'Feeling of worry, nervousness, or unease',
            'coordinates': [0.30, 0.20, 0.70, 0.40] # Low J, High P
        },
        'frustration': {
            'name': 'Frustration',
            'definition': 'Feeling of being upset or annoyed at inability to change something',
            'coordinates': [0.30, 0.30, 0.65, 0.50]
        },
        'boredom': {
            'name': 'Boredom',
            'definition': 'Feeling weary because one is unoccupied',
            'coordinates': [0.40, 0.50, 0.10, 0.30] # Very Low P
        },

        # --- COMPLEX / SOCIAL STATES ---
        'empathy': {
            'name': 'Empathy',
            'definition': 'Ability to understand and share feelings of another',
            'coordinates': [0.90, 0.70, 0.40, 0.85] # High L, High W
        },
        'sympathy': {
            'name': 'Sympathy',
            'definition': 'Feelings of pity and sorrow for someone else\'s misfortune',
            'coordinates': [0.80, 0.60, 0.30, 0.70]
        },
        'compassion': {
            'name': 'Compassion',
            'definition': 'Sympathetic pity and concern for sufferings of others',
            'coordinates': [0.92, 0.75, 0.40, 0.88] # High L
        },
        'admiration': {
            'name': 'Admiration',
            'definition': 'Respect and warm approval',
            'coordinates': [0.75, 0.70, 0.50, 0.65]
        },
        'contempt': {
            'name': 'Contempt',
            'definition': 'Feeling that a person or thing is beneath consideration',
            'coordinates': [0.10, 0.30, 0.50, 0.50] # Very Low L
        },
        'awe': {
            'name': 'Awe',
            'definition': 'Feeling of reverential respect mixed with fear or wonder',
            'coordinates': [0.60, 0.50, 0.70, 0.80] # High W
        },
        'numbness': {
            'name': 'Numbness',
            'definition': 'Deprived of feeling or responsiveness',
            'coordinates': [0.30, 0.40, 0.05, 0.30] # Near zero P
        },
        'apathy': {
            'name': 'Apathy',
            'definition': 'Lack of interest, enthusiasm, or concern',
            'coordinates': [0.20, 0.40, 0.10, 0.40] # Low P
        },
        'melancholy': {
            'name': 'Melancholy',
            'definition': 'Feeling of pensive sadness, typically with no obvious cause',
            'coordinates': [0.40, 0.50, 0.20, 0.70] # High W (pensive)
        },
        'nostalgia': {
            'name': 'Nostalgia',
            'definition': 'Sentimental longing for the past',
            'coordinates': [0.70, 0.60, 0.30, 0.65]
        },

        # --- COGNITIVE / MENTAL STATES ---
        'confusion': {
            'name': 'Confusion',
            'definition': 'Uncertainty about what is happening, intended, or required',
            'coordinates': [0.40, 0.20, 0.50, 0.10] # Very Low W, Low J
        },
        'clarity': {
            'name': 'Clarity',
            'definition': 'Quality of being clear and easy to understand',
            'coordinates': [0.50, 0.80, 0.50, 0.95] # Very High W
        },
        'doubt': {
            'name': 'Doubt',
            'definition': 'Feeling of uncertainty or lack of conviction',
            'coordinates': [0.40, 0.30, 0.40, 0.30] # Low J/W
        },
        'certainty': {
            'name': 'Certainty',
            'definition': 'Firm conviction that something is the case',
            'coordinates': [0.50, 0.90, 0.60, 0.80] # High J
        },
        'focus': {
            'name': 'Focus',
            'definition': 'Center of interest or activity',
            'coordinates': [0.50, 0.85, 0.60, 0.90] # High W/J
        },
        'distraction': {
            'name': 'Distraction',
            'definition': 'Thing that prevents someone from giving full attention',
            'coordinates': [0.40, 0.20, 0.50, 0.20] # Low J/W
        },
        'curiosity': {
            'name': 'Curiosity',
            'definition': 'Strong desire to know or learn something',
            'coordinates': [0.60, 0.50, 0.65, 0.85] # High W
        },
        'inspiration': {
            'name': 'Inspiration',
            'definition': 'Process of being mentally stimulated to do or feel something',
            'coordinates': [0.70, 0.60, 0.80, 0.90] # High W, High P
        },
        'realization': {
            'name': 'Realization',
            'definition': 'Act of becoming fully aware of something as a fact',
            'coordinates': [0.50, 0.70, 0.60, 0.92] # High W
        },
        'epiphany': {
            'name': 'Epiphany',
            'definition': 'Moment of sudden revelation or insight',
            'coordinates': [0.60, 0.60, 0.80, 0.98] # Very High W/P
        },

        # --- PHYSIOLOGICAL / VISCERAL ---
        'pain': {
            'name': 'Pain',
            'definition': 'Physical suffering or discomfort',
            'coordinates': [0.10, 0.20, 0.90, 0.30] # High P (intense)
        },
        'pleasure': {
            'name': 'Pleasure',
            'definition': 'Feeling of happy satisfaction and enjoyment',
            'coordinates': [0.80, 0.60, 0.70, 0.40]
        },
        'fatigue': {
            'name': 'Fatigue',
            'definition': 'Extreme tiredness',
            'coordinates': [0.30, 0.30, 0.10, 0.30] # Low P
        },
        'energy': {
            'name': 'Energy',
            'definition': 'Strength and vitality required for sustained physical or mental activity',
            'coordinates': [0.60, 0.60, 0.95, 0.60] # High P
        },
        'hunger': {
            'name': 'Hunger',
            'definition': 'Feeling of discomfort or weakness caused by lack of food',
            'coordinates': [0.30, 0.30, 0.60, 0.40]
        },
        'thirst': {
            'name': 'Thirst',
            'definition': 'Feeling of needing or wanting to drink something',
            'coordinates': [0.30, 0.30, 0.60, 0.40]
        },
        'sickness': {
            'name': 'Sickness',
            'definition': 'State of being ill',
            'coordinates': [0.20, 0.20, 0.20, 0.40]
        },
        'health': {
            'name': 'Health',
            'definition': 'State of being free from illness or injury',
            'coordinates': [0.70, 0.80, 0.70, 0.70] # High J (Ordered)
        },
        'comfort': {
            'name': 'Comfort',
            'definition': 'State of physical ease and freedom from pain',
            'coordinates': [0.80, 0.80, 0.30, 0.50]
        },
        'stress': {
            'name': 'Stress',
            'definition': 'State of mental or emotional strain',
            'coordinates': [0.20, 0.10, 0.80, 0.40] # High P, Low J
        },
        
        # --- SUBTLE/NUANCED ---
        'ambivalence': {
            'name': 'Ambivalence',
            'definition': 'State of having mixed feelings',
            'coordinates': [0.50, 0.40, 0.40, 0.60]
        },
        'indifference': {
            'name': 'Indifference',
            'definition': 'Lack of interest, concern, or sympathy',
            'coordinates': [0.20, 0.40, 0.20, 0.30]
        },
        'resignation': {
            'name': 'Resignation',
            'definition': 'Acceptance of something undesirable but inevitable',
            'coordinates': [0.40, 0.60, 0.20, 0.50]
        },
        'determination': {
            'name': 'Determination',
            'definition': 'Firmness of purpose',
            'coordinates': [0.50, 0.80, 0.80, 0.70] # High J/P
        },
        'courage': {
            'name': 'Courage',
            'definition': 'Ability to do something that frightens one',
            'coordinates': [0.70, 0.70, 0.85, 0.75] # High P
        },
        'cowardice': {
            'name': 'Cowardice',
            'definition': 'Lack of bravery',
            'coordinates': [0.20, 0.30, 0.20, 0.30] # Low P/L
        },
        'humility': {
            'name': 'Humility',
            'definition': 'Modest or low view of one\'s own importance',
            'coordinates': [0.70, 0.80, 0.30, 0.80] # Low P, High J/W
        },
        'arrogance': {
            'name': 'Arrogance',
            'definition': 'Having an exaggerated sense of one\'s own importance',
            'coordinates': [0.20, 0.40, 0.80, 0.20] # High P, Low L/W
        },
        'patience': {
            'name': 'Patience',
            'definition': 'Capacity to accept or tolerate delay without getting angry',
            'coordinates': [0.75, 0.85, 0.30, 0.80] # High J
        },
        'impatience': {
            'name': 'Impatience',
            'definition': 'Tendency to be quickly irritated or provoked',
            'coordinates': [0.30, 0.30, 0.70, 0.30]
        },
        'restlessness': {
            'name': 'Restlessness',
            'definition': 'Inability to rest or relax',
            'coordinates': [0.30, 0.20, 0.65, 0.40]
        },
        'calmness': {
            'name': 'Calmness',
            'definition': 'State of being free from agitation',
            'coordinates': [0.70, 0.90, 0.20, 0.70] # High J
        },
        'fascination': {
            'name': 'Fascination',
            'definition': 'Power to fascinate someone',
            'coordinates': [0.65, 0.50, 0.60, 0.80]
        },
        'disappointment': {
            'name': 'Disappointment',
            'definition': 'Sadness or displeasure caused by non-fulfillment of hopes',
            'coordinates': [0.30, 0.40, 0.30, 0.50]
        },
        'regret': {
            'name': 'Regret',
            'definition': 'Feeling of sadness over something done or lost',
            'coordinates': [0.30, 0.50, 0.30, 0.60]
        },
        'remorse': {
            'name': 'Remorse',
            'definition': 'Deep regret or guilt for a wrong committed',
            'coordinates': [0.40, 0.60, 0.40, 0.65] 
        },
        'panic': {
            'name': 'Panic',
            'definition': 'Sudden uncontrollable fear or anxiety',
            'coordinates': [0.20, 0.10, 0.95, 0.20] # Very Low J, Very High P
        },
        'hysteria': {
            'name': 'Hysteria',
            'definition': 'Exaggerated or uncontrollable emotion',
            'coordinates': [0.20, 0.10, 0.90, 0.15]
        },
        'shock': {
            'name': 'Shock',
            'definition': 'Sudden upsetting or surprising event/experience',
            'coordinates': [0.30, 0.20, 0.80, 0.40]
        },
        'amazement': {
            'name': 'Amazement',
            'definition': 'Feeling of great surprise or wonder',
            'coordinates': [0.70, 0.50, 0.75, 0.75]
        },
        'alienation': {
            'name': 'Alienation',
            'definition': 'State of being isolated from a group',
            'coordinates': [0.10, 0.40, 0.30, 0.40] # Low L
        },
        'belonging': {
            'name': 'Belonging',
            'definition': 'Feeling of being a member or part of a group',
            'coordinates': [0.90, 0.70, 0.50, 0.60] # High L
        },
        'vulnerability': {
            'name': 'Vulnerability',
            'definition': 'State of being exposed to possibility of being attacked or harmed',
            'coordinates': [0.60, 0.40, 0.20, 0.60]
        },
        'security': {
            'name': 'Security',
            'definition': 'State of being free from danger or threat',
            'coordinates': [0.70, 0.90, 0.60, 0.70] # High J
        },
        'freedom': {
            'name': 'Freedom',
            'definition': 'Power or right to act, speak, or think as one wants',
            'coordinates': [0.80, 0.60, 0.80, 0.80] # High P/W/L
        },
        'oppression': {
            'name': 'Oppression',
            'definition': 'Blue state of being subject to unjust treatment',
            'coordinates': [0.10, 0.20, 0.20, 0.30]
        }
    }
    
    return concepts


def add_to_semantic_space():
    """Add emotional concepts to semantic space."""
    print("="*70)
    print("EXPANDING CONCEPT LIBRARY: EMOTIONS & STATES")
    print("="*70)
    
    # Input file (output of previous step)
    input_file = "experiments/semantic_space_6454_SPIRITUAL.json"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Add new domain
    if 'emotional_states' not in data['domains']:
        data['domains']['emotional_states'] = {
            'name': 'Emotions and Psychological States',
            'description': 'Human emotions, moods, and cognitive states',
            'concepts': {}
        }
    
    domain = data['domains']['emotional_states']['concepts']
    
    # Generate new concepts
    new_concepts = generate_emotional_concepts()
    print(f"\nGenerating: {len(new_concepts)} new concepts")
    
    # Add to domain
    for key, concept in new_concepts.items():
        domain[key] = concept
    
    # Update metadata
    current_total = data['metadata']['total_concepts']
    new_total = current_total + len(new_concepts)
    data['metadata']['total_concepts'] = new_total
    data['metadata']['version'] = "19.0-EMOTIONS"
    
    # Save
    output_file = "experiments/semantic_space_6534_EMOTIONAL.json"
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
    
    samples = ['joy', 'anger', 'confusion', 'epiphany', 'numbness']
    for key in samples:
        if key in new_concepts:
            c = new_concepts[key]
            print(f"{c['name']}:")
            print(f"  {c['definition']}")
            print(f"  L={c['coordinates'][0]:.2f}, J={c['coordinates'][1]:.2f}, "
                  f"P={c['coordinates'][2]:.2f}, W={c['coordinates'][3]:.2f}\n")


if __name__ == "__main__":
    add_to_semantic_space()
