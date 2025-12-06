"""
Extract Wedau verses from HTML and save to JSON
"""

from wedau_html_parser import WedauHTMLParser
import json


def main():
    parser = WedauHTMLParser('experiments/wed-topura_html')
    
    # Extract Mark Chapter 1
    verses = parser.parse_chapter('MRK', 1)
    
    # Save to JSON
    output = {
        'book': 'Mark',
        'chapter': 1,
        'verse_count': len(verses),
        'verses': verses
    }
    
    with open('experiments/wedau_mark_chapter1.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"Extracted {len(verses)} verses from Mark Chapter 1")
    print("Saved to: experiments/wedau_mark_chapter1.json")
    
    # Show first 5 verses (sample)
    print("\nSample verses:")
    for i in range(1, min(6, len(verses)+1)):
        verse = verses.get(i, "")
        # Truncate for display
        display = verse[:80] + "..." if len(verse) > 80 else verse
        print(f"  {i}: {display}")


if __name__ == "__main__":
    main()
