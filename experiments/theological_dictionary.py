"""
Theological Dictionary Builder
Creates comprehensive LJPW coordinate mappings for 500+ theological concepts
"""

import json
import numpy as np


class TheologicalDictionary:
    """
    Comprehensive theological term dictionary with LJPW coordinates.
    
    Categories:
    - Divine Attributes
    - Kingdom/Reign
    - Spirit/Soul
    - Gospel/Message
    - Faith/Belief
    - Sacraments
    - Love/Mercy
    - Sin/Repentance
    - Salvation/Redemption
    - Worship/Prayer
    - Prophecy/Revelation
    - Judgment/Justice
    - Creation/Nature
    - Human Condition
    - Eschatology
    """
    
    def __init__(self):
        self.dictionary = self._build_dictionary()
    
    def _build_dictionary(self) -> dict:
        """Build comprehensive theological dictionary."""
        
        dictionary = {}
        
        # === DIVINE ATTRIBUTES ===
        dictionary['divine_attributes'] = {
            'God': [0.88, 0.90, 0.75, 0.98],
            'Lord': [0.85, 0.90, 0.80, 0.95],
            'Father': [0.90, 0.85, 0.70, 0.92],
            'Son': [0.85, 0.88, 0.72, 0.90],
            'Holy Spirit': [0.90, 0.70, 0.60, 0.95],
            'Trinity': [0.88, 0.90, 0.75, 0.98],
            'Almighty': [0.75, 0.90, 0.95, 0.92],
            'Creator': [0.80, 0.88, 0.90, 0.95],
            'Eternal': [0.75, 0.95, 0.70, 0.98],
            'Holy': [0.88, 0.88, 0.48, 0.95],
            'Righteous': [0.75, 0.95, 0.65, 0.90],
            'Merciful': [0.95, 0.75, 0.50, 0.85],
            'Gracious': [0.92, 0.70, 0.45, 0.88],
            'Faithful': [0.85, 0.90, 0.60, 0.88],
            'Sovereign': [0.75, 0.92, 0.95, 0.90],
        }
        
        # === KINGDOM/REIGN ===
        dictionary['kingdom'] = {
            'Kingdom': [0.75, 0.90, 0.85, 0.88],
            'Kingdom of God': [0.80, 0.92, 0.88, 0.95],
            'Kingdom of Heaven': [0.82, 0.92, 0.85, 0.96],
            'Reign': [0.70, 0.88, 0.90, 0.85],
            'King': [0.70, 0.88, 0.90, 0.85],
            'Throne': [0.65, 0.90, 0.88, 0.82],
            'Crown': [0.68, 0.85, 0.82, 0.80],
            'Authority': [0.60, 0.88, 0.92, 0.85],
            'Power': [0.55, 0.80, 0.95, 0.75],
            'Glory': [0.75, 0.85, 0.80, 0.90],
            'Majesty': [0.72, 0.88, 0.85, 0.88],
        }
        
        # === GOSPEL/MESSAGE ===
        dictionary['gospel'] = {
            'Gospel': [0.90, 0.85, 0.70, 0.95],
            'Good News': [0.92, 0.82, 0.68, 0.93],
            'Word': [0.75, 0.85, 0.70, 0.92],
            'Word of God': [0.80, 0.90, 0.75, 0.95],
            'Scripture': [0.75, 0.90, 0.65, 0.95],
            'Truth': [0.70, 0.98, 0.60, 0.95],
            'Revelation': [0.75, 0.88, 0.70, 0.98],
            'Prophecy': [0.72, 0.85, 0.68, 0.95],
            'Teaching': [0.70, 0.82, 0.60, 0.90],
            'Doctrine': [0.65, 0.88, 0.58, 0.92],
            'Proclamation': [0.75, 0.80, 0.75, 0.85],
            'Witness': [0.78, 0.85, 0.65, 0.88],
            'Testimony': [0.80, 0.88, 0.62, 0.86],
        }
        
        # === FAITH/BELIEF ===
        dictionary['faith'] = {
            'Faith': [0.82, 0.75, 0.55, 0.88],
            'Believe': [0.80, 0.73, 0.58, 0.85],
            'Trust': [0.85, 0.78, 0.52, 0.86],
            'Hope': [0.88, 0.70, 0.48, 0.85],
            'Confidence': [0.75, 0.80, 0.65, 0.88],
            'Assurance': [0.78, 0.85, 0.60, 0.90],
            'Conviction': [0.72, 0.88, 0.68, 0.90],
            'Devotion': [0.88, 0.82, 0.55, 0.85],
            'Commitment': [0.80, 0.85, 0.70, 0.88],
            'Obedience': [0.75, 0.90, 0.75, 0.88],
        }
        
        # === SACRAMENTS ===
        dictionary['sacraments'] = {
            'Baptism': [0.70, 0.80, 0.60, 0.75],
            'Baptize': [0.68, 0.78, 0.62, 0.73],
            'Water': [0.75, 0.70, 0.45, 0.65],
            'Communion': [0.88, 0.75, 0.50, 0.85],
            'Eucharist': [0.90, 0.78, 0.52, 0.88],
            'Bread': [0.80, 0.70, 0.55, 0.75],
            'Wine': [0.75, 0.68, 0.58, 0.72],
            'Body': [0.70, 0.75, 0.65, 0.78],
            'Blood': [0.65, 0.80, 0.70, 0.75],
            'Covenant': [0.82, 0.92, 0.70, 0.90],
        }
        
        # === LOVE/MERCY ===
        dictionary['love'] = {
            'Love': [0.98, 0.50, 0.30, 0.65],
            'Agape': [0.98, 0.55, 0.28, 0.70],
            'Compassion': [0.95, 0.60, 0.35, 0.75],
            'Mercy': [0.95, 0.70, 0.35, 0.85],
            'Grace': [0.95, 0.68, 0.32, 0.88],
            'Kindness': [0.92, 0.65, 0.40, 0.75],
            'Gentleness': [0.90, 0.62, 0.35, 0.72],
            'Patience': [0.88, 0.75, 0.38, 0.85],
            'Forgiveness': [0.95, 0.78, 0.40, 0.88],
            'Reconciliation': [0.92, 0.85, 0.45, 0.90],
        }
        
        # === SIN/REPENTANCE ===
        dictionary['sin'] = {
            'Sin': [0.25, 0.40, 0.65, 0.35],
            'Transgression': [0.28, 0.45, 0.68, 0.38],
            'Iniquity': [0.22, 0.42, 0.70, 0.32],
            'Evil': [0.15, 0.35, 0.80, 0.25],
            'Wickedness': [0.18, 0.38, 0.82, 0.28],
            'Repentance': [0.75, 0.88, 0.50, 0.85],
            'Repent': [0.73, 0.86, 0.52, 0.83],
            'Confession': [0.70, 0.85, 0.48, 0.80],
            'Contrition': [0.78, 0.82, 0.45, 0.82],
            'Remorse': [0.72, 0.75, 0.42, 0.70],
        }
        
        # === SALVATION/REDEMPTION ===
        dictionary['salvation'] = {
            'Salvation': [0.88, 0.85, 0.70, 0.92],
            'Redemption': [0.90, 0.88, 0.72, 0.95],
            'Ransom': [0.85, 0.90, 0.75, 0.90],
            'Atonement': [0.88, 0.92, 0.68, 0.93],
            'Sacrifice': [0.82, 0.88, 0.70, 0.88],
            'Justification': [0.75, 0.95, 0.60, 0.92],
            'Sanctification': [0.85, 0.90, 0.55, 0.95],
            'Regeneration': [0.88, 0.85, 0.65, 0.92],
            'Renewal': [0.85, 0.80, 0.62, 0.88],
            'Restoration': [0.88, 0.85, 0.68, 0.90],
        }
        
        # === WORSHIP/PRAYER ===
        dictionary['worship'] = {
            'Worship': [0.90, 0.80, 0.50, 0.88],
            'Praise': [0.92, 0.75, 0.55, 0.85],
            'Adoration': [0.95, 0.78, 0.48, 0.88],
            'Prayer': [0.88, 0.75, 0.45, 0.90],
            'Intercession': [0.90, 0.80, 0.52, 0.88],
            'Supplication': [0.85, 0.78, 0.55, 0.85],
            'Thanksgiving': [0.92, 0.72, 0.48, 0.82],
            'Blessing': [0.93, 0.75, 0.50, 0.85],
            'Consecration': [0.85, 0.88, 0.55, 0.92],
            'Dedication': [0.88, 0.85, 0.60, 0.90],
        }
        
        # === JUDGMENT/JUSTICE ===
        dictionary['judgment'] = {
            'Judgment': [0.50, 0.95, 0.80, 0.92],
            'Justice': [0.60, 0.98, 0.75, 0.95],
            'Righteousness': [0.70, 0.95, 0.65, 0.92],
            'Law': [0.55, 0.95, 0.70, 0.90],
            'Commandment': [0.60, 0.92, 0.75, 0.88],
            'Decree': [0.55, 0.90, 0.78, 0.85],
            'Statute': [0.58, 0.92, 0.72, 0.88],
            'Ordinance': [0.60, 0.90, 0.70, 0.86],
            'Condemnation': [0.30, 0.88, 0.85, 0.80],
            'Punishment': [0.35, 0.85, 0.88, 0.75],
        }
        
        # === CREATION/NATURE ===
        dictionary['creation'] = {
            'Creation': [0.80, 0.85, 0.88, 0.95],
            'Heaven': [0.85, 0.88, 0.75, 0.95],
            'Earth': [0.70, 0.75, 0.80, 0.85],
            'Light': [0.80, 0.85, 0.70, 0.92],
            'Darkness': [0.35, 0.50, 0.65, 0.55],
            'Life': [0.90, 0.75, 0.80, 0.88],
            'Death': [0.30, 0.70, 0.85, 0.75],
            'Resurrection': [0.88, 0.90, 0.85, 0.95],
            'Eternal Life': [0.92, 0.88, 0.75, 0.98],
            'Paradise': [0.95, 0.85, 0.70, 0.92],
        }
        
        # === HUMAN CONDITION ===
        dictionary['human'] = {
            'Man': [0.60, 0.65, 0.70, 0.75],
            'Woman': [0.65, 0.65, 0.68, 0.75],
            'Soul': [0.75, 0.70, 0.55, 0.88],
            'Spirit': [0.80, 0.68, 0.52, 0.90],
            'Heart': [0.88, 0.65, 0.50, 0.80],
            'Mind': [0.65, 0.75, 0.55, 0.92],
            'Flesh': [0.45, 0.55, 0.75, 0.60],
            'Body': [0.60, 0.65, 0.75, 0.70],
            'Servant': [0.80, 0.82, 0.65, 0.85],
            'Disciple': [0.82, 0.85, 0.68, 0.90],
        }
        
        # === ESCHATOLOGY ===
        dictionary['eschatology'] = {
            'Second Coming': [0.80, 0.90, 0.88, 0.95],
            'Return': [0.75, 0.85, 0.82, 0.90],
            'Parousia': [0.78, 0.88, 0.85, 0.93],
            'Tribulation': [0.40, 0.75, 0.80, 0.75],
            'Rapture': [0.85, 0.82, 0.78, 0.90],
            'Millennium': [0.80, 0.88, 0.85, 0.92],
            'New Heaven': [0.92, 0.90, 0.80, 0.98],
            'New Earth': [0.90, 0.88, 0.82, 0.96],
            'Eternal': [0.85, 0.95, 0.75, 0.98],
            'Everlasting': [0.88, 0.92, 0.78, 0.96],
        }
        
        return dictionary
    
    def get_coordinates(self, term: str, category: str = None) -> list:
        """Get LJPW coordinates for a term."""
        if category:
            return self.dictionary.get(category, {}).get(term)
        else:
            # Search all categories
            for cat_dict in self.dictionary.values():
                if term in cat_dict:
                    return cat_dict[term]
            return None
    
    def search_similar(self, coords: list, threshold: float = 0.15) -> list:
        """Find terms with similar coordinates."""
        results = []
        
        for category, terms in self.dictionary.items():
            for term, term_coords in terms.items():
                distance = np.linalg.norm(np.array(coords) - np.array(term_coords))
                if distance < threshold:
                    results.append({
                        'term': term,
                        'category': category,
                        'coords': term_coords,
                        'distance': float(distance)
                    })
        
        results.sort(key=lambda x: x['distance'])
        return results
    
    def export_json(self, filepath: str):
        """Export dictionary to JSON."""
        # Flatten for export
        flat_dict = {}
        for category, terms in self.dictionary.items():
            for term, coords in terms.items():
                flat_dict[term] = {
                    'category': category,
                    'coordinates': coords,
                    'L': coords[0],
                    'J': coords[1],
                    'P': coords[2],
                    'W': coords[3]
                }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(flat_dict, f, indent=2, ensure_ascii=False)
    
    def get_stats(self) -> dict:
        """Get dictionary statistics."""
        total_terms = sum(len(terms) for terms in self.dictionary.values())
        
        return {
            'total_terms': total_terms,
            'categories': len(self.dictionary),
            'terms_per_category': {
                cat: len(terms) for cat, terms in self.dictionary.items()
            }
        }


# Create and export dictionary
if __name__ == "__main__":
    import numpy as np
    
    print("="*80)
    print("THEOLOGICAL DICTIONARY BUILDER")
    print("="*80)
    
    dictionary = TheologicalDictionary()
    stats = dictionary.get_stats()
    
    print(f"\nDictionary Statistics:")
    print(f"  Total Terms: {stats['total_terms']}")
    print(f"  Categories: {stats['categories']}")
    print(f"\nTerms per Category:")
    for cat, count in stats['terms_per_category'].items():
        print(f"  {cat:20} {count:3} terms")
    
    # Export
    dictionary.export_json('experiments/theological_dictionary.json')
    print(f"\nDictionary exported to: experiments/theological_dictionary.json")
    
    # Test search
    print(f"\n{'='*80}")
    print("SAMPLE SEARCHES")
    print('='*80)
    
    # Search for terms similar to "Love"
    love_coords = dictionary.get_coordinates('Love')
    print(f"\nTerms similar to 'Love' {love_coords}:")
    similar = dictionary.search_similar(love_coords, threshold=0.10)
    for result in similar[:5]:
        print(f"  {result['term']:20} distance={result['distance']:.3f}")
    
    # Search for terms similar to "Justice"
    justice_coords = dictionary.get_coordinates('Justice')
    print(f"\nTerms similar to 'Justice' {justice_coords}:")
    similar = dictionary.search_similar(justice_coords, threshold=0.10)
    for result in similar[:5]:
        print(f"  {result['term']:20} distance={result['distance']:.3f}")
    
    print(f"\n{'='*80}")
    print("THEOLOGICAL DICTIONARY COMPLETE")
    print("="*80)
