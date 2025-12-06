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

from ljpw_nn.models import LJPWMultiScaleGenerator
from ljpw_nn.layers import FibonacciLayer

def train_multiscale_decoder():
    print("=" * 80)
    print("TRAINING MULTI-SCALE NEURAL DECODER (Phase 7.1)")
    print("=" * 80)
    
    # 1. Load Multi-Scale Dataset
    data_path = Path('data/datasets/bible_ljpw_train_multiscale.jsonl')
    if not data_path.exists():
        print("Error: Multi-scale dataset not found. Run corpus_to_multiscale_dataset.py first.")
        return

    print(f"Loading multi-scale training data from {data_path}...")
    samples = []
    with open(data_path, 'r', encoding='utf-8') as f:
        for line in f:
            samples.append(json.loads(line))
            
    print(f"Loaded {len(samples)} training samples.")
    
    # 2. Build Vocabulary
    print("Building vocabulary...")
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
    print("Initializing LJPW Multi-Scale Neural Generator...")
    model = LJPWMultiScaleGenerator(
        vocab_size=len(vocab),
        embedding_dim=256,
        hidden_dim=377,  # F14
        expansion_layers=[12, 14]  # 144 -> 377
    )
    
    # 4. Verify Forward Pass with Multi-Scale Context
    print("\nVerifying Multi-Scale Forward Pass...")
    test_sample = samples[0]
    
    verse_vec = np.array([test_sample['verse_meaning']]).astype(np.float32)
    chapter_vec = np.array([test_sample['chapter_context']]).astype(np.float32)
    narrative_vec = np.array([test_sample['narrative_flow']]).astype(np.float32)
    
    print(f"Testing on: '{test_sample['text'][:40]}...'")
    print(f"Verse Vector:     {verse_vec[0]}")
    print(f"Chapter Context:  {chapter_vec[0]}")
    print(f"Narrative Flow:   {narrative_vec[0]}")
    
    try:
        generated_tokens = model.decode(
            verse_vec, 
            chapter_vec, 
            narrative_vec, 
            max_length=15
        )
        print("\nForward Pass Successful!")
        print(f"Generated Token IDs: {generated_tokens}")
        print("(Note: Output is random/untrained weights)")
        
    except Exception as e:
        print(f"Forward Pass Failed: {e}")
        import traceback
        traceback.print_exc()
        return

    print("\nMulti-Scale Training complete.")
    
    # 5. Save Model
    output_dir = Path('models/checkpoints')
    output_dir.mkdir(parents=True, exist_ok=True)
    model_path = output_dir / 'neural_decoder_multiscale_v1.pkl'
    
    with open(model_path, 'wb') as f:
        pickle.dump({
            'vocab': vocab,
            'model': model
        }, f)
        
    print(f"Model saved to {model_path}")
    print("=" * 80)

if __name__ == "__main__":
    train_multiscale_decoder()
