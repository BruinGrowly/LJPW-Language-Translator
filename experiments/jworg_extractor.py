"""
JW.org Bible Web Scraper
Extracts clean Gospel verses from jw.org website
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from pathlib import Path

class JWOrgExtractor:
    """Extract Bible verses from JW.org website."""
    
    BASE_URL = "https://www.jw.org/en/library/bible/nwt/books"
    
    # Priority chapters for Phase 6
    PRIORITY_CHAPTERS = {
        'mark': [1, 2, 4, 8, 13, 16],
        'matthew': [5, 6, 7, 13, 24, 25, 28],
        'luke': [1, 6, 15, 24],
        'john': [1, 3, 14, 15, 16, 17, 20, 21]
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def extract_chapter(self, book: str, chapter: int) -> dict:
        """Extract all verses from a specific chapter."""
        url = f"{self.BASE_URL}/{book}/{chapter}/"
        
        print(f"  Fetching {book.title()} {chapter}...")
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all verse elements
            verses = {}
            verse_elements = soup.find_all('p', class_='sb')
            
            for verse_elem in verse_elements:
                # Get verse number
                verse_num_elem = verse_elem.find('strong', class_='v')
                if not verse_num_elem:
                    continue
                
                verse_num = verse_num_elem.text.strip()
                
                # Get verse text (everything after the verse number)
                verse_text = verse_elem.get_text()
                # Remove verse number from text
                verse_text = verse_text.replace(verse_num, '', 1).strip()
                
                # Clean up extra whitespace
                verse_text = ' '.join(verse_text.split())
                
                verses[verse_num] = verse_text
            
            if not verses:
                print(f"    [WARN] No verses found for {book} {chapter}")
                return None
            
            return {
                'book': book.title(),
                'chapter': chapter,
                'translation': 'New World Translation',
                'language': 'English',
                'verse_count': len(verses),
                'verses': verses
            }
            
        except Exception as e:
            print(f"    [ERROR] Failed to extract {book} {chapter}: {e}")
            return None
    
    def extract_all_priority_chapters(self):
        """Extract all priority chapters for Phase 6."""
        print("="*80)
        print("JW.ORG GOSPEL EXTRACTOR")
        print("="*80)
        print()
        
        total_verses = 0
        total_chapters = 0
        
        for book, chapters in self.PRIORITY_CHAPTERS.items():
            print(f"Extracting {book.title()}...")
            
            # Create corpus directory
            corpus_dir = Path(f'corpus/{book}')
            corpus_dir.mkdir(parents=True, exist_ok=True)
            
            for chapter in chapters:
                chapter_data = self.extract_chapter(book, chapter)
                
                if chapter_data:
                    # Save to JSON
                    output_file = corpus_dir / f'chapter_{chapter:02d}.json'
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(chapter_data, f, indent=2, ensure_ascii=False)
                    
                    verse_count = chapter_data['verse_count']
                    total_verses += verse_count
                    total_chapters += 1
                    print(f"    [OK] {book.title()} {chapter}: {verse_count} verses")
                
                # Be respectful - don't hammer the server
                time.sleep(1)
            
            print()
        
        print("="*80)
        print("EXTRACTION COMPLETE")
        print("="*80)
        print(f"\nTotal chapters extracted: {total_chapters}")
        print(f"Total verses extracted: {total_verses}")
        print(f"Progress toward 1000-verse goal: {total_verses/10:.1f}%")
        print()

def main():
    extractor = JWOrgExtractor()
    extractor.extract_all_priority_chapters()

if __name__ == '__main__':
    main()
