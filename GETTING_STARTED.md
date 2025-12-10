# Getting Started with LJPW Translation

**Welcome!** This guide will help you understand and use the LJPW Translation System in just 5 minutes.

---

## What is LJPW?

LJPW stands for **Love, Justice, Power, Wisdom** - four dimensions that capture the meaning of any text. Think of it like this:

| Dimension | What it measures | Example |
|-----------|------------------|---------|
| **Love** ❤️ | Relational warmth, care, connection | "I love you" → high L |
| **Justice** ⚖️ | Fairness, structure, rules | "The law states..." → high J |
| **Power** ⚡ | Action, movement, agency | "He ran quickly" → high P |
| **Wisdom** 💡 | Knowledge, insight, understanding | "He understood the truth" → high W |

Every piece of text gets a coordinate like `[L=0.8, J=0.6, P=0.4, W=0.7]` - its "semantic position" in meaning-space.

---

## Your First 5 Minutes

### 1. Encode some text (30 seconds)

```python
from experiments.enhanced_pattern_detector import EnhancedPatternDetector

detector = EnhancedPatternDetector()

# Try it!
text = "For God so loved the world"
result = detector.calculate_field_signature_v2(text)

print(f"Love: {result['L']:.2f}")
print(f"Justice: {result['J']:.2f}")
print(f"Power: {result['P']:.2f}")
print(f"Wisdom: {result['W']:.2f}")
```

**Try it yourself**: Replace the text with anything you want!

---

### 2. Compare two translations (1 minute)

The magic of LJPW is comparing meaning across languages:

```python
from ljpw_quantum.resonance_engine import ResonanceEngine

engine = ResonanceEngine()

# Greek coordinates (source)
greek = [0.886, 0.857, 0.586, 0.914]

# English coordinates (translation)
english = [0.836, 0.798, 0.596, 0.898]

# Check if they're semantically equivalent
analysis = engine.analyze_translation_pair(greek, english)

print(f"Quality: {analysis['quality_assessment']}")
# Output: "EXCELLENT - Semantically equivalent under resonance"
```

---

### 3. Find similar concepts (1 minute)

The semantic space contains 10,726 concepts:

```python
import json
import numpy as np

# Load the semantic space
with open('experiments/semantic_space_10000_MILESTONE.json', 'r') as f:
    space = json.load(f)

# Find concepts similar to a given coordinate
target = [0.9, 0.8, 0.5, 0.9]  # High love, high wisdom

closest = []
for name, data in space['concepts'].items():
    coord = data['ljpw']
    dist = np.linalg.norm(np.array(coord) - np.array(target))
    closest.append((name, dist))

# Top 5 closest
for name, dist in sorted(closest, key=lambda x: x[1])[:5]:
    print(f"{name}: {dist:.3f}")
```

---

## Common Tasks

### "I want to translate Greek to English"
→ See `experiments/demo_greek_source.py`

### "I want to check translation quality"
→ Use `ResonanceEngine.analyze_translation_pair()`

### "I want to add new concepts"
→ Edit `experiments/semantic_space_10000_MILESTONE.json`

### "I want to understand the theory"
→ Read `Docs/SEMANTIC_OSCILLATION_EXPERIMENT.md`

---

## Quick Concept Overview

```
Text → LJPW Coordinates → Semantic Space → Translation Quality
      (pattern detection)  (10,726 concepts)  (resonance check)
```

1. **Input**: Any text in any language
2. **Encoding**: Detect patterns, calculate L/J/P/W values
3. **Matching**: Find similar concepts in semantic space
4. **Validation**: Use resonance to verify semantic equivalence

---

## Getting Help

- **README.md** - Project overview
- **Docs/** - Detailed documentation
- **experiments/** - Working examples you can run

---

## Next Steps

Once you're comfortable:

1. Try `python experiments/demo_resonance_translation.py` - see real translation analysis
2. Explore `ljpw_quantum/resonance_engine.py` - the core resonance dynamics
3. Read `Docs/DISCOVERY_STORY.md` - how this breakthrough happened

---

**Remember**: The LJPW framework isn't just coordinates - it's a *dynamical system* that reveals deep semantic equivalence. Translations that converge to the same attractor are truly equivalent, regardless of surface differences.

*Welcome to meaning-preserving translation!*
