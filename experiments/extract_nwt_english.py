"""
Extract Mark Chapter 1 from NWT PDF
Parse nwtsty1_E.pdf to get English verses
"""

import pdfplumber
import re
import json
from pathlib import Path


class NWTParser:
    """Parse New World Translation PDF."""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)
    
    def find_mark_chapter_1(self):
        """Find the page(s) containing Mark Chapter 1."""
        mark_pages = []
        
        with pdfplumber.open(self.pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                
                # Look for "MARK" and "1" or "CHAPTER 1"
                if text and ('MARK' in text.upper() or 'Mark' in text):
                    # Check if this is chapter 1
                    if re.search(r'\b1\b', text) or 'CHAPTER 1' in text.upper():
                        mark_pages.append({
                            'page_num': page_num,
                            'page_obj': page,
                            'text_sample': text[:500]
                        })
        
        return mark_pages
    
    def extract_verses(self, page):
        """Extract verses from a page."""
        text = page.extract_text()
        verses = {}
        
        # Pattern: verse number followed by text
        # NWT format typically: "1 The beginning..." or "1The beginning..."
        verse_pattern = r'(\d+)\s*([A-Z][^0-9]+?)(?=\d+\s*[A-Z]|$)'
        
        matches = re.finditer(verse_pattern, text, re.MULTILINE)
        
        for match in matches:
            verse_num = int(match.group(1))
            verse_text = match.group(2).strip()
            
            # Clean up text
            verse_text = re.sub(r'\s+', ' ', verse_text)
            verse_text = re.sub(r'\n', ' ', verse_text)
            
            if verse_num <= 45:  # Mark 1 has 45 verses
                verses[verse_num] = verse_text
        
        return verses
    
    def extract_mark_chapter_1(self):
        """Extract all verses from Mark Chapter 1."""
        print("Searching for Mark Chapter 1 in PDF...")
        
        mark_pages = self.find_mark_chapter_1()
        
        if not mark_pages:
            print("Could not find Mark Chapter 1 in PDF")
            return {}
        
        print(f"Found {len(mark_pages)} potential page(s)")
        
        all_verses = {}
        
        for page_info in mark_pages:
            print(f"\nExamining page {page_info['page_num']}...")
            print(f"Sample: {page_info['text_sample'][:200]}...")
            
            verses = self.extract_verses(page_info['page_obj'])
            
            if verses:
                print(f"Extracted {len(verses)} verses from this page")
                all_verses.update(verses)
        
        return all_verses


def main():
    """Extract Mark Chapter 1 from NWT PDF."""
    pdf_path = 'experiments/nwtsty1_E.pdf'
    
    print("="*80)
    print("NWT PDF PARSER - Mark Chapter 1 Extraction")
    print("="*80)
    
    parser = NWTParser(pdf_path)
    
    # First, let's just explore the PDF structure
    print("\nExploring PDF structure...")
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total pages: {len(pdf.pages)}")
        
        # Sample first few pages to understand structure
        print("\nSampling first 5 pages:")
        for i in range(min(5, len(pdf.pages))):
            page = pdf.pages[i]
            text = page.extract_text()
            if text:
                # Show first 200 chars
                sample = text[:200].replace('\n', ' ')
                print(f"\nPage {i}: {sample}...")
    
    print("\n" + "="*80)
    print("Searching for Mark Chapter 1...")
    print("="*80)
    
    verses = parser.extract_mark_chapter_1()
    
    if verses:
        print(f"\n✓ Successfully extracted {len(verses)} verses")
        
        # Save to JSON
        output = {
            'book': 'Mark',
            'chapter': 1,
            'translation': 'New World Translation',
            'verse_count': len(verses),
            'verses': verses
        }
        
        output_path = 'experiments/nwt_mark_chapter1.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"Saved to: {output_path}")
        
        # Show sample verses
        print("\nSample verses:")
        for i in range(1, min(6, len(verses)+1)):
            if i in verses:
                verse = verses[i]
                display = verse[:80] + "..." if len(verse) > 80 else verse
                print(f"  {i}: {display}")
    else:
        print("\n✗ No verses extracted - need to adjust parsing strategy")
        print("Will need to manually inspect PDF structure")


if __name__ == "__main__":
    main()
