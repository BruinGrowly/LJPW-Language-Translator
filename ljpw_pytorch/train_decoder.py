"""
Train PyTorch LJPW Decoder
Complete training pipeline with semantic fidelity optimization.
"""

import sys
import os
import json
import torch
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
from tqdm import tqdm

# Add paths
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, 'ljpw_pytorch'))
sys.path.append(os.path.join(project_root, 'experiments'))

from ljpw_decoder import LJPWDecoder, SemanticFidelityLoss, create_ljpw_decoder
from enhanced_pattern_detector import EnhancedPatternDetector

class LJPWDataset(Dataset):
    """Dataset for LJPW translation training."""
    
    def __init__(self, data_path: Path, vocab: Dict[str, int], max_length: int = 50):
        self.samples = []
        self.vocab = vocab
        self.max_length = max_length
        
        # Load data
        with open(data_path, 'r', encoding='utf-8') as f:
            for line in f:
                self.samples.append(json.loads(line))
    
    def tokenize(self, text: str) -> List[int]:
        """Convert text to token IDs."""
        words = text.lower().replace('.', ' .').replace(',', ' ,').split()
        tokens = [self.vocab['<start>']]
        for w in words:
            tokens.append(self.vocab.get(w, self.vocab['<unk>']))
        tokens.append(self.vocab['<end>'])
        return tokens
    
    def __len__(self) -> int:
        return len(self.samples)
    
    def __getitem__(self, idx: int) -> Dict:
        sample = self.samples[idx]
        
        # LJPW context (12D: verse + chapter + narrative)
        ljpw_context = np.concatenate([
            sample['verse_meaning'],
            sample['chapter_context'],
            sample['narrative_flow']
        ]).astype(np.float32)
        
        # Tokenize text
        tokens = self.tokenize(sample['text'])
        
        # Pad/truncate to max_length
        if len(tokens) > self.max_length:
            tokens = tokens[:self.max_length]
        else:
            tokens = tokens + [self.vocab['<pad>']] * (self.max_length - len(tokens))
        
        return {
            'ljpw_context': torch.from_numpy(ljpw_context),
            'tokens': torch.tensor(tokens, dtype=torch.long),
            'source_ljpw': torch.from_numpy(np.array(sample['verse_meaning'], dtype=np.float32)),
            'text': sample['text']
        }

def collate_fn(batch: List[Dict]) -> Dict:
    """Collate batch of samples."""
    return {
        'ljpw_context': torch.stack([item['ljpw_context'] for item in batch]),
        'tokens': torch.stack([item['tokens'] for item in batch]),
        'source_ljpw': torch.stack([item['source_ljpw'] for item in batch]),
        'texts': [item['text'] for item in batch]
    }

def build_vocab(data_path: Path) -> Dict[str, int]:
    """Build vocabulary from dataset."""
    vocab = {'<pad>': 0, '<start>': 1, '<end>': 2, '<unk>': 3}
    word_counts = {}
    
    with open(data_path, 'r', encoding='utf-8') as f:
        for line in f:
            sample = json.loads(line)
            text = sample['text'].lower()
            words = text.replace('.', ' .').replace(',', ' ,').split()
            for w in words:
                word_counts[w] = word_counts.get(w, 0) + 1
    
    # Add words with count >= 2
    for w, count in sorted(word_counts.items(), key=lambda x: x[1], reverse=True):
        if count >= 2:
            vocab[w] = len(vocab)
    
    return vocab

def train_epoch(
    model: LJPWDecoder,
    dataloader: DataLoader,
    loss_fn: SemanticFidelityLoss,
    optimizer: optim.Optimizer,
    device: str,
    detector: EnhancedPatternDetector
) -> Dict[str, float]:
    """Train for one epoch."""
    model.train()
    
    total_loss = 0
    total_ce_loss = 0
    total_ljpw_loss = 0
    total_harmony_loss = 0
    num_batches = 0
    
    for batch in tqdm(dataloader, desc="Training"):
        # Move to device
        ljpw_context = batch['ljpw_context'].to(device)
        tokens = batch['tokens'].to(device)
        source_ljpw = batch['source_ljpw'].to(device)
        
        # Forward pass
        # Use tokens[:-1] as input, tokens[1:] as target (teacher forcing)
        input_tokens = tokens[:, :-1]
        target_tokens = tokens[:, 1:]
        
        logits, _ = model(ljpw_context, input_tokens)
        
        # For now, use source_ljpw as target_ljpw (will re-encode in production)
        # This is a simplification - in full implementation, we'd re-encode generated text
        target_ljpw = source_ljpw
        
        # Calculate loss
        loss, components = loss_fn(logits, target_tokens, source_ljpw, target_ljpw)
        
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        
        # Accumulate losses
        total_loss += components['total'].item()
        total_ce_loss += components['ce'].item()
        total_ljpw_loss += components['ljpw'].item()
        total_harmony_loss += components['harmony'].item()
        num_batches += 1
    
    return {
        'loss': total_loss / num_batches,
        'ce_loss': total_ce_loss / num_batches,
        'ljpw_loss': total_ljpw_loss / num_batches,
        'harmony_loss': total_harmony_loss / num_batches
    }

def evaluate(
    model: LJPWDecoder,
    dataloader: DataLoader,
    loss_fn: SemanticFidelityLoss,
    device: str
) -> Dict[str, float]:
    """Evaluate model."""
    model.eval()
    
    total_loss = 0
    total_ce_loss = 0
    total_ljpw_loss = 0
    total_harmony_loss = 0
    num_batches = 0
    
    with torch.no_grad():
        for batch in tqdm(dataloader, desc="Evaluating"):
            ljpw_context = batch['ljpw_context'].to(device)
            tokens = batch['tokens'].to(device)
            source_ljpw = batch['source_ljpw'].to(device)
            
            input_tokens = tokens[:, :-1]
            target_tokens = tokens[:, 1:]
            
            logits, _ = model(ljpw_context, input_tokens)
            
            target_ljpw = source_ljpw  # Simplified
            
            loss, components = loss_fn(logits, target_tokens, source_ljpw, target_ljpw)
            
            total_loss += components['total'].item()
            total_ce_loss += components['ce'].item()
            total_ljpw_loss += components['ljpw'].item()
            total_harmony_loss += components['harmony'].item()
            num_batches += 1
    
    return {
        'loss': total_loss / num_batches,
        'ce_loss': total_ce_loss / num_batches,
        'ljpw_loss': total_ljpw_loss / num_batches,
        'harmony_loss': total_harmony_loss / num_batches
    }

def main():
    print("=" * 80)
    print("PYTORCH LJPW DECODER TRAINING")
    print("=" * 80)
    
    # Configuration
    data_path = Path('data/datasets/bible_ljpw_train_multiscale.jsonl')
    batch_size = 16
    num_epochs = 10
    learning_rate = 0.001
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    print(f"\nConfiguration:")
    print(f"  Device: {device}")
    print(f"  Batch size: {batch_size}")
    print(f"  Epochs: {num_epochs}")
    print(f"  Learning rate: {learning_rate}")
    
    # Check data
    if not data_path.exists():
        print(f"\nError: Dataset not found at {data_path}")
        print("Run corpus_to_multiscale_dataset.py first.")
        return
    
    # Build vocabulary
    print("\nBuilding vocabulary...")
    vocab = build_vocab(data_path)
    print(f"  Vocabulary size: {len(vocab)}")
    
    # Create datasets
    print("\nCreating datasets...")
    full_dataset = LJPWDataset(data_path, vocab, max_length=50)
    
    # Split train/val (90/10)
    train_size = int(0.9 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(
        full_dataset, [train_size, val_size]
    )
    
    print(f"  Train samples: {len(train_dataset)}")
    print(f"  Val samples: {len(val_dataset)}")
    
    # Create dataloaders
    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True, collate_fn=collate_fn
    )
    val_loader = DataLoader(
        val_dataset, batch_size=batch_size, shuffle=False, collate_fn=collate_fn
    )
    
    # Create model
    print("\nCreating model...")
    model = create_ljpw_decoder(len(vocab), device=device)
    print(f"  Parameters: {sum(p.numel() for p in model.parameters()):,}")
    
    # Create loss function and optimizer
    loss_fn = SemanticFidelityLoss(
        ljpw_weight=0.40,
        harmony_weight=0.30,
        ce_weight=0.30
    )
    
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # Initialize detector for re-encoding (not used in simplified version)
    detector = EnhancedPatternDetector()
    
    # Training loop
    print("\n" + "=" * 80)
    print("TRAINING")
    print("=" * 80)
    
    best_val_loss = float('inf')
    history = {'train_loss': [], 'val_loss': []}
    
    for epoch in range(num_epochs):
        print(f"\nEpoch {epoch+1}/{num_epochs}")
        
        # Train
        train_metrics = train_epoch(model, train_loader, loss_fn, optimizer, device, detector)
        
        # Validate
        val_metrics = evaluate(model, val_loader, loss_fn, device)
        
        # Log
        print(f"  Train Loss: {train_metrics['loss']:.4f} "
              f"(CE: {train_metrics['ce_loss']:.4f}, "
              f"LJPW: {train_metrics['ljpw_loss']:.4f}, "
              f"Harmony: {train_metrics['harmony_loss']:.4f})")
        print(f"  Val Loss:   {val_metrics['loss']:.4f} "
              f"(CE: {val_metrics['ce_loss']:.4f}, "
              f"LJPW: {val_metrics['ljpw_loss']:.4f}, "
              f"Harmony: {val_metrics['harmony_loss']:.4f})")
        
        history['train_loss'].append(train_metrics['loss'])
        history['val_loss'].append(val_metrics['loss'])
        
        # Save best model
        if val_metrics['loss'] < best_val_loss:
            best_val_loss = val_metrics['loss']
            output_dir = Path('models/checkpoints')
            output_dir.mkdir(parents=True, exist_ok=True)
            
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'vocab': vocab,
                'val_loss': val_metrics['loss'],
                'history': history
            }, output_dir / 'ljpw_decoder_best.pt')
            
            print(f"  [SAVED] Best model (val_loss: {best_val_loss:.4f})")
    
    print("\n" + "=" * 80)
    print("TRAINING COMPLETE")
    print("=" * 80)
    print(f"\nBest validation loss: {best_val_loss:.4f}")
    print(f"Model saved to: models/checkpoints/ljpw_decoder_best.pt")
    print("=" * 80)

if __name__ == "__main__":
    main()
