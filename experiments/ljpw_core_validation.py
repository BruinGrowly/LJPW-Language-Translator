#!/usr/bin/env python3
"""
LJPW Core Validation Suite
===========================

Rigorous, falsifiable tests for the three core LJPW claims:
1. LJPW semantic field produces consistent, meaningful coordinates
2. All languages converge toward the Anchor Point (1,1,1,1)
3. Anchor Point translation preserves meaning across languages

Each test has:
- Clear hypothesis
- Large sample size
- Statistical significance testing
- Pass/fail criteria defined in advance
"""

import sys
import os
import json
import numpy as np
from pathlib import Path
from scipy import stats
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding='utf-8')

from experiments.enhanced_pattern_detector import EnhancedPatternDetector

# Constants
ANCHOR_POINT = np.array([1.0, 1.0, 1.0, 1.0])
DIMENSIONS = ['Love', 'Justice', 'Power', 'Wisdom']

# ============================================================================
# TEST 1: LJPW SEMANTIC FIELD VALIDATION
# ============================================================================

# Known concepts that should map to specific dimensions
KNOWN_CONCEPTS = {
    'Love': [
        "God so loved the world that he gave his only begotten Son",
        "Love your neighbor as yourself",
        "The greatest of these is love",
        "Love is patient, love is kind",
        "Perfect love casts out fear",
        "By this all will know you are my disciples, if you have love",
        "Beloved, let us love one another",
        "A new commandment I give unto you, that ye love one another",
        "Greater love has no man than this, that he lay down his life",
        "And now these three remain: faith, hope and love",
    ],
    'Justice': [
        "Let justice roll down like waters",
        "He has shown you what is good: to act justly and to love mercy",
        "The Lord is a God of justice",
        "Righteousness and justice are the foundation of his throne",
        "Learn to do right, seek justice, defend the oppressed",
        "He will judge the world in righteousness",
        "Blessed are those who hunger and thirst for righteousness",
        "The righteous shall live by faith",
        "Execute true judgment and show mercy",
        "What does the Lord require of you but to do justice",
    ],
    'Power': [
        "All power is given unto me in heaven and in earth",
        "You shall receive power when the Holy Spirit comes upon you",
        "The kingdom of God is not in word but in power",
        "For thine is the kingdom and the power and the glory",
        "He spoke and it was done, he commanded and it stood fast",
        "Who is this king of glory? The Lord strong and mighty",
        "Not by might nor by power but by my spirit",
        "Greater is he that is in you than he that is in the world",
        "I can do all things through Christ who strengthens me",
        "The weapons of our warfare are mighty through God",
    ],
    'Wisdom': [
        "The fear of the Lord is the beginning of wisdom",
        "If any of you lack wisdom, let him ask of God",
        "Wisdom is the principal thing, therefore get wisdom",
        "The wisdom that is from above is first pure, then peaceable",
        "In whom are hidden all the treasures of wisdom and knowledge",
        "To know wisdom and instruction, to perceive the words of understanding",
        "Wisdom calls aloud in the street, she raises her voice in the squares",
        "By wisdom the Lord laid the earth's foundations",
        "Get wisdom, get understanding; do not forget my words",
        "Blessed is the one who finds wisdom, who gains understanding",
    ],
}


def test_semantic_field_consistency(detector):
    """Test 1.1: Same text produces same coordinates (consistency)."""
    
    print("\n" + "="*70)
    print("TEST 1.1: SEMANTIC FIELD CONSISTENCY")
    print("Hypothesis: Same text → same LJPW coordinates")
    print("="*70)
    
    test_texts = [
        "Love is the greatest commandment",
        "Justice and righteousness are the foundation",
        "All power belongs to God",
        "Wisdom comes from above",
    ]
    
    consistent = 0
    total = 0
    
    for text in test_texts:
        results = []
        for _ in range(5):  # Run 5 times
            coord = get_ljpw_coords(text, detector)
            results.append(coord)
        
        # Check if all results are identical
        all_same = all(np.allclose(results[0], r) for r in results)
        total += 1
        if all_same:
            consistent += 1
            print(f"  ✓ '{text[:40]}...' - CONSISTENT")
        else:
            variance = np.var(results, axis=0)
            print(f"  ✗ '{text[:40]}...' - VARIANCE: {variance}")
    
    pct = consistent / total * 100
    passed = pct == 100
    
    print(f"\nResult: {consistent}/{total} texts consistent ({pct:.0f}%)")
    print(f"VERDICT: {'PASS' if passed else 'FAIL'}")
    
    return {'passed': passed, 'score': pct, 'n': total}


def test_semantic_field_discriminability(detector):
    """Test 1.2: Different semantic content produces different coordinates."""
    
    print("\n" + "="*70)
    print("TEST 1.2: SEMANTIC FIELD DISCRIMINABILITY")
    print("Hypothesis: Different content → different coordinates")
    print("="*70)
    
    # Pairs of texts from DIFFERENT dimensions should have different coordinates
    different_pairs = [
        ("Love your neighbor as yourself", "All power belongs to God"),
        ("God is love", "The Lord is a God of justice"),
        ("Wisdom is the principal thing", "Love is patient, love is kind"),
        ("The fear of the Lord is the beginning of wisdom", "You shall receive power"),
    ]
    
    discriminated = 0
    total = 0
    
    for text1, text2 in different_pairs:
        coord1 = get_ljpw_coords(text1, detector)
        coord2 = get_ljpw_coords(text2, detector)
        
        distance = np.linalg.norm(coord1 - coord2)
        dom1 = DIMENSIONS[np.argmax(coord1)]
        dom2 = DIMENSIONS[np.argmax(coord2)]
        
        different = dom1 != dom2  # Different dominant dimension
        total += 1
        
        if different:
            discriminated += 1
            print(f"  ✓ '{text1[:30]}...' [{dom1}] vs '{text2[:30]}...' [{dom2}] - DIFFERENT")
        else:
            print(f"  ✗ Both map to {dom1}")
    
    pct = discriminated / total * 100
    passed = pct >= 75
    
    print(f"\nResult: {discriminated}/{total} pairs discriminated ({pct:.0f}%)")
    print(f"Pass criterion: ≥75%")
    print(f"VERDICT: {'PASS' if passed else 'FAIL'}")
    
    return {'passed': passed, 'score': pct, 'n': total}


def test_semantic_field_meaningfulness(detector):
    """Test 1.3: Known concepts map to expected dimensions."""
    
    print("\n" + "="*70)
    print("TEST 1.3: SEMANTIC FIELD MEANINGFULNESS")
    print("Hypothesis: Known religious concepts map to expected LJPW dimensions")
    print("="*70)
    
    correct = 0
    total = 0
    dimension_results = defaultdict(list)
    
    for expected_dim, texts in KNOWN_CONCEPTS.items():
        print(f"\n  {expected_dim.upper()} concepts:")
        dim_correct = 0
        
        for text in texts:
            coord = get_ljpw_coords(text, detector)
            actual_dim = DIMENSIONS[np.argmax(coord)]
            strength = coord[DIMENSIONS.index(expected_dim)]
            
            match = actual_dim == expected_dim
            total += 1
            
            if match:
                correct += 1
                dim_correct += 1
                dimension_results[expected_dim].append(1)
            else:
                dimension_results[expected_dim].append(0)
        
        dim_pct = dim_correct / len(texts) * 100
        print(f"    {dim_correct}/{len(texts)} correct ({dim_pct:.0f}%)")
    
    overall_pct = correct / total * 100
    passed = overall_pct >= 70
    
    print(f"\nOverall: {correct}/{total} concepts mapped correctly ({overall_pct:.1f}%)")
    print(f"Pass criterion: ≥70%")
    print(f"VERDICT: {'PASS' if passed else 'FAIL'}")
    
    return {'passed': passed, 'score': overall_pct, 'n': total, 
            'by_dimension': {d: sum(r)/len(r)*100 for d, r in dimension_results.items()}}


# ============================================================================
# TEST 2: ANCHOR POINT CONVERGENCE
# ============================================================================

# Concepts across languages that should converge to Anchor Point
MULTILINGUAL_CONCEPTS = {
    'God': {
        'english': 'God the Almighty Creator',
        'greek': 'Theos Pantokrator',
        'hebrew': 'Elohim HaKol Yachol',
        'arabic': 'Allah al-Khaliq al-Qadir',
        'chinese': 'Quanneng de Shangdi',
        'japanese': 'Zennou no Kami',
        'korean': 'Jeonneung hasin Hananim',
        'spanish': 'Dios Todopoderoso',
        'french': 'Dieu Tout-Puissant',
        'german': 'Gott der Allmaechtige',
        'russian': 'Bog Vsemogushchiy',
        'portuguese': 'Deus Todo-Poderoso',
        'indonesian': 'Allah Yang Mahakuasa',
        'wedau': 'God Rewapana Ḡaeḡaena',
    },
    'Love': {
        'english': 'God is Love',
        'greek': 'Ho Theos agape estin',
        'hebrew': 'Elohim ahavah',
        'arabic': 'Allah huwa al-hubb',
        'chinese': 'Shangdi shi ai',
        'japanese': 'Kami wa ai desu',
        'korean': 'Hananim eun sarang isida',
        'spanish': 'Dios es amor',
        'french': 'Dieu est amour',
        'german': 'Gott ist Liebe',
        'russian': 'Bog yest lyubov',
        'portuguese': 'Deus e amor',
        'indonesian': 'Allah adalah kasih',
        'wedau': 'God Auna Nonoana',
    },
    'Truth': {
        'english': 'Your word is truth',
        'greek': 'Ho logos aletheia estin',
        'hebrew': 'Devarcha emet',
        'arabic': 'Kalimatuka haqq',
        'chinese': 'Ni de hua shi zhenli',
        'japanese': 'Anata no kotoba wa shinjitsu',
        'korean': 'Dangsin ui malsseum eun jinsil',
        'spanish': 'Tu palabra es verdad',
        'french': 'Ta parole est verite',
        'german': 'Dein Wort ist Wahrheit',
        'russian': 'Slovo tvoye istina',
        'portuguese': 'Tua palavra e verdade',
        'indonesian': 'Firman-Mu adalah kebenaran',
        'wedau': 'Am Riwa Maemaena',
    },
    'Salvation': {
        'english': 'Salvation belongs to the Lord',
        'greek': 'Soteria tou Kyriou',
        'hebrew': 'Yeshuah laAdonai',
        'arabic': 'Al-khalas lilrabb',
        'chinese': 'Jiuende shi zhu de',
        'japanese': 'Sukui wa Shu no mono',
        'korean': 'Guweoneun Junim kkeo',
        'spanish': 'La salvacion es del Senor',
        'french': 'Le salut appartient au Seigneur',
        'german': 'Das Heil gehoert dem Herrn',
        'russian': 'Spaseniye Gospodu',
        'portuguese': 'A salvacao e do Senhor',
        'indonesian': 'Keselamatan adalah milik Tuhan',
        'wedau': 'Vilawana Bada Ana',
    },
    'Kingdom': {
        'english': 'The Kingdom of Heaven',
        'greek': 'Basileia ton Ouranon',
        'hebrew': 'Malkhut haShamayim',
        'arabic': 'Malakut al-Samawat',
        'chinese': 'Tianguo',
        'japanese': 'Tengoku',
        'korean': 'Cheon-guk',
        'spanish': 'El Reino de los Cielos',
        'french': 'Le Royaume des Cieux',
        'german': 'Das Himmelreich',
        'russian': 'Tsarstvo Nebesnoye',
        'portuguese': 'O Reino dos Ceus',
        'indonesian': 'Kerajaan Surga',
        'wedau': 'Mara ana Vigulau',
    },
    'Spirit': {
        'english': 'The Holy Spirit',
        'greek': 'To Hagion Pneuma',
        'hebrew': 'Ruach HaKodesh',
        'arabic': 'Ruh al-Qudus',
        'chinese': 'Shengling',
        'japanese': 'Seirei',
        'korean': 'Seongryeong',
        'spanish': 'El Espiritu Santo',
        'french': 'Le Saint-Esprit',
        'german': 'Der Heilige Geist',
        'russian': 'Svyatoy Dukh',
        'portuguese': 'O Espirito Santo',
        'indonesian': 'Roh Kudus',
        'wedau': 'Arua Vivivireina',
    },
    'Mercy': {
        'english': 'His mercy endures forever',
        'greek': 'To eleos autou eis ton aiona',
        'hebrew': 'Chasdo leolam',
        'arabic': 'Rahmatuhu ila al-abad',
        'chinese': 'Ta de cibei yongyuan changcun',
        'japanese': 'Sono awaremi wa eien',
        'korean': 'Geu ui jasim i yeong-won',
        'spanish': 'Su misericordia es eterna',
        'french': 'Sa misericorde dure a jamais',
        'german': 'Seine Gnade waehrt ewiglich',
        'russian': 'Milost yego voveki',
        'portuguese': 'Sua misericordia dura para sempre',
        'indonesian': 'Belas kasihan-Nya selama-lamanya',
        'wedau': 'Ana Nuavaina Nonoana',
    },
    'Righteousness': {
        'english': 'Seek first the Kingdom and His righteousness',
        'greek': 'Zeteite proton ten basileian kai ten dikaiosynen',
        'hebrew': 'Bakshu rishona et malchuto ve tzidkato',
        'arabic': 'Atluboo awwalan mamlakat Allah wa birrah',
        'chinese': 'Xian qiu ta de guo he ta de yi',
        'japanese': 'Mazu Kami no kuni to gi wo motomeyo',
        'korean': 'Meonjeo geu ui nara wa geu ui uireul guharâ',
        'spanish': 'Buscad primero el reino y su justicia',
        'french': 'Cherchez premierement le royaume et sa justice',
        'german': 'Trachtet zuerst nach dem Reich und seiner Gerechtigkeit',
        'russian': 'Ishchite zhe prezhde Tsarstva i pravdy yego',
        'portuguese': 'Buscai primeiro o Reino e a sua justica',
        'indonesian': 'Carilah dahulu Kerajaan-Nya dan kebenaran-Nya',
        'wedau': 'Baia Naona God Ana Vigulau ma Jijimanina',
    },
}


def test_anchor_convergence(detector):
    """Test 2: All languages converge toward Anchor Point (1,1,1,1)."""
    
    print("\n" + "="*70)
    print("TEST 2: ANCHOR POINT CONVERGENCE")
    print("Hypothesis: All languages point toward Anchor Point (1,1,1,1)")
    print("="*70)
    
    concept_results = {}
    all_directions = []
    all_similarities = []
    
    for concept, translations in MULTILINGUAL_CONCEPTS.items():
        print(f"\n  Concept: {concept}")
        
        directions = []
        coords_list = []
        
        for lang, text in translations.items():
            coord = get_ljpw_coords(text, detector)
            coords_list.append(coord)
            
            # Direction toward anchor
            diff = ANCHOR_POINT - coord
            norm = np.linalg.norm(diff)
            if norm > 0.001:
                direction = diff / norm
            else:
                direction = np.zeros(4)
            directions.append(direction)
        
        # Measure agreement between all pairs
        similarities = []
        for i in range(len(directions)):
            for j in range(i+1, len(directions)):
                sim = np.dot(directions[i], directions[j])
                similarities.append(sim)
        
        mean_sim = np.mean(similarities) if similarities else 0
        all_similarities.extend(similarities)
        all_directions.extend(directions)
        
        # Measure variance in coordinates
        coord_variance = np.var(coords_list, axis=0)
        total_variance = np.sum(coord_variance)
        
        print(f"    Languages: {len(translations)}")
        print(f"    Direction agreement: {mean_sim:.3f}")
        print(f"    Coordinate variance: {total_variance:.4f}")
        
        concept_results[concept] = {
            'n_languages': len(translations),
            'direction_agreement': mean_sim,
            'coord_variance': total_variance,
        }
    
    # Overall statistics
    overall_agreement = np.mean(all_similarities)
    
    # Statistical test: Is mean agreement > 0.5 (better than random)?
    t_stat, p_value = stats.ttest_1samp(all_similarities, 0.5, alternative='greater')
    
    print(f"\n" + "-"*50)
    print(f"OVERALL RESULTS:")
    print(f"  Total concept pairs: {len(all_similarities)}")
    print(f"  Mean direction agreement: {overall_agreement:.3f}")
    print(f"  T-statistic: {t_stat:.3f}")
    print(f"  P-value: {p_value:.6f}")
    
    # Pass if agreement > 0.7 and p < 0.05
    passed = overall_agreement > 0.7 and p_value < 0.05
    
    print(f"\nPass criteria: Agreement > 0.7 AND p < 0.05")
    print(f"VERDICT: {'PASS' if passed else 'FAIL'}")
    
    return {
        'passed': passed,
        'agreement': overall_agreement,
        'p_value': p_value,
        'n_concepts': len(MULTILINGUAL_CONCEPTS),
        'n_languages': len(list(MULTILINGUAL_CONCEPTS.values())[0]),
        'n_pairs': len(all_similarities),
    }


# ============================================================================
# TEST 3: TRANSLATION ARCHITECTURE
# ============================================================================

TRANSLATION_PAIRS = [
    {
        'source': "God so loved the world that he gave his only begotten Son",
        'target': "Car Dieu a tant aime le monde qu'il a donne son Fils unique",
        'source_lang': 'English',
        'target_lang': 'French',
    },
    {
        'source': "In the beginning was the Word",
        'target': "Au commencement etait la Parole",
        'source_lang': 'English',
        'target_lang': 'French',
    },
    {
        'source': "The Lord is my shepherd, I shall not want",
        'target': "El Senor es mi pastor, nada me faltara",
        'source_lang': 'English',
        'target_lang': 'Spanish',
    },
    {
        'source': "Blessed are the peacemakers",
        'target': "Selig sind die Friedfertigen",
        'source_lang': 'English',
        'target_lang': 'German',
    },
    {
        'source': "Love your enemies and pray for those who persecute you",
        'target': "Aimez vos ennemis et priez pour ceux qui vous persecutent",
        'source_lang': 'English',
        'target_lang': 'French',
    },
    {
        'source': "The truth shall set you free",
        'target': "A verdade vos libertara",
        'source_lang': 'English',
        'target_lang': 'Portuguese',
    },
    {
        'source': "Ask and it shall be given unto you",
        'target': "Demandez et l'on vous donnera",
        'source_lang': 'English',
        'target_lang': 'French',
    },
    {
        'source': "Fear not, for I am with you",
        'target': "Non temere, perche io sono con te",
        'source_lang': 'English',
        'target_lang': 'Italian',
    },
    {
        'source': "I am the way, the truth, and the life",
        'target': "Yo soy el camino, la verdad y la vida",
        'source_lang': 'English',
        'target_lang': 'Spanish',
    },
    {
        'source': "Forgive us our sins as we forgive those who sin against us",
        'target': "Pardonne-nous nos offenses comme nous pardonnons a ceux qui nous ont offenses",
        'source_lang': 'English',
        'target_lang': 'French',
    },
]


def test_translation_architecture(detector):
    """Test 3: Translation via Anchor Point preserves meaning."""
    
    print("\n" + "="*70)
    print("TEST 3: TRANSLATION ARCHITECTURE")
    print("Hypothesis: Source and target maintain same semantic coordinates")
    print("="*70)
    
    similarities = []
    dimension_matches = []
    
    for pair in TRANSLATION_PAIRS:
        source_coord = get_ljpw_coords(pair['source'], detector)
        target_coord = get_ljpw_coords(pair['target'], detector)
        
        # Cosine similarity
        cos_sim = np.dot(source_coord, target_coord) / (
            np.linalg.norm(source_coord) * np.linalg.norm(target_coord) + 1e-10
        )
        
        # Dominant dimension match
        source_dim = DIMENSIONS[np.argmax(source_coord)]
        target_dim = DIMENSIONS[np.argmax(target_coord)]
        dim_match = source_dim == target_dim
        
        similarities.append(cos_sim)
        dimension_matches.append(1 if dim_match else 0)
        
        status = "✓" if dim_match else "✗"
        print(f"  {status} {pair['source_lang']}→{pair['target_lang']}: "
              f"sim={cos_sim:.3f}, dims={source_dim}/{target_dim}")
    
    mean_similarity = np.mean(similarities)
    dim_match_rate = np.mean(dimension_matches) * 100
    
    # Statistical test: Is similarity > 0.8?
    t_stat, p_value = stats.ttest_1samp(similarities, 0.8, alternative='greater')
    
    print(f"\n" + "-"*50)
    print(f"RESULTS:")
    print(f"  Mean semantic similarity: {mean_similarity:.3f}")
    print(f"  Dimension match rate: {dim_match_rate:.1f}%")
    print(f"  T-statistic: {t_stat:.3f}")
    print(f"  P-value: {p_value:.6f}")
    
    # Pass if similarity > 0.85 and dimension match > 70%
    passed = mean_similarity > 0.85 and dim_match_rate >= 70
    
    print(f"\nPass criteria: Similarity > 0.85 AND dimension match ≥ 70%")
    print(f"VERDICT: {'PASS' if passed else 'FAIL'}")
    
    return {
        'passed': passed,
        'similarity': mean_similarity,
        'dimension_match_rate': dim_match_rate,
        'p_value': p_value,
        'n': len(TRANSLATION_PAIRS),
    }


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_ljpw_coords(text, detector):
    """Get LJPW coordinates for a text."""
    result = detector.calculate_field_signature_v2(text)
    return np.array([result['L'], result['J'], result['P'], result['W']])


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("="*70)
    print("LJPW CORE VALIDATION SUITE")
    print("Rigorous testing of fundamental claims")
    print("="*70)
    
    detector = EnhancedPatternDetector()
    
    # Run all tests
    results = {}
    
    # Test 1: Semantic Field
    print("\n" + "#"*70)
    print("# TEST SUITE 1: LJPW SEMANTIC FIELD")
    print("#"*70)
    
    results['consistency'] = test_semantic_field_consistency(detector)
    results['discriminability'] = test_semantic_field_discriminability(detector)
    results['meaningfulness'] = test_semantic_field_meaningfulness(detector)
    
    # Test 2: Anchor Convergence
    print("\n" + "#"*70)
    print("# TEST SUITE 2: ANCHOR POINT CONVERGENCE")
    print("#"*70)
    
    results['anchor_convergence'] = test_anchor_convergence(detector)
    
    # Test 3: Translation
    print("\n" + "#"*70)
    print("# TEST SUITE 3: TRANSLATION ARCHITECTURE")
    print("#"*70)
    
    results['translation'] = test_translation_architecture(detector)
    
    # Final Summary
    print("\n" + "="*70)
    print("FINAL VALIDATION SUMMARY")
    print("="*70)
    
    all_passed = []
    
    print("\nSEMANTIC FIELD TESTS:")
    print(f"  1.1 Consistency:      {'PASS' if results['consistency']['passed'] else 'FAIL'}")
    print(f"  1.2 Discriminability: {'PASS' if results['discriminability']['passed'] else 'FAIL'}")
    print(f"  1.3 Meaningfulness:   {'PASS' if results['meaningfulness']['passed'] else 'FAIL'}")
    all_passed.extend([results['consistency']['passed'], 
                       results['discriminability']['passed'],
                       results['meaningfulness']['passed']])
    
    print("\nANCHOR CONVERGENCE TEST:")
    print(f"  2.1 Convergence:      {'PASS' if results['anchor_convergence']['passed'] else 'FAIL'}")
    print(f"      Agreement: {results['anchor_convergence']['agreement']:.3f}")
    print(f"      P-value:   {results['anchor_convergence']['p_value']:.6f}")
    all_passed.append(results['anchor_convergence']['passed'])
    
    print("\nTRANSLATION ARCHITECTURE TEST:")
    print(f"  3.1 Semantic Preservation: {'PASS' if results['translation']['passed'] else 'FAIL'}")
    print(f"      Similarity: {results['translation']['similarity']:.3f}")
    print(f"      Dimension Match: {results['translation']['dimension_match_rate']:.1f}%")
    all_passed.append(results['translation']['passed'])
    
    passed_count = sum(all_passed)
    total_tests = len(all_passed)
    
    print("\n" + "="*70)
    print(f"OVERALL: {passed_count}/{total_tests} tests passed")
    print("="*70)
    
    if passed_count == total_tests:
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                    ALL TESTS PASSED                               ║
╠══════════════════════════════════════════════════════════════════╣
║  The LJPW framework demonstrates:                                 ║
║  • Consistent semantic field measurements                         ║
║  • Meaningful dimension mapping                                   ║
║  • Universal anchor point convergence                             ║
║  • Cross-language semantic preservation                           ║
╚══════════════════════════════════════════════════════════════════╝
""")
    elif passed_count >= 4:
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                  MOSTLY VALIDATED                                 ║
╠══════════════════════════════════════════════════════════════════╣
║  Core functionality confirmed. Some areas need improvement.       ║
╚══════════════════════════════════════════════════════════════════╝
""")
    else:
        print("""
╔══════════════════════════════════════════════════════════════════╗
║              VALIDATION INCOMPLETE                                ║
╠══════════════════════════════════════════════════════════════════╣
║  Multiple tests failed. Review methodology and implementation.    ║
╚══════════════════════════════════════════════════════════════════╝
""")
    
    return results


if __name__ == '__main__':
    main()
