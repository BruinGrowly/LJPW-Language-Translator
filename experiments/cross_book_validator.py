import json
import numpy as np
from pathlib import Path
from collections import defaultdict

class CrossBookValidator:
    """Analyze LJPW semantic patterns across the 4 Gospels."""
    
    def __init__(self):
        self.corpus_root = Path('corpus')
        self.data = self._load_corpus()
        
    def _load_corpus(self):
        """Load all processed JSON files."""
        data = defaultdict(dict)
        books = ['mark', 'matthew', 'luke', 'john']
        
        print("Loading corpus...")
        for book in books:
            book_dir = self.corpus_root / book
            for json_file in book_dir.glob('*.json'):
                with open(json_file, 'r', encoding='utf-8') as f:
                    chapter_data = json.load(f)
                    ch = chapter_data['chapter']
                    coords = chapter_data.get('ljpw_coordinates', {})
                    data[book][str(ch)] = coords
        print(f"Loaded {len(data)} books.")
        return data

    def run_validation(self):
        print("\n" + "="*80)
        print("CROSS-BOOK SEMANTIC VALIDATION")
        print("="*80)
        
        self.validate_parallel_passages()
        self.analyze_book_signatures()
        self.analyze_theological_consistency()
        
    def validate_parallel_passages(self):
        """Compare known parallel passages."""
        print("\n1. PARALLEL PASSAGE VALIDATION")
        print("-" * 30)
        
        # Define key parallel events
        parallels = [
            {
                "name": "Feeding of 5000",
                "passages": [
                    ("matthew", "14", "19"), # He instructed the crowds to sit down...
                    ("mark", "6", "41"),    # He took the five loaves...
                    ("luke", "9", "16"),    # He took the five loaves...
                    ("john", "6", "11")     # Jesus took the loaves...
                ]
            },
            {
                "name": "The Great Commission / Ascension Command",
                "passages": [
                    ("matthew", "28", "19"), # Go and make disciples...
                    ("mark", "16", "15"),    # Go into all the world...
                    ("luke", "24", "47")     # repentance and remission of sins should be preached...
                    # John doesn't have direct parallel here
                ]
            },
             {
                "name": "Peter's Confession",
                "passages": [
                    ("matthew", "16", "16"), # You are the Christ...
                    ("mark", "8", "29"),     # You are the Christ...
                    ("luke", "9", "20")      # The Christ of God...
                ]
            }
        ]
        
        total_dist = 0
        count = 0
        
        for event in parallels:
            print(f"\nEvent: {event['name']}")
            coords_list = []
            
            for book, ch, v in event['passages']:
                try:
                    c = self.data[book][ch][v]
                    c_np = np.array(c)
                    coords_list.append(c_np)
                    print(f"  {book.title()} {ch}:{v} -> L={c[0]:.2f}, J={c[1]:.2f}, P={c[2]:.2f}, W={c[3]:.2f}")
                except KeyError:
                    print(f"  [MISSING] {book} {ch}:{v}")
            
            if len(coords_list) > 1:
                # Calculate centroid and avg distance
                centroid = np.mean(coords_list, axis=0)
                dists = [np.linalg.norm(c - centroid) for c in coords_list]
                avg_dist = np.mean(dists)
                total_dist += avg_dist
                count += 1
                
                print(f"  >> Average Distance from Centroid: {avg_dist:.3f}")
                if avg_dist < 0.2:
                    print("  >> [PASS] High semantic consistency")
                elif avg_dist < 0.3:
                    print("  >> [PASS] Moderate semantic consistency")
                else:
                    print("  >> [WARN] Low semantic consistency")

    def analyze_book_signatures(self):
        """Analyze overall LJPW signature for each book."""
        print("\n2. BOOK AUTHORSHIP SIGNATURES")
        print("-" * 30)
        
        print(f"{'Book':<10} {'Love':<6} {'Justice':<8} {'Power':<6} {'Wisdom':<6} {'Entropy'}")
        
        for book, chapters in self.data.items():
            all_coords = []
            for ch, verses in chapters.items():
                for v, c in verses.items():
                    all_coords.append(c)
            
            if not all_coords:
                continue
                
            avg = np.mean(all_coords, axis=0)
            # Entropy/Variance as a proxy for "dynamic range"
            variance = np.mean(np.var(all_coords, axis=0))
            
            print(f"{book.title():<10} {avg[0]:.3f}  {avg[1]:.3f}    {avg[2]:.3f}  {avg[3]:.3f}   {variance:.3f}")

    def analyze_theological_consistency(self):
        print("\n3. THEOLOGICAL CONSISTENCY (Top Verse Analysis)")
        print("-" * 30)
        # Find verse with highest Love, Justice, etc across entire corpus
        
        all_verses = []
        for book, chapters in self.data.items():
            for ch, verses in chapters.items():
                for v, c in verses.items():
                    all_verses.append({
                        'ref': f"{book.title()} {ch}:{v}",
                        'coords': c
                    })
        
        dims = ['Love', 'Justice', 'Power', 'Wisdom']
        for i, dim in enumerate(dims):
            print(f"\nHighest {dim}:")
            # Sort by dimension i
            top = sorted(all_verses, key=lambda x: x['coords'][i], reverse=True)[:3]
            for item in top:
                print(f"  {item['ref']} ({item['coords'][i]:.3f})")

if __name__ == "__main__":
    validator = CrossBookValidator()
    validator.run_validation()
