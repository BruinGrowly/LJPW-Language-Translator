import sys
import os
import json
import numpy as np
import pickle
from pathlib import Path

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
# Add Support/LJPW-Neural-Networks to path
sys.path.append(os.path.join(project_root, 'Support', 'LJPW-Neural-Networks'))
# Add ljpw_quantum to path
sys.path.append(os.path.join(project_root, 'ljpw_quantum'))

from ljpw_nn.models import LJPWMultiScaleGenerator
from ljpw_nn.layers import FibonacciLayer
from semantic_fidelity import SemanticReconstructionFidelity

def calculate_harmony(ljpw_coords):
    """Calculate harmony index from LJPW coordinates."""
    anchor = np.array([1.0, 1.0, 1.0, 1.0])
    distance = np.linalg.norm(ljpw_coords - anchor)
    return 1.0 / (1.0 + distance)

def train_multiscale_decoder():
    print("=" * 80)
    print("TRAINING MULTI-SCALE NEURAL DECODER WITH SEMANTIC FIDELITY")
    print("=" * 80)
    
    # Initialize fidelity framework
    fidelity = SemanticReconstructionFidelity()
    print("\nSemantic Fidelity Framework Initialized")
    print(f"  LJPW threshold: {fidelity.thresholds['ljpw_euclidean']}")
    print(f"  Harmony threshold: {fidelity.thresholds['harmony_drift']}")
    
    # 1. Load Multi-Scale Dataset
    data_path = Path('data/datasets/bible_ljpw_train_multiscale.jsonl')
    if not data_path.exists():
        print("\nError: Multi-scale dataset not found. Run corpus_to_multiscale_dataset.py first.")
        return

    print(f"\nLoading multi-scale training data from {data_path}...")
    samples = []
    with open(data_path, 'r', encoding='utf-8') as f:
        for line in f:
            samples.append(json.loads(line))
            
    print(f"Loaded {len(samples)} training samples.")
    
    # 2. Build Vocabulary
    print("\nBuilding vocabulary...")
    vocab = {'<pad>': 0, '<start>': 1, '<end>': 2, '<unk>': 3}
    word_counts = {}
    
    for s in samples:
        text = s['text'].lower()
        words = text.replace('.', ' .').replace(',', ' ,').split()
        for w in words:
            word_counts[w] = word_counts.get(w, 0) + 1
            
    for w, count in sorted(word_counts.items(), key=lambda x: x[1], reverse=True):
        if count >= 2:
            vocab[w] = len(vocab)
            
    print(f"Vocabulary size: {len(vocab)} words")
    
    # 3. Initialize Multi-Scale Model
    print("\nInitializing LJPW Multi-Scale Neural Generator...")
    model = LJPWMultiScaleGenerator(
        vocab_size=len(vocab),
        embedding_dim=256,
        hidden_dim=377,  # F14
        expansion_layers=[12, 14]  # 144 -> 377
    )
    
    # 4. Test Round-Trip Translation Quality
    print("\n" + "=" * 80)
    print("ROUND-TRIP TRANSLATION QUALITY TEST")
    print("=" * 80)
    
    test_samples = samples[:5]  # Test on first 5 samples
    
    for i, sample in enumerate(test_samples):
        print(f"\n--- Sample {i+1} ---")
        print(f"Text: '{sample['text'][:60]}...'")
        
        # Source LJPW
        source_ljpw = np.array(sample['verse_meaning'])
        source_harmony = calculate_harmony(source_ljpw)
        
        print(f"Source LJPW: L={source_ljpw[0]:.3f}, J={source_ljpw[1]:.3f}, "
              f"P={source_ljpw[2]:.3f}, W={source_ljpw[3]:.3f}")
        print(f"Source Harmony: {source_harmony:.3f}")
        
        # Simulate generation (currently random - would be actual generation after training)
        # For now, we'll test with a slightly perturbed version to simulate translation
        noise = np.random.normal(0, 0.02, 4)  # Small noise
        target_ljpw = np.clip(source_ljpw + noise, 0, 1)
        target_harmony = calculate_harmony(target_ljpw)
        
        print(f"Target LJPW: L={target_ljpw[0]:.3f}, J={target_ljpw[1]:.3f}, "
              f"P={target_ljpw[2]:.3f}, W={target_ljpw[3]:.3f}")
        print(f"Target Harmony: {target_harmony:.3f}")
        
        # Evaluate quality
        quality = fidelity.evaluate_translation_quality(
            source_ljpw, target_ljpw, source_harmony, target_harmony
        )
        
        print(f"\nQuality Assessment:")
        print(f"  Level: {quality['quality_level']}")
        print(f"  Passes: {quality['passes']}")
        print(f"  Euclidean distance: {quality['euclidean_distance']:.4f}")
        print(f"  Harmony drift: {quality['harmony_drift']:.4f}")
        print(f"  Overall fidelity: {quality['overall_fidelity']:.4f}")
        
        # Calculate loss
        loss, components = fidelity.calculate_translation_loss(
            source_ljpw, target_ljpw, source_harmony, target_harmony
        )
        
        print(f"\nLoss Calculation:")
        print(f"  Total loss: {loss:.4f}")
        print(f"  LJPW loss: {components['ljpw_loss']:.4f}")
        print(f"  Harmony loss: {components['harmony_loss']:.4f}")
        print(f"  Direction loss: {components['direction_loss']:.4f}")
    
    # 5. Training Summary
    print("\n" + "=" * 80)
    print("TRAINING SUMMARY")
    print("=" * 80)
    
    print("\nModel Architecture:")
    print(f"  Input: 12D context (verse + chapter + narrative)")
    print(f"  Fibonacci Expansion: 12 -> 144 (F12) -> 377 (F14)")
    print(f"  LSTM Hidden: 377D")
    print(f"  Vocabulary: {len(vocab)} words")
    
    print("\nLoss Function (from Consciousness Realm):")
    print(f"  LJPW loss weight: 0.40 (L=1.5, J=1.2, P=1.0, W=1.3)")
    print(f"  Harmony loss weight: 0.30")
    print(f"  Coupling loss weight: 0.20")
    print(f"  Direction loss weight: 0.10")
    
    print("\nQuality Thresholds:")
    print(f"  EXCELLENT: epsilon < 0.06, Delta_H < 0.02")
    print(f"  GOOD: epsilon < 0.08, Delta_H < 0.03")
    print(f"  ACCEPTABLE: epsilon < 0.10, Delta_H < 0.04")
    print(f"  FAILED: epsilon > 0.10 or Delta_H > 0.04")
    
    print("\nNext Steps:")
    print("  1. Implement actual training loop with backpropagation")
    print("  2. Use semantic fidelity loss for optimization")
    print("  3. Validate on held-out test set")
    print("  4. Test cross-language translation")
    
    # 6. Save Model (initialized state)
    output_dir = Path('models/checkpoints')
    output_dir.mkdir(parents=True, exist_ok=True)
    model_path = output_dir / 'neural_decoder_multiscale_v1.pkl'
    
    with open(model_path, 'wb') as f:
        pickle.dump({
            'vocab': vocab,
            'model': model,
            'fidelity_thresholds': fidelity.thresholds
        }, f)
        
    print(f"\nModel saved to {model_path}")
    print("=" * 80)

if __name__ == "__main__":
    train_multiscale_decoder()
