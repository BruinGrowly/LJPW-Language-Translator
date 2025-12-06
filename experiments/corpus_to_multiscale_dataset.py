import json
import numpy as np
from pathlib import Path
import random

class MultiScaleDatasetBuilder:
    """
    Builds a Multi-Scale training dataset for the Neural Decoder.
    
    Implements "Fractal Profiling" from LJPW Codex:
    - Atomic: Word-level (future)
    - Entity: Verse-level (current)
    - Cluster: Chapter-level context
    - System: Narrative flow (previous verse)
    """
    
    def __init__(self):
        self.corpus_root = Path('corpus')
        self.output_dir = Path('data/datasets')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def build_dataset(self):
        print("="*80)
        print("BUILDING MULTI-SCALE NEURAL TRANSLATION DATASET")
        print("="*80)
        
        samples = []
        books = ['mark', 'matthew', 'luke', 'john']
        
        # 1. Collect all chapters first to calculate chapter contexts
        book_chapters = {}
        for book in books:
            book_dir = self.corpus_root / book
            if not book_dir.exists():
                continue
            book_chapters[book] = self._load_all_chapters(book_dir)
        
        # 2. Build samples with multi-scale context
        for book, chapters in book_chapters.items():
            print(f"Processing {book.title()}...")
            for chapter_data in chapters:
                samples.extend(self._process_chapter_multiscale(chapter_data, chapters))
        
        # 3. Shuffle
        random.seed(42)
        random.shuffle(samples)
        
        # 4. Split (80/10/10)
        n = len(samples)
        train_idx = int(0.8 * n)
        val_idx = int(0.9 * n)
        
        train_set = samples[:train_idx]
        val_set = samples[train_idx:val_idx]
        test_set = samples[val_idx:]
        
        # 5. Save
        self._save_split('train_multiscale', train_set)
        self._save_split('val_multiscale', val_set)
        self._save_split('test_multiscale', test_set)
        
        print("-" * 50)
        print(f"Total Samples: {n}")
        print(f"Training:      {len(train_set)}")
        print(f"Validation:    {len(val_set)}")
        print(f"Test:          {len(test_set)}")
        print("="*80)

    def _load_all_chapters(self, book_dir: Path):
        """Load all chapters for a book."""
        chapters = []
        for json_file in sorted(book_dir.glob('*.json')):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                chapters.append(data)
            except Exception as e:
                print(f"Error loading {json_file}: {e}")
        return chapters

    def _calculate_chapter_context(self, chapter_data):
        """Calculate the average LJPW vector for the entire chapter."""
        coords_map = chapter_data.get('ljpw_coordinates', {})
        if not coords_map:
            return [0.5, 0.5, 0.5, 0.5]  # Neutral fallback
        
        vectors = [coords for coords in coords_map.values() if len(coords) == 4]
        if not vectors:
            return [0.5, 0.5, 0.5, 0.5]
            
        return np.mean(vectors, axis=0).tolist()

    def _process_chapter_multiscale(self, chapter_data, all_chapters):
        """Extract multi-scale context pairs from a chapter."""
        pairs = []
        
        verses = chapter_data.get('verses', {})
        coords_map = chapter_data.get('ljpw_coordinates', {})
        
        # Calculate chapter context
        chapter_context = self._calculate_chapter_context(chapter_data)
        
        # Sort verse numbers for sequential processing
        verse_nums = sorted([int(v) for v in verses.keys()])
        
        prev_coords = None
        for i, v_num in enumerate(verse_nums):
            v_str = str(v_num)
            if v_str not in coords_map:
                continue
                
            coords = coords_map[v_str]
            if len(coords) != 4 or not all(isinstance(x, (int, float)) for x in coords):
                continue
            
            # Narrative flow: use previous verse or neutral
            narrative_flow = prev_coords if prev_coords else [0.5, 0.5, 0.5, 0.5]
            
            pairs.append({
                'verse_meaning': coords,
                'chapter_context': chapter_context,
                'narrative_flow': narrative_flow,
                'text': verses[v_str].strip(),
                'ref': f"{chapter_data['book']} {chapter_data['chapter']}:{v_num}"
            })
            
            prev_coords = coords
            
        return pairs

    def _save_split(self, split_name, data):
        """Save dataset split to JSONL."""
        out_path = self.output_dir / f"bible_ljpw_{split_name}.jsonl"
        with open(out_path, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        print(f"Saved {split_name} set to {out_path}")

if __name__ == "__main__":
    builder = MultiScaleDatasetBuilder()
    builder.build_dataset()
