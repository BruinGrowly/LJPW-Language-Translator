"""
Tune Semantic Space
Adjusts coordinates of key theological concepts to align with idealized signatures.
"""
import json
import numpy as np
import os

SPACE_PATH = "experiments/semantic_space_6386_ENRICHED.json"

def tune_space():
    print(f"Loading {SPACE_PATH}...")
    with open(SPACE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Target coordinates (Idealized Kingdom)
    # L=0.71, J=0.85, P=0.72, W=0.92
    target_coords = [0.71, 0.85, 0.72, 0.92]
    
    concepts_to_update = ['Kingdom', 'Kingdom_of_God', 'Rule_of_God']
    updated_count = 0
    
    for domain in data['domains'].values():
        if 'concepts' in domain:
            for key in domain['concepts']:
                # normalize key for checking
                norm_key = key.replace('_', ' ').title()
                
                if norm_key in concepts_to_update or key in concepts_to_update:
                    print(f"Updating {key}...")
                    print(f"  Old: {domain['concepts'][key]['coordinates']}")
                    domain['concepts'][key]['coordinates'] = target_coords
                    print(f"  New: {target_coords}")
                    updated_count += 1
    
    if updated_count > 0:
        print(f"\nSaving {updated_count} updates to {SPACE_PATH}...")
        with open(SPACE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print("Done.")
    else:
        print("No concepts found to update.")

if __name__ == "__main__":
    tune_space()
