"""
Generate Natural World Concepts
Expands the library with 60 concepts related to nature, elements, animals, and the physical environment.
Target: 320 -> 380 concepts.
"""

import json
import numpy as np

def generate_nature_concepts():
    """Generate 60 nature concepts with LJPW coordinates."""
    
    # L = Life/Nurture (High: Tree/Animal, Low: Rock/Desert)
    # J = Justice/Law/Cycle (High: Season/Orbit, Low: Storm/Flood)
    # P = Power/Energy (High: Fire/Storm, Low: Grass/Cloud)
    # W = Wisdom/Complexity (High: Ecosystem/Web, Low: Dirt/Water)

    concepts = {
        # --- ELEMENTS ---
        'earth': {
            'name': 'Earth',
            'definition': 'Substance of the land surface; soil',
            'coordinates': [0.50, 0.60, 0.50, 0.20] # Solid (High J), Low W
        },
        'air': {
            'name': 'Air',
            'definition': 'Invisible gaseous substance surrounding the earth',
            'coordinates': [0.50, 0.40, 0.30, 0.30]
        },
        'fire': {
            'name': 'Fire',
            'definition': 'Combustion or burning',
            'coordinates': [0.20, 0.10, 0.95, 0.30] # High P, Low L/J (Destructive potential)
        },
        'water': {
            'name': 'Water',
            'definition': 'Colorless, transparent, odorless liquid',
            'coordinates': [0.80, 0.50, 0.60, 0.40] # High L (Life-giving)
        },
        'light': {
            'name': 'Light',
            'definition': 'Natural agent that stimulates sight',
            'coordinates': [0.80, 0.70, 0.70, 0.90] # High W (Illumination)
        },
        'darkness': {
            'name': 'Darkness',
            'definition': 'Partial or total absence of light',
            'coordinates': [0.20, 0.30, 0.40, 0.20]
        },
        'stone': {
            'name': 'Stone',
            'definition': 'Hard solid non-metallic mineral matter',
            'coordinates': [0.10, 0.80, 0.60, 0.10] # High J (Stable/Unchanging)
        },
        'metal': {
            'name': 'Metal',
            'definition': 'Solid material that is typically hard and shiny',
            'coordinates': [0.10, 0.70, 0.70, 0.20]
        },
        'gold': {
            'name': 'Gold',
            'definition': 'Yellow precious metal',
            'coordinates': [0.40, 0.60, 0.60, 0.50]
        },
        'dust': {
            'name': 'Dust',
            'definition': 'Fine powder consisting of waste matter',
            'coordinates': [0.20, 0.20, 0.10, 0.10] # Low everything
        },

        # --- CELESTIAL ---
        'sun': {
            'name': 'Sun',
            'definition': 'Star around which the earth orbits',
            'coordinates': [0.90, 0.90, 0.95, 0.80] # High L (Life), J (Order), P (Energy)
        },
        'moon': {
            'name': 'Moon',
            'definition': 'Natural satellite of the earth',
            'coordinates': [0.60, 0.80, 0.40, 0.70] # High J (Cycles)
        },
        'star': {
            'name': 'Star',
            'definition': 'Fixed luminous point in the night sky',
            'coordinates': [0.70, 0.90, 0.80, 0.90] # High W (Guidance)
        },
        'sky': {
            'name': 'Sky',
            'definition': 'Region of the atmosphere and outer space',
            'coordinates': [0.70, 0.60, 0.60, 0.80]
        },
        'cloud': {
            'name': 'Cloud',
            'definition': 'Visible mass of condensed water vapor',
            'coordinates': [0.60, 0.40, 0.30, 0.40]
        },
        'universe': {
            'name': 'Universe',
            'definition': 'All existing matter and space',
            'coordinates': [0.80, 0.90, 0.90, 0.95] # Max everything
        },

        # --- LANDSCAPE ---
        'mountain': {
            'name': 'Mountain',
            'definition': 'Large natural elevation of the earth\'s surface',
            'coordinates': [0.60, 0.90, 0.85, 0.70] # High J (Permanence), P
        },
        'valley': {
            'name': 'Valley',
            'definition': 'Low area of land between hills or mountains',
            'coordinates': [0.70, 0.60, 0.30, 0.50] # High L (Shelter)
        },
        'river': {
            'name': 'River',
            'definition': 'Large natural stream of water',
            'coordinates': [0.80, 0.70, 0.60, 0.60] # High L (Life), J (Path)
        },
        'ocean': {
            'name': 'Ocean',
            'definition': 'Very large expanse of sea',
            'coordinates': [0.70, 0.60, 0.90, 0.80] # High P (Depth/Power)
        },
        'sea': {
            'name': 'Sea',
            'definition': 'Expanse of salt water',
            'coordinates': [0.70, 0.60, 0.80, 0.70]
        },
        'land': {
            'name': 'Land',
            'definition': 'Part of the earth\'s surface not covered by water',
            'coordinates': [0.60, 0.70, 0.50, 0.40]
        },
        'desert': {
            'name': 'Desert',
            'definition': 'Waterless, desolate area of land',
            'coordinates': [0.10, 0.40, 0.60, 0.30] # Low L (No life)
        },
        'forest': {
            'name': 'Forest',
            'definition': 'Large area covered chiefly with trees',
            'coordinates': [0.90, 0.60, 0.60, 0.80] # High L (Life density), W
        },
        'garden': {
            'name': 'Garden',
            'definition': 'Piece of ground used for growing flowers or vegetables',
            'coordinates': [0.90, 0.80, 0.40, 0.70] # High L, J (Cultivated)
        },
        'world': {
            'name': 'World',
            'definition': 'The earth along with all its people and things',
            'coordinates': [0.70, 0.70, 0.70, 0.70]
        },

        # --- FLORA ---
        'tree': {
            'name': 'Tree',
            'definition': 'Woody perennial plant',
            'coordinates': [0.85, 0.80, 0.60, 0.70] # High L, J
        },
        'flower': {
            'name': 'Flower',
            'definition': 'Seed-bearing part of a plant',
            'coordinates': [0.90, 0.60, 0.30, 0.60] # High L (Beauty)
        },
        'grass': {
            'name': 'Grass',
            'definition': 'Short plants with long narrow leaves',
            'coordinates': [0.70, 0.50, 0.20, 0.40]
        },
        'seed': {
            'name': 'Seed',
            'definition': 'Flowering plant\'s unit of reproduction',
            'coordinates': [0.80, 0.70, 0.50, 0.90] # High W (Potential/Pattern)
        },
        'fruit': {
            'name': 'Fruit',
            'definition': 'Sweet and fleshy product of a tree',
            'coordinates': [0.90, 0.60, 0.40, 0.50] # High L (Nourishment)
        },
        'wood': {
            'name': 'Wood',
            'definition': 'Hard fibrous material from trees',
            'coordinates': [0.40, 0.60, 0.50, 0.30]
        },
        
        # --- FAUNA ---
        'animal': {
            'name': 'Animal',
            'definition': 'Living organism that feeds on organic matter',
            'coordinates': [0.70, 0.50, 0.60, 0.60]
        },
        'bird': {
            'name': 'Bird',
            'definition': 'Warm-blooded egg-laying vertebrate',
            'coordinates': [0.70, 0.50, 0.50, 0.60]
        },
        'fish': {
            'name': 'Fish',
            'definition': 'Limbless cold-blooded vertebrate',
            'coordinates': [0.60, 0.50, 0.40, 0.50]
        },
        'insect': {
            'name': 'Insect',
            'definition': 'Small arthropod animal',
            'coordinates': [0.40, 0.50, 0.20, 0.60] # High W (Hive mind/complexity)
        },
        'snake': {
            'name': 'Snake',
            'definition': 'Long limbless reptile',
            'coordinates': [0.30, 0.40, 0.60, 0.70] # Low L, High W (Cunning)
        },
        'lion': {
            'name': 'Lion',
            'definition': 'Large cat',
            'coordinates': [0.50, 0.60, 0.90, 0.60] # High P
        },
        'sheep': {
            'name': 'Sheep',
            'definition': 'Domesticated ruminant animal',
            'coordinates': [0.60, 0.50, 0.20, 0.30] # Low P, Low W
        },
        'dog': {
            'name': 'Dog',
            'definition': 'Domesticated carnivorous mammal',
            'coordinates': [0.85, 0.60, 0.50, 0.50] # High L (Loyalty)
        },
        'eagle': {
            'name': 'Eagle',
            'definition': 'Large bird of prey',
            'coordinates': [0.60, 0.70, 0.80, 0.70] # High P, J
        },

        # --- PHENOMENA / WEATHER ---
        'wind': {
            'name': 'Wind',
            'definition': 'Natural movement of the air',
            'coordinates': [0.50, 0.40, 0.60, 0.50]
        },
        'rain': {
            'name': 'Rain',
            'definition': 'Condensed moisture from the atmosphere falling in drops',
            'coordinates': [0.80, 0.60, 0.50, 0.50] # High L (Nurturing)
        },
        'storm': {
            'name': 'Storm',
            'definition': 'Violent disturbance of the atmosphere',
            'coordinates': [0.20, 0.20, 0.95, 0.40] # High P, Low J
        },
        'thunder': {
            'name': 'Thunder',
            'definition': 'Loud noise caused by lightning',
            'coordinates': [0.30, 0.30, 0.90, 0.30]
        },
        'lightning': {
            'name': 'Lightning',
            'definition': 'Natural electrical discharge',
            'coordinates': [0.40, 0.30, 0.95, 0.70]
        },
        'snow': {
            'name': 'Snow',
            'definition': 'Atmospheric water vapor frozen into ice crystals',
            'coordinates': [0.60, 0.70, 0.30, 0.60] # High J (Crystalline/Still)
        },
        'earthquake': {
            'name': 'Earthquake',
            'definition': 'Sudden violent shaking of the ground',
            'coordinates': [0.10, 0.10, 0.98, 0.20] # Extreme P, Low J
        },
        'flood': {
            'name': 'Flood',
            'definition': 'Overflow of a large amount of water',
            'coordinates': [0.20, 0.20, 0.90, 0.30]
        },
        'drought': {
            'name': 'Drought',
            'definition': 'Prolonged period of abnormally low rainfall',
            'coordinates': [0.10, 0.30, 0.60, 0.30] # Low L
        },
        'nature': {
            'name': 'Nature',
            'definition': 'The physical world and everything in it',
            'coordinates': [0.80, 0.80, 0.80, 0.90] # Balanced High
        },
        'life': {
            'name': 'Life',
            'definition': 'Condition that distinguishes animals and plants',
            'coordinates': [0.95, 0.80, 0.70, 0.90]
        },
        'death': {
            'name': 'Death',
            'definition': 'Action or fact of dying',
            'coordinates': [0.10, 0.40, 0.60, 0.40]
        },
        'season': {
            'name': 'Season',
            'definition': 'Each of the four divisions of the year',
            'coordinates': [0.60, 0.90, 0.50, 0.70] # High J (Cycle)
        },
        'day': {
            'name': 'Day',
            'definition': 'Period of light',
            'coordinates': [0.70, 0.80, 0.60, 0.60]
        },
        'night': {
            'name': 'Night',
            'definition': 'Period of darkness',
            'coordinates': [0.40, 0.70, 0.40, 0.60]
        }
    }
    
    return concepts

def add_to_semantic_space():
    """Add nature concepts to semantic space."""
    print("="*70)
    print("EXPANDING CONCEPT LIBRARY: NATURAL WORLD")
    print("="*70)
    
    # Input file
    input_file = "experiments/semantic_space_6674_ACTIONS.json"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Add new domain
    if 'natural_world' not in data['domains']:
        data['domains']['natural_world'] = {
            'name': 'Natural World',
            'description': 'Elements, landscape, flora, fauna, and phenomena',
            'concepts': {}
        }
    
    domain = data['domains']['natural_world']['concepts']
    
    # Generate new concepts
    new_concepts = generate_nature_concepts()
    print(f"\nGenerating: {len(new_concepts)} new concepts")
    
    # Add to domain
    for key, concept in new_concepts.items():
        domain[key] = concept
    
    # Update metadata
    current_total = data['metadata']['total_concepts']
    new_total = current_total + len(new_concepts)
    data['metadata']['total_concepts'] = new_total
    data['metadata']['version'] = "22.0-NATURE"
    
    # Save
    output_file = "experiments/semantic_space_6734_NATURE.json"
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
    
    samples = ['sun', 'storm', 'tree', 'lion', 'river']
    for key in samples:
        if key in new_concepts:
            c = new_concepts[key]
            print(f"{c['name']}:")
            print(f"  {c['definition']}")
            print(f"  L={c['coordinates'][0]:.2f}, J={c['coordinates'][1]:.2f}, "
                  f"P={c['coordinates'][2]:.2f}, W={c['coordinates'][3]:.2f}\n")


if __name__ == "__main__":
    add_to_semantic_space()
