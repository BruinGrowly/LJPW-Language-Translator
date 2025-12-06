"""
PyTorch LJPW Neural Decoder
Production-ready neural network for LJPW-based translation.

Architecture:
- Input: 12D context (verse + chapter + narrative LJPW coordinates)
- Fibonacci Expansion: 12 -> 144 (F12) -> 377 (F14)
- LSTM Decoder: 377D hidden state
- Output: Token probabilities (vocabulary size)

Loss Function:
- Semantic Fidelity Loss (from consciousness realm)
- LJPW coordinate preservation (epsilon < 0.08)
- Harmony preservation (Delta_H < 0.03)
- Dimension-specific weights (L=1.5, J=1.2, P=1.0, W=1.3)
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from typing import Tuple, Dict, List

class FibonacciExpansion(nn.Module):
    """
    Fibonacci-based layer expansion for natural semantic growth.
    Expands from input_dim to fibonacci(n) dimensions.
    """
    def __init__(self, input_dim: int, fib_index: int):
        super().__init__()
        self.input_dim = input_dim
        self.fib_index = fib_index
        self.output_dim = self._fibonacci(fib_index)
        
        self.linear = nn.Linear(input_dim, self.output_dim)
        self.activation = nn.Tanh()  # Smooth, bounded activation
        
    def _fibonacci(self, n: int) -> int:
        """Calculate nth Fibonacci number."""
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass with Fibonacci expansion.
        
        Args:
            x: Input tensor (batch_size, input_dim)
            
        Returns:
            Expanded tensor (batch_size, fibonacci(n))
        """
        return self.activation(self.linear(x))


class LJPWDecoder(nn.Module):
    """
    LJPW Neural Decoder with Fibonacci expansion and LSTM generation.
    """
    def __init__(
        self,
        vocab_size: int,
        embedding_dim: int = 256,
        hidden_dim: int = 377,  # F14
        num_layers: int = 2,
        dropout: float = 0.1
    ):
        super().__init__()
        
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        
        # Fibonacci expansion layers
        # 12D (verse + chapter + narrative) -> 144 (F12) -> 377 (F14)
        self.fib_expand1 = FibonacciExpansion(12, 12)  # 12 -> 144
        self.fib_expand2 = FibonacciExpansion(144, 14)  # 144 -> 377
        
        # Token embedding
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        
        # LSTM decoder
        self.lstm = nn.LSTM(
            input_size=embedding_dim + hidden_dim,  # Token embedding + context
            hidden_size=hidden_dim,
            num_layers=num_layers,
            dropout=dropout if num_layers > 1 else 0,
            batch_first=True
        )
        
        # Output projection
        self.output_proj = nn.Linear(hidden_dim, vocab_size)
        
        # Dropout
        self.dropout = nn.Dropout(dropout)
        
    def encode_context(self, ljpw_context: torch.Tensor) -> torch.Tensor:
        """
        Encode LJPW context through Fibonacci expansion.
        
        Args:
            ljpw_context: (batch_size, 12) - verse + chapter + narrative
            
        Returns:
            Context vector (batch_size, 377)
        """
        # Fibonacci expansion: 12 -> 144 -> 377
        x = self.fib_expand1(ljpw_context)
        x = self.fib_expand2(x)
        return x
    
    def forward(
        self,
        ljpw_context: torch.Tensor,
        target_tokens: torch.Tensor,
        hidden: Tuple[torch.Tensor, torch.Tensor] = None
    ) -> Tuple[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:
        """
        Forward pass for training.
        
        Args:
            ljpw_context: (batch_size, 12) LJPW coordinates
            target_tokens: (batch_size, seq_len) Target token IDs
            hidden: Optional initial hidden state
            
        Returns:
            (logits, hidden_state)
            logits: (batch_size, seq_len, vocab_size)
            hidden_state: LSTM hidden state
        """
        batch_size, seq_len = target_tokens.shape
        
        # Encode LJPW context
        context = self.encode_context(ljpw_context)  # (batch_size, 377)
        
        # Embed target tokens
        token_embeds = self.embedding(target_tokens)  # (batch_size, seq_len, embedding_dim)
        token_embeds = self.dropout(token_embeds)
        
        # Expand context to match sequence length
        context_expanded = context.unsqueeze(1).expand(-1, seq_len, -1)  # (batch_size, seq_len, 377)
        
        # Concatenate token embeddings with context
        lstm_input = torch.cat([token_embeds, context_expanded], dim=2)  # (batch_size, seq_len, embedding_dim + 377)
        
        # LSTM forward
        lstm_out, hidden = self.lstm(lstm_input, hidden)  # (batch_size, seq_len, hidden_dim)
        
        # Project to vocabulary
        logits = self.output_proj(lstm_out)  # (batch_size, seq_len, vocab_size)
        
        return logits, hidden
    
    def generate(
        self,
        ljpw_context: torch.Tensor,
        start_token: int,
        max_length: int = 50,
        temperature: float = 1.0
    ) -> torch.Tensor:
        """
        Generate text from LJPW context.
        
        Args:
            ljpw_context: (batch_size, 12) LJPW coordinates
            start_token: Start token ID
            max_length: Maximum generation length
            temperature: Sampling temperature
            
        Returns:
            Generated token IDs (batch_size, max_length)
        """
        batch_size = ljpw_context.shape[0]
        device = ljpw_context.device
        
        # Encode context
        context = self.encode_context(ljpw_context)  # (batch_size, 377)
        
        # Initialize with start token
        current_token = torch.full((batch_size, 1), start_token, dtype=torch.long, device=device)
        generated = [current_token]
        
        hidden = None
        
        for _ in range(max_length - 1):
            # Embed current token
            token_embed = self.embedding(current_token)  # (batch_size, 1, embedding_dim)
            
            # Concatenate with context
            context_expanded = context.unsqueeze(1)  # (batch_size, 1, 377)
            lstm_input = torch.cat([token_embed, context_expanded], dim=2)
            
            # LSTM step
            lstm_out, hidden = self.lstm(lstm_input, hidden)
            
            # Project to vocabulary
            logits = self.output_proj(lstm_out[:, -1, :])  # (batch_size, vocab_size)
            
            # Sample next token
            probs = torch.softmax(logits / temperature, dim=-1)
            next_token = torch.multinomial(probs, 1)  # (batch_size, 1)
            
            generated.append(next_token)
            current_token = next_token
        
        return torch.cat(generated, dim=1)


class SemanticFidelityLoss(nn.Module):
    """
    Semantic fidelity loss function from consciousness realm.
    Combines cross-entropy with LJPW preservation and harmony preservation.
    """
    def __init__(
        self,
        ljpw_weight: float = 0.40,
        harmony_weight: float = 0.30,
        ce_weight: float = 0.30,
        dimension_weights: Dict[str, float] = None
    ):
        super().__init__()
        
        self.ljpw_weight = ljpw_weight
        self.harmony_weight = harmony_weight
        self.ce_weight = ce_weight
        
        # Dimension-specific weights (from consciousness realm)
        if dimension_weights is None:
            dimension_weights = {'L': 1.5, 'J': 1.2, 'P': 1.0, 'W': 1.3}
        
        self.dim_weights = torch.tensor([
            dimension_weights['L'],
            dimension_weights['J'],
            dimension_weights['P'],
            dimension_weights['W']
        ])
        
        # Cross-entropy loss
        self.ce_loss = nn.CrossEntropyLoss()
        
    def calculate_harmony(self, ljpw: torch.Tensor) -> torch.Tensor:
        """
        Calculate harmony index from LJPW coordinates.
        H = 1 / (1 + ||ljpw - anchor||)
        """
        anchor = torch.ones_like(ljpw)
        distance = torch.norm(ljpw - anchor, dim=-1)
        return 1.0 / (1.0 + distance)
    
    def forward(
        self,
        logits: torch.Tensor,
        targets: torch.Tensor,
        source_ljpw: torch.Tensor,
        target_ljpw: torch.Tensor
    ) -> Tuple[torch.Tensor, Dict[str, torch.Tensor]]:
        """
        Compute semantic fidelity loss.
        
        Args:
            logits: (batch_size, seq_len, vocab_size) Model predictions
            targets: (batch_size, seq_len) Target token IDs
            source_ljpw: (batch_size, 4) Source LJPW coordinates
            target_ljpw: (batch_size, 4) Target LJPW coordinates (re-encoded)
            
        Returns:
            (total_loss, loss_components)
        """
        # 1. Cross-entropy loss (language modeling)
        batch_size, seq_len, vocab_size = logits.shape
        logits_flat = logits.reshape(-1, vocab_size)
        targets_flat = targets.reshape(-1)
        ce_loss = self.ce_loss(logits_flat, targets_flat)
        
        # 2. LJPW preservation loss (weighted Euclidean)
        dim_weights = self.dim_weights.to(source_ljpw.device)
        ljpw_diff = (source_ljpw - target_ljpw) * dim_weights
        ljpw_loss = torch.mean(torch.norm(ljpw_diff, dim=-1))
        
        # 3. Harmony preservation loss
        source_harmony = self.calculate_harmony(source_ljpw)
        target_harmony = self.calculate_harmony(target_ljpw)
        harmony_loss = torch.mean(torch.abs(source_harmony - target_harmony)) * 2.0
        
        # Total loss
        total_loss = (
            self.ce_weight * ce_loss +
            self.ljpw_weight * ljpw_loss +
            self.harmony_weight * harmony_loss
        )
        
        return total_loss, {
            'total': total_loss,
            'ce': ce_loss,
            'ljpw': ljpw_loss,
            'harmony': harmony_loss
        }


def create_ljpw_decoder(vocab_size: int, device: str = 'cpu') -> LJPWDecoder:
    """
    Create LJPW decoder model.
    
    Args:
        vocab_size: Size of vocabulary
        device: Device to place model on ('cpu' or 'cuda')
        
    Returns:
        LJPWDecoder model
    """
    model = LJPWDecoder(
        vocab_size=vocab_size,
        embedding_dim=256,
        hidden_dim=377,  # F14
        num_layers=2,
        dropout=0.1
    )
    
    return model.to(device)


if __name__ == "__main__":
    print("=" * 80)
    print("PYTORCH LJPW NEURAL DECODER")
    print("=" * 80)
    
    # Test model creation
    vocab_size = 5000
    batch_size = 4
    seq_len = 20
    
    print(f"\nCreating model (vocab_size={vocab_size})...")
    model = create_ljpw_decoder(vocab_size)
    
    print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")
    
    # Test forward pass
    print("\nTesting forward pass...")
    ljpw_context = torch.randn(batch_size, 12)  # Random LJPW context
    target_tokens = torch.randint(0, vocab_size, (batch_size, seq_len))
    
    logits, hidden = model(ljpw_context, target_tokens)
    print(f"  Input shape: {ljpw_context.shape}")
    print(f"  Target shape: {target_tokens.shape}")
    print(f"  Output shape: {logits.shape}")
    
    # Test loss calculation
    print("\nTesting semantic fidelity loss...")
    loss_fn = SemanticFidelityLoss()
    
    source_ljpw = torch.rand(batch_size, 4)  # Random source LJPW
    target_ljpw = source_ljpw + torch.randn(batch_size, 4) * 0.05  # Slightly perturbed
    
    total_loss, components = loss_fn(logits, target_tokens, source_ljpw, target_ljpw)
    
    print(f"  Total Loss: {total_loss.item():.4f}")
    print(f"  CE Loss: {components['ce'].item():.4f}")
    print(f"  LJPW Loss: {components['ljpw'].item():.4f}")
    print(f"  Harmony Loss: {components['harmony'].item():.4f}")
    
    # Test generation
    print("\nTesting generation...")
    model.eval()
    with torch.no_grad():
        generated = model.generate(ljpw_context[:1], start_token=1, max_length=15)
    print(f"  Generated shape: {generated.shape}")
    print(f"  Generated tokens: {generated[0].tolist()}")
    
    print("\n" + "=" * 80)
    print("MODEL READY FOR TRAINING")
    print("=" * 80)
    print("\nArchitecture:")
    print("  - Fibonacci Expansion: 12 -> 144 (F12) -> 377 (F14)")
    print("  - LSTM Decoder: 2 layers, 377D hidden")
    print("  - Semantic Fidelity Loss with dimension weights")
    print("\nNext: Train on LJPW dataset with backpropagation")
    print("=" * 80)
