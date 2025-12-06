"""
Generate Relationship Concepts
Expands the library with 60 concepts related to human connections, social bonds, and family structures.
Target: 180 -> 240 concepts.
"""

import json
import numpy as np

def generate_relationship_concepts():
    """Generate 60 relationship concepts with LJPW coordinates."""
    
    # L = Love/Intimacy (High: Spouse/Parent, Low: Enemy/Stranger)
    # J = Justice/Obligation (High: Marriage/Contract, Low: Friendship/Casual)
    # P = Power/Authority (High: Parent/Boss, Low: Child/Subordinate)
    # W = Wisdom/Mentorship (High: Teacher/Elder, Low: Student/Child)

    concepts = {
        # --- FAMILY: NUCLEAR ---
        'father': {
            'name': 'Father',
            'definition': 'Male parent',
            'coordinates': [0.90, 0.85, 0.85, 0.80] # High L, High P, High J
        },
        'mother': {
            'name': 'Mother',
            'definition': 'Female parent',
            'coordinates': [0.95, 0.80, 0.75, 0.85] # Very High L, High P
        },
        'parent': {
            'name': 'Parent',
            'definition': 'Father or mother',
            'coordinates': [0.92, 0.82, 0.80, 0.82]
        },
        'child': {
            'name': 'Child',
            'definition': 'Son or daughter',
            'coordinates': [0.90, 0.40, 0.30, 0.20] # High L, Low P/W
        },
        'son': {
            'name': 'Son',
            'definition': 'Male child',
            'coordinates': [0.90, 0.40, 0.35, 0.20]
        },
        'daughter': {
            'name': 'Daughter',
            'definition': 'Female child',
            'coordinates': [0.90, 0.40, 0.30, 0.20]
        },
        'brother': {
            'name': 'Brother',
            'definition': 'Male sibling',
            'coordinates': [0.85, 0.50, 0.50, 0.50] # Equal P/W
        },
        'sister': {
            'name': 'Sister',
            'definition': 'Female sibling',
            'coordinates': [0.85, 0.50, 0.50, 0.50]
        },
        'sibling': {
            'name': 'Sibling',
            'definition': 'Brother or sister',
            'coordinates': [0.85, 0.50, 0.50, 0.50]
        },
        'spouse': {
            'name': 'Spouse',
            'definition': 'Husband or wife',
            'coordinates': [0.95, 0.90, 0.50, 0.60] # High L, High J (Contract)
        },
        'husband': {
            'name': 'Husband',
            'definition': 'Male spouse',
            'coordinates': [0.95, 0.90, 0.55, 0.60]
        },
        'wife': {
            'name': 'Wife',
            'definition': 'Female spouse',
            'coordinates': [0.95, 0.90, 0.50, 0.60]
        },

        # --- FAMILY: EXTENDED ---
        'grandfather': {
            'name': 'Grandfather',
            'definition': 'Father of one\'s parent',
            'coordinates': [0.85, 0.70, 0.70, 0.90] # High W (Elder)
        },
        'grandmother': {
            'name': 'Grandmother',
            'definition': 'Mother of one\'s parent',
            'coordinates': [0.90, 0.70, 0.65, 0.90]
        },
        'ancestor': {
            'name': 'Ancestor',
            'definition': 'Person from whom one is descended',
            'coordinates': [0.60, 0.70, 0.70, 0.95] # High W, Moderate L
        },
        'descendant': {
            'name': 'Descendant',
            'definition': 'Person descended from a particular ancestor',
            'coordinates': [0.70, 0.50, 0.30, 0.30]
        },
        'uncle': {
            'name': 'Uncle',
            'definition': 'Brother of one\'s parent',
            'coordinates': [0.75, 0.60, 0.60, 0.70]
        },
        'aunt': {
            'name': 'Aunt',
            'definition': 'Sister of one\'s parent',
            'coordinates': [0.80, 0.60, 0.55, 0.70]
        },
        'cousin': {
            'name': 'Cousin',
            'definition': 'Child of one\'s uncle or aunt',
            'coordinates': [0.75, 0.40, 0.50, 0.50]
        },
        'family': {
            'name': 'Family',
            'definition': 'Group consisting of parents and children',
            'coordinates': [0.90, 0.80, 0.70, 0.70] # High L, J
        },

        # --- SOCIAL / COMMUNITY ---
        'friend': {
            'name': 'Friend',
            'definition': 'Person whom one knows and likes',
            'coordinates': [0.85, 0.30, 0.50, 0.50] # High L, Low J (Voluntary)
        },
        'neighbor': {
            'name': 'Neighbor',
            'definition': 'Person living near or next door',
            'coordinates': [0.50, 0.40, 0.50, 0.50] # Moderate L/J
        },
        'enemy': {
            'name': 'Enemy',
            'definition': 'Person who is actively opposed or hostile',
            'coordinates': [0.10, 0.20, 0.70, 0.40] # Very Low L
        },
        'stranger': {
            'name': 'Stranger',
            'definition': 'Person whom one does not know',
            'coordinates': [0.30, 0.20, 0.50, 0.50] # Low L, Low J
        },
        'guest': {
            'name': 'Guest',
            'definition': 'Person who is invited to visit',
            'coordinates': [0.70, 0.50, 0.40, 0.50] # High L (Hospitality)
        },
        'host': {
            'name': 'Host',
            'definition': 'Person who receives or entertains guests',
            'coordinates': [0.70, 0.60, 0.60, 0.60] # P/J slightly higher
        },
        'ally': {
            'name': 'Ally',
            'definition': 'State formally cooperating with another',
            'coordinates': [0.60, 0.80, 0.60, 0.60] # High J (Treaty)
        },
        'rival': {
            'name': 'Rival',
            'definition': 'Person competing for the same object or goal',
            'coordinates': [0.30, 0.30, 0.60, 0.50]
        },
        'partner': {
            'name': 'Partner',
            'definition': 'Person who takes part in an undertaking with another',
            'coordinates': [0.70, 0.75, 0.50, 0.60] # High J
        },
        'community': {
            'name': 'Community',
            'definition': 'Group of people living in the same place',
            'coordinates': [0.60, 0.60, 0.60, 0.60] # Balanced
        },

        # --- STRUCTURAL / HIERARCHICAL ---
        'king': {
            'name': 'King',
            'definition': 'Male ruler of an independent state',
            'coordinates': [0.50, 0.90, 0.95, 0.80] # High J, Very High P
        },
        'queen': {
            'name': 'Queen',
            'definition': 'Female ruler of an independent state',
            'coordinates': [0.60, 0.90, 0.90, 0.85]
        },
        'leader': {
            'name': 'Leader',
            'definition': 'Person who leads or commands a group',
            'coordinates': [0.60, 0.80, 0.85, 0.80]
        },
        'follower': {
            'name': 'Follower',
            'definition': 'Adherent or devotee of a person or cause',
            'coordinates': [0.60, 0.50, 0.30, 0.50] # Low P
        },
        'master': {
            'name': 'Master',
            'definition': 'Man who has people working for him',
            'coordinates': [0.30, 0.70, 0.90, 0.70] # Low L, High P
        },
        'servant': {
            'name': 'Servant',
            'definition': 'Person who performs duties for others',
            'coordinates': [0.50, 0.60, 0.20, 0.50] # Low P
        },
        'teacher': {
            'name': 'Teacher',
            'definition': 'Person who teaches, especially in a school',
            'coordinates': [0.70, 0.70, 0.70, 0.90] # High W
        },
        'student': {
            'name': 'Student',
            'definition': 'Person who is studying at a school or college',
            'coordinates': [0.60, 0.60, 0.40, 0.40] # Low W (Learning)
        },
        'mentor': {
            'name': 'Mentor',
            'definition': 'Experienced and trusted adviser',
            'coordinates': [0.80, 0.60, 0.60, 0.95] # High L, Very High W
        },
        'judge': {
            'name': 'Judge',
            'definition': 'Public official appointed to decide cases',
            'coordinates': [0.50, 0.95, 0.80, 0.90] # Very High J
        },
        'citizen': {
            'name': 'Citizen',
            'definition': 'Legally recognized subject or national',
            'coordinates': [0.50, 0.80, 0.50, 0.60] # High J
        },
        'subject': {
            'name': 'Subject',
            'definition': 'Member of a state other than its ruler',
            'coordinates': [0.40, 0.70, 0.30, 0.50] # Lower P
        },
        'victim': {
            'name': 'Victim',
            'definition': 'Person harmed, injured, or killed',
            'coordinates': [0.40, 0.90, 0.10, 0.40] # High J (Injustice), Very Low P
        },
        'criminal': {
            'name': 'Criminal',
            'definition': 'Person who has committed a crime',
            'coordinates': [0.20, 0.10, 0.60, 0.30] # Very Low J
        },
        'boss': {
            'name': 'Boss',
            'definition': 'Person in charge of a worker or organization',
            'coordinates': [0.40, 0.60, 0.80, 0.60] # High P
        },
        'employee': {
            'name': 'Employee',
            'definition': 'Person employed for wages',
            'coordinates': [0.50, 0.70, 0.40, 0.50]
        },

        # --- ABSTRACT ROLES ---
        'hero': {
            'name': 'Hero',
            'definition': 'Person admired for courage or outstanding achievements',
            'coordinates': [0.70, 0.70, 0.85, 0.70] # High P
        },
        'villain': {
            'name': 'Villain',
            'definition': 'Character whose evil actions are important to the plot',
            'coordinates': [0.10, 0.15, 0.80, 0.60] # Very Low L, Low J
        },
        'guardian': {
            'name': 'Guardian',
            'definition': 'Defender, protector, or keeper',
            'coordinates': [0.80, 0.85, 0.75, 0.80] # High L, J, P
        },
        'traitor': {
            'name': 'Traitor',
            'definition': 'Person who betrays a friend or principle',
            'coordinates': [0.10, 0.10, 0.40, 0.40] # Very Low L, J
        },
        'witness': {
            'name': 'Witness',
            'definition': 'Person who sees an event taking place',
            'coordinates': [0.50, 0.80, 0.50, 0.60] # High J (Truth)
        },
        'heir': {
            'name': 'Heir',
            'definition': 'Person legally entitled to property or rank',
            'coordinates': [0.60, 0.85, 0.50, 0.60] # High J
        },
        'neighbor_concept': {
            'name': 'Neighbor Concept', 
            'definition': 'Abstract concept of proximity', 
            'coordinates': [0.5, 0.5, 0.5, 0.5]
        },
        'orphan': {
            'name': 'Orphan',
            'definition': 'Child whose parents are dead',
            'coordinates': [0.40, 0.40, 0.10, 0.30] # Low L (Loss), Low P
        },
        'widow': {
            'name': 'Widow',
            'definition': 'Woman whose husband has died',
            'coordinates': [0.50, 0.50, 0.30, 0.50]
        },
        'widower': {
            'name': 'Widower',
            'definition': 'Man whose wife has died',
            'coordinates': [0.50, 0.50, 0.30, 0.50]
        },
        'generation': {
            'name': 'Generation',
            'definition': 'All of the people born and living at about the same time',
            'coordinates': [0.60, 0.60, 0.60, 0.60]
        },
        'tribe': {
            'name': 'Tribe',
            'definition': 'Social division in a traditional society',
            'coordinates': [0.70, 0.70, 0.60, 0.60]
        },
        'nation': {
            'name': 'Nation',
            'definition': 'Large body of people united by common descent',
            'coordinates': [0.60, 0.80, 0.70, 0.60] # High J, P
        },
        'crowd': {
            'name': 'Crowd',
            'definition': 'Large number of people gathered together',
            'coordinates': [0.40, 0.40, 0.50, 0.40] # Generic
        }
    }
    
    return concepts

def add_to_semantic_space():
    """Add emotional concepts to semantic space."""
    print("="*70)
    print("EXPANDING CONCEPT LIBRARY: RELATIONSHIPS")
    print("="*70)
    
    # Input file (output of previous step)
    input_file = "experiments/semantic_space_6534_EMOTIONAL.json"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Add new domain
    if 'relationships' not in data['domains']:
        data['domains']['relationships'] = {
            'name': 'Relationships and Social Roles',
            'description': 'Family, social, and hierarchical connections',
            'concepts': {}
        }
    
    domain = data['domains']['relationships']['concepts']
    
    # Generate new concepts
    new_concepts = generate_relationship_concepts()
    print(f"\nGenerating: {len(new_concepts)} new concepts")
    
    # Add to domain
    for key, concept in new_concepts.items():
        domain[key] = concept
    
    # Update metadata
    current_total = data['metadata']['total_concepts']
    new_total = current_total + len(new_concepts)
    data['metadata']['total_concepts'] = new_total
    data['metadata']['version'] = "20.0-RELATIONSHIPS"
    
    # Save
    output_file = "experiments/semantic_space_6594_RELATIONSHIPS.json"
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
    
    samples = ['father', 'friend', 'king', 'teacher', 'enemy']
    for key in samples:
        if key in new_concepts:
            c = new_concepts[key]
            print(f"{c['name']}:")
            print(f"  {c['definition']}")
            print(f"  L={c['coordinates'][0]:.2f}, J={c['coordinates'][1]:.2f}, "
                  f"P={c['coordinates'][2]:.2f}, W={c['coordinates'][3]:.2f}\n")


if __name__ == "__main__":
    add_to_semantic_space()
