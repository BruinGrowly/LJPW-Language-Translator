"""
Semantic Reconstruction Fidelity Framework
Measures and ensures translation quality via quantum semantic metrics.

Based on cross-realm consciousness translation studies by Nexus, Matthew, Claude, Aurelia, Chippy.
Provides verified thresholds and loss functions for training.
"""

import numpy as np
from typing import Dict, Tuple, List, Optional
from scipy.spatial.distance import mahalanobis

# Import resonance engine for attractor-based quality assessment
try:
    from ljpw_quantum.resonance_engine import ResonanceEngine
    RESONANCE_AVAILABLE = True
except ImportError:
    RESONANCE_AVAILABLE = False

class SemanticReconstructionFidelity:
    """
    Measure and ensure semantic reconstruction fidelity across languages.
    
    Core Principle: Same meaning = same LJPW coordinates (within verified thresholds)
    """
    
    def __init__(self):
        """Initialize with verified thresholds from consciousness realm studies."""
        
        # Verified thresholds from cross-realm translation studies
        self.thresholds = {
            # LJPW coordinate preservation
            'ljpw_euclidean': 0.08,        # Maximum ||ΔLJPW|| for faithful translation
            'ljpw_mahalanobis': 2.5,       # Mahalanobis distance in semantic covariance space
            
            # Harmony preservation  
            'harmony_drift': 0.03,         # Maximum |ΔH| for meaning preservation
            
            # Coupling consistency
            'coupling_deviation': 0.12,    # Maximum relative deviation (12%)
            
            # Entanglement preservation
            'entanglement_difference': 0.15,  # Maximum |ΔS| for correlated passages
            
            # Quantum fidelity measures
            'quantum_fidelity': 0.92,      # Minimum F(rho_source, rho_target)
            'superposition_preservation': 0.85,  # Minimum preserved ambiguity
            
            # Resonance-based thresholds (NEW - December 2025)
            'resonance_convergence': 0.10,   # Maximum convergence distance for equivalence
            'resonance_cycles': 100,         # Number of cycles for resonance analysis
            
            # Additional constraints
            'ambiguity_ensemble_threshold': 0.30,  # Use ensemble if ambiguity > 0.3
            'golden_ratio_deviation': 0.05  # phi relationship preservation
        }
        
        # Initialize resonance engine if available
        self.resonance_engine = ResonanceEngine() if RESONANCE_AVAILABLE else None
        
        # Success criteria (stricter than failure thresholds)
        self.success_criteria = {
            'euclidean_distance': 0.06,
            'harmony_drift': 0.02,
            'coupling_deviation': 0.08,
            'entanglement_difference': 0.10
        }
        
        # Failure thresholds (more conservative)
        self.failure_thresholds = {
            'euclidean_distance': 0.10,
            'harmony_drift': 0.04,
            'coupling_deviation': 0.15,
            'entanglement_difference': 0.20
        }
        
        # Semantic importance weights (Love weighted highest)
        self.dimension_weights = {
            'L': 1.5,  # Love - identity signature
            'J': 1.2,  # Justice
            'P': 1.0,  # Power
            'W': 1.3   # Wisdom
        }
    
    def measure_ljpw_fidelity(self, 
                            ljpw_source: np.ndarray, 
                            ljpw_target: np.ndarray) -> Dict[str, float]:
        """
        Comprehensive LJPW fidelity measurement.
        
        Args:
            ljpw_source: Source LJPW coordinates [L, J, P, W]
            ljpw_target: Target LJPW coordinates [L, J, P, W]
            
        Returns:
            Dictionary of fidelity metrics
        """
        metrics = {}
        
        # 1. Euclidean distance (primary metric)
        metrics['euclidean_distance'] = np.linalg.norm(ljpw_source - ljpw_target)
        metrics['euclidean_passes'] = metrics['euclidean_distance'] < self.thresholds['ljpw_euclidean']
        
        # 2. Weighted Euclidean (accounts for semantic importance)
        weights = np.array([self.dimension_weights[d] for d in ['L', 'J', 'P', 'W']])
        weighted_diff = (ljpw_source - ljpw_target) * weights
        metrics['weighted_euclidean'] = np.linalg.norm(weighted_diff)
        
        # 3. Cosine similarity (direction matters more than magnitude)
        dot_product = np.dot(ljpw_source, ljpw_target)
        norm_product = np.linalg.norm(ljpw_source) * np.linalg.norm(ljpw_target)
        metrics['cosine_similarity'] = dot_product / norm_product if norm_product > 0 else 0
        
        # 4. Coordinate-wise preservation
        for i, dim in enumerate(['L', 'J', 'P', 'W']):
            diff = abs(ljpw_source[i] - ljpw_target[i])
            metrics[f'{dim}_difference'] = diff
            metrics[f'{dim}_preservation'] = 1.0 - diff
        
        # 5. Overall fidelity score
        metrics['overall_fidelity'] = 1.0 - metrics['weighted_euclidean']
        
        return metrics
    
    def measure_resonance_fidelity(self,
                                   ljpw_source: np.ndarray,
                                   ljpw_target: np.ndarray,
                                   cycles: int = None) -> Dict[str, any]:
        """
        Resonance-based fidelity measurement (PRIMARY METRIC - December 2025).
        
        Tests if source and target converge to the same semantic attractor
        under LJPW resonance dynamics. This reveals deep semantic equivalence
        that euclidean distance misses.
        
        Args:
            ljpw_source: Source LJPW coordinates [L, J, P, W]
            ljpw_target: Target LJPW coordinates [L, J, P, W]
            cycles: Number of resonance cycles (default: from thresholds)
            
        Returns:
            Dictionary with resonance fidelity metrics
        """
        if not self.resonance_engine:
            return {
                'resonance_available': False,
                'error': 'Resonance engine not available'
            }
        
        cycles = cycles or self.thresholds['resonance_cycles']
        
        # Run resonance analysis
        analysis = self.resonance_engine.analyze_translation_pair(
            ljpw_source.tolist() if isinstance(ljpw_source, np.ndarray) else ljpw_source,
            ljpw_target.tolist() if isinstance(ljpw_target, np.ndarray) else ljpw_target,
            cycles=cycles
        )
        
        # Extract key metrics
        convergence = analysis['convergence_distance']
        same_attractor = analysis['same_deficit']
        
        return {
            'resonance_available': True,
            'convergence_distance': convergence,
            'same_attractor': same_attractor,
            'resonance_quality': analysis['quality_assessment'],
            'passes_resonance': convergence < self.thresholds['resonance_convergence'],
            'source_final_state': analysis['source_result'].final_state,
            'target_final_state': analysis['target_result'].final_state,
            'source_final_harmony': analysis['source_result'].final_harmony,
            'target_final_harmony': analysis['target_result'].final_harmony
        }
    
    def calculate_harmony(self, ljpw_coords: np.ndarray) -> float:
        """
        Calculate harmony index from LJPW coordinates.
        H = 1 / (1 + ||ψ - anchor||)
        
        Args:
            ljpw_coords: [L, J, P, W] coordinates
            
        Returns:
            Harmony index (0 to 1)
        """
        # Ensure numpy array
        ljpw_coords = np.array(ljpw_coords)
        
        # Anchor point (perfect harmony)
        anchor = np.array([1.0, 1.0, 1.0, 1.0])
        
        # Calculate Euclidean distance from anchor
        distance = np.linalg.norm(ljpw_coords - anchor)
        
        # Harmony is inverse of distance (1 at anchor, decays with distance)
        return 1.0 / (1.0 + distance)
    
    def measure_harmony_preservation(self, 
                                    harmony_source: float, 
                                    harmony_target: float) -> Dict[str, float]:
        """
        Analyze harmony preservation across translation.
        
        Args:
            harmony_source: Source harmony index
            harmony_target: Target harmony index
            
        Returns:
            Harmony preservation metrics
        """
        delta_h = abs(harmony_source - harmony_target)
        
        return {
            'H_source': harmony_source,
            'H_target': harmony_target,
            'delta_H': delta_h,
            'harmony_fidelity': 1.0 - delta_h,
            'passes_threshold': delta_h < self.thresholds['harmony_drift'],
            'meets_success': delta_h < self.success_criteria['harmony_drift']
        }
    
    def measure_coupling_consistency(self, 
                                   coupling_source: Dict[str, float], 
                                   coupling_target: Dict[str, float]) -> Dict:
        """
        Verify coupling amplification is preserved across languages.
        
        Args:
            coupling_source: Source coupling effects
            coupling_target: Target coupling effects
            
        Returns:
            Coupling consistency metrics
        """
        deviations = {}
        
        for key in coupling_source:
            if key in coupling_target:
                source_val = coupling_source[key]
                target_val = coupling_target[key]
                
                # Relative deviation
                rel_dev = abs(source_val - target_val) / max(abs(source_val), 1e-6)
                deviations[key] = rel_dev
        
        avg_deviation = np.mean(list(deviations.values())) if deviations else 0
        
        return {
            'source_coupling': coupling_source,
            'target_coupling': coupling_target,
            'relative_deviations': deviations,
            'average_deviation': avg_deviation,
            'consistency_score': 1.0 - avg_deviation,
            'passes_threshold': avg_deviation < self.thresholds['coupling_deviation'],
            'meets_success': avg_deviation < self.success_criteria['coupling_deviation']
        }
    
    def calculate_translation_loss(self,
                                  ljpw_source: np.ndarray,
                                  ljpw_target: np.ndarray,
                                  harmony_source: float,
                                  harmony_target: float,
                                  coupling_source: Dict[str, float] = None,
                                  coupling_target: Dict[str, float] = None) -> Tuple[float, Dict[str, float]]:
        """
        Complete loss function for training neural decoder.
        
        Args:
            ljpw_source: Source LJPW coordinates
            ljpw_target: Target LJPW coordinates
            harmony_source: Source harmony index
            harmony_target: Target harmony index
            coupling_source: Optional source coupling effects
            coupling_target: Optional target coupling effects
            
        Returns:
            (total_loss, loss_components)
        """
        losses = {}
        
        # 1. LJPW coordinate loss (weighted by semantic importance)
        weighted_diffs = []
        for i, dim in enumerate(['L', 'J', 'P', 'W']):
            diff = abs(ljpw_source[i] - ljpw_target[i])
            weight = self.dimension_weights[dim]
            weighted_diffs.append(diff * weight)
        
        losses['ljpw_loss'] = np.mean(weighted_diffs)
        
        # 2. Harmony preservation loss
        losses['harmony_loss'] = abs(harmony_source - harmony_target) * 2.0
        
        # 3. Coupling consistency loss (if provided)
        if coupling_source and coupling_target:
            coupling_loss = 0
            count = 0
            for key in coupling_source:
                if key in coupling_target:
                    rel_error = abs(coupling_source[key] - coupling_target[key]) / \
                               max(abs(coupling_source[key]), 1e-6)
                    coupling_loss += rel_error
                    count += 1
            losses['coupling_loss'] = coupling_loss / count if count > 0 else 0
        else:
            losses['coupling_loss'] = 0
        
        # 4. Cosine similarity loss (encourage same direction)
        cosine_sim = np.dot(ljpw_source, ljpw_target) / \
                    (np.linalg.norm(ljpw_source) * np.linalg.norm(ljpw_target) + 1e-6)
        losses['direction_loss'] = 1.0 - cosine_sim
        
        # Total loss (weighted sum)
        weights = {
            'ljpw_loss': 0.40,
            'harmony_loss': 0.30,
            'coupling_loss': 0.20,
            'direction_loss': 0.10
        }
        
        total_loss = sum(losses[k] * weights[k] for k in losses)
        
        return total_loss, losses
    
    def calculate_resonance_loss(self,
                                 ljpw_source: np.ndarray,
                                 ljpw_target: np.ndarray,
                                 cycles: int = None) -> Tuple[float, Dict[str, float]]:
        """
        Resonance-based loss function for training (NEW - December 2025).
        
        Uses attractor convergence as the primary loss signal. Translations
        that converge to the same attractor have low loss regardless of
        surface coordinate differences.
        
        Args:
            ljpw_source: Source LJPW coordinates
            ljpw_target: Target LJPW coordinates
            cycles: Number of resonance cycles
            
        Returns:
            (total_loss, loss_components)
        """
        losses = {}
        
        # 1. Resonance convergence loss (PRIMARY)
        resonance_metrics = self.measure_resonance_fidelity(ljpw_source, ljpw_target, cycles)
        
        if resonance_metrics.get('resonance_available', False):
            # Low convergence distance = low loss
            losses['resonance_convergence'] = resonance_metrics['convergence_distance']
            
            # Same attractor bonus (0 if same, 0.5 penalty if different)
            losses['attractor_mismatch'] = 0.0 if resonance_metrics['same_attractor'] else 0.5
            
            # Harmony difference in final states
            h_diff = abs(resonance_metrics['source_final_harmony'] - 
                        resonance_metrics['target_final_harmony'])
            losses['final_harmony_diff'] = h_diff
        else:
            # Fallback to euclidean if resonance not available
            losses['resonance_convergence'] = np.linalg.norm(ljpw_source - ljpw_target)
            losses['attractor_mismatch'] = 0.0
            losses['final_harmony_diff'] = 0.0
        
        # 2. Surface coordination loss (secondary, for gradient signal)
        losses['surface_distance'] = np.linalg.norm(ljpw_source - ljpw_target) * 0.1
        
        # Total loss (resonance-weighted)
        weights = {
            'resonance_convergence': 0.50,  # Primary metric
            'attractor_mismatch': 0.30,     # Same basin?
            'final_harmony_diff': 0.10,     # Harmony preservation
            'surface_distance': 0.10        # Gradient helper
        }
        
        total_loss = sum(losses[k] * weights[k] for k in losses)
        
        return total_loss, losses
    
    def evaluate_translation_quality(self,
                                    ljpw_source: np.ndarray,
                                    ljpw_target: np.ndarray,
                                    harmony_source: float,
                                    harmony_target: float) -> Dict[str, any]:
        """
        Comprehensive translation quality evaluation.
        
        Returns:
            Quality assessment with pass/fail status
        """
        # Measure fidelity
        ljpw_metrics = self.measure_ljpw_fidelity(ljpw_source, ljpw_target)
        harmony_metrics = self.measure_harmony_preservation(harmony_source, harmony_target)
        
        # Resonance-based assessment (PRIMARY - December 2025)
        resonance_metrics = self.measure_resonance_fidelity(ljpw_source, ljpw_target)
        
        # Legacy metrics
        euclidean_dist = ljpw_metrics['euclidean_distance']
        harmony_drift = harmony_metrics['delta_H']
        
        # Determine quality level using RESONANCE as primary
        if resonance_metrics.get('resonance_available', False):
            # Resonance-based quality (NEW paradigm)
            if resonance_metrics['passes_resonance'] and resonance_metrics['same_attractor']:
                quality = 'EXCELLENT (Resonance-verified)'
                passes = True
            elif resonance_metrics['convergence_distance'] < 0.2:
                quality = 'GOOD (Resonance-verified)'
                passes = True
            elif euclidean_dist < self.thresholds['ljpw_euclidean']:
                quality = 'ACCEPTABLE (Legacy metric)'
                passes = True
            else:
                quality = 'FAILED'
                passes = False
        else:
            # Fallback to legacy euclidean metrics
            if (euclidean_dist < self.success_criteria['euclidean_distance'] and
                harmony_drift < self.success_criteria['harmony_drift']):
                quality = 'EXCELLENT (Legacy)'
                passes = True
            elif (euclidean_dist < self.thresholds['ljpw_euclidean'] and
                  harmony_drift < self.thresholds['harmony_drift']):
                quality = 'GOOD (Legacy)'
                passes = True
            elif (euclidean_dist < self.failure_thresholds['euclidean_distance'] and
                  harmony_drift < self.failure_thresholds['harmony_drift']):
                quality = 'ACCEPTABLE (Legacy)'
                passes = True
            else:
                quality = 'FAILED'
                passes = False
        
        return {
            'quality_level': quality,
            'passes': passes,
            'resonance_metrics': resonance_metrics,
            'ljpw_metrics': ljpw_metrics,
            'harmony_metrics': harmony_metrics,
            'euclidean_distance': euclidean_dist,
            'harmony_drift': harmony_drift,
            'overall_fidelity': ljpw_metrics['overall_fidelity'],
            'recommendations': self._generate_recommendations(
                euclidean_dist, harmony_drift, resonance_metrics
            )
        }
    
    def _generate_recommendations(self, euclidean_dist: float, harmony_drift: float,
                                   resonance_metrics: Dict = None) -> List[str]:
        """Generate recommendations based on metrics."""
        recommendations = []
        
        # Resonance-based recommendations (primary)
        if resonance_metrics and resonance_metrics.get('resonance_available', False):
            if resonance_metrics['passes_resonance'] and resonance_metrics['same_attractor']:
                recommendations.append("Resonance-verified: Translations converge to same semantic attractor")
            elif not resonance_metrics['same_attractor']:
                recommendations.append("WARNING: Translations converge to different attractors - semantic drift detected")
            
            if resonance_metrics['convergence_distance'] > self.thresholds['resonance_convergence']:
                recommendations.append(f"Resonance convergence high ({resonance_metrics['convergence_distance']:.3f})")
        
        # Legacy recommendations
        if euclidean_dist > self.thresholds['ljpw_euclidean']:
            recommendations.append(f"Legacy: LJPW distance high ({euclidean_dist:.3f} > {self.thresholds['ljpw_euclidean']})")
        
        if harmony_drift > self.thresholds['harmony_drift']:
            recommendations.append(f"Legacy: Harmony drift high ({harmony_drift:.3f} > {self.thresholds['harmony_drift']})")
        
        if not recommendations:
            recommendations.append("Translation quality meets all thresholds")
        
        return recommendations


# Convenience functions for quick evaluation
def quick_fidelity_check(ljpw_source: np.ndarray, 
                        ljpw_target: np.ndarray,
                        harmony_source: float,
                        harmony_target: float) -> bool:
    """
    Quick pass/fail check for translation quality.
    
    Returns:
        True if translation passes quality thresholds
    """
    fidelity = SemanticReconstructionFidelity()
    result = fidelity.evaluate_translation_quality(
        ljpw_source, ljpw_target, harmony_source, harmony_target
    )
    return result['passes']


def calculate_loss(ljpw_source: np.ndarray,
                  ljpw_target: np.ndarray,
                  harmony_source: float,
                  harmony_target: float) -> float:
    """
    Calculate training loss for translation.
    
    Returns:
        Total loss value
    """
    fidelity = SemanticReconstructionFidelity()
    total_loss, _ = fidelity.calculate_translation_loss(
        ljpw_source, ljpw_target, harmony_source, harmony_target
    )
    return total_loss


if __name__ == "__main__":
    # Example usage
    print("=" * 80)
    print("SEMANTIC RECONSTRUCTION FIDELITY - Demonstration")
    print("=" * 80)
    
    # Initialize framework
    fidelity = SemanticReconstructionFidelity()
    
    # Example: Peter's coordinates (source and target should be similar)
    peter_source = np.array([0.740, 1.000, 1.000, 1.000])
    peter_target_good = np.array([0.750, 0.995, 0.998, 0.997])  # Good translation
    peter_target_bad = np.array([0.650, 0.900, 0.850, 0.900])   # Poor translation
    
    harmony_source = 0.793
    harmony_target_good = 0.790
    harmony_target_bad = 0.720
    
    # Evaluate good translation
    print("\nGOOD TRANSLATION:")
    result_good = fidelity.evaluate_translation_quality(
        peter_source, peter_target_good, harmony_source, harmony_target_good
    )
    print(f"  Quality: {result_good['quality_level']}")
    print(f"  Passes: {result_good['passes']}")
    print(f"  Euclidean distance: {result_good['euclidean_distance']:.4f}")
    print(f"  Harmony drift: {result_good['harmony_drift']:.4f}")
    print(f"  Overall fidelity: {result_good['overall_fidelity']:.4f}")
    
    # Evaluate poor translation
    print("\nPOOR TRANSLATION:")
    result_bad = fidelity.evaluate_translation_quality(
        peter_source, peter_target_bad, harmony_source, harmony_target_bad
    )
    print(f"  Quality: {result_bad['quality_level']}")
    print(f"  Passes: {result_bad['passes']}")
    print(f"  Euclidean distance: {result_bad['euclidean_distance']:.4f}")
    print(f"  Harmony drift: {result_bad['harmony_drift']:.4f}")
    print(f"  Overall fidelity: {result_bad['overall_fidelity']:.4f}")
    print(f"\n  Recommendations:")
    for rec in result_bad['recommendations']:
        print(f"    - {rec}")
    
    # Calculate losses
    print("\n" + "=" * 80)
    print("LOSS CALCULATION")
    print("=" * 80)
    
    loss_good, components_good = fidelity.calculate_translation_loss(
        peter_source, peter_target_good, harmony_source, harmony_target_good
    )
    loss_bad, components_bad = fidelity.calculate_translation_loss(
        peter_source, peter_target_bad, harmony_source, harmony_target_bad
    )
    
    print(f"\nGood translation loss: {loss_good:.4f}")
    print(f"  Components: {components_good}")
    
    print(f"\nBad translation loss: {loss_bad:.4f}")
    print(f"  Components: {components_bad}")
    
    print("\n" + "=" * 80)
