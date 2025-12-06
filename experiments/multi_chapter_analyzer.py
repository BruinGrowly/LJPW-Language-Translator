"""
Multi-Chapter Content Expansion
Framework for extracting and analyzing content beyond Mark Chapter 1
"""

import sys
sys.path.append('experiments')

from enhanced_pattern_detector import EnhancedPatternDetector
import numpy as np
import json


class MultiChapterAnalyzer:
    """
    Analyze multiple chapters to:
    - Validate consistency across chapters
    - Build larger corpus for training
    - Identify chapter-specific patterns
    """
    
    def __init__(self):
        self.detector = EnhancedPatternDetector()
        
        # Sample verses from Mark Chapter 2 (manually entered for demonstration)
        self.mark_chapter_2 = {
            "1": "And again he entered into Capernaum after some days; and it was noised that he was in the house.",
            "2": "And straightway many were gathered together, insomuch that there was no room to receive them, no, not so much as about the door: and he preached the word unto them.",
            "3": "And they come unto him, bringing one sick of the palsy, which was borne of four.",
            "4": "And when they could not come nigh unto him for the press, they uncovered the roof where he was: and when they had broken it up, they let down the bed wherein the sick of the palsy lay.",
            "5": "When Jesus saw their faith, he said unto the sick of the palsy, Son, thy sins be forgiven thee.",
            "6": "But there were certain of the scribes sitting there, and reasoning in their hearts,",
            "7": "Why doth this man thus speak blasphemies? who can forgive sins but God only?",
            "8": "And immediately when Jesus perceived in his spirit that they so reasoned within themselves, he said unto them, Why reason ye these things in your hearts?",
            "9": "Whether is it easier to say to the sick of the palsy, Thy sins be forgiven thee; or to say, Arise, and take up thy bed, and walk?",
            "10": "But that ye may know that the Son of man hath power on earth to forgive sins, (he saith to the sick of the palsy,)",
        }
    
    def analyze_chapter(self, verses: dict, chapter_num: int) -> dict:
        """Analyze all verses in a chapter."""
        results = []
        
        for verse_num, text in verses.items():
            sig = self.detector.calculate_field_signature(text)
            coords = [sig['L'], sig['J'], sig['P'], sig['W']]
            
            results.append({
                'chapter': chapter_num,
                'verse': int(verse_num),
                'text': text,
                'coordinates': coords,
                'harmony': self.calculate_harmony(coords),
                'confidence': sig['confidence']
            })
        
        return {
            'chapter': chapter_num,
            'verse_count': len(results),
            'verses': results,
            'statistics': self.calculate_chapter_stats(results)
        }
    
    def calculate_harmony(self, coords):
        """Calculate harmony index."""
        L, J, P, W = coords
        distance = np.sqrt((1-L)**2 + (1-J)**2 + (1-P)**2 + (1-W)**2)
        return 1.0 / (1.0 + distance)
    
    def calculate_chapter_stats(self, verses: list) -> dict:
        """Calculate statistics for a chapter."""
        coords_array = np.array([v['coordinates'] for v in verses])
        
        return {
            'avg_L': float(np.mean(coords_array[:, 0])),
            'avg_J': float(np.mean(coords_array[:, 1])),
            'avg_P': float(np.mean(coords_array[:, 2])),
            'avg_W': float(np.mean(coords_array[:, 3])),
            'std_L': float(np.std(coords_array[:, 0])),
            'std_J': float(np.std(coords_array[:, 1])),
            'std_P': float(np.std(coords_array[:, 2])),
            'std_W': float(np.std(coords_array[:, 3])),
            'avg_harmony': float(np.mean([v['harmony'] for v in verses]))
        }
    
    def compare_chapters(self, chapter1_data: dict, chapter2_data: dict) -> dict:
        """Compare two chapters."""
        stats1 = chapter1_data['statistics']
        stats2 = chapter2_data['statistics']
        
        # Calculate centroid distance
        centroid1 = [stats1['avg_L'], stats1['avg_J'], stats1['avg_P'], stats1['avg_W']]
        centroid2 = [stats2['avg_L'], stats2['avg_J'], stats2['avg_P'], stats2['avg_W']]
        
        centroid_distance = np.linalg.norm(np.array(centroid1) - np.array(centroid2))
        
        return {
            'chapter1': chapter1_data['chapter'],
            'chapter2': chapter2_data['chapter'],
            'centroid1': centroid1,
            'centroid2': centroid2,
            'centroid_distance': float(centroid_distance),
            'dimension_differences': {
                'L': abs(stats1['avg_L'] - stats2['avg_L']),
                'J': abs(stats1['avg_J'] - stats2['avg_J']),
                'P': abs(stats1['avg_P'] - stats2['avg_P']),
                'W': abs(stats1['avg_W'] - stats2['avg_W'])
            }
        }


def test_multi_chapter():
    """Test multi-chapter analysis."""
    analyzer = MultiChapterAnalyzer()
    
    print("="*80)
    print("MULTI-CHAPTER CONTENT EXPANSION")
    print("="*80)
    print("\nAnalyzing Mark Chapter 2 (sample verses)\n")
    
    # Analyze Chapter 2
    chapter2_analysis = analyzer.analyze_chapter(analyzer.mark_chapter_2, 2)
    
    print(f"Chapter 2 Statistics:")
    print(f"  Verses analyzed: {chapter2_analysis['verse_count']}")
    stats = chapter2_analysis['statistics']
    print(f"  Avg coordinates: L={stats['avg_L']:.3f}, J={stats['avg_J']:.3f}, "
          f"P={stats['avg_P']:.3f}, W={stats['avg_W']:.3f}")
    print(f"  Avg harmony: {stats['avg_harmony']:.3f}")
    
    # Load Chapter 1 for comparison
    with open('experiments/nwt_mark_chapter1.json', 'r', encoding='utf-8') as f:
        chapter1_data = json.load(f)
    
    chapter1_analysis = analyzer.analyze_chapter(chapter1_data['verses'], 1)
    
    print(f"\nChapter 1 Statistics (for comparison):")
    print(f"  Verses analyzed: {chapter1_analysis['verse_count']}")
    stats1 = chapter1_analysis['statistics']
    print(f"  Avg coordinates: L={stats1['avg_L']:.3f}, J={stats1['avg_J']:.3f}, "
          f"P={stats1['avg_P']:.3f}, W={stats1['avg_W']:.3f}")
    print(f"  Avg harmony: {stats1['avg_harmony']:.3f}")
    
    # Compare chapters
    comparison = analyzer.compare_chapters(chapter1_analysis, chapter2_analysis)
    
    print(f"\n{'='*80}")
    print("CHAPTER COMPARISON")
    print('='*80)
    print(f"\nCentroid Distance: {comparison['centroid_distance']:.3f}")
    print(f"\nDimension Differences:")
    for dim, diff in comparison['dimension_differences'].items():
        print(f"  {dim}: {diff:.3f}")
    
    # Interpretation
    print(f"\nInterpretation:")
    if comparison['centroid_distance'] < 0.10:
        print("  [EXCELLENT]: Chapters are very similar semantically")
    elif comparison['centroid_distance'] < 0.20:
        print("  [GOOD]: Chapters show consistent semantic patterns")
    elif comparison['centroid_distance'] < 0.30:
        print("  [MODERATE]: Some variation between chapters")
    else:
        print("  [SIGNIFICANT]: Chapters have different semantic focus")
    
    # Save results
    output = {
        'chapter1': chapter1_analysis,
        'chapter2': chapter2_analysis,
        'comparison': comparison
    }
    
    with open('experiments/multi_chapter_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved to: experiments/multi_chapter_analysis.json")
    
    # Recommendations for expansion
    print(f"\n{'='*80}")
    print("EXPANSION RECOMMENDATIONS")
    print('='*80)
    print("\nTo fully expand the system:")
    print("1. Extract all 16 chapters of Mark")
    print("2. Add Matthew, Luke, John (4 Gospels total)")
    print("3. Validate consistency across books")
    print("4. Build comprehensive corpus (1000+ verses)")
    print("5. Train generative translator on full corpus")
    
    print(f"\n{'='*80}")
    print("MULTI-CHAPTER ANALYSIS COMPLETE")
    print("="*80)


if __name__ == "__main__":
    test_multi_chapter()
