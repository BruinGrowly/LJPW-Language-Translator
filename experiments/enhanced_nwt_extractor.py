"""
Enhanced NWT Gospel Extractor
Extract multiple chapters from all 4 Gospels from nwtsty1_E.pdf
"""

import pdfplumber
import re
import json
from pathlib import Path


class EnhancedNWTParser:
    """Parse New World Translation PDF for multiple Gospel chapters."""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)
        self.gospel_structure = {
            'Matthew': {'chapters': 28, 'start_page': None},
            'Mark': {'chapters': 16, 'start_page': None},
            'Luke': {'chapters': 24, 'start_page': None},
            'John': {'chapters': 21, 'start_page': None}
        }
    
    def find_gospel_pages(self):
        """Scan PDF to find where each Gospel starts."""
        print("Scanning PDF for Gospel locations...")
        
        with pdfplumber.open(self.pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if not text:
                    continue
                
                # Look for Gospel headers
                for gospel in ['Matthew', 'Mark', 'Luke', 'John']:
                    # Look for book title (usually in caps or title case)
                    if gospel.upper() in text or gospel in text:
                        # Check if this looks like the start (chapter 1)
                        if re.search(r'\b1\b', text[:500]):  # Chapter 1 near top
                            if self.gospel_structure[gospel]['start_page'] is None:
                                self.gospel_structure[gospel]['start_page'] = page_num
                                print(f"  Found {gospel} starting at page {page_num}")
        
        return self.gospel_structure
    
    def extract_chapter(self, book: str, chapter: int, start_page: int, max_pages: int = 5):
        """
        Extract a specific chapter from a Gospel.
        
        Args:
            book: Gospel name (Matthew, Mark, Luke, John)
            chapter: Chapter number
            start_page: Page to start searching from
            max_pages: Maximum pages to search
        """
        verses = {}
        
        print(f"\nExtracting {book} Chapter {chapter}...")
        
        with pdfplumber.open(self.pdf_path) as pdf:
            # Search from start_page forward
            for offset in range(max_pages):
                page_num = start_page + offset
                if page_num >= len(pdf.pages):
                    break
                
                page = pdf.pages[page_num]
                text = page.extract_text()
                
                if not text:
                    continue
                
                # Check if this page contains our chapter
                # Look for chapter heading or verse 1
                chapter_pattern = rf'{book}.*?{chapter}\b|CHAPTER\s+{chapter}\b'
                if not re.search(chapter_pattern, text, re.IGNORECASE):
                    # Also check if we see verse numbers that match
                    if not re.search(r'\b1\s+[A-Z]', text):
                        continue
                
                # Extract verses from this page
                page_verses = self._extract_verses_from_text(text)
                
                if page_verses:
                    print(f"  Page {page_num}: Found {len(page_verses)} verses")
                    verses.update(page_verses)
                
                # Stop if we've found a good number of verses
                if len(verses) > 20:
                    # Check if next page has higher verse numbers
                    if offset + 1 < max_pages:
                        next_page = pdf.pages[page_num + 1]
                        next_text = next_page.extract_text()
                        if next_text:
                            next_verses = self._extract_verses_from_text(next_text)
                            if next_verses:
                                max_verse_current = max(verses.keys()) if verses else 0
                                min_verse_next = min(next_verses.keys()) if next_verses else 999
                                if min_verse_next > max_verse_current:
                                    # Continue to next page
                                    verses.update(next_verses)
        
        return verses
    
    def _extract_verses_from_text(self, text: str) -> dict:
        """Extract verse numbers and text from page text."""
        verses = {}
        
        # Pattern: verse number followed by text
        # More flexible pattern to handle various formats
        lines = text.split('\n')
        
        current_verse = None
        current_text = []
        
        for line in lines:
            # Check if line starts with a verse number
            verse_match = re.match(r'^(\d+)\s+(.+)$', line.strip())
            
            if verse_match:
                # Save previous verse if exists
                if current_verse is not None and current_text:
                    verse_text = ' '.join(current_text).strip()
                    verse_text = re.sub(r'\s+', ' ', verse_text)
                    verses[current_verse] = verse_text
                
                # Start new verse
                current_verse = int(verse_match.group(1))
                current_text = [verse_match.group(2)]
            elif current_verse is not None:
                # Continue current verse
                current_text.append(line.strip())
        
        # Save last verse
        if current_verse is not None and current_text:
            verse_text = ' '.join(current_text).strip()
            verse_text = re.sub(r'\s+', ' ', verse_text)
            verses[current_verse] = verse_text
        
        return verses
    
    def extract_priority_chapters(self):
        """Extract priority chapters for Phase 6."""
        priority = {
            'Mark': [1, 2, 4, 8, 13, 16],
            'Matthew': [5, 6, 7, 13, 24, 25, 28],
            'Luke': [1, 6, 15, 24],
            'John': [1, 3, 14, 15, 16, 17, 20, 21]
        }
        
        # Find Gospel locations
        self.find_gospel_pages()
        
        results = {}
        
        for book, chapters in priority.items():
            start_page = self.gospel_structure[book]['start_page']
            
            if start_page is None:
                print(f"\nWarning: Could not find {book} in PDF")
                continue
            
            results[book] = {}
            
            for chapter in chapters:
                # Estimate page offset (rough: ~2-3 pages per chapter)
                estimated_offset = (chapter - 1) * 2
                search_start = start_page + estimated_offset
                
                verses = self.extract_chapter(book, chapter, search_start, max_pages=10)
                
                if verses:
                    results[book][chapter] = verses
                    print(f"  [OK] {book} {chapter}: {len(verses)} verses extracted")
                else:
                    print(f"  [FAIL] {book} {chapter}: No verses found")
        
        return results


def main():
    """Extract priority Gospel chapters."""
    pdf_path = 'experiments/nwt_E.pdf'
    
    print("="*80)
    print("ENHANCED NWT GOSPEL EXTRACTOR")
    print("="*80)
    print("\nExtracting priority chapters from all 4 Gospels\n")
    
    parser = EnhancedNWTParser(pdf_path)
    
    # Extract priority chapters
    results = parser.extract_priority_chapters()
    
    # Save results
    print(f"\n{'='*80}")
    print("SAVING RESULTS")
    print('='*80)
    
    total_verses = 0
    
    for book, chapters in results.items():
        for chapter, verses in chapters.items():
            # Save to corpus directory
            corpus_dir = Path('corpus') / book.lower()
            corpus_dir.mkdir(parents=True, exist_ok=True)
            
            output = {
                'book': book,
                'chapter': chapter,
                'translation': 'New World Translation',
                'language': 'English',
                'verse_count': len(verses),
                'verses': {str(k): v for k, v in verses.items()}
            }
            
            filepath = corpus_dir / f'chapter_{chapter:02d}.json'
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            
            print(f"  Saved: {filepath} ({len(verses)} verses)")
            total_verses += len(verses)
    
    print(f"\n{'='*80}")
    print(f"EXTRACTION COMPLETE")
    print('='*80)
    print(f"\nTotal verses extracted: {total_verses}")
    print(f"Progress toward 1000-verse goal: {(total_verses/1000)*100:.1f}%")


if __name__ == "__main__":
    main()
