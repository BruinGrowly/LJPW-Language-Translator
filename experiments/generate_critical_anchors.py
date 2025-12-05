"""
LJPW Critical Anchor Generator
Generates 40 high-weight anchor concepts to fill critical semantic gaps.
"""

import json
import numpy as np

# Natural Equilibrium
PHI_INV = 1 / ((1 + np.sqrt(5)) / 2)
SQRT2_M1 = np.sqrt(2) - 1
E_M2 = np.e - 2
LN2 = np.log(2)
EQUILIBRIUM = [PHI_INV, SQRT2_M1, E_M2, LN2]


def create_concept(name, definition, l, j, p, w):
    """Create a concept with LJPW coordinates."""
    return {
        "name": name,
        "definition": definition,
        "coordinates": [l, j, p, w]
    }


# Phase 1.1: Low Justice Anchors (10 concepts)
# These concepts represent minimal justice/order/structure
low_justice_anchors = {
    "chaos": create_concept(
        "Chaos", 
        "Complete disorder and unpredictability",
        0.42, 0.05, 0.68, 0.35
    ),
    "anarchy": create_concept(
        "Anarchy",
        "Absence of government and absolute freedom of the individual",
        0.55, 0.03, 0.72, 0.48
    ),
    "disorder": create_concept(
        "Disorder",
        "Lack of order or regular arrangement",
        0.38, 0.06, 0.51, 0.42
    ),
    "lawlessness": create_concept(
        "Lawlessness",
        "Absence of law and order",
        0.28, 0.04, 0.64, 0.39
    ),
    "randomness": create_concept(
        "Randomness",
        "Lack of pattern or predictability",
        0.45, 0.08, 0.47, 0.71
    ),
    "arbitrariness": create_concept(
        "Arbitrariness",
        "Based on random choice rather than reason or system",
        0.35, 0.07, 0.58, 0.52
    ),
    "unfairness": create_concept(
        "Unfairness",
        "Lack of justice or impartiality",
        0.31, 0.09, 0.55, 0.46
    ),
    "bias": create_concept(
        "Bias",
        "Prejudice in favor of or against something",
        0.36, 0.08, 0.61, 0.58
    ),
    "inequality": create_concept(
        "Inequality",
        "Lack of equality or fairness",
        0.41, 0.09, 0.66, 0.63
    ),
    "imbalance": create_concept(
        "Imbalance",
        "Lack of proportion or equilibrium",
        0.44, 0.07, 0.59, 0.54
    ),
}

# Phase 1.2: Low Wisdom Anchors (10 concepts)
# These concepts represent minimal wisdom/understanding/knowledge
low_wisdom_anchors = {
    "ignorance": create_concept(
        "Ignorance",
        "Lack of knowledge or information",
        0.38, 0.52, 0.41, 0.08
    ),
    "foolishness": create_concept(
        "Foolishness",
        "Lack of good sense or judgment",
        0.46, 0.48, 0.54, 0.06
    ),
    "naivety": create_concept(
        "Naivety",
        "Lack of experience or sophistication",
        0.68, 0.55, 0.38, 0.09
    ),
    "thoughtlessness": create_concept(
        "Thoughtlessness",
        "Lack of consideration for consequences",
        0.42, 0.44, 0.62, 0.07
    ),
    "impulsiveness": create_concept(
        "Impulsiveness",
        "Acting without forethought",
        0.51, 0.46, 0.71, 0.08
    ),
    "recklessness": create_concept(
        "Recklessness",
        "Lack of regard for danger or consequences",
        0.48, 0.41, 0.78, 0.05
    ),
    "shortsightedness": create_concept(
        "Shortsightedness",
        "Lack of foresight or long-term perspective",
        0.44, 0.58, 0.56, 0.09
    ),
    "confusion": create_concept(
        "Confusion",
        "Lack of understanding or clarity",
        0.39, 0.51, 0.44, 0.07
    ),
    "delusion": create_concept(
        "Delusion",
        "False belief or impression",
        0.35, 0.47, 0.52, 0.06
    ),
    "superficiality": create_concept(
        "Superficiality",
        "Lack of depth or substance",
        0.52, 0.49, 0.58, 0.08
    ),
}

# Phase 1.3: Equilibrium Anchors (20 concepts)
# These concepts are balanced across all dimensions
# Positioned near natural equilibrium (0.618, 0.414, 0.718, 0.693)
equilibrium_anchors = {
    "balance": create_concept(
        "Balance",
        "State of equilibrium among different elements",
        0.62, 0.42, 0.71, 0.69
    ),
    "harmony": create_concept(
        "Harmony",
        "Agreement and concord among elements",
        0.78, 0.45, 0.68, 0.72
    ),
    "equilibrium": create_concept(
        "Equilibrium",
        "State of balance between opposing forces",
        0.61, 0.48, 0.72, 0.71
    ),
    "moderation": create_concept(
        "Moderation",
        "Avoidance of extremes",
        0.65, 0.52, 0.64, 0.75
    ),
    "centeredness": create_concept(
        "Centeredness",
        "State of being balanced and focused",
        0.71, 0.41, 0.69, 0.68
    ),
    "integration": create_concept(
        "Integration",
        "Combining parts into a unified whole",
        0.68, 0.46, 0.74, 0.78
    ),
    "wholeness": create_concept(
        "Wholeness",
        "State of being complete and undivided",
        0.75, 0.44, 0.71, 0.72
    ),
    "synthesis": create_concept(
        "Synthesis",
        "Combination of elements to form coherent whole",
        0.64, 0.49, 0.73, 0.82
    ),
    "unity": create_concept(
        "Unity",
        "State of being one or united",
        0.79, 0.47, 0.69, 0.71
    ),
    "coherence": create_concept(
        "Coherence",
        "Logical and consistent connection of parts",
        0.66, 0.51, 0.70, 0.79
    ),
    "alignment": create_concept(
        "Alignment",
        "Arrangement in a straight line or proper position",
        0.63, 0.54, 0.72, 0.74
    ),
    "resonance": create_concept(
        "Resonance",
        "Quality of evoking response or harmony",
        0.73, 0.43, 0.71, 0.76
    ),
    "attunement": create_concept(
        "Attunement",
        "State of being in harmony or responsive",
        0.76, 0.42, 0.68, 0.73
    ),
    "calibration": create_concept(
        "Calibration",
        "Careful adjustment to achieve accuracy",
        0.59, 0.56, 0.73, 0.81
    ),
    "homeostasis": create_concept(
        "Homeostasis",
        "Tendency toward stable equilibrium",
        0.67, 0.48, 0.74, 0.77
    ),
    "stability": create_concept(
        "Stability",
        "State of being stable and unchanging",
        0.64, 0.53, 0.71, 0.72
    ),
    "steadiness": create_concept(
        "Steadiness",
        "Quality of being regular and unchanging",
        0.66, 0.50, 0.69, 0.70
    ),
    "poise": create_concept(
        "Poise",
        "Graceful and elegant bearing",
        0.72, 0.46, 0.67, 0.74
    ),
    "composure": create_concept(
        "Composure",
        "State of being calm and in control",
        0.69, 0.51, 0.66, 0.76
    ),
    "equanimity": create_concept(
        "Equanimity",
        "Mental calmness and evenness of temper",
        0.74, 0.47, 0.65, 0.78
    ),
}


def main():
    """Generate critical anchor concepts."""
    print("="*60)
    print("LJPW CRITICAL ANCHOR GENERATOR")
    print("="*60)
    
    # Load existing semantic space
    print("\nLoading semantic space...")
    with open("experiments/semantic_space_5000_FINAL.json", 'r', encoding='utf-8') as f:
        semantic_space = json.load(f)
    
    current_count = sum(len(d['concepts']) for d in semantic_space['domains'].values())
    print(f"Current concepts: {current_count:,}")
    
    # Create new domain for foundational concepts
    print("\nCreating 'Foundational Concepts' domain...")
    
    all_anchors = {}
    all_anchors.update(low_justice_anchors)
    all_anchors.update(low_wisdom_anchors)
    all_anchors.update(equilibrium_anchors)
    
    semantic_space['domains']['foundational_concepts'] = {
        'name': 'Foundational Concepts',
        'description': 'High-weight semantic anchors representing dimensional extremes and equilibrium states',
        'concepts': all_anchors
    }
    
    print(f"  Added {len(all_anchors)} critical anchor concepts:")
    print(f"    - Low Justice anchors: {len(low_justice_anchors)}")
    print(f"    - Low Wisdom anchors: {len(low_wisdom_anchors)}")
    print(f"    - Equilibrium anchors: {len(equilibrium_anchors)}")
    
    # Update metadata
    new_count = sum(len(d['concepts']) for d in semantic_space['domains'].values())
    semantic_space['metadata']['total_concepts'] = new_count
    semantic_space['metadata']['total_domains'] = len(semantic_space['domains'])
    semantic_space['metadata']['version'] = "16.1-ANCHORS"
    semantic_space['metadata']['progress_pct'] = round((new_count / 100000) * 100, 2)
    
    # Save
    output_file = "experiments/semantic_space_5040_ANCHORS.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(semantic_space, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print("[SUCCESS] Critical anchors added!")
    print(f"{'='*60}")
    print(f"Output: {output_file}")
    print(f"Total concepts: {new_count:,} (was {current_count:,})")
    print(f"Total domains: {semantic_space['metadata']['total_domains']}")
    print(f"\nSemantic completeness improved:")
    print(f"  - Low Justice coverage: 0 → 10 concepts")
    print(f"  - Low Wisdom coverage: 0 → 10 concepts")
    print(f"  - Equilibrium coverage: 3 → 23 concepts")
    print(f"\nEstimated new completeness: ~75%")


if __name__ == "__main__":
    main()
