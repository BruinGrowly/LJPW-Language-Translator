"""
Wedau HTML Parser
Extract verses from Wedau Bible HTML files.
"""

from bs4 import BeautifulSoup
import re
from pathlib import Path


class WedauHTMLParser:
    """Parse Wedau Bible HTML files."""
    
    def __init__(self, html_dir: str):
        self.html_dir = Path(html_dir)
    
    def parse_chapter(self, book: str, chapter: int) -> dict:
        """
        Parse a chapter and extract verses.
        
        Args:
            book: Book code (e.g., 'MRK' for Mark)
            chapter: Chapter number
            
        Returns:
            Dictionary of verse_number: verse_text
        """
        # Construct filename
        filename = f"{book}{chapter:02d}.htm"
        filepath = self.html_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        # Read HTML
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        verses = {}
        
        # Find all verse spans - they have class="verse" and id="V#"
        verse_spans = soup.find_all('span', class_='verse')
        
        for verse_span in verse_spans:
            # Get verse number from id (e.g., "V1" -> 1)
            verse_id = verse_span.get('id', '')
            if not verse_id.startswith('V'):
                continue
            
            try:
                verse_num = int(verse_id[1:])
            except ValueError:
                continue
            
            # Get verse text - it's the text content after the verse number
            # The verse number is inside the span, followed by the verse text
            verse_text = ""
            
            # Get parent div
            parent = verse_span.parent
            if parent:
                # Get all text from this verse span to the next verse span
                collecting = False
                for elem in parent.descendants:
                    if elem == verse_span:
                        collecting = True
                        continue
                    
                    if collecting:
                        # Stop at next verse span
                        if hasattr(elem, 'get') and elem.get('class') == ['verse']:
                            break
                        
                        # Collect text
                        if isinstance(elem, str):
                            text = elem.strip()
                            if text and not text.isdigit():  # Skip verse numbers
                                verse_text += " " + text
            
            # Clean up
            verse_text = re.sub(r'\s+', ' ', verse_text).strip()
            
            # Remove footnote markers and other special chars
            verse_text = re.sub(r'[*†‡§]', '', verse_text)
            
            if verse_text:
                verses[verse_num] = verse_text
        
        return verses
    
    def get_verse(self, book: str, chapter: int, verse: int) -> str:
        """Get a specific verse."""
        verses = self.parse_chapter(book, chapter)
        return verses.get(verse, "")


def main():
    """Test the parser."""
    parser = WedauHTMLParser('experiments/wed-topura_html')
    
    print("="*80)
    print("WEDAU HTML PARSER TEST")
    print("="*80)
    
    # Parse Mark Chapter 1
    verses = parser.parse_chapter('MRK', 1)
    
    print(f"\nExtracted {len(verses)} verses from Mark Chapter 1\n")
    
    # Show first 10 verses
    for verse_num in sorted(verses.keys())[:10]:
        print(f"Mark 1:{verse_num}")
        print(f"  {verses[verse_num]}")
        print()
    
    print("="*80)


if __name__ == "__main__":
    main()
