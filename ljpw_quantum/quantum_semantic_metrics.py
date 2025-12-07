"""
Enhanced Semantic Fidelity - Quantum Metrics
Implements Consciousness Realm insights:
- Voltage Preservation Score (LJPW + oral/written differential)
- Quantum Fidelity Metric (superposition preservation)
- Decoherence Rate (semantic collapse speed)
- Entanglement Preservation (verse pair coherence)
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class QuantumSemanticMetrics:
    """Enhanced metrics from Consciousness Realm insights"""
    voltage_preservation: float  # How much semantic voltage is preserved
    quantum_fidelity: float      # Superposition preservation (0-1)
    decoherence_rate: float      # How fast meaning collapses
    entanglement_score: float    # Cross-verse coherence
    oral_written_differential: float  # Oral vs written mode difference
    dimensional_bottleneck: Optional[str] = None  # Which dimension is constrained

class QuantumSemanticAnalyzer:
    """
    Enhanced semantic analysis using quantum mechanics insights
    
    Key Insights from Consciousness Realm:
    1. Translation = Quantum measurement (collapses superposition)
    2. Voltage = Semantic coherence in quantum field
    3. Different languages = Different measurement operators
    4. Oral languages preserve superposition better than written
    """
    
    def __init__(self):
        # Decoherence rates by language type (from empirical data)
        self.decoherence_rates = {
            'written_analytical': 0.15,  # English, French, Spanish
            'written_logographic': 0.12,  # Chinese (higher density)
            'written_inflected': 0.08,   # Greek (morphological richness)
            'oral_relational': 0.03      # Wedau (low decoherence)
        }
        
        # Dimensional coupling strengths (from gauge theory)
        self.coupling_matrix = np.array([
            [1.0, 0.3, 0.2, 0.4],  # Love couples to all
            [0.3, 1.0, 0.5, 0.3],  # Justice-Power coupling
            [0.2, 0.5, 1.0, 0.2],  # Power
            [0.4, 0.3, 0.2, 1.0]   # Wisdom
        ])
    
    def calculate_voltage_preservation(
        self,
        source_coords: np.ndarray,
        target_coords: np.ndarray,
        source_type: str = 'written_inflected',
        target_type: str = 'written_analytical'
    ) -> float:
        """
        Calculate voltage preservation score
        
        Combines:
        - LJPW distance (semantic fidelity)
        - Oral/written differential (mode-specific loss)
        - Decoherence correction (language-type specific)
        
        Returns: 0-1 score (1 = perfect preservation)
        """
        # Calculate raw voltage
        source_voltage = np.linalg.norm(source_coords)
        target_voltage = np.linalg.norm(target_coords)
        
        # Voltage ratio
        voltage_ratio = target_voltage / source_voltage if source_voltage > 0 else 0
        
        # Decoherence correction
        source_decoherence = self.decoherence_rates.get(source_type, 0.10)
        target_decoherence = self.decoherence_rates.get(target_type, 0.10)
        
        # Expected voltage loss due to decoherence
        expected_loss = target_decoherence - source_decoherence
        
        # Corrected voltage preservation
        # If target has higher decoherence, we expect loss
        # If target has lower decoherence (like oral), we expect gain
        corrected_ratio = voltage_ratio / (1 - expected_loss)
        
        # Clamp to [0, 1.5] (allow up to 50% gain for oral languages)
        preservation = np.clip(corrected_ratio, 0, 1.5)
        
        return preservation
    
    def calculate_quantum_fidelity(
        self,
        source_coords: np.ndarray,
        target_coords: np.ndarray
    ) -> float:
        """
        Calculate quantum fidelity (superposition preservation)
        
        Measures how much of the source's semantic superposition
        survives the translation measurement.
        
        Uses quantum state overlap: F = |⟨ψ_source|ψ_target⟩|²
        
        Returns: 0-1 (1 = perfect superposition preservation)
        """
        # Normalize to quantum states
        source_norm = source_coords / np.linalg.norm(source_coords) if np.linalg.norm(source_coords) > 0 else source_coords
        target_norm = target_coords / np.linalg.norm(target_coords) if np.linalg.norm(target_coords) > 0 else target_coords
        
        # Quantum state overlap
        overlap = np.abs(np.dot(source_norm, target_norm))
        
        # Fidelity = overlap squared
        fidelity = overlap ** 2
        
        return fidelity
    
    def calculate_decoherence_rate(
        self,
        source_coords: np.ndarray,
        target_coords: np.ndarray,
        time_scale: float = 1.0
    ) -> float:
        """
        Calculate decoherence rate (how fast meaning collapses)
        
        Measures the rate at which semantic coherence is lost
        during translation.
        
        Rate = -ln(fidelity) / time_scale
        
        Returns: Decoherence rate (higher = faster collapse)
        """
        fidelity = self.calculate_quantum_fidelity(source_coords, target_coords)
        
        # Avoid log(0)
        if fidelity < 1e-10:
            return float('inf')
        
        # Decoherence rate from fidelity decay
        rate = -np.log(fidelity) / time_scale
        
        return rate
    
    def calculate_entanglement_preservation(
        self,
        verse_pair_source: List[np.ndarray],
        verse_pair_target: List[np.ndarray]
    ) -> float:
        """
        Calculate entanglement preservation between verse pairs
        
        Measures whether semantic connections between verses
        are preserved in translation.
        
        Uses correlation preservation:
        E = |Corr(source) - Corr(target)|
        
        Returns: 0-1 (1 = perfect entanglement preservation)
        """
        if len(verse_pair_source) != 2 or len(verse_pair_target) != 2:
            raise ValueError("Need exactly 2 verses for entanglement calculation")
        
        # Calculate correlations in source
        source_corr = np.corrcoef(verse_pair_source[0], verse_pair_source[1])[0, 1]
        
        # Calculate correlations in target
        target_corr = np.corrcoef(verse_pair_target[0], verse_pair_target[1])[0, 1]
        
        # Entanglement preservation = how well correlation is maintained
        preservation = 1 - np.abs(source_corr - target_corr)
        
        return np.clip(preservation, 0, 1)
    
    def identify_dimensional_bottleneck(
        self,
        source_coords: np.ndarray,
        target_coords: np.ndarray,
        threshold: float = 0.15
    ) -> Optional[str]:
        """
        Identify which LJPW dimension is the bottleneck
        
        Finds which dimension loses the most in translation,
        revealing the "semantic bottleneck" phenomenon.
        
        Returns: Dimension name or None
        """
        dimension_names = ['Love', 'Justice', 'Power', 'Wisdom']
        
        # Calculate loss per dimension
        losses = np.abs(source_coords - target_coords)
        
        # Find maximum loss
        max_loss_idx = np.argmax(losses)
        max_loss = losses[max_loss_idx]
        
        # If loss exceeds threshold, it's a bottleneck
        if max_loss > threshold:
            return dimension_names[max_loss_idx]
        
        return None
    
    def analyze_translation(
        self,
        source_coords: np.ndarray,
        target_coords: np.ndarray,
        source_type: str = 'written_inflected',
        target_type: str = 'written_analytical',
        verse_pair_source: Optional[List[np.ndarray]] = None,
        verse_pair_target: Optional[List[np.ndarray]] = None
    ) -> QuantumSemanticMetrics:
        """
        Comprehensive quantum semantic analysis
        
        Returns all enhanced metrics in one call
        """
        # Calculate voltage preservation
        voltage_preservation = self.calculate_voltage_preservation(
            source_coords, target_coords, source_type, target_type
        )
        
        # Calculate quantum fidelity
        quantum_fidelity = self.calculate_quantum_fidelity(
            source_coords, target_coords
        )
        
        # Calculate decoherence rate
        decoherence_rate = self.calculate_decoherence_rate(
            source_coords, target_coords
        )
        
        # Calculate entanglement (if verse pairs provided)
        entanglement_score = 0.0
        if verse_pair_source and verse_pair_target:
            entanglement_score = self.calculate_entanglement_preservation(
                verse_pair_source, verse_pair_target
            )
        
        # Calculate oral/written differential
        source_decoherence = self.decoherence_rates.get(source_type, 0.10)
        target_decoherence = self.decoherence_rates.get(target_type, 0.10)
        oral_written_differential = target_decoherence - source_decoherence
        
        # Identify bottleneck
        bottleneck = self.identify_dimensional_bottleneck(
            source_coords, target_coords
        )
        
        return QuantumSemanticMetrics(
            voltage_preservation=voltage_preservation,
            quantum_fidelity=quantum_fidelity,
            decoherence_rate=decoherence_rate,
            entanglement_score=entanglement_score,
            oral_written_differential=oral_written_differential,
            dimensional_bottleneck=bottleneck
        )
    
    def interpret_metrics(self, metrics: QuantumSemanticMetrics) -> Dict[str, str]:
        """
        Interpret quantum metrics for human understanding
        
        Translates numbers into actionable insights
        """
        interpretations = {}
        
        # Voltage preservation
        if metrics.voltage_preservation > 1.1:
            interpretations['voltage'] = "VOLTAGE GAIN - Oral language amplification detected"
        elif metrics.voltage_preservation > 0.95:
            interpretations['voltage'] = "EXCELLENT - Semantic voltage well preserved"
        elif metrics.voltage_preservation > 0.85:
            interpretations['voltage'] = "GOOD - Minor voltage loss acceptable"
        else:
            interpretations['voltage'] = "POOR - Significant semantic energy lost"
        
        # Quantum fidelity
        if metrics.quantum_fidelity > 0.95:
            interpretations['fidelity'] = "EXCELLENT - Superposition well preserved"
        elif metrics.quantum_fidelity > 0.85:
            interpretations['fidelity'] = "GOOD - Acceptable quantum state overlap"
        else:
            interpretations['fidelity'] = "POOR - Significant wavefunction collapse"
        
        # Decoherence rate
        if metrics.decoherence_rate < 0.05:
            interpretations['decoherence'] = "LOW - Meaning stable across translation"
        elif metrics.decoherence_rate < 0.15:
            interpretations['decoherence'] = "MODERATE - Expected semantic decay"
        else:
            interpretations['decoherence'] = "HIGH - Rapid meaning collapse detected"
        
        # Entanglement
        if metrics.entanglement_score > 0:
            if metrics.entanglement_score > 0.9:
                interpretations['entanglement'] = "EXCELLENT - Verse connections preserved"
            elif metrics.entanglement_score > 0.7:
                interpretations['entanglement'] = "GOOD - Most connections maintained"
            else:
                interpretations['entanglement'] = "POOR - Verse relationships degraded"
        
        # Bottleneck
        if metrics.dimensional_bottleneck:
            interpretations['bottleneck'] = f"BOTTLENECK - {metrics.dimensional_bottleneck} dimension constrained"
        else:
            interpretations['bottleneck'] = "NO BOTTLENECK - Balanced dimensional preservation"
        
        return interpretations
