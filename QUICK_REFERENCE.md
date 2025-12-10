# LJPW Quick Reference Card

A one-page guide for common tasks. Print this or keep it handy!

---

## Core Concepts

```
L = Love     → Relational warmth, care, connection
J = Justice  → Fairness, structure, rules  
P = Power    → Action, movement, agency
W = Wisdom   → Knowledge, insight, understanding
```

**Harmony**: H = 1/(1 + distance_from_[1,1,1,1])
- H → 1.0 = Perfect balance
- H → 0.5 = Moderate imbalance

---

## Quick Code Snippets

### Encode Text to LJPW
```python
from experiments.enhanced_pattern_detector import EnhancedPatternDetector
detector = EnhancedPatternDetector()
result = detector.calculate_field_signature_v2("your text here")
coords = [result['L'], result['J'], result['P'], result['W']]
```

### Check Translation Quality
```python
from ljpw_quantum.resonance_engine import ResonanceEngine
engine = ResonanceEngine()
analysis = engine.analyze_translation_pair(source_coords, target_coords)
print(analysis['quality_assessment'])
```

### Calculate Harmony
```python
from ljpw_quantum.resonance_engine import ResonanceEngine
engine = ResonanceEngine()
import numpy as np
harmony = engine.calculate_harmony(np.array([0.8, 0.7, 0.6, 0.9]))
```

### Run Resonance Cycles
```python
result = engine.run_resonance_cycles(coords, cycles=1000)
print(f"Final harmony: {result.final_harmony}")
print(f"Deficit detected: {result.deficit_detected}")
```

---

## Quality Thresholds

| Metric | Threshold | Meaning |
|--------|-----------|---------|
| Resonance convergence | < 0.10 | Semantically equivalent ✅ |
| Same attractor | True | Same semantic basin ✅ |
| Euclidean distance | < 0.08 | Good surface match |

---

## Key Files

| Need to... | Look at... |
|------------|------------|
| Encode text | `experiments/enhanced_pattern_detector.py` |
| Check quality | `ljpw_quantum/resonance_engine.py` |
| Train decoder | `ljpw_pytorch/train_decoder.py` |
| Find concepts | `experiments/semantic_space_10000_MILESTONE.json` |
| Understand theory | `Docs/SEMANTIC_OSCILLATION_EXPERIMENT.md` |

---

## Run Demos

```bash
# Translation quality demo
python experiments/demo_resonance_translation.py

# Multi-language validation
python experiments/validate_multilang_resonance.py

# Harmony calibration by language
python experiments/harmony_calibration.py
```

---

## LJPW Dimension Cheatsheet

| High in... | Typically indicates... |
|------------|------------------------|
| L (Love) | Relational text, emotions, care |
| J (Justice) | Rules, laws, structure, logic |
| P (Power) | Actions, commands, movement |
| W (Wisdom) | Teaching, insight, knowledge |

---

## Troubleshooting

**"Import error for resonance_engine"**
→ Make sure you're in the project root directory

**"Translations showing high euclidean distance"**  
→ Use resonance analysis instead - distances up to 0.8+ can still be equivalent!

**"Need to add new concepts"**
→ Edit `experiments/semantic_space_10000_MILESTONE.json`

---

*For more details, see GETTING_STARTED.md or README.md*
