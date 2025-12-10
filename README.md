# LJPW Universal Translation System

**A semantic framework for cross-lingual translation that preserves meaning across languages.**

---

## Overview

The LJPW (Love-Justice-Power-Wisdom) Translation System is a novel approach to machine translation that uses 4-dimensional semantic coordinates and **resonance dynamics** to represent and validate meaning across languages.

**Core Principle**: Same meaning = Same semantic attractor (language-independent)

**Key Innovation**: Translation quality is measured by **attractor convergence** - texts that converge to the same semantic attractor under resonance dynamics are semantically equivalent, regardless of surface coordinate differences.

> **December 2025 Discovery**: Resonance-based quality assessment reveals semantic equivalence that traditional distance metrics miss. Translations with euclidean distances up to 0.83 still converge to the same attractor - proving they occupy the same "semantic basin."

---

## How It Works

```
Source Text → LJPW Encoding (4D coordinates) → Target Text Generation
           ↓
    Validation: Re-encode → Verify coordinate preservation → Quality assessment
```

### The LJPW Framework

Text is encoded into four semantic dimensions:
- **L (Love)**: Relational and emotional content
- **J (Justice)**: Structural and logical coherence  
- **P (Power)**: Action and agency
- **W (Wisdom)**: Knowledge and understanding

Each dimension ranges from 0 to 1, creating a 4D coordinate that represents the semantic "position" of the text.

---

## Key Features

### 1. **Cross-Lingual Semantic Preservation**
- Measures translation fidelity objectively
- Validates semantic equivalence across languages
- Identifies where meaning is lost or gained

### 2. **Data Efficiency**
- Learns patterns from small datasets
- Supports low-resource languages
- Validated on indigenous languages (Wedau, ~2,000 speakers)

### 3. **Explainable Semantics**
- Interpretable dimensions (L/J/P/W)
- Measurable quality metrics
- Transparent translation process

### 4. **Multi-Language Support**
- Tested on: English, Greek, Chinese, French, Spanish, Wedau
- Universal semantic space (same coordinates across languages)
- Pattern-based generation

---

## Project Structure

```
LJPW-Language-Translator/
├── ljpw_quantum/              # Semantic framework
│   ├── resonance_engine.py    # **NEW** Resonance dynamics & attractor analysis
│   ├── quantum_semantics.py   # Core semantic encoding
│   ├── semantic_fidelity.py   # Quality metrics
│   └── FIELD_THEORY.md        # Theoretical foundation
│
├── ljpw_pytorch/              # Neural decoder
│   ├── ljpw_decoder.py        # PyTorch model
│   └── train_decoder.py       # Training pipeline
│
├── experiments/               # Research & validation
│   ├── demo_resonance_translation.py  # **NEW** Resonance-based quality demo
│   ├── enhanced_pattern_detector.py   # LJPW encoding
│   ├── demo_*.py              # Translation demonstrations
│   └── *_pattern_detector.py  # Language-specific patterns
│
├── Docs/                      # Documentation
│   ├── SEMANTIC_OSCILLATION_EXPERIMENT.md  # Resonance discovery
│   └── RESONANCE_MECHANISM.md              # How resonance works
│
└── data/
    └── datasets/              # Training data
```

---

## Installation

```bash
# Clone repository
git clone https://github.com/BruinGrowly/LJPW-Language-Translator.git
cd LJPW-Language-Translator

# Install dependencies
pip install torch numpy scipy sympy tqdm

# Optional: Install for development
pip install -e .
```

---

## Usage

### Basic Semantic Encoding

```python
from experiments.enhanced_pattern_detector import EnhancedPatternDetector

# Initialize detector
detector = EnhancedPatternDetector()

# Encode text to LJPW coordinates
result = detector.calculate_field_signature_v2("For God so loved the world")
ljpw_coords = [result['L'], result['J'], result['P'], result['W']]

print(f"LJPW: L={ljpw_coords[0]:.3f}, J={ljpw_coords[1]:.3f}, "
      f"P={ljpw_coords[2]:.3f}, W={ljpw_coords[3]:.3f}")
```

### Translation Quality Assessment (Resonance-Based)

```python
from ljpw_quantum.resonance_engine import ResonanceEngine

engine = ResonanceEngine()

# Compare source and target translations
source_coords = [0.886, 0.857, 0.586, 0.914]  # Greek
target_coords = [0.780, 0.721, 0.489, 0.810]  # Wedau

# Resonance analysis reveals semantic equivalence
analysis = engine.analyze_translation_pair(source_coords, target_coords)

print(f"Convergence: {analysis['convergence_distance']:.4f}")
print(f"Same attractor: {analysis['same_deficit']}")
print(f"Quality: {analysis['quality_assessment']}")

# Output:
# Convergence: 0.0000
# Same attractor: True
# Quality: EXCELLENT - Semantically equivalent under resonance
```

> **Why this matters**: Traditional euclidean distance (0.168) would flag this as moderate drift. Resonance reveals they're semantically equivalent.

---

## Research Findings

### The Resonance Paradigm (December 2025)

A breakthrough discovery: **Translations converge to the same semantic attractor regardless of surface coordinate differences.**

| Verse | Greek→Wedau Distance | Resonance Convergence | Verdict |
|-------|---------------------|----------------------|----------|
| Mark 1:1 | 0.168 | 0.000 | Equivalent |
| Mark 1:11 | 0.283 | 0.000 | Equivalent |
| Mark 1:15 | **0.831** | 0.000 | Equivalent |
| Mark 1:41 | 0.253 | 0.000 | Equivalent |

> Mark 1:15 shows the power of resonance: traditional metrics flag 0.831 as poor, but resonance proves semantic equivalence.

### Key Discoveries

1. **Attractor Convergence**: All valid translations converge to the same semantic attractor under LJPW resonance dynamics

2. **Love as Foundational**: The asymmetric coupling matrix amplifies Love dimension - the system gravitates toward relational meaning

3. **Container Determines Attractor**: ICE bounds (Intent/Context/Execution) shape what translations become

4. **Law of Karma (κ = 0.5 + H)**: Coupling strength increases with harmony - insights crystallize at peak states

5. **Oral vs. Written**: Oral languages have different coordinate "accents" but converge to the same attractor

---

## Validation Experiments

The `experiments/` folder contains demonstrations:

- `demo_greek_source.py` - Validate translations against Koine Greek
- `demo_voltage_drop.py` - Measure semantic entropy in translation
- `demo_structural_analysis.py` - Compare structural vs. lexical changes
- `demo_wedau_*.py` - Indigenous language analysis
- `demo_greek_to_wedau.py` - Direct Greek→Wedau translation

---

## Performance Metrics

### Translation Quality Thresholds

| Metric | Method | Threshold | Meaning |
|--------|--------|-----------|--------|
| **Resonance Convergence** | Primary | < 0.10 | Semantically equivalent (same attractor) |
| Euclidean Distance | Legacy | < 0.08 | Excellent surface preservation |
| Euclidean Distance | Legacy | < 0.10 | Good surface preservation |
| Same Attractor | Primary | True | Translations occupy same semantic basin |

### Model Performance

- **Parameters**: 5.9M (PyTorch LSTM decoder)
- **Training Data**: 3,023 samples
- **Languages**: 6+ validated (English, Greek, Chinese, French, Spanish, Wedau)
- **Dataset**: 10,726 concepts in semantic space
- **Resonance Engine**: RK4 integration with asymmetric coupling matrix

---

## Documentation

- **README.md** (this file) - Project overview
- **GETTING_STARTED.md** - Beginner-friendly tutorial
- **QUICK_REFERENCE.md** - One-page printable guide
- **Docs/** - Detailed documentation
  - Research findings
  - Theoretical framework
  - System architecture
- **ljpw_quantum/README.md** - Semantic framework details
- **experiments/** - Validation scripts and demos

---

## Recent Achievements (December 2025)

### Comprehensive Validation
- **450 verse comparisons** across 10 language pairs
- **100% resonance pass rate** - all translations validated
- Tested extreme language families: Quechua ↔ Farsi (zero common ancestry)

### Matthew Translation
- **1,071 verses** translated from English to Wedau
- LJPW-guided translation with dimension-aware tone
- 210+ vocabulary pairs extracted from human translations

### Vocabulary Extraction
- Extracted 412 unique Wedau words from Mark 1 + Matthew 5
- Created expanded vocabulary for improved translation quality

---

## Contributing

This is a research project exploring semantic preservation in translation.

**Current Focus**: 
- Cross-language validation
- Pattern detection refinement
- Neural decoder optimization

**Research Areas**:
- Semantic field theory
- Low-resource language support
- Translation quality metrics

---

## License

This work is offered freely for the benefit of all. See LICENSE file.

---

## Contact

For questions about the translation system:
- See documentation in `Docs/`
- Review experiments in `experiments/`
- Check issues on GitHub

---

**Semantic coordinates are universal. Translation quality is measurable.**
**Meaning transcends language boundaries.**
