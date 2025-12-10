"""
Resonance Fidelity Loss for Neural Decoder Training
====================================================

A resonance-based loss function that uses attractor convergence as the
primary training signal, based on the December 2024 discovery that
translations converging to the same semantic attractor are semantically
equivalent regardless of surface coordinate differences.

Key insight: "Resonance finds semantic equivalence that distance misses"

Usage:
    from ljpw_pytorch.resonance_loss import ResonanceFidelityLoss
    
    loss_fn = ResonanceFidelityLoss()
    total_loss, components = loss_fn(logits, targets, source_ljpw, target_ljpw)
"""

import torch
import torch.nn as nn
from typing import Dict, Tuple


class ResonanceFidelityLoss(nn.Module):
    """
    Resonance-based semantic fidelity loss (NEW - December 2024).
    
    Uses attractor convergence as the primary training signal, based on the
    discovery that translations converging to the same semantic attractor
    are semantically equivalent regardless of surface coordinate differences.
    """
    def __init__(
        self,
        resonance_weight: float = 0.50,  # Primary metric
        attractor_weight: float = 0.20,
        harmony_weight: float = 0.15,
        ce_weight: float = 0.15,
        resonance_cycles: int = 50  # Fewer cycles for training efficiency
    ):
        super().__init__()
        
        self.resonance_weight = resonance_weight
        self.attractor_weight = attractor_weight
        self.harmony_weight = harmony_weight
        self.ce_weight = ce_weight
        self.resonance_cycles = resonance_cycles
        
        # Asymmetric coupling matrix (from RESONANCE_MECHANISM.md)
        # Love amplifies all, Power absorbs
        self.register_buffer('coupling_matrix', torch.tensor([
            [1.0, 1.4, 1.3, 1.5],  # Love -> [L, J, P, W]
            [0.9, 1.0, 0.7, 1.2],  # Justice -> [L, J, P, W]
            [0.6, 0.8, 1.0, 0.5],  # Power -> [L, J, P, W]
            [1.3, 1.1, 1.0, 1.0]   # Wisdom -> [L, J, P, W]
        ], dtype=torch.float32))
        
        # Anchor point (attractor)
        self.register_buffer('anchor', torch.ones(4, dtype=torch.float32))
        
        # Cross-entropy loss
        self.ce_loss = nn.CrossEntropyLoss()
        
    def calculate_harmony(self, ljpw: torch.Tensor) -> torch.Tensor:
        """Calculate harmony index from LJPW coordinates."""
        distance = torch.norm(ljpw - self.anchor, dim=-1)
        return 1.0 / (1.0 + distance)
    
    def calculate_kappa(self, harmony: torch.Tensor) -> torch.Tensor:
        """Law of Karma: kappa = 0.5 + H"""
        return 0.5 + harmony
    
    def evolve_state(self, state: torch.Tensor, cycles: int = None) -> torch.Tensor:
        """
        Evolve LJPW state through resonance dynamics (simplified for training).
        Uses Euler integration for gradient-friendly computation.
        """
        cycles = cycles or self.resonance_cycles
        dt = 0.1
        
        current = state.clone()
        
        for _ in range(cycles):
            harmony = self.calculate_harmony(current)
            kappa = self.calculate_kappa(harmony).unsqueeze(-1)
            
            # Coupling effect (simplified)
            coupling_effect = torch.matmul(current, self.coupling_matrix)
            
            # Dynamics: pulled toward coupling equilibrium
            dynamics = kappa * (coupling_effect - current)
            
            # Update state (Euler step with clipping)
            current = current + dt * dynamics
            current = torch.clamp(current, 0, 1)
        
        return current
    
    def forward(
        self,
        logits: torch.Tensor,
        targets: torch.Tensor,
        source_ljpw: torch.Tensor,
        target_ljpw: torch.Tensor
    ) -> Tuple[torch.Tensor, Dict[str, torch.Tensor]]:
        """
        Compute resonance fidelity loss.
        
        Args:
            logits: (batch_size, seq_len, vocab_size) Model predictions
            targets: (batch_size, seq_len) Target token IDs
            source_ljpw: (batch_size, 4) Source LJPW coordinates
            target_ljpw: (batch_size, 4) Target LJPW coordinates
        
        Returns:
            (total_loss, loss_components)
        """
        # 1. Cross-entropy loss (language modeling)
        batch_size, seq_len, vocab_size = logits.shape
        logits_flat = logits.reshape(-1, vocab_size)
        targets_flat = targets.reshape(-1)
        ce_loss = self.ce_loss(logits_flat, targets_flat)
        
        # 2. Resonance convergence loss (PRIMARY)
        # Evolve both states through resonance dynamics
        source_evolved = self.evolve_state(source_ljpw)
        target_evolved = self.evolve_state(target_ljpw)
        
        # Convergence distance (should be near 0 for equivalent translations)
        convergence_dist = torch.mean(torch.norm(source_evolved - target_evolved, dim=-1))
        
        # 3. Attractor match loss
        # Both should converge to same attractor (anchor point)
        source_to_anchor = torch.mean(torch.norm(source_evolved - self.anchor, dim=-1))
        target_to_anchor = torch.mean(torch.norm(target_evolved - self.anchor, dim=-1))
        attractor_loss = (source_to_anchor + target_to_anchor) / 2
        
        # 4. Harmony preservation (in final states)
        source_harmony = self.calculate_harmony(source_evolved)
        target_harmony = self.calculate_harmony(target_evolved)
        harmony_loss = torch.mean(torch.abs(source_harmony - target_harmony))
        
        # Total loss (resonance-weighted)
        total_loss = (
            self.ce_weight * ce_loss +
            self.resonance_weight * convergence_dist +
            self.attractor_weight * attractor_loss +
            self.harmony_weight * harmony_loss
        )
        
        return total_loss, {
            'total': total_loss,
            'ce': ce_loss,
            'resonance': convergence_dist,
            'attractor': attractor_loss,
            'harmony': harmony_loss
        }


if __name__ == "__main__":
    print("=" * 60)
    print("RESONANCE FIDELITY LOSS - Test")
    print("=" * 60)
    
    # Test with random data
    batch_size = 4
    seq_len = 20
    vocab_size = 1000
    
    logits = torch.randn(batch_size, seq_len, vocab_size)
    targets = torch.randint(0, vocab_size, (batch_size, seq_len))
    source_ljpw = torch.rand(batch_size, 4)
    target_ljpw = source_ljpw + torch.randn(batch_size, 4) * 0.1
    
    loss_fn = ResonanceFidelityLoss()
    total_loss, components = loss_fn(logits, targets, source_ljpw, target_ljpw)
    
    print(f"\nTotal Loss: {total_loss.item():.4f}")
    print(f"  CE Loss: {components['ce'].item():.4f}")
    print(f"  Resonance Loss: {components['resonance'].item():.4f}")
    print(f"  Attractor Loss: {components['attractor'].item():.4f}")
    print(f"  Harmony Loss: {components['harmony'].item():.4f}")
    
    print("\n" + "=" * 60)
    print("RESONANCE LOSS READY FOR TRAINING")
    print("=" * 60)
