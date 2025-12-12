#!/usr/bin/env python3
"""
Wedau Bible Vocabulary Extractor
=================================

Extracts vocabulary from the complete Wedau Bible USFM files.
This gives us a massive authentic vocabulary source.

Available books:
- Acts (185KB)
- Mark (118KB)  
- Genesis (93KB)
- Exodus (71KB)
- 1 Samuel (34KB)
- Isaiah (28KB)
- Numbers (26KB)
- Psalms (24KB)
- 2 Kings (24KB)
- Job (13KB)
- And many more...
"""

import os
import re
import sys
import json
from pathlib import Path
from collections import Counter

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')

# Path to Wedau Bible files
BIBLE_DIR = Path(__file__).parent.parent / "corpus" / "wedau_bible"

# USFM markers to skip (metadata, not content)
SKIP_MARKERS = ['id', 'h', 'toc1', 'toc2', 'mt1', 'mt2', 'imt1', 'imq', 'ipr', 
                'im', 'ili', 'iot', 'io1', 'io2', 'io3', 'c', 's1', 's2', 
                'f', 'x', 'fig', 'fr', 'ft', 'fq', 'xo', 'xt', 'r', 'rq',
                'mi', 'sp', 'qs', 'qa', 'qac']


def extract_wedau_text(usfm_content: str) -> str:
    """Extract plain Wedau text from USFM markup."""
    
    # Remove footnotes and cross-references
    text = re.sub(r'\\f\s+.*?\\f\*', '', usfm_content)
    text = re.sub(r'\\x\s+.*?\\x\*', '', text)
    
    # Remove figure references
    text = re.sub(r'\\fig\s+.*?\\fig\*', '', text)
    
    # Remove word attributes
    text = re.sub(r'\\w\s+(.*?)\|.*?\\w\*', r'\1', text)
    
    # Remove quoted text markers but keep content
    text = re.sub(r'\\qt\s+(.*?)\\qt\*', r'\1', text)
    
    # Remove emphasis markers but keep content
    text = re.sub(r'\\em\s+(.*?)\\em\*', r'\1', text)
    
    # Remove transliteration markers but keep content
    text = re.sub(r'\\tl\s+(.*?)\\tl\*', r'\1', text)
    
    # Remove divine name markers but keep content
    text = re.sub(r'\\nd\s+(.*?)\\nd\*', r'\1', text)
    
    # Remove proper name markers but keep content
    text = re.sub(r'\\pn\s*(.*?)\\pn\*', r'\1', text)
    
    # Remove structural markers (keep verse content)
    for marker in SKIP_MARKERS:
        text = re.sub(rf'\\{marker}\s+.*', '', text)
    
    # Keep verse markers for context but extract text after them
    # \v 1 text -> extract "text"
    
    # Remove remaining USFM markers
    text = re.sub(r'\\[a-z0-9]+\s*', ' ', text)
    
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text


def extract_words(text: str) -> list:
    """Extract individual words from text."""
    
    # Remove punctuation except for special Wedau characters
    text = re.sub(r'[.,;:!?"\'\[\]()—\-–]', ' ', text)
    
    # Split into words
    words = text.lower().split()
    
    # Filter out numbers, references, and very short strings
    words = [w for w in words if len(w) > 1 and not w.isdigit()]
    
    return words


def process_usfm_file(filepath: Path) -> dict:
    """Process a single USFM file."""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get book name
    book_match = re.search(r'\\h\s+(.+)', content)
    book_name = book_match.group(1).strip() if book_match else filepath.stem
    
    # Extract text
    text = extract_wedau_text(content)
    
    # Extract words
    words = extract_words(text)
    
    # Count words
    word_counts = Counter(words)
    
    return {
        'book': book_name,
        'word_count': len(words),
        'unique_words': len(word_counts),
        'words': word_counts
    }


def main():
    print("=" * 70)
    print("WEDAU BIBLE VOCABULARY EXTRACTOR")
    print("=" * 70)
    
    if not BIBLE_DIR.exists():
        print(f"ERROR: Bible directory not found: {BIBLE_DIR}")
        return
    
    # Find all USFM files
    usfm_files = list(BIBLE_DIR.glob("*.usfm"))
    print(f"\nFound {len(usfm_files)} USFM files")
    
    # Process each file
    all_words = Counter()
    book_stats = []
    
    for filepath in sorted(usfm_files):
        if filepath.name.startswith('00-') or filepath.name.startswith('01-'):
            continue  # Skip front matter
            
        result = process_usfm_file(filepath)
        book_stats.append({
            'file': filepath.name,
            'book': result['book'],
            'words': result['word_count'],
            'unique': result['unique_words']
        })
        all_words.update(result['words'])
        
        print(f"  {result['book']}: {result['word_count']:,} words, {result['unique_words']:,} unique")
    
    # Summary statistics
    print(f"\n{'='*70}")
    print("VOCABULARY SUMMARY")
    print("="*70)
    
    print(f"\nTotal words processed: {sum(all_words.values()):,}")
    print(f"Unique Wedau words: {len(all_words):,}")
    
    # Most common words
    print(f"\nTop 50 most common Wedau words:")
    print("-" * 50)
    for i, (word, count) in enumerate(all_words.most_common(50), 1):
        print(f"  {i:2}. {word:<20} ({count:,})")
    
    # Save vocabulary to JSON
    output = {
        'source': 'eBible.org Wedau Bible (Wycliffe 2010)',
        'total_words': sum(all_words.values()),
        'unique_words': len(all_words),
        'books_processed': len(book_stats),
        'book_statistics': book_stats,
        'vocabulary': dict(all_words.most_common()),  # Sorted by frequency
    }
    
    output_path = Path(__file__).parent / "wedau_bible_vocabulary.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\nVocabulary saved to: {output_path}")
    
    # Create word-frequency mapping for translation
    print(f"\n{'='*70}")
    print("SAMPLE MAPPINGS (for translation verification)")
    print("="*70)
    
    # Look for known words
    known_patterns = [
        ('god', ['god', 'bada']),
        ('jesus', ['iesu']),
        ('spirit', ['arua']),
        ('love', ['auna']),
        ('holy', ['vivivireina', 'vivivirei']),
        ('truth', ['riwa']),
        ('kingdom', ['vibadana', 'vigulau']),
        ('power', ['rewapana']),
        ('lord', ['bada']),
        ('father', ['amau', 'ama']),
        ('mother', ['ina', 'alo']),
        ('son', ['natu']),
        ('brother', ['tura', 'vareva']),
        ('sister', ['vara', 'varavu']),
    ]
    
    print("\nWord frequency verification:")
    for english, wedau_patterns in known_patterns:
        counts = []
        for pattern in wedau_patterns:
            # Find words containing this pattern
            matching = [(w, c) for w, c in all_words.items() if pattern in w]
            counts.extend(matching)
        
        if counts:
            counts.sort(key=lambda x: -x[1])
            top_matches = counts[:3]
            matches_str = ", ".join([f"{w}({c})" for w, c in top_matches])
            print(f"  {english:<12}: {matches_str}")
    
    return output


if __name__ == '__main__':
    main()
