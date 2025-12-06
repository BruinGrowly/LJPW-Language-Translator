"""
Verification Script for Universal Translation System
Runs a series of tests to validate the full pipeline:
Detection -> Resonance -> Translation
"""

import sys
import os
# Add current directory to path so we can import experiments modules
sys.path.append(os.getcwd())

from experiments.universal_translator_core import UniversalTranslator

def run_verification():
    print("="*70)
    print("UNIVERSAL TRANSLATION SYSTEM - VERIFICATION")
    print("="*70)
    
    # 1. Initialize System
    print("\n[Init] Initializing Universal Translator...")
    try:
        translator = UniversalTranslator()
        print("[Init] Success.")
    except Exception as e:
        print(f"[Init] FAILED: {e}")
        return

    # 2. Define Test Cases
    test_cases = [
        {
            'source': 'Tuyeghana Ahiahina',
            'context': 'Good news/Gospel',
            'expected_keywords': ['Gospel', 'Good News', 'Message'],
            'description': 'Standard Gospel Case'
        },
        {
            'source': 'Aruwa Vivivireinei',
            'context': 'Holy Spirit',
            'expected_keywords': ['Spirit', 'Holy', 'Wind'],
            'description': 'Divine/Spirit Case'
        },
        {
            'source': 'apoapoe',
            'context': 'sin/wrong',
            'expected_keywords': ['Sin', 'Evil', 'Wrong'],
            'description': 'Negative concept'
        },
        {
            'source': 'God ana vibadana vouna',
            'context': 'Kingdom of God',
            'expected_keywords': ['Kingdom', 'Rule', 'Reign'],
            'description': 'Complex Phrase (Kingdom)'
        },
        {
            'source': 'Unknown Gibberish 123',
            'context': None,
            'expected_keywords': [], # Might be unknown or map to something neutral
            'description': 'Stress Test - Unknown Input'
        }
    ]
    
    # 3. Run Tests
    print(f"\n[Testing] Running {len(test_cases)} test cases...\n")
    
    for i, test in enumerate(test_cases, 1):
        print(f"Test {i}: {test['description']}")
        print(f"  Source: '{test['source']}'")
        print(f"  Context: {test['context']}")
        
        result = translator.translate(test['source'], test['context'])
        
        # Output Results
        sig = result['field_signature']
        print(f"  -> Signature: L={sig['L']:.2f} J={sig['J']:.2f} P={sig['P']:.2f} W={sig['W']:.2f} (Conf: {sig['confidence']:.2f})")
        print(f"  -> Top Result: {result['translation']}")
        
        # Check Top Matches Details
        print("  -> Top 3 Candidates:")
        for idx, match in enumerate(result['top_matches'][:3], 1):
            print(f"     {idx}. {match['name']} (Resonance: {match['strength']:.3f}) [{match['type']}]")
            # Show resonance components for top match
            if idx == 1:
                comps = match['components']
                print(f"        Components: Dist={comps['distance']:.2f}, Harm={comps['harmonic']:.2f}, Align={comps['alignment']:.2f}, Emg={comps['emergent']:.2f}")

        # Verification Logic
        expected_found = False
        if test['expected_keywords']:
            translation_lower = result['translation'].lower()
            top_matches_lower = [m['name'].lower() for m in result['top_matches'][:5]]
            
            for keyword in test['expected_keywords']:
                kw_lower = keyword.lower()
                if kw_lower in translation_lower or any(kw_lower in m for m in top_matches_lower):
                    expected_found = True
                    break
            
            if expected_found:
                print("  => [PASS] Expected concept found.")
            else:
                print(f"  => [FAIL] Expected {test['expected_keywords']} but got top results.")
        else:
            print("  => [INFO] No specific expectation set.")
            
        print("-" * 50)
        
    print("\n[Verification] Complete.")

if __name__ == "__main__":
    run_verification()
