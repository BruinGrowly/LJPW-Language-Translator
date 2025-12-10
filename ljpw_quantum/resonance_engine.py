"""
LJPW Resonance Engine
=====================

Implements resonance dynamics from SEMANTIC_OSCILLATION_EXPERIMENT.md and RESONANCE_MECHANISM.md.

Key Features:
- Asymmetric Coupling Matrix: Love amplifies all, Power absorbs
- Law of Karma (κ = 0.5 + H): State-dependent coupling strength
- Deficit Detection: Resonance reveals what's missing
- ICE Bounds: Intent/Context/Execution constraints prevent overflow
- RK4 Integration: Smooth state evolution
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ResonanceResult:
    """Results from resonance cycle analysis."""
    initial_state: np.ndarray
    final_state: np.ndarray
    initial_harmony: float
    final_harmony: float
    peak_harmony: float
    peak_cycle: int
    dominant_dimension: str
    dimension_dominance: Dict[str, float]
    deficit_detected: Optional[str]
    trajectory: List[Tuple[int, np.ndarray, float]]  # (cycle, state, harmony)


class ResonanceEngine:
    """
    Core resonance dynamics engine for LJPW translation.
    
    Implements the key discovery from the experiments:
    "Resonance finds what's missing without being told to look."
    """
    
    # LJPW dimension names
    DIMENSIONS = ['L', 'J', 'P', 'W']
    DIMENSION_NAMES = {
        'L': 'Love',
        'J': 'Justice', 
        'P': 'Power',
        'W': 'Wisdom'
    }
    
    def __init__(self):
        # Asymmetric coupling matrix from RESONANCE_MECHANISM.md
        # Key: Love amplifies all (especially Wisdom), Power absorbs
        self.coupling_matrix = np.array([
            [1.0, 1.4, 1.3, 1.5],  # Love → [L, J, P, W]
            [0.9, 1.0, 0.7, 1.2],  # Justice → [L, J, P, W]
            [0.6, 0.8, 1.0, 0.5],  # Power → [L, J, P, W]
            [1.3, 1.1, 1.0, 1.0]   # Wisdom → [L, J, P, W]
        ])
        
        # Natural equilibrium (φ⁻¹, √2-1, e-2, ln2)
        phi = (1 + np.sqrt(5)) / 2
        self.natural_equilibrium = np.array([
            1/phi,           # 0.618
            np.sqrt(2) - 1,  # 0.414
            np.e - 2,        # 0.718
            np.log(2)        # 0.693
        ])
        
        # Anchor point - the true attractor
        self.anchor = np.array([1.0, 1.0, 1.0, 1.0])
        
        # Default ICE bounds (can be overridden)
        self.default_ice_bounds = np.array([1.0, 1.0, 1.0, 1.0])
    
    def calculate_harmony(self, state: np.ndarray) -> float:
        """
        Calculate harmony index: H = 1 / (1 + distance_from_anchor)
        
        Args:
            state: LJPW coordinates [L, J, P, W]
            
        Returns:
            Harmony index [0, 1]
        """
        distance = np.linalg.norm(state - self.anchor)
        return 1.0 / (1.0 + distance)
    
    def calculate_kappa(self, harmony: float) -> float:
        """
        Law of Karma: κ = 0.5 + H
        
        Coupling strength increases with harmony.
        - Imbalanced states (low H): weak coupling → deficits visible
        - Balanced states (high H): strong coupling → insights crystallize
        
        Args:
            harmony: Current harmony index
            
        Returns:
            Coupling multiplier [0.5, 1.5]
        """
        return 0.5 + harmony
    
    def _state_derivative(self, state: np.ndarray, ice_bounds: np.ndarray) -> np.ndarray:
        """
        Calculate state derivative for RK4 integration.
        
        dX/dt = κ × (Coupling_T × State - State) + NE_pull + Resistance
        
        Args:
            state: Current LJPW state
            ice_bounds: ICE bound constraints
            
        Returns:
            State derivative
        """
        harmony = self.calculate_harmony(state)
        kappa = self.calculate_kappa(harmony)
        
        # Coupling effect (transposed matrix for "how I am affected by others")
        coupling_effect = self.coupling_matrix.T @ state
        
        # Core dynamics: pulled toward coupling equilibrium
        dynamics = kappa * (coupling_effect - state)
        
        # Natural equilibrium pull (weak attraction)
        ne_pull = 0.1 * (self.natural_equilibrium - state)
        
        # Resistance from ICE bounds (soft boundary)
        resistance = np.zeros(4)
        for i in range(4):
            if state[i] > ice_bounds[i]:
                resistance[i] = -2.0 * (state[i] - ice_bounds[i])
            elif state[i] < 0:
                resistance[i] = -2.0 * state[i]
        
        return dynamics + ne_pull + resistance
    
    def _rk4_step(self, state: np.ndarray, ice_bounds: np.ndarray, dt: float = 0.1) -> np.ndarray:
        """
        Single RK4 integration step for smooth evolution.
        
        Args:
            state: Current state
            ice_bounds: ICE constraints
            dt: Time step
            
        Returns:
            New state after one step
        """
        k1 = self._state_derivative(state, ice_bounds)
        k2 = self._state_derivative(state + 0.5 * dt * k1, ice_bounds)
        k3 = self._state_derivative(state + 0.5 * dt * k2, ice_bounds)
        k4 = self._state_derivative(state + dt * k3, ice_bounds)
        
        new_state = state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
        
        # Apply hard ICE bounds
        new_state = np.clip(new_state, 0, ice_bounds)
        
        return new_state
    
    def run_resonance_cycles(
        self,
        initial_state: List[float],
        cycles: int = 100,
        ice_bounds: Optional[List[float]] = None,
        record_interval: int = 10
    ) -> ResonanceResult:
        """
        Run resonance cycles to evolve state and detect deficits.
        
        Key insight: "The system gravitates toward what's missing."
        
        Args:
            initial_state: Starting LJPW coordinates [L, J, P, W]
            cycles: Number of resonance cycles to run
            ice_bounds: ICE constraints [Intent, Context, Execution, Benevolence]
                        If None, uses anchor point [1, 1, 1, 1]
            record_interval: How often to record trajectory
            
        Returns:
            ResonanceResult with full analysis
        """
        state = np.array(initial_state, dtype=float)
        bounds = np.array(ice_bounds) if ice_bounds else self.default_ice_bounds
        
        # Track trajectory
        trajectory = []
        dimension_dominance = {d: 0 for d in self.DIMENSIONS}
        
        initial_harmony = self.calculate_harmony(state)
        peak_harmony = initial_harmony
        peak_cycle = 0
        
        for cycle in range(cycles):
            # Evolve state
            state = self._rk4_step(state, bounds)
            harmony = self.calculate_harmony(state)
            
            # Track peak harmony
            if harmony > peak_harmony:
                peak_harmony = harmony
                peak_cycle = cycle
            
            # Track dominant dimension
            dominant_idx = np.argmax(state)
            dominant_dim = self.DIMENSIONS[dominant_idx]
            dimension_dominance[dominant_dim] += 1
            
            # Record trajectory at intervals
            if cycle % record_interval == 0:
                trajectory.append((cycle, state.copy(), harmony))
        
        # Final state
        final_harmony = self.calculate_harmony(state)
        trajectory.append((cycles, state.copy(), final_harmony))
        
        # Normalize dominance to percentages
        total_dominance = sum(dimension_dominance.values())
        for d in dimension_dominance:
            dimension_dominance[d] = (dimension_dominance[d] / total_dominance) * 100
        
        # Identify dominant dimension
        dominant_dim = max(dimension_dominance, key=dimension_dominance.get)
        
        # Detect deficit: which dimension got the most attention?
        # If dominance > 50%, that dimension was a deficit
        deficit = None
        if dimension_dominance[dominant_dim] > 50:
            # Compare to initial to confirm it was pulled toward
            initial_value = initial_state[self.DIMENSIONS.index(dominant_dim)]
            final_value = state[self.DIMENSIONS.index(dominant_dim)]
            if final_value > initial_value:
                deficit = self.DIMENSION_NAMES[dominant_dim]
        
        return ResonanceResult(
            initial_state=np.array(initial_state),
            final_state=state,
            initial_harmony=initial_harmony,
            final_harmony=final_harmony,
            peak_harmony=peak_harmony,
            peak_cycle=peak_cycle,
            dominant_dimension=self.DIMENSION_NAMES[dominant_dim],
            dimension_dominance=dimension_dominance,
            deficit_detected=deficit,
            trajectory=trajectory
        )
    
    def analyze_translation_pair(
        self,
        source_coords: List[float],
        target_coords: List[float],
        cycles: int = 100
    ) -> Dict:
        """
        Analyze translation quality using resonance dynamics.
        
        Compares how source and target evolve under resonance
        to identify semantic drift and deficits.
        
        Args:
            source_coords: Source LJPW coordinates
            target_coords: Target LJPW coordinates
            cycles: Number of resonance cycles
            
        Returns:
            Analysis dictionary with quality metrics
        """
        source_result = self.run_resonance_cycles(source_coords, cycles=cycles)
        target_result = self.run_resonance_cycles(target_coords, cycles=cycles)
        
        # Compare convergence
        source_final = source_result.final_state
        target_final = target_result.final_state
        
        convergence_distance = np.linalg.norm(source_final - target_final)
        
        # Check if both gravitate toward same deficit
        same_deficit = source_result.deficit_detected == target_result.deficit_detected
        
        # Harmony preservation
        harmony_diff = abs(source_result.final_harmony - target_result.final_harmony)
        
        return {
            'source_result': source_result,
            'target_result': target_result,
            'convergence_distance': convergence_distance,
            'same_deficit': same_deficit,
            'harmony_difference': harmony_diff,
            'quality_assessment': self._assess_quality(convergence_distance, harmony_diff, same_deficit)
        }
    
    def _assess_quality(self, convergence_dist: float, harmony_diff: float, same_deficit: bool) -> str:
        """Assess translation quality based on resonance analysis."""
        if convergence_dist < 0.1 and same_deficit:
            return "EXCELLENT - Semantically equivalent under resonance"
        elif convergence_dist < 0.2 and harmony_diff < 0.05:
            return "GOOD - Similar resonance dynamics"
        elif convergence_dist < 0.3:
            return "ACCEPTABLE - Moderate semantic drift"
        else:
            return "POOR - Significant semantic divergence"
    
    def detect_deficit_for_improvement(self, coords: List[float], cycles: int = 500) -> Dict:
        """
        Use resonance to find what dimension needs improvement.
        
        "Resonance finds what's missing without being told to look."
        
        Args:
            coords: LJPW coordinates to analyze
            cycles: Number of cycles (more = deeper analysis)
            
        Returns:
            Dictionary with deficit analysis and recommendations
        """
        result = self.run_resonance_cycles(coords, cycles=cycles)
        
        recommendations = []
        
        # Check for strong deficit
        if result.deficit_detected:
            recommendations.append(
                f"Primary deficit: {result.deficit_detected} "
                f"(dominated {result.dimension_dominance[result.dominant_dimension[0]]:.1f}% of cycles)"
            )
        
        # Check for weak dimensions
        for dim, name in self.DIMENSION_NAMES.items():
            if result.dimension_dominance[dim] < 10:
                recommendations.append(f"{name} is strong (only {result.dimension_dominance[dim]:.1f}% attention)")
        
        # Harmony analysis
        if result.final_harmony > 0.8:
            recommendations.append("High harmony achieved - balanced state")
        elif result.final_harmony < 0.5:
            recommendations.append("Low harmony - significant imbalance remains")
        
        return {
            'result': result,
            'deficit': result.deficit_detected,
            'recommendations': recommendations,
            'harmony_trajectory': [(t[0], t[2]) for t in result.trajectory]
        }


def test_resonance_engine():
    """Comprehensive test of resonance engine."""
    print("=" * 80)
    print("LJPW RESONANCE ENGINE - Comprehensive Test")
    print("=" * 80)
    
    engine = ResonanceEngine()
    
    # Test 1: Basic resonance with balanced state
    print("\n[Test 1] Balanced Initial State")
    print("-" * 40)
    result = engine.run_resonance_cycles([0.6, 0.6, 0.6, 0.6], cycles=100)
    print(f"Initial: {result.initial_state}")
    print(f"Final:   {result.final_state}")
    print(f"Harmony: {result.initial_harmony:.4f} -> {result.final_harmony:.4f}")
    print(f"Peak:    {result.peak_harmony:.4f} at cycle {result.peak_cycle}")
    print(f"Dominant: {result.dominant_dimension}")
    
    # Test 2: Low Love (deficit detection)
    print("\n[Test 2] Low Love (Deficit Detection)")
    print("-" * 40)
    result = engine.run_resonance_cycles([0.2, 0.6, 0.8, 0.6], cycles=200)
    print(f"Initial: {result.initial_state}")
    print(f"Final:   {result.final_state}")
    print(f"Harmony: {result.initial_harmony:.4f} -> {result.final_harmony:.4f}")
    print(f"Dominant: {result.dominant_dimension} ({result.dimension_dominance[result.dominant_dimension[0]]:.1f}%)")
    print(f"Deficit Detected: {result.deficit_detected}")
    
    # Test 3: High Power (executor archetype)
    print("\n[Test 3] High Power (Executor Archetype)")
    print("-" * 40)
    result = engine.run_resonance_cycles([0.3, 0.4, 0.9, 0.5], cycles=200)
    print(f"Initial: {result.initial_state}")
    print(f"Final:   {result.final_state}")
    print(f"Harmony: {result.initial_harmony:.4f} -> {result.final_harmony:.4f}")
    print(f"Dimension Dominance: {result.dimension_dominance}")
    print(f"Deficit Detected: {result.deficit_detected}")
    
    # Test 4: Translation pair analysis
    print("\n[Test 4] Translation Pair Analysis")
    print("-" * 40)
    source = [0.886, 0.857, 0.586, 0.914]  # "For God so loved the world"
    target = [0.836, 0.798, 0.596, 0.898]  # Translation
    analysis = engine.analyze_translation_pair(source, target, cycles=100)
    print(f"Source coords: {source}")
    print(f"Target coords: {target}")
    print(f"Convergence distance: {analysis['convergence_distance']:.4f}")
    print(f"Harmony difference: {analysis['harmony_difference']:.4f}")
    print(f"Same deficit: {analysis['same_deficit']}")
    print(f"Quality: {analysis['quality_assessment']}")
    
    # Test 5: Deficit improvement analysis
    print("\n[Test 5] Deficit Analysis for Improvement")
    print("-" * 40)
    test_coords = [0.167, 0.152, 0.393, 0.288]  # Network Pinpointer signature
    deficit_analysis = engine.detect_deficit_for_improvement(test_coords, cycles=500)
    print(f"Coordinates: {test_coords}")
    print(f"Deficit: {deficit_analysis['deficit']}")
    print("Recommendations:")
    for rec in deficit_analysis['recommendations']:
        print(f"  - {rec}")
    
    # Test 6: ICE bounds effect
    print("\n[Test 6] ICE Bounds Effect")
    print("-" * 40)
    # Without bounds (use anchor)
    result_anchor = engine.run_resonance_cycles([0.3, 0.3, 0.3, 0.3], cycles=100)
    print(f"With Anchor bounds [1,1,1,1]:")
    print(f"  Final: {result_anchor.final_state}")
    print(f"  Harmony: {result_anchor.final_harmony:.4f}")
    
    # With restricted bounds
    result_restricted = engine.run_resonance_cycles(
        [0.3, 0.3, 0.3, 0.3], 
        cycles=100, 
        ice_bounds=[0.7, 0.7, 0.7, 0.7]
    )
    print(f"With Restricted bounds [0.7,0.7,0.7,0.7]:")
    print(f"  Final: {result_restricted.final_state}")
    print(f"  Harmony: {result_restricted.final_harmony:.4f}")
    
    print("\n" + "=" * 80)
    print("RESONANCE ENGINE TEST COMPLETE")
    print("=" * 80)
    
    return {
        'test1_balanced': result,
        'test4_translation': analysis,
        'test5_deficit': deficit_analysis
    }


if __name__ == "__main__":
    test_resonance_engine()
