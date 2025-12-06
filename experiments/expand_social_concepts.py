"""
Generate Social Structure Concepts
Expands the library with 60 concepts related to human organization, buildings, infrastructure, and roles.
Target: 440 -> 500 concepts.
"""

import json
import numpy as np

def generate_social_concepts():
    """Generate 60 social concepts with LJPW coordinates."""
    
    # L = Community/Care (High: Hospital/Park, Low: Prison/Ghetto)
    # J = Justice/Regulation (High: Court/City, Low: Riot/Slum)
    # P = Power/Industry (High: Factory/Tower, Low: Cottage/Path)
    # W = Wisdom/Culture (High: Library/Museum, Low: Mall/Stadium)

    concepts = {
        # --- BUILDINGS / PLACES ---
        'house': {
            'name': 'House',
            'definition': 'Building for human habitation',
            'coordinates': [0.80, 0.70, 0.50, 0.60] # High L (Home)
        },
        'home': {
            'name': 'Home',
            'definition': 'Place where one lives permanently',
            'coordinates': [0.90, 0.70, 0.40, 0.70] # High L
        },
        'cottage': {
            'name': 'Cottage',
            'definition': 'Small simple house',
            'coordinates': [0.70, 0.60, 0.30, 0.50]
        },
        'palace': {
            'name': 'Palace',
            'definition': 'Large and impressive building serving as a royal residence',
            'coordinates': [0.60, 0.90, 0.95, 0.80] # High P, J
        },
        'castle': {
            'name': 'Castle',
            'definition': 'Large building fortified against attack',
            'coordinates': [0.50, 0.85, 0.90, 0.70] # High P, J
        },
        'tower': {
            'name': 'Tower',
            'definition': 'Tall narrow building',
            'coordinates': [0.40, 0.80, 0.85, 0.70] # High P (Height)
        },
        'school': {
            'name': 'School',
            'definition': 'Institution for educating children',
            'coordinates': [0.70, 0.80, 0.50, 0.90] # High W
        },
        'university': {
            'name': 'University',
            'definition': 'High-level educational institution',
            'coordinates': [0.60, 0.85, 0.60, 0.95] # Very High W
        },
        'library': {
            'name': 'Library',
            'definition': 'Building containing collections of books',
            'coordinates': [0.60, 0.80, 0.40, 0.98] # Max W
        },
        'museum': {
            'name': 'Museum',
            'definition': 'Building in which objects of historical interest are stored',
            'coordinates': [0.60, 0.80, 0.50, 0.95] # High W
        },
        'church': {
            'name': 'Church',
            'definition': 'Building used for public Christian worship',
            'coordinates': [0.90, 0.80, 0.60, 0.90] # High L, W
        },
        'temple_structure': { # Renamed to diff from spiritual concept
            'name': 'Temple Structure',
            'definition': 'Building devoted to the worship of a god',
            'coordinates': [0.85, 0.85, 0.70, 0.90]
        },
        'hospital': {
            'name': 'Hospital',
            'definition': 'Institution providing medical treatment',
            'coordinates': [0.95, 0.85, 0.70, 0.90] # High L (Care), J (Order)
        },
        'clinic': {
            'name': 'Clinic',
            'definition': 'Establishment for medical treatment',
            'coordinates': [0.90, 0.80, 0.50, 0.85]
        },
        'prison': {
            'name': 'Prison',
            'definition': 'Building for the confinement of criminals',
            'coordinates': [0.10, 0.95, 0.90, 0.40] # Low L, High J, P
        },
        'court': {
            'name': 'Court',
            'definition': 'Tribunal presided over by a judge',
            'coordinates': [0.50, 0.98, 0.85, 0.90] # Max J
        },
        'market': {
            'name': 'Market',
            'definition': 'Regular gathering of people for purchase and sale of provisions',
            'coordinates': [0.60, 0.60, 0.70, 0.60] # High P (Trade)
        },
        'store': {
            'name': 'Store',
            'definition': 'Retail establishment selling items',
            'coordinates': [0.50, 0.60, 0.60, 0.50]
        },
        'factory': {
            'name': 'Factory',
            'definition': 'Building where goods are manufactured',
            'coordinates': [0.30, 0.70, 0.90, 0.60] # High P, J
        },
        'office': {
            'name': 'Office',
            'definition': 'Room or building used for commercial work',
            'coordinates': [0.40, 0.80, 0.60, 0.70]
        },

        # --- INFRASTRUCTURE ---
        'city': {
            'name': 'City',
            'definition': 'Large human settlement',
            'coordinates': [0.60, 0.90, 0.90, 0.80] # High J, P
        },
        'village': {
            'name': 'Village',
            'definition': 'Group of houses and associated buildings in rural area',
            'coordinates': [0.80, 0.60, 0.40, 0.50] # High L (Community)
        },
        'town': {
            'name': 'Town',
            'definition': 'Urban area smaller than a city',
            'coordinates': [0.70, 0.75, 0.60, 0.65]
        },
        'road': {
            'name': 'Road',
            'definition': 'Wide way leading from one place to another',
            'coordinates': [0.50, 0.70, 0.70, 0.60] # High J (Order/Path)
        },
        'path': {
            'name': 'Path',
            'definition': 'Way or track laid down for walking',
            'coordinates': [0.60, 0.50, 0.40, 0.60]
        },
        'bridge': {
            'name': 'Bridge',
            'definition': 'Structure carrying a road or path across an obstacle',
            'coordinates': [0.70, 0.80, 0.70, 0.80] # High J (Connection)
        },
        'gate': {
            'name': 'Gate',
            'definition': 'Hinged barrier used to close an opening',
            'coordinates': [0.50, 0.80, 0.60, 0.70]
        },
        'wall': {
            'name': 'Wall',
            'definition': 'Continuous vertical brick or stone structure',
            'coordinates': [0.40, 0.70, 0.80, 0.50] # High P (Defense)
        },
        'park': {
            'name': 'Park',
            'definition': 'Large public garden',
            'coordinates': [0.85, 0.70, 0.30, 0.60] # High L
        },
        'farm': {
            'name': 'Farm',
            'definition': 'Area of land used for growing crops',
            'coordinates': [0.70, 0.60, 0.60, 0.60]
        },

        # --- INSTITUTIONS ---
        'government': {
            'name': 'Government',
            'definition': 'Governing body of a nation',
            'coordinates': [0.40, 0.95, 0.90, 0.80] # High J, P
        },
        'state': {
            'name': 'State',
            'definition': 'Nation or territory considered as an organized political community',
            'coordinates': [0.50, 0.90, 0.80, 0.70]
        },
        'army': {
            'name': 'Army',
            'definition': 'Organized military force',
            'coordinates': [0.30, 0.80, 0.95, 0.60] # High P, J
        },
        'bank': {
            'name': 'Bank',
            'definition': 'Financial institution',
            'coordinates': [0.30, 0.90, 0.85, 0.70] # High J, P
        },
        'company': {
            'name': 'Company',
            'definition': 'Commercial business',
            'coordinates': [0.40, 0.70, 0.80, 0.70]
        },
        'charity': {
            'name': 'Charity',
            'definition': 'Organization set up to provide help',
            'coordinates': [0.95, 0.60, 0.40, 0.80] # High L
        },

        # --- ROLES ---
        'doctor': {
            'name': 'Doctor',
            'definition': 'Qualified practitioner of medicine',
            'coordinates': [0.90, 0.70, 0.60, 0.90] # High L, W
        },
        'nurse': {
            'name': 'Nurse',
            'definition': 'Person trained to care for the sick',
            'coordinates': [0.95, 0.60, 0.50, 0.80] # High L
        },
        'soldier': {
            'name': 'Soldier',
            'definition': 'Person who serves in an army',
            'coordinates': [0.40, 0.80, 0.90, 0.60] # High P, J
        },
        'police': {
            'name': 'Police',
            'definition': 'Civil force suitable for maintaining public order',
            'coordinates': [0.50, 0.90, 0.85, 0.60] # High J, P
        },
        'farmer': {
            'name': 'Farmer',
            'definition': 'Person who owns or manages a farm',
            'coordinates': [0.70, 0.60, 0.60, 0.70]
        },
        'merchant': {
            'name': 'Merchant',
            'definition': 'Person involved in trade',
            'coordinates': [0.50, 0.60, 0.70, 0.70]
        },
        'builder': {
            'name': 'Builder',
            'definition': 'Person who constructs something',
            'coordinates': [0.60, 0.80, 0.80, 0.70] # High J, P
        },
        'worker': {
            'name': 'Worker',
            'definition': 'Person who does work',
            'coordinates': [0.50, 0.60, 0.60, 0.50]
        },
        'artist': {
            'name': 'Artist',
            'definition': 'Person who produces paintings or drawings',
            'coordinates': [0.80, 0.40, 0.50, 0.90] # High L, W
        },
        'author': {
            'name': 'Author',
            'definition': 'Writer of a book',
            'coordinates': [0.60, 0.60, 0.50, 0.90] # High W
        },

        # --- ARTIFACTS / TOOLS ---
        'book': {
            'name': 'Book',
            'definition': 'Written or printed work',
            'coordinates': [0.60, 0.70, 0.40, 0.95] # High W
        },
        'paper': {
            'name': 'Paper',
            'definition': 'Material manufactured for writing on',
            'coordinates': [0.50, 0.60, 0.30, 0.60]
        },
        'pen': {
            'name': 'Pen',
            'definition': 'Instrument for writing',
            'coordinates': [0.50, 0.60, 0.40, 0.70]
        },
        'sword': {
            'name': 'Sword',
            'definition': 'Weapon with a long metal blade',
            'coordinates': [0.20, 0.40, 0.90, 0.40] # High P
        },
        'shield': {
            'name': 'Shield',
            'definition': 'Piece of armor used for protection',
            'coordinates': [0.60, 0.80, 0.80, 0.60] # High J (Protection)
        },
        'money': {
            'name': 'Money',
            'definition': 'Medium of exchange',
            'coordinates': [0.30, 0.70, 0.85, 0.60] # High P (Buying power)
        },
        'coin': {
            'name': 'Coin',
            'definition': 'Flat, typically round piece of metal used as money',
            'coordinates': [0.30, 0.70, 0.80, 0.60]
        },
        'clothing': {
            'name': 'Clothing',
            'definition': 'Items worn to cover the body',
            'coordinates': [0.60, 0.60, 0.40, 0.50]
        },
        'food': {
            'name': 'Food',
            'definition': 'Nutritious substance people eat',
            'coordinates': [0.90, 0.60, 0.50, 0.40] # High L
        },
        'bread': {
            'name': 'Bread',
            'definition': 'Food made of flour, water, and yeast',
            'coordinates': [0.85, 0.60, 0.40, 0.40]
        },
        'wine': {
            'name': 'Wine',
            'definition': 'Alcoholic drink made from fermented grape juice',
            'coordinates': [0.80, 0.50, 0.50, 0.50] # High L
        },
        'tool': {
            'name': 'Tool',
            'definition': 'Device used to carry out a particular function',
            'coordinates': [0.50, 0.80, 0.70, 0.80] # High J, P, W
        },
        'machine': {
            'name': 'Machine',
            'definition': 'Apparatus using mechanical power',
            'coordinates': [0.30, 0.90, 0.95, 0.80] # High J, P
        },
        'computer': {
            'name': 'Computer',
            'definition': 'Electronic device for storing and processing data',
            'coordinates': [0.40, 0.95, 0.80, 0.98] # High J, W
        }
    }
    
    return concepts

def add_to_semantic_space():
    """Add social concepts to semantic space."""
    print("="*70)
    print("EXPANDING CONCEPT LIBRARY: SOCIAL STRUCTURES")
    print("="*70)
    
    # Input file
    input_file = "experiments/semantic_space_6794_ABSTRACT.json"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Add new domain
    if 'social_structures' not in data['domains']:
        data['domains']['social_structures'] = {
            'name': 'Social Structures and Infrastructure',
            'description': 'Buildings, institutions, professions, and artifacts',
            'concepts': {}
        }
    
    domain = data['domains']['social_structures']['concepts']
    
    # Generate new concepts
    new_concepts = generate_social_concepts()
    print(f"\nGenerating: {len(new_concepts)} new concepts")
    
    # Add to domain
    for key, concept in new_concepts.items():
        domain[key] = concept
    
    # Update metadata
    current_total = data['metadata']['total_concepts']
    new_total = current_total + len(new_concepts)
    data['metadata']['total_concepts'] = new_total
    data['metadata']['version'] = "24.0-SOCIAL"
    
    # Save
    output_file = "experiments/semantic_space_6854_SOCIAL.json"
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
    
    samples = ['house', 'city', 'hospital', 'library', 'sword']
    for key in samples:
        if key in new_concepts:
            c = new_concepts[key]
            print(f"{c['name']}:")
            print(f"  {c['definition']}")
            print(f"  L={c['coordinates'][0]:.2f}, J={c['coordinates'][1]:.2f}, "
                  f"P={c['coordinates'][2]:.2f}, W={c['coordinates'][3]:.2f}\n")


if __name__ == "__main__":
    add_to_semantic_space()
