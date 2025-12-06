"""
Test Suite for Phase 3: Semantic Composition
Validates emergent compositional behavior.
"""

import sys
sys.path.append('experiments')

from semantic_composer import SemanticComposer
import numpy as np


def test_modifier_head_composition():
    """Test that modifiers amplify heads appropriately."""
    composer = SemanticComposer('experiments/semantic_space_6854_SOCIAL.json')
    
    print("="*70)
    print("TEST 1: MODIFIER-HEAD COMPOSITION")
    print("="*70)
    
    tests = [
        {
            'phrase': 'Kingdom of God',
            'expected_dominance': 'God',
            'expected_synergy': 'positive',
            'min_L': 0.80,
            'min_W': 0.90
        }
    ]
    
    results = []
    for test in tests:
        result = composer.compose(test['phrase'])
        
        print(f"\n'{test['phrase']}':")
        print(f"  Coordinates: L={result['coordinates'][0]:.3f}, J={result['coordinates'][1]:.3f}, P={result['coordinates'][2]:.3f}, W={result['coordinates'][3]:.3f}")
        print(f"  Weights: {result['weights']}")
        print(f"  Synergy: {result['synergy']:.3f}")
        
        # Check dominance
        weights = result['weights']
        dominant = max(weights.items(), key=lambda x: x[1])[0]
        dominance_pass = dominant == test['expected_dominance']
        
        # Check synergy
        synergy_pass = (result['synergy'] > 0) == (test['expected_synergy'] == 'positive')
        
        # Check coordinates
        coords_pass = (result['coordinates'][0] >= test['min_L'] and 
                      result['coordinates'][3] >= test['min_W'])
        
        passed = dominance_pass and synergy_pass and coords_pass
        results.append(passed)
        
        print(f"  Dominance: {'[PASS]' if dominance_pass else '[FAIL]'} (expected {test['expected_dominance']}, got {dominant})")
        print(f"  Synergy: {'[PASS]' if synergy_pass else '[FAIL]'} (expected {test['expected_synergy']})")
        print(f"  Coordinates: {'[PASS]' if coords_pass else '[FAIL]'} (L>={test['min_L']}, W>={test['min_W']})")
    
    success_rate = sum(results) / len(results)
    print(f"\n{'='*70}")
    print(f"Modifier-Head Composition: {sum(results)}/{len(results)} passed ({success_rate:.0%})")
    return success_rate


def test_attribute_composition():
    """Test that attributes modify nouns appropriately."""
    composer = SemanticComposer('experiments/semantic_space_6854_SOCIAL.json')
    
    print("\n" + "="*70)
    print("TEST 2: ATTRIBUTE COMPOSITION")
    print("="*70)
    
    tests = [
        {
            'phrase': 'Holy Spirit',
            'expected_dominance': 'Spirit',  # Noun should anchor
            'expected_synergy': 'positive',
            'min_L': 0.80,
            'min_W': 0.85
        }
    ]
    
    results = []
    for test in tests:
        result = composer.compose(test['phrase'])
        
        print(f"\n'{test['phrase']}':")
        print(f"  Coordinates: L={result['coordinates'][0]:.3f}, J={result['coordinates'][1]:.3f}, P={result['coordinates'][2]:.3f}, W={result['coordinates'][3]:.3f}")
        print(f"  Weights: {result['weights']}")
        print(f"  Synergy: {result['synergy']:.3f}")
        
        # Check dominance
        weights = result['weights']
        dominant = max(weights.items(), key=lambda x: x[1])[0]
        dominance_pass = dominant == test['expected_dominance']
        
        # Check synergy
        synergy_pass = (result['synergy'] > 0) == (test['expected_synergy'] == 'positive')
        
        # Check coordinates
        coords_pass = (result['coordinates'][0] >= test['min_L'] and 
                      result['coordinates'][3] >= test['min_W'])
        
        passed = dominance_pass and synergy_pass and coords_pass
        results.append(passed)
        
        print(f"  Dominance: {'[PASS]' if dominance_pass else '[FAIL]'} (expected {test['expected_dominance']}, got {dominant})")
        print(f"  Synergy: {'[PASS]' if synergy_pass else '[FAIL]'} (expected {test['expected_synergy']})")
        print(f"  Coordinates: {'[PASS]' if coords_pass else '[FAIL]'} (L>={test['min_L']}, W>={test['min_W']})")
    
    success_rate = sum(results) / len(results)
    print(f"\n{'='*70}")
    print(f"Attribute Composition: {sum(results)}/{len(results)} passed ({success_rate:.0%})")
    return success_rate


def test_emergent_behavior():
    """Test that composition weights emerge from coordinates."""
    composer = SemanticComposer('experiments/semantic_space_6854_SOCIAL.json')
    
    print("\n" + "="*70)
    print("TEST 3: EMERGENT BEHAVIOR")
    print("="*70)
    
    # Test: Higher W concepts should have more influence
    phrase = "Kingdom of God"
    result = composer.compose(phrase)
    
    print(f"\n'{phrase}':")
    print(f"  Components: {result['components']}")
    
    # Get individual concepts
    kingdom = composer.lookup.find_concept('Kingdom')
    god = composer.lookup.find_concept('God')
    
    print(f"\n  Kingdom: W={kingdom['coordinates'][3]:.2f}")
    print(f"  God: W={god['coordinates'][3]:.2f}")
    
    # God has higher W, so should have higher influence
    god_influence = result['weights']['God']
    kingdom_influence = result['weights']['Kingdom']
    
    emergent_pass = god_influence > kingdom_influence
    
    print(f"\n  Kingdom influence: {kingdom_influence:.1%}")
    print(f"  God influence: {god_influence:.1%}")
    print(f"\n  Result: {'[PASS]' if emergent_pass else '[FAIL]'} (Higher W → Higher influence)")
    
    print(f"\n{'='*70}")
    print(f"Emergent Behavior: {'1/1 passed (100%)' if emergent_pass else '0/1 passed (0%)'}")
    return 1.0 if emergent_pass else 0.0


def test_synergy_detection():
    """Test that synergy is correctly detected."""
    composer = SemanticComposer('experiments/semantic_space_6854_SOCIAL.json')
    
    print("\n" + "="*70)
    print("TEST 4: SYNERGY DETECTION")
    print("="*70)
    
    tests = [
        {
            'phrase': 'Kingdom of God',
            'expected': 'positive',
            'reason': 'Both high L and W should reinforce'
        },
        {
            'phrase': 'Holy Spirit',
            'expected': 'positive',
            'reason': 'Both high L and W should reinforce'
        }
    ]
    
    results = []
    for test in tests:
        result = composer.compose(test['phrase'])
        
        print(f"\n'{test['phrase']}':")
        print(f"  Synergy: {result['synergy']:.3f}")
        print(f"  Expected: {test['expected']}")
        print(f"  Reason: {test['reason']}")
        
        if test['expected'] == 'positive':
            passed = result['synergy'] > 0
        else:
            passed = result['synergy'] <= 0
        
        results.append(passed)
        print(f"  Result: {'[PASS]' if passed else '[FAIL]'}")
    
    success_rate = sum(results) / len(results)
    print(f"\n{'='*70}")
    print(f"Synergy Detection: {sum(results)}/{len(results)} passed ({success_rate:.0%})")
    return success_rate


def main():
    print("\n" + "="*70)
    print("PHASE 3 COMPREHENSIVE TEST SUITE")
    print("="*70)
    print("\nTesting Dynamic Semantic Composition\n")
    
    # Run all tests
    modifier_score = test_modifier_head_composition()
    attribute_score = test_attribute_composition()
    emergent_score = test_emergent_behavior()
    synergy_score = test_synergy_detection()
    
    # Overall results
    overall = (modifier_score + attribute_score + emergent_score + synergy_score) / 4
    
    print("\n" + "="*70)
    print("OVERALL RESULTS")
    print("="*70)
    print(f"Modifier-Head Composition:  {modifier_score:.0%}")
    print(f"Attribute Composition:      {attribute_score:.0%}")
    print(f"Emergent Behavior:          {emergent_score:.0%}")
    print(f"Synergy Detection:          {synergy_score:.0%}")
    print(f"\nOverall Success Rate:       {overall:.0%}")
    print("="*70)
    
    if overall >= 0.85:
        print("\nPhase 3 implementation PASSED")
    else:
        print("\nPhase 3 implementation needs improvement")


if __name__ == "__main__":
    main()
