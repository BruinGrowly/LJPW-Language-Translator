"""
Test Suite for Phase 2: Context Integration and Multi-Layer Combination
Validates phrase detection, context disambiguation, and adaptive weighting.
"""

import sys
sys.path.append('experiments')

from enhanced_pattern_detector import EnhancedPatternDetector
import numpy as np


def test_phrase_composition():
    """Test that compound phrases get boosted vs individual words."""
    detector = EnhancedPatternDetector()
    
    print("="*70)
    print("TEST 1: PHRASE COMPOSITION")
    print("="*70)
    
    tests = [
        {
            'phrase': 'Kingdom of God',
            'individual': 'Kingdom',
            'expected_boost': 'Higher J/W for compound',
            'context': 'Divine rule'
        },
        {
            'phrase': 'Holy Spirit',
            'individual': 'Spirit',
            'expected_boost': 'Higher L for compound',
            'context': None
        }
    ]
    
    results = []
    for test in tests:
        phrase_sig = detector.calculate_field_signature_v2(test['phrase'], test['context'])
        individual_sig = detector.calculate_field_signature_v2(test['individual'], test['context'])
        
        print(f"\n{test['phrase']} vs {test['individual']}:")
        print(f"  Phrase:     L={phrase_sig['L']:.3f}, J={phrase_sig['J']:.3f}, P={phrase_sig['P']:.3f}, W={phrase_sig['W']:.3f}")
        print(f"  Individual: L={individual_sig['L']:.3f}, J={individual_sig['J']:.3f}, P={individual_sig['P']:.3f}, W={individual_sig['W']:.3f}")
        
        # Check if phrase has higher confidence
        phrase_conf = phrase_sig['confidence']
        individual_conf = individual_sig['confidence']
        
        passed = phrase_conf > individual_conf
        results.append(passed)
        
        print(f"  Confidence: Phrase={phrase_conf:.2f}, Individual={individual_conf:.2f}")
        print(f"  Result: {'[PASS]' if passed else '[FAIL]'} - {test['expected_boost']}")
    
    success_rate = sum(results) / len(results)
    print(f"\n{'='*70}")
    print(f"Phrase Composition: {sum(results)}/{len(results)} passed ({success_rate:.0%})")
    return success_rate


def test_context_disambiguation():
    """Test that context helps disambiguate meaning."""
    detector = EnhancedPatternDetector()
    
    print("\n" + "="*70)
    print("TEST 2: CONTEXT DISAMBIGUATION")
    print("="*70)
    
    tests = [
        {
            'word': 'Light',
            'context1': 'Sun shines bright',
            'context2': 'Truth and wisdom',
            'expected': 'Context 1 -> Higher P (physical), Context 2 -> Higher W (spiritual)'
        },
        {
            'word': 'Power',
            'context1': 'Physical strength',
            'context2': 'Divine authority',
            'expected': 'Context 1 -> Higher P, Context 2 -> Higher W/L'
        }
    ]
    
    results = []
    for test in tests:
        sig1 = detector.calculate_field_signature_v2(test['word'], test['context1'])
        sig2 = detector.calculate_field_signature_v2(test['word'], test['context2'])
        
        print(f"\n'{test['word']}':")
        print(f"  Context 1 ('{test['context1']}'): L={sig1['L']:.3f}, J={sig1['J']:.3f}, P={sig1['P']:.3f}, W={sig1['W']:.3f}")
        print(f"  Context 2 ('{test['context2']}'): L={sig2['L']:.3f}, J={sig2['J']:.3f}, P={sig2['P']:.3f}, W={sig2['W']:.3f}")
        
        # Check if contexts produce different signatures
        diff = np.linalg.norm(np.array([sig1['L'], sig1['J'], sig1['P'], sig1['W']]) - 
                             np.array([sig2['L'], sig2['J'], sig2['P'], sig2['W']]))
        
        passed = diff > 0.1  # Significant difference
        results.append(passed)
        
        print(f"  Difference: {diff:.3f}")
        print(f"  Result: {'[PASS]' if passed else '[FAIL]'} - {test['expected']}")
    
    success_rate = sum(results) / len(results)
    print(f"\n{'='*70}")
    print(f"Context Disambiguation: {sum(results)}/{len(results)} passed ({success_rate:.0%})")
    return success_rate


def test_adaptive_weighting():
    """Test that high-confidence layers get more weight."""
    detector = EnhancedPatternDetector()
    
    print("\n" + "="*70)
    print("TEST 3: ADAPTIVE WEIGHTING")
    print("="*70)
    
    tests = [
        {
            'text': 'Kingdom of God',
            'context': 'Divine rule',
            'expected_dominant': 'semantic or context',
            'reason': 'Strong semantic markers should dominate'
        },
        {
            'text': 'xyz',
            'context': None,
            'expected_dominant': 'phonetic',
            'reason': 'Unknown word should rely on phonetics'
        }
    ]
    
    results = []
    for test in tests:
        sig = detector.calculate_field_signature_v2(test['text'], test['context'])
        weights = sig['phase2_metadata']['layer_weights']
        
        dominant_layer = max(weights.items(), key=lambda x: x[1])[0]
        
        print(f"\n'{test['text']}':")
        print(f"  Weights: {weights}")
        print(f"  Dominant: {dominant_layer}")
        print(f"  Expected: {test['expected_dominant']}")
        
        # Check if dominant layer matches expectation
        passed = dominant_layer in test['expected_dominant']
        results.append(passed)
        
        print(f"  Result: {'[PASS]' if passed else '[FAIL]'} - {test['reason']}")
    
    success_rate = sum(results) / len(results)
    print(f"\n{'='*70}")
    print(f"Adaptive Weighting: {sum(results)}/{len(results)} passed ({success_rate:.0%})")
    return success_rate


def test_confidence_calibration():
    """Test that confidence scores correlate with detection quality."""
    detector = EnhancedPatternDetector()
    
    print("\n" + "="*70)
    print("TEST 4: CONFIDENCE CALIBRATION")
    print("="*70)
    
    tests = [
        {'text': 'Kingdom of God', 'context': 'Divine rule', 'expected_conf': 'high', 'threshold': 0.7},
        {'text': 'Holy Spirit', 'context': 'Divine presence', 'expected_conf': 'high', 'threshold': 0.7},
        {'text': 'Random word', 'context': None, 'expected_conf': 'low', 'threshold': 0.4}
    ]
    
    results = []
    for test in tests:
        sig = detector.calculate_field_signature_v2(test['text'], test['context'])
        conf = sig['confidence']
        
        print(f"\n'{test['text']}':")
        print(f"  Confidence: {conf:.2f}")
        print(f"  Expected: {test['expected_conf']} (threshold: {test['threshold']})")
        
        if test['expected_conf'] == 'high':
            passed = conf >= test['threshold']
        else:
            passed = conf < test['threshold']
        
        results.append(passed)
        print(f"  Result: {'[PASS]' if passed else '[FAIL]'}")
    
    success_rate = sum(results) / len(results)
    print(f"\n{'='*70}")
    print(f"Confidence Calibration: {sum(results)}/{len(results)} passed ({success_rate:.0%})")
    return success_rate


def main():
    print("\n" + "="*70)
    print("PHASE 2 COMPREHENSIVE TEST SUITE")
    print("="*70)
    print("\nTesting Context Integration and Multi-Layer Combination\n")
    
    # Run all tests
    phrase_score = test_phrase_composition()
    context_score = test_context_disambiguation()
    weighting_score = test_adaptive_weighting()
    confidence_score = test_confidence_calibration()
    
    # Overall results
    overall = (phrase_score + context_score + weighting_score + confidence_score) / 4
    
    print("\n" + "="*70)
    print("OVERALL RESULTS")
    print("="*70)
    print(f"Phrase Composition:      {phrase_score:.0%}")
    print(f"Context Disambiguation:  {context_score:.0%}")
    print(f"Adaptive Weighting:      {weighting_score:.0%}")
    print(f"Confidence Calibration:  {confidence_score:.0%}")
    print(f"\nOverall Success Rate:    {overall:.0%}")
    print("="*70)
    
    if overall >= 0.85:
        print("\n✓ Phase 2 implementation PASSED")
    else:
        print("\n✗ Phase 2 implementation needs improvement")


if __name__ == "__main__":
    main()
