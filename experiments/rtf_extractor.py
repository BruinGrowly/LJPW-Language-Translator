"""
RTF Bible Extractor
Extracts clean Gospel verses from NWT RTF files
"""

from striprtf.striprtf import rtf_to_text
import re
import json
from pathlib import Path

class RTFBibleExtractor:
    """Extract Bible verses from RTF files."""
    
    RTF_DIR = Path('experiments/nwt_E.rtf')
    
    # Gospel files
    GOSPEL_FILES = {
        'matthew': 'nwt_40_Mt_E.rtf',
        'mark': 'nwt_41_Mr_E.rtf',
        'luke': 'nwt_42_Lu_E.rtf',
        'john': 'nwt_43_Joh_E.rtf'
    }
    
    # Priority chapters for Phase 6
    PRIORITY_CHAPTERS = {
        'mark': [1, 2, 4, 8, 13, 16],
        'matthew': [5, 6, 7, 13, 24, 25, 28],
        'luke': [1, 6, 15, 24],
        'john': [1, 3, 14, 15, 16, 17, 20, 21]
    }
    
    def extract_chapter(self, book: str, chapter: int) -> dict:
        """Extract all verses from a specific chapter."""
        rtf_file = self.RTF_DIR / self.GOSPEL_FILES[book]
        
        print(f"  Extracting {book.title()} {chapter}...")
        
        try:
            # Read and convert RTF to plain text
            with open(rtf_file, 'r', encoding='utf-8', errors='ignore') as f:
                rtf_content = f.read()
            
            text = rtf_to_text(rtf_content)
            
            # Find the chapter block
            # 1. Find all "Chapter X" occurrences
            chapter_marker = f"Chapter {chapter}"
            matches = list(re.finditer(rf'^{chapter_marker}\s*$', text, re.MULTILINE))
            
            start_idx = -1
            end_idx = len(text)
            
            # 2. Identify the REAL chapter start (not Outline)
            # The real chapter is followed by verse 1
            for m in matches:
                # Look ahead for "1 "
                # Reduced window to 200 chars to avoid catching Verse 1 of NEXT chapter (or First chapter if matching Outline)
                chunk = text[m.end():m.end()+200] 
                if re.search(r'(?:^|\s)1[\s\xa0]', chunk):
                    start_idx = m.end()
                    break
            
            if start_idx == -1:
                # Fallback: Try just finding "1 " after ANY "Chapter X"
                # If rigorous check failed, just take the last "Chapter X" as it's usually the text body
                # (Outline is usually at start)
                if matches:
                    start_idx = matches[-1].end()
                    print(f"    [WARN] Rigorous check failed, using last occurrence of 'Chapter {chapter}'")
                else:
                    print(f"    [WARN] Could not locate 'Chapter {chapter}' marker")
                    return None

            # 3. Find end of chapter (Chapter X+1 OR End of text)
            next_chapter_marker = f"Chapter {chapter + 1}"
            next_matches = list(re.finditer(rf'^{next_chapter_marker}\s*$', text, re.MULTILINE))
            
            for m in next_matches:
                if m.start() > start_idx:
                    end_idx = m.start()
                    break
            
            chapter_text = text[start_idx:end_idx]
            
            # 4. Sequential Verse Scanning
            # Extract verses 1, 2, 3... in order
            verses = {}
            current_v = 1
            
            # Replace non-breaking spaces with regular spaces for easier regex
            chapter_text = chapter_text.replace('\u00a0', ' ')
            
            # Current search cursor within chapter_text
            cursor = 0
            
            while True:
                # Find start of current verse
                # Pattern: (Start or Space) + N + Space
                # We search from current cursor position
                pattern_start = rf'(?:^|\s){current_v}\s'
                match = re.search(pattern_start, chapter_text[cursor:])
                
                if not match:
                    if current_v == 1:
                        print(f"    [WARN] Verse 1 not found in extracted text block")
                        # Debug: print first 100 chars
                        print(f"    Snippe: {chapter_text[:100]!r}")
                        return None
                    break # No more verses found (normal end of chapter)
                
                # Start of verse text is end of number match
                # match.start() is relative to cursor
                match_abs_start = cursor + match.start()
                v_start = cursor + match.end()
                
                # Find start of NEXT verse to define end of THIS verse
                pattern_next = rf'(?:^|\s){current_v + 1}\s'
                match_next = re.search(pattern_next, chapter_text[v_start:])
                
                if match_next:
                    # Found next verse, so this verse ends here
                    v_end = v_start + match_next.start()
                    v_text = chapter_text[v_start:v_end]
                    
                    # Update cursor to point to the start of the next verse NUMBER
                    # (so the next iteration finds '{current_v+1} ')
                    # match_next.start() points to the space before number
                    cursor = v_start + match_next.start()
                    
                else:
                    # Last verse in chapter
                    # Capture everything until end of chapter block
                    # But be careful of trailing junk. Actually chapter split should handle it.
                    v_text = chapter_text[v_start:]
                    verses[str(current_v)] = self._clean_text(v_text)
                    break
                
                verses[str(current_v)] = self._clean_text(v_text)
                current_v += 1
            
            if not verses:
                 print(f"    [WARN] No verses extracted")
                 return None
                 
            print(f"    [OK] {len(verses)} verses extracted")
            
            return {
                'book': book.title(),
                'chapter': chapter,
                'translation': 'New World Translation',
                'language': 'English',
                'verse_count': len(verses),
                'verses': verses
            }
            
        except Exception as e:
            print(f"    [ERROR] {e}")
            import traceback
            traceback.print_exc()
            return None

    def _clean_text(self, text: str) -> str:
        """Clean extracted verse text."""
        # Remove footnotes markers like + or *
        # Consolidate whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def extract_all_priority_chapters(self):
        """Extract all priority chapters for Phase 6."""
        print("="*80)
        print("RTF GOSPEL EXTRACTOR (SEQUENTIAL SCAN)")
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
                    
                    total_verses += chapter_data['verse_count']
                    total_chapters += 1
            
            print()
        
        print("="*80)
        print("EXTRACTION COMPLETE")
        print("="*80)
        print(f"\nTotal chapters extracted: {total_chapters}")
        print(f"Total verses extracted: {total_verses}")
        print(f"Progress toward 1000-verse goal: {total_verses/10:.1f}%")
        print()

def main():
    extractor = RTFBibleExtractor()
    extractor.extract_all_priority_chapters()

if __name__ == '__main__':
    main()
