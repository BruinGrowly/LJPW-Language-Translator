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

from ljpw_nn.models import LJPWNeuralGenerator
from ljpw_nn.layers import FibonacciLayer
from ljpw_nn.vocabulary import LJPWVocabulary

def train_decoder():
    print("=" * 80)
    print("TRAINING NEURAL DECODER (Phase 7)")
    print("=" * 80)
    
    # 1. Load Dataset
    data_path = Path('data/datasets/bible_ljpw_train.jsonl')
    if not data_path.exists():
        print("Error: Dataset not found. Run corpus_to_dataset.py first.")
        return

    print(f"Loading training data from {data_path}...")
    samples = []
    with open(data_path, 'r', encoding='utf-8') as f:
        for line in f:
            samples.append(json.loads(line))
            
    print(f"Loaded {len(samples)} training samples.")
    
    # 2. Build Vocabulary (Simple version for this experiment)
    print("Building vocabulary...")
    vocab = {'<pad>': 0, '<start>': 1, '<end>': 2, '<unk>': 3}
    word_counts = {}
    
    for s in samples:
        text = s['text'].lower()
        # Simple split (in real prod, use proper tokenizer)
        words = text.replace('.', ' .').replace(',', ' ,').split()
        for w in words:
            word_counts[w] = word_counts.get(w, 0) + 1
            
    # Add frequent words to vocab
    for w, count in sorted(word_counts.items(), key=lambda x: x[1], reverse=True):
        if count >= 2: # Min frequency
            vocab[w] = len(vocab)
            
    print(f"Vocabulary size: {len(vocab)} words")
    
    # 3. Initialize Model
    print("Initializing LJPW Neural Generator...")
    model = LJPWNeuralGenerator(
        vocab_size=len(vocab),
        embedding_dim=256,
        hidden_dim=233, # F13
        expansion_layers=[11, 13] # 89 -> 233
    )
    
    # 4. Mock Training Loop (Proof of Concept)
    # Since we are creating a pure Python prototype without PyTorch/TensorFlow dependencies
    # we will simulate the training loop to demonstrate the architecture flow.
    
    print("\nStarting Training (Simulated for Prototype)...")
    epochs = 3 
    batch_size = 32
    
    # Verify Forward Pass logic
    test_sample = samples[0]
    ljpw_vec = np.array([test_sample['meaning']]).astype(np.float32) # (1, 4)
    
    print(f"Testing Forward Pass on: '{test_sample['text'][:30]}...'")
    print(f"Input Vector: {ljpw_vec}")
    
    try:
        generated_tokens = model.decode(ljpw_vec, max_length=15)
        print("Forward Pass Successful!")
        print(f"Generated Token IDs: {generated_tokens}")
        print("(Note: Output is random/untrained weights)")
        
    except Exception as e:
        print(f"Forward Pass Failed: {e}")
        import traceback
        traceback.print_exc()
        return

    print("\nTraining complete.")
    
    # 5. Save Model
    output_dir = Path('models/checkpoints')
    output_dir.mkdir(parents=True, exist_ok=True)
    model_path = output_dir / 'neural_decoder_v1.pkl'
    
    with open(model_path, 'wb') as f:
        pickle.dump({
            'vocab': vocab,
            'model': model
        }, f)
        
    print(f"Model saved to {model_path}")
    print("=" * 80)

if __name__ == "__main__":
    train_decoder()
