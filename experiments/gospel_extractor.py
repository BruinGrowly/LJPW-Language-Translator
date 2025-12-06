"""
Gospel Extraction Framework
Tools for extracting and managing multi-Gospel corpus
"""

import json
import os
from pathlib import Path


class GospelExtractor:
    """Helper for creating and validating Gospel chapter entries."""
    
    def __init__(self, corpus_dir='corpus'):
        self.corpus_dir = Path(corpus_dir)
        self.corpus_dir.mkdir(exist_ok=True)
        
        # Create book directories
        for book in ['matthew', 'mark', 'luke', 'john']:
            (self.corpus_dir / book).mkdir(exist_ok=True)
    
    def create_chapter_template(self, book: str, chapter: int, verse_count: int) -> dict:
        """Generate JSON template for manual entry."""
        template = {
            "book": book.capitalize(),
            "chapter": chapter,
            "translation": "New World Translation",
            "language": "English",
            "verse_count": verse_count,
            "verses": {
                str(i): f"[Enter verse {i} text here]"
                for i in range(1, verse_count + 1)
            }
        }
        return template
    
    def save_template(self, book: str, chapter: int, verse_count: int):
        """Save template to file for manual editing."""
        template = self.create_chapter_template(book, chapter, verse_count)
        filepath = self.corpus_dir / book / f"chapter_{chapter:02d}_template.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2, ensure_ascii=False)
        
        print(f"Template created: {filepath}")
        print(f"Please edit this file to add verse text, then validate.")
        return filepath
    
    def validate_entry(self, filepath: str) -> dict:
        """Validate chapter entry."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        errors = []
        warnings = []
        
        # Check required fields
        required_fields = ['book', 'chapter', 'translation', 'language', 'verse_count', 'verses']
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        # Check verse count matches
        if 'verses' in data and 'verse_count' in data:
            actual_count = len(data['verses'])
            expected_count = data['verse_count']
            if actual_count != expected_count:
                errors.append(f"Verse count mismatch: expected {expected_count}, got {actual_count}")
        
        # Check for placeholder text
        if 'verses' in data:
            for verse_num, text in data['verses'].items():
                if '[Enter verse' in text or text.strip() == '':
                    warnings.append(f"Verse {verse_num} appears to be placeholder or empty")
        
        result = {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'verse_count': len(data.get('verses', {}))
        }
        
        return result
    
    def get_corpus_statistics(self) -> dict:
        """Get statistics about the corpus."""
        stats = {
            'books': {},
            'total_chapters': 0,
            'total_verses': 0
        }
        
        for book in ['matthew', 'mark', 'luke', 'john']:
            book_dir = self.corpus_dir / book
            if not book_dir.exists():
                continue
            
            chapter_files = list(book_dir.glob('chapter_*.json'))
            # Exclude templates
            chapter_files = [f for f in chapter_files if 'template' not in f.name]
            
            book_verses = 0
            for chapter_file in chapter_files:
                with open(chapter_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    book_verses += len(data.get('verses', {}))
            
            stats['books'][book] = {
                'chapters': len(chapter_files),
                'verses': book_verses
            }
            stats['total_chapters'] += len(chapter_files)
            stats['total_verses'] += book_verses
        
        return stats


def create_mark_templates():
    """Create templates for all Mark chapters."""
    extractor = GospelExtractor()
    
    # Mark chapter verse counts
    mark_verses = {
        1: 45, 2: 28, 3: 35, 4: 41, 5: 43, 6: 56,
        7: 37, 8: 38, 9: 50, 10: 52, 11: 33, 12: 44,
        13: 37, 14: 72, 15: 47, 16: 20
    }
    
    print("="*80)
    print("CREATING MARK GOSPEL TEMPLATES")
    print("="*80)
    print(f"\nCreating templates for all 16 chapters of Mark\n")
    
    for chapter, verse_count in mark_verses.items():
        if chapter == 1:
            print(f"Chapter {chapter}: Skipping (already complete)")
            continue
        
        filepath = extractor.save_template('mark', chapter, verse_count)
        print(f"  Created: {filepath.name} ({verse_count} verses)")
    
    print(f"\n{'='*80}")
    print("TEMPLATES CREATED")
    print('='*80)
    print("\nNext steps:")
    print("1. Edit template files to add verse text")
    print("2. Run validation to check entries")
    print("3. Analyze chapters with batch analyzer")


def show_corpus_stats():
    """Display corpus statistics."""
    extractor = GospelExtractor()
    stats = extractor.get_corpus_statistics()
    
    print("="*80)
    print("CORPUS STATISTICS")
    print("="*80)
    
    print(f"\nTotal Chapters: {stats['total_chapters']}")
    print(f"Total Verses: {stats['total_verses']}")
    
    print(f"\nBy Book:")
    for book, book_stats in stats['books'].items():
        print(f"  {book.capitalize():10} {book_stats['chapters']:2} chapters, {book_stats['verses']:4} verses")
    
    print(f"\n{'='*80}")
    
    # Progress toward goal
    goal_verses = 1000
    progress = (stats['total_verses'] / goal_verses) * 100
    print(f"Progress toward 1000-verse goal: {progress:.1f}%")
    print(f"Remaining: {goal_verses - stats['total_verses']} verses")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'create':
        create_mark_templates()
    elif len(sys.argv) > 1 and sys.argv[1] == 'stats':
        show_corpus_stats()
    else:
        print("Gospel Extraction Framework")
        print("\nUsage:")
        print("  python gospel_extractor.py create  - Create Mark chapter templates")
        print("  python gospel_extractor.py stats   - Show corpus statistics")
