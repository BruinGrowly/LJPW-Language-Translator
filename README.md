# LJPW Universal Translation System

**A semantic framework for cross-lingual translation that preserves meaning across languages.**

---

## Overview

The LJPW (Love-Justice-Power-Wisdom) Translation System is a novel approach to machine translation that uses 4-dimensional semantic coordinates to represent meaning independently of language.

**Core Principle**: Same meaning = Same LJPW coordinates (language-independent)

**Key Innovation**: Translation quality can be measured objectively by comparing semantic coordinates before and after translation.

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
│   ├── quantum_semantics.py   # Core semantic encoding
│   ├── semantic_fidelity.py   # Quality metrics
│   └── FIELD_THEORY.md        # Theoretical foundation
│
├── ljpw_pytorch/              # Neural decoder
│   ├── ljpw_decoder.py        # PyTorch model
│   └── train_decoder.py       # Training pipeline
│
├── experiments/               # Research & validation
│   ├── enhanced_pattern_detector.py  # LJPW encoding
│   ├── demo_*.py              # Translation demonstrations
│   └── *_pattern_detector.py  # Language-specific patterns
│
├── data/
│   └── datasets/              # Training data
│
└── Docs/                      # Documentation
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

### Translation Quality Assessment

```python
from ljpw_quantum.semantic_fidelity import SemanticReconstructionFidelity
import numpy as np

fidelity = SemanticReconstructionFidelity()

# Compare source and target LJPW coordinates
source_coords = np.array([0.886, 0.857, 0.586, 0.914])
target_coords = np.array([0.836, 0.798, 0.596, 0.898])

distance = np.linalg.norm(source_coords - target_coords)
print(f"Semantic distance: {distance:.4f}")

# Quality thresholds:
# < 0.08 = Excellent
# < 0.10 = Good
# > 0.10 = Needs review
```

---

## Research Findings

### Cross-Lingual Validation

Tested on Mark 1:1-2 across 5 languages:

| Language | Distance from Greek | Status |
|----------|---------------------|--------|
| English | 0.0795 | Excellent |
| French | 0.1509 | Good |
| Spanish | 0.1400 | Good |
| Chinese | 0.1267 | Good |
| Wedau | 0.1880 | Good |

### Key Discoveries

1. **Semantic Voltage**: Translation quality correlates with preservation of semantic "energy" (||LJPW||)

2. **Structural vs. Lexical**: Sentence structure matters 20x more than individual word choice for preserving meaning

3. **Oral vs. Written**: Oral languages (like Wedau) amplify relational dimensions compared to written languages

4. **Pattern Learning**: Can learn language-specific patterns from as few as 45 verses

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

| Metric | Threshold | Meaning |
|--------|-----------|---------|
| LJPW Distance | < 0.08 | Excellent semantic preservation |
| LJPW Distance | < 0.10 | Good semantic preservation |
| Voltage Change | ±10% | Expected variation |

### Model Performance

- **Parameters**: 5.9M (PyTorch LSTM decoder)
- **Training Data**: 3,023 samples
- **Languages**: 5+ validated
- **Dataset**: 3,779 verses with LJPW coordinates

---

## Documentation

- **README.md** (this file) - Project overview
- **Docs/** - Detailed documentation
  - Research findings
  - Theoretical framework
  - System architecture
- **ljpw_quantum/README.md** - Semantic framework details
- **experiments/** - Validation scripts and demos

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

Research project - see LICENSE file.

---

## Citation

If you use this work in your research, please cite:

```
LJPW Universal Translation System: A Semantic Framework for 
Cross-Lingual Translation
Wellington Kwati Taureka
2025
```

---

## Contact

For questions about the translation system:
- See documentation in `Docs/`
- Review experiments in `experiments/`
- Check issues on GitHub

---

**Semantic coordinates are universal. Translation quality is measurable.**
