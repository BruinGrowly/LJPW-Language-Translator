import json
import numpy as np
from pathlib import Path
import random

class DatasetBuilder:
    """
    Builds a training dataset for the Neural Decoder.
    
    Converts the analyzed Bible corpus into (LJPW Vector -> Text) pairs.
    """
    
    def __init__(self):
        self.corpus_root = Path('corpus')
        self.output_dir = Path('data/datasets')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def build_dataset(self):
        print("="*80)
        print("BUILDING NEURAL TRANSLATION DATASET")
        print("="*80)
        
        samples = []
        books = ['mark', 'matthew', 'luke', 'john']
        
        # 1. Collect all valid verse pairs
        for book in books:
            book_dir = self.corpus_root / book
            if not book_dir.exists():
                continue
                
            print(f"Processing {book.title()}...")
            for json_file in sorted(book_dir.glob('*.json')):
                samples.extend(self._process_chapter(json_file))
                
        # 2. Shuffle
        random.seed(42)
        random.shuffle(samples)
        
        # 3. Split (80/10/10)
        n = len(samples)
        train_idx = int(0.8 * n)
        val_idx = int(0.9 * n)
        
        train_set = samples[:train_idx]
        val_set = samples[train_idx:val_idx]
        test_set = samples[val_idx:]
        
        # 4. Save
        self._save_split('train', train_set)
        self._save_split('val', val_set)
        self._save_split('test', test_set)
        
        print("-" * 50)
        print(f"Total Samples: {n}")
        print(f"Training:      {len(train_set)}")
        print(f"Validation:    {len(val_set)}")
        print(f"Test:          {len(test_set)}")
        print("="*80)

    def _process_chapter(self, file_path: Path):
        """Extract valid (coords, text) pairs from a chapter."""
        pairs = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            verses = data.get('verses', {})
            coords_map = data.get('ljpw_coordinates', {})
            
            for v_num, text in verses.items():
                if v_num in coords_map:
                    coords = coords_map[v_num]
                    # Ensure valid 4D vector
                    if len(coords) == 4 and all(isinstance(x, (int, float)) for x in coords):
                        pairs.append({
                            'meaning': coords,
                            'text': text.strip(),
                            'ref': f"{data['book']} {data['chapter']}:{v_num}"
                        })
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            
        return pairs

    def _save_split(self, split_name, data):
        """Save dataset split to JSONL."""
        out_path = self.output_dir / f"bible_ljpw_{split_name}.jsonl"
        with open(out_path, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        print(f"Saved {split_name} set to {out_path}")

if __name__ == "__main__":
    builder = DatasetBuilder()
    builder.build_dataset()
