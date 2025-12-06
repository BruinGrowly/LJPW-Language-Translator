import json
import requests
from pathlib import Path
import time

class WebBibleExtractor:
    """Extracts Bible verses from World English Bible (WEB) JSON files on GitHub."""
    
    BASE_URL = "https://raw.githubusercontent.com/TehShrike/world-english-bible/master/json"
    
    BOOKS = ['mark', 'matthew', 'luke', 'john']
    
    def extract_all(self):
        print("="*80)
        print("WORLD ENGLISH BIBLE (WEB) EXTRACTOR")
        print("="*80)
        
        total_verses = 0
        total_chapters = 0
        
        for book in self.BOOKS:
            print(f"\nProcessing {book.title()}...")
            
            # Download JSON
            url = f"{self.BASE_URL}/{book}.json"
            print(f"  Downloading {url}...")
            
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
            except Exception as e:
                print(f"  [ERROR] Failed to download/parse {book}: {e}")
                continue
            
            # Parse Verses
            # Structure: list of objects.
            # We want to group by chapter, then verse.
            bible_data = {} # {chapter_num: {verse_num: text}}
            
            print(f"  Parsing {len(data)} chunks...")
            
            for item in data:
                if 'chapterNumber' in item and 'verseNumber' in item and 'value' in item:
                    ch = item['chapterNumber']
                    v = item['verseNumber']
                    text = item['value']
                    
                    if ch not in bible_data:
                        bible_data[ch] = {}
                    
                    if v not in bible_data[ch]:
                        bible_data[ch][v] = ""
                        
                    bible_data[ch][v] += text
            
            # Save Chapters
            corpus_dir = Path(f'corpus/{book}')
            corpus_dir.mkdir(parents=True, exist_ok=True)
            
            # Iterate chapters in order
            chapters = sorted(bible_data.keys())
            for chapter in chapters:
                verses_map = bible_data[chapter]
                cleaned_verses = {}
                
                # Clean text
                for v_num in sorted(verses_map.keys()):
                    raw_text = verses_map[v_num]
                    # Consolidate whitespace
                    clean = " ".join(raw_text.split())
                    cleaned_verses[str(v_num)] = clean
                
                # Create Chapter JSON
                chapter_data = {
                    'book': book.title(),
                    'chapter': chapter,
                    'translation': 'World English Bible',
                    'language': 'English',
                    'verse_count': len(cleaned_verses),
                    'verses': cleaned_verses
                }
                
                output_file = corpus_dir / f'chapter_{chapter:02d}.json'
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(chapter_data, f, indent=2, ensure_ascii=False)
                
                print(f"    Saved Chapter {chapter}: {len(cleaned_verses)} verses")
                total_chapters += 1
                total_verses += len(cleaned_verses)
                
            time.sleep(1) # Be nice to GitHub
            
        print("="*80)
        print("EXTRACTION COMPLETE")
        print(f"Total Chapters: {total_chapters}")
        print(f"Total Verses: {total_verses}")
        print("="*80)

if __name__ == "__main__":
    extractor = WebBibleExtractor()
    extractor.extract_all()
