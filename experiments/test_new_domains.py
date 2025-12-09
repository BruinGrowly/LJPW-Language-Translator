"""
Test New Domains - Coherence Validation
Verifies that concepts in Arts & Aesthetics and Economy & Commerce 
are semantically distinct and coherent.
"""

import json
import numpy as np
from pathlib import Path

def test_domains():
    print("="*60)
    print("VALIDATING NEW DOMAINS")
    print("="*60)
    
    # Construct path relative to this script file
    script_dir = Path(__file__).parent
    file_path = script_dir / "semantic_space_10000_MILESTONE.json"

    if not file_path.exists():
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    arts_domain = data['domains'].get('arts_aesthetics', {})
    econ_domain = data['domains'].get('economy_commerce', {})
    
    if not arts_domain or not econ_domain:
        print("Error: Missing new domains.")
        return
        
    arts_concepts = list(arts_domain['concepts'].values())
    econ_concepts = list(econ_domain['concepts'].values())
    
    print(f"Arts Concepts: {len(arts_concepts)}")
    print(f"Economy Concepts: {len(econ_concepts)}")
    
    # helper
    def get_avg_dist(group1, group2):
        dists = []
        # Sample for speed if large
        s1 = group1[:50] if len(group1) > 50 else group1
        s2 = group2[:50] if len(group2) > 50 else group2
        
        for c1 in s1:
            for c2 in s2:
                v1 = np.array(c1['coordinates'])
                v2 = np.array(c2['coordinates'])
                dists.append(np.linalg.norm(v1 - v2))
        return np.mean(dists)

    # 1. Intra-domain coherence (should be low distance)
    arts_intra = get_avg_dist(arts_concepts, arts_concepts)
    econ_intra = get_avg_dist(econ_concepts, econ_concepts)
    
    print(f"\nIntra-domain Distance (Coherence):")
    print(f"  Arts (Internal):    {arts_intra:.4f}")
    print(f"  Economy (Internal): {econ_intra:.4f}")
    
    # 2. Inter-domain distance (should be higher)
    inter_dist = get_avg_dist(arts_concepts, econ_concepts)
    
    print(f"\nInter-domain Distance (Separation):")
    print(f"  Arts vs Economy:    {inter_dist:.4f}")
    
    # Validation
    success = True
    if arts_intra > inter_dist:
        print("FAIL: Arts concepts closer to Economy than themselves.")
        success = False
    if econ_intra > inter_dist:
        print("FAIL: Economy concepts closer to Arts than themselves.")
        success = False
        
    if success:
        print("\nSUCCESS: Domains are semantically distinct and coherent.")
        ratio = inter_dist / ((arts_intra + econ_intra) / 2)
        print(f"Separation Ratio: {ratio:.2f} (Target > 1.2)")
    
    print("\nSample Concepts:")
    print("Arts: Painting LJPW =", arts_concepts[0]['coordinates'])
    print("Econ: Money    LJPW =", econ_concepts[0]['coordinates'])

if __name__ == "__main__":
    test_domains()
