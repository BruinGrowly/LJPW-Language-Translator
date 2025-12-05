"""
Add Missing Concepts to Enriched Set
Gospel and Kingdom are essential for our tests.
"""

import json

def add_missing_concepts():
    """Add Gospel and Kingdom to enriched concepts."""
    print("Adding missing concepts to enriched set...")
    
    # Load
    with open("experiments/semantic_space_6386_ENRICHED.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Add to enriched domain
    enriched = data['domains']['spiritual_moral_enrichment']['concepts']
    
    # Add Gospel
    enriched['gospel'] = {
        'name': 'Gospel',
        'definition': 'Good news of divine salvation and redemption',
        'coordinates': [0.85, 0.75, 0.60, 0.90]
    }
    
    # Add Kingdom (if not exists)
    if 'kingdom' not in enriched:
        enriched['kingdom'] = {
            'name': 'Kingdom',
            'definition': 'Divine realm of rule and authority',
            'coordinates': [0.75, 0.90, 0.85, 0.88]
        }
    
    # Update metadata
    total = sum(len(d['concepts']) for d in data['domains'].values())
    data['metadata']['total_concepts'] = total
    data['metadata']['version'] = "17.1-COMPLETE"
    
    # Save
    with open("experiments/semantic_space_6388_COMPLETE.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Added Gospel and Kingdom")
    print(f"Total concepts: {total}")
    print(f"Saved to: semantic_space_6388_COMPLETE.json")


if __name__ == "__main__":
    add_missing_concepts()
