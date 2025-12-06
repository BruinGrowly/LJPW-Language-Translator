import json
import sys
from pathlib import Path

# Add experiments dir to path so we can import the detector
sys.path.append(str(Path(__file__).parent))

from enhanced_pattern_detector import EnhancedPatternDetector

class CorpusProcessor:
    """Enrich the biblical corpus with LJPW semantic coordinates."""
    
    def __init__(self):
        self.detector = EnhancedPatternDetector()
        self.corpus_root = Path('corpus')
        
    def process_all(self):
        print("="*80)
        print("BIBLICAL CORPUS SEMANTIC PROCESSOR")
        print("="*80)
        
        books = ['mark', 'matthew', 'luke', 'john']
        total_verses = 0
        total_chapters = 0
        
        for book in books:
            book_dir = self.corpus_root / book
            if not book_dir.exists():
                print(f"Skipping {book} (not found)")
                continue
                
            print(f"\nProcessing {book.title()}...")
            
            # Process all JSON files in the book directory
            json_files = sorted(book_dir.glob('*.json'))
            
            for json_file in json_files:
                self.process_chapter(json_file)
                total_chapters += 1
            
            # Count verses
            # (We could return count from process_chapter)
            
        print("="*80)
        print("PROCESSING COMPLETE")
        print(f"Total Chapters Processed: {total_chapters}")
        print("="*80)

    def process_chapter(self, file_path: Path):
        """Load chapter, calculate coordinates, save back."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            verses = data.get('verses', {})
            ljpw_map = {}
            
            # Check if already processed to avoid double work? 
            # Re-running is fast enough for 3000 verses.
            
            for v_num, text in verses.items():
                # Detect pattern using Phase 2 logic
                # calculate_field_signature_v2 returns dict with L, J, P, W keys
                result = self.detector.calculate_field_signature_v2(text)
                
                # Format coordinates as list [L, J, P, W]
                coords = [
                    result['L'],
                    result['J'],
                    result['P'],
                    result['W']
                ]
                
                # Store coordinates
                ljpw_map[v_num] = coords
                
            # Update data
            data['ljpw_coordinates'] = ljpw_map
            
            # Save back
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            print(f"  Processed {file_path.name} ({len(verses)} verses)")
            
        except Exception as e:
            print(f"  [ERROR] Processing {file_path.name}: {e}")

if __name__ == "__main__":
    processor = CorpusProcessor()
    processor.process_all()
