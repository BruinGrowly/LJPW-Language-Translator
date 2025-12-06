"""
Generate Action & Process Concepts
Expands the library with 80 concepts related to human actions, verbs, and dynamic processes.
Target: 240 -> 320 concepts.
"""

import json
import numpy as np

def generate_action_concepts():
    """Generate 80 action concepts with LJPW coordinates."""
    
    # L = Love/Constructive (High: Create/Heal, Low: Destroy/Hurt)
    # J = Justice/Order (High: Build/Organize, Low: Scatter/Confuse)
    # P = Power/Energy (High: Run/Fight, Low: Sleep/Wait)
    # W = Wisdom/Intent (High: Plan/Teach, Low: Follow/Wander)

    concepts = {
        # --- PHYSICAL ACTIONS ---
        'walk': {
            'name': 'Walk',
            'definition': 'Move at a regular pace',
            'coordinates': [0.50, 0.50, 0.40, 0.40]
        },
        'run': {
            'name': 'Run',
            'definition': 'Move at a speed faster than a walk',
            'coordinates': [0.50, 0.50, 0.80, 0.40] # High P
        },
        'jump': {
            'name': 'Jump',
            'definition': 'Push oneself off a surface into the air',
            'coordinates': [0.50, 0.40, 0.70, 0.30]
        },
        'sleep': {
            'name': 'Sleep',
            'definition': 'Rest with eyes closed',
            'coordinates': [0.60, 0.60, 0.10, 0.30] # Very Low P
        },
        'eat': {
            'name': 'Eat',
            'definition': 'Put food into the mouth and swallow it',
            'coordinates': [0.60, 0.50, 0.40, 0.30]
        },
        'drink': {
            'name': 'Drink',
            'definition': 'Take liquid into the mouth and swallow it',
            'coordinates': [0.60, 0.50, 0.40, 0.30]
        },
        'work': {
            'name': 'Work',
            'definition': 'Activity involving mental or physical effort',
            'coordinates': [0.50, 0.70, 0.70, 0.60] # High J, P
        },
        'rest': {
            'name': 'Rest',
            'definition': 'Cease work or movement in order to relax',
            'coordinates': [0.70, 0.70, 0.15, 0.50] # Low P
        },
        'fight': {
            'name': 'Fight',
            'definition': 'Take part in a violent struggle',
            'coordinates': [0.10, 0.20, 0.90, 0.30] # Low L, High P
        },
        'stand': {
            'name': 'Stand',
            'definition': 'Have or maintain an upright position',
            'coordinates': [0.50, 0.60, 0.30, 0.40]
        },
        'sit': {
            'name': 'Sit',
            'definition': 'Adopt or be in a position in which one\'s weight is supported by one\'s buttocks',
            'coordinates': [0.50, 0.50, 0.20, 0.30]
        },
        'fall': {
            'name': 'Fall',
            'definition': 'Move downwards, typically rapidly and freely',
            'coordinates': [0.30, 0.30, 0.40, 0.20] # Low J (Loss of control)
        },
        'fly': {
            'name': 'Fly',
            'definition': 'Move through the air using wings',
            'coordinates': [0.60, 0.50, 0.70, 0.60]
        },
        'swim': {
            'name': 'Swim',
            'definition': 'Propel the body through water',
            'coordinates': [0.50, 0.50, 0.60, 0.50]
        },
        'lift': {
            'name': 'Lift',
            'definition': 'Raise to a higher position',
            'coordinates': [0.50, 0.50, 0.70, 0.40] # High P
        },
        'carry': {
            'name': 'Carry',
            'definition': 'Support and move someone or something',
            'coordinates': [0.60, 0.50, 0.60, 0.40]
        },
        'throw': {
            'name': 'Throw',
            'definition': 'Propel with force through the air',
            'coordinates': [0.40, 0.40, 0.75, 0.40]
        },
        'catch': {
            'name': 'Catch',
            'definition': 'Intercept and hold something thrown',
            'coordinates': [0.50, 0.60, 0.50, 0.50]
        },

        # --- CONSTRUCTIVE / PRODUCTIVE ---
        'build': {
            'name': 'Build',
            'definition': 'Construct by putting parts or material together',
            'coordinates': [0.70, 0.90, 0.80, 0.80] # High L, J, P, W
        },
        'create': {
            'name': 'Create',
            'definition': 'Bring something into existence',
            'coordinates': [0.80, 0.80, 0.85, 0.95] # High L, P, W
        },
        'make': {
            'name': 'Make',
            'definition': 'Form by putting parts together or combining substances',
            'coordinates': [0.60, 0.70, 0.70, 0.70]
        },
        'fix': {
            'name': 'Fix',
            'definition': 'Mend or repair',
            'coordinates': [0.75, 0.85, 0.60, 0.75] # High L, J
        },
        'heal': {
            'name': 'Heal',
            'definition': 'Cause to become sound or healthy again',
            'coordinates': [0.95, 0.90, 0.60, 0.85] # Very High L, J
        },
        'help': {
            'name': 'Help',
            'definition': 'Make it easier for someone to do something',
            'coordinates': [0.90, 0.70, 0.50, 0.70] # High L
        },
        'give': {
            'name': 'Give',
            'definition': 'Freely transfer the possession of something',
            'coordinates': [0.90, 0.60, 0.40, 0.70] # High L
        },
        'grow': {
            'name': 'Grow',
            'definition': 'Become larger or greater over time',
            'coordinates': [0.70, 0.80, 0.60, 0.80]
        },
        'plant': {
            'name': 'Plant',
            'definition': 'Put a seed or plant in the ground to grow',
            'coordinates': [0.70, 0.80, 0.50, 0.80]
        },
        'harvest': {
            'name': 'Harvest',
            'definition': 'Gather a crop',
            'coordinates': [0.80, 0.80, 0.70, 0.70]
        },
        'save': {
            'name': 'Save',
            'definition': 'Keep safe or rescue (someone or something) from harm',
            'coordinates': [0.90, 0.85, 0.70, 0.80]
        },
        'protect': {
            'name': 'Protect',
            'definition': 'Keep safe from harm or injury',
            'coordinates': [0.85, 0.85, 0.75, 0.80]
        },

        # --- DESTRUCTIVE / NEGATIVE ---
        'destroy': {
            'name': 'Destroy',
            'definition': 'Put an end to the existence of something',
            'coordinates': [0.10, 0.10, 0.90, 0.20] # Very Low L, J
        },
        'break': {
            'name': 'Break',
            'definition': 'Separate into pieces as a result of a blow, shock, or strain',
            'coordinates': [0.30, 0.20, 0.60, 0.30]
        },
        'kill': {
            'name': 'Kill',
            'definition': 'Cause the death of',
            'coordinates': [0.05, 0.05, 0.95, 0.10] # Extreme Negative
        },
        'hurt': {
            'name': 'Hurt',
            'definition': 'Cause physical pain or injury to',
            'coordinates': [0.10, 0.20, 0.70, 0.20]
        },
        'steal': {
            'name': 'Steal',
            'definition': 'Take another person\'s property without permission',
            'coordinates': [0.20, 0.10, 0.50, 0.40] # Very Low J
        },
        'lie': {
            'name': 'Lie',
            'definition': 'Tell an untruth',
            'coordinates': [0.20, 0.10, 0.30, 0.20] # Very Low J (Truth)
        },
        'attack': {
            'name': 'Attack',
            'definition': 'Take aggressive action against',
            'coordinates': [0.10, 0.20, 0.85, 0.30]
        },
        'hate': {
            'name': 'Hate',
            'definition': 'Feel intense or passionate dislike',
            'coordinates': [0.05, 0.20, 0.80, 0.20]
        },

        # --- MENTAL / COGNITIVE ---
        'think': {
            'name': 'Think',
            'definition': 'Have a particular opinion, belief, or idea',
            'coordinates': [0.50, 0.60, 0.40, 0.80] # High W
        },
        'know': {
            'name': 'Know',
            'definition': 'Be aware of through observation, inquiry, or information',
            'coordinates': [0.50, 0.70, 0.50, 0.90] # Very High W
        },
        'understand': {
            'name': 'Understand',
            'definition': 'Perceive the intended meaning of',
            'coordinates': [0.60, 0.70, 0.40, 0.95] # Very High W
        },
        'learn': {
            'name': 'Learn',
            'definition': 'Gain or acquire knowledge of or skill in',
            'coordinates': [0.60, 0.60, 0.50, 0.85]
        },
        'teach': {
            'name': 'Teach',
            'definition': 'Show or explain to someone how to do something',
            'coordinates': [0.80, 0.70, 0.60, 0.90]
        },
        'decide': {
            'name': 'Decide',
            'definition': 'Come to a resolution in the mind as a result of consideration',
            'coordinates': [0.50, 0.80, 0.70, 0.75] # High J (Judgment)
        },
        'choose': {
            'name': 'Choose',
            'definition': 'Pick out or select as being the best or most appropriate',
            'coordinates': [0.50, 0.60, 0.60, 0.70]
        },
        'plan': {
            'name': 'Plan',
            'definition': 'Decide on and arrange in advance',
            'coordinates': [0.50, 0.90, 0.50, 0.85] # High J, W
        },
        'remember': {
            'name': 'Remember',
            'definition': 'Have in or be able to bring to one\'s mind an awareness of',
            'coordinates': [0.60, 0.70, 0.40, 0.80]
        },
        'forget': {
            'name': 'Forget',
            'definition': 'Fail to remember',
            'coordinates': [0.40, 0.30, 0.30, 0.20] # Low W
        },
        'believe': {
            'name': 'Believe',
            'definition': 'Accept something as true; feel sure of the truth of',
            'coordinates': [0.70, 0.60, 0.50, 0.75]
        },

        # --- SOCIAL / COMMUNICATION ---
        'speak': {
            'name': 'Speak',
            'definition': 'Say something in order to convey information',
            'coordinates': [0.60, 0.60, 0.50, 0.70]
        },
        'listen': {
            'name': 'Listen',
            'definition': 'Give one\'s attention to a sound',
            'coordinates': [0.70, 0.60, 0.20, 0.80] # Low P, High L/W
        },
        'ask': {
            'name': 'Ask',
            'definition': 'Say something in order to obtain an answer',
            'coordinates': [0.50, 0.50, 0.40, 0.60]
        },
        'answer': {
            'name': 'Answer',
            'definition': 'Say or write something to deal with or as a reaction',
            'coordinates': [0.60, 0.60, 0.50, 0.75]
        },
        'call': {
            'name': 'Call',
            'definition': 'Cry out to',
            'coordinates': [0.50, 0.50, 0.60, 0.50]
        },
        'command': {
            'name': 'Command',
            'definition': 'Give an authoritative order',
            'coordinates': [0.30, 0.80, 0.90, 0.70] # High P, J
        },
        'obey': {
            'name': 'Obey',
            'definition': 'Comply with the command, direction, or request',
            'coordinates': [0.60, 0.85, 0.30, 0.60] # High J, Low P
        },
        'lead': {
            'name': 'Lead',
            'definition': 'Show the way',
            'coordinates': [0.70, 0.70, 0.80, 0.85]
        },
        'follow': {
            'name': 'Follow',
            'definition': 'Go or come after',
            'coordinates': [0.60, 0.60, 0.40, 0.50]
        },
        'meet': {
            'name': 'Meet',
            'definition': 'Come into the presence or company of',
            'coordinates': [0.70, 0.50, 0.50, 0.50]
        },

        # --- SPIRITUAL / CEREMONIAL ---
        'pray': {
            'name': 'Pray',
            'definition': 'Address a solemn request or expression of thanks to a deity',
            'coordinates': [0.90, 0.70, 0.30, 0.90] # High L, W
        },
        'worship': {
            'name': 'Worship',
            'definition': 'Show reverence and adoration for',
            'coordinates': [0.95, 0.80, 0.40, 0.90]
        },
        'bless': {
            'name': 'Bless',
            'definition': 'Pronounce words in a religious rite, to confer or invoke divine favor',
            'coordinates': [0.95, 0.80, 0.70, 0.90] # High L, P (Divine Power)
        },
        'curse': {
            'name': 'Curse',
            'definition': 'Invoke or use a hex or evil spell against',
            'coordinates': [0.10, 0.20, 0.80, 0.30] # Low L, High P
        },
        'sing': {
            'name': 'Sing',
            'definition': 'Make musical sounds with the voice',
            'coordinates': [0.80, 0.50, 0.50, 0.70] # High L (Joy)
        },
        'praise': {
            'name': 'Praise',
            'definition': 'Express warm approval or admiration of',
            'coordinates': [0.90, 0.60, 0.50, 0.80]
        },
        'repent': {
            'name': 'Repent',
            'definition': 'Feel or express sincere regret or remorse',
            'coordinates': [0.60, 0.70, 0.40, 0.80]
        },
        'baptize': {
            'name': 'Baptize',
            'definition': 'Administer baptism to',
            'coordinates': [0.85, 0.85, 0.60, 0.90]
        },
        'fast': {
            'name': 'Fast',
            'definition': 'Abstain from all or some kinds of food or drink',
            'coordinates': [0.70, 0.80, 0.30, 0.85] # Self-denial (Low P), High J/W
        },

        # --- MOVEMENT / PROCESS ABSTRACTIONS ---
        'begin': {
            'name': 'Begin',
            'definition': 'Start; perform or undergo the first part of',
            'coordinates': [0.60, 0.60, 0.60, 0.60]
        },
        'end': {
            'name': 'End',
            'definition': 'Come or bring to a final point',
            'coordinates': [0.50, 0.70, 0.40, 0.70]
        },
        'change': {
            'name': 'Change',
            'definition': 'Make or become different',
            'coordinates': [0.50, 0.50, 0.70, 0.60]
        },
        'wait': {
            'name': 'Wait',
            'definition': 'Stay where one is or delay action',
            'coordinates': [0.50, 0.50, 0.20, 0.60] # Low P
        },
        'search': {
            'name': 'Search',
            'definition': 'Try to find something by looking',
            'coordinates': [0.50, 0.50, 0.60, 0.80] # High W
        },
        'find': {
            'name': 'Find',
            'definition': 'Discover or perceive by chance or unexpectedly',
            'coordinates': [0.70, 0.60, 0.50, 0.90] # High W (Discovery)
        },
        'lose': {
            'name': 'Lose',
            'definition': 'Be deprived of or cease to have',
            'coordinates': [0.30, 0.40, 0.30, 0.30]
        },
        'win': {
            'name': 'Win',
            'definition': 'Be successful or victorious',
            'coordinates': [0.80, 0.70, 0.80, 0.60] # High P
        },
        'fail': {
            'name': 'Fail',
            'definition': 'Be unsuccessful in achieving one\'s goal',
            'coordinates': [0.30, 0.40, 0.20, 0.40]
        },
        'succeed': {
            'name': 'Succeed',
            'definition': 'Achieve the desired aim or result',
            'coordinates': [0.80, 0.80, 0.70, 0.70]
        }
    }
    
    return concepts

def add_to_semantic_space():
    """Add action concepts to semantic space."""
    print("="*70)
    print("EXPANDING CONCEPT LIBRARY: ACTIONS & PROCESSES")
    print("="*70)
    
    # Input file
    input_file = "experiments/semantic_space_6594_RELATIONSHIPS.json"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Add new domain
    if 'actions_processes' not in data['domains']:
        data['domains']['actions_processes'] = {
            'name': 'Actions and Dynamic Processes',
            'description': 'Verbs, activities, and changes of state',
            'concepts': {}
        }
    
    domain = data['domains']['actions_processes']['concepts']
    
    # Generate new concepts
    new_concepts = generate_action_concepts()
    print(f"\nGenerating: {len(new_concepts)} new concepts")
    
    # Add to domain
    for key, concept in new_concepts.items():
        domain[key] = concept
    
    # Update metadata
    current_total = data['metadata']['total_concepts']
    new_total = current_total + len(new_concepts)
    data['metadata']['total_concepts'] = new_total
    data['metadata']['version'] = "21.0-ACTIONS"
    
    # Save
    output_file = "experiments/semantic_space_6674_ACTIONS.json"
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
    
    samples = ['run', 'build', 'destroy', 'pray', 'think']
    for key in samples:
        if key in new_concepts:
            c = new_concepts[key]
            print(f"{c['name']}:")
            print(f"  {c['definition']}")
            print(f"  L={c['coordinates'][0]:.2f}, J={c['coordinates'][1]:.2f}, "
                  f"P={c['coordinates'][2]:.2f}, W={c['coordinates'][3]:.2f}\n")


if __name__ == "__main__":
    add_to_semantic_space()
