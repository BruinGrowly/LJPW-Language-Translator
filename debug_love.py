import json
from pathlib import Path

path = Path("experiments/semantic_space_10000_MILESTONE.json")
print(f"Loading {path}...")
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

emotions = data['domains'].get('emotions')
if not emotions:
    print("Emotions domain NOT found!")
else:
    print("Emotions domain found.")
    concepts = emotions.get('concepts', {})
    print(f"Concepts in emotions: {len(concepts)}")
    
    
    # Search entire space
    print("\nSearching ALL domains for 'love'...")
    found = []
    for d_name, d_data in data['domains'].items():
        for c_name in d_data.get('concepts', {}):
            if "love" in c_name.lower():
                found.append(f"{c_name} ({d_name})")
    
    print(f"Found {len(found)} matches:")
    for match in found[:20]:
        print(f" - {match}")
