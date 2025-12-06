"""
Multi-Layer Combiner for Universal Translation System
Intelligently combines phonetic, morphological, semantic, and contextual signals.
"""

import numpy as np
from typing import Dict, List, Optional, Any
from scipy.stats import hmean  # Harmonic mean for balanced combination


class MultiLayerCombiner:
    """Combines multiple detection layers with adaptive weighting."""
    
    def __init__(self):
        """Initialize combiner with default layer weights."""
        # Base weights (will be adapted based on confidence)
        self.base_weights = {
            'phonetic': 0.15,
            'morphological': 0.15,
            'semantic': 0.40,
            'context': 0.30
        }
        
        # Confidence thresholds
        self.high_confidence_threshold = 0.7
        self.low_confidence_threshold = 0.3
    
    def calculate_layer_confidence(self, layer_data: Dict[str, Any], layer_type: str) -> float:
        """
        Calculate confidence score for a detection layer.
        
        Args:
            layer_data: The data from the detection layer
            layer_type: Type of layer ('phonetic', 'morphological', 'semantic', 'context')
            
        Returns:
            Confidence score (0-1)
        """
        if layer_type == 'phonetic':
            # Confidence based on how many phonetic features were detected
            features = layer_data.get('features_detected', 0)
            return min(features * 0.25, 1.0)
        
        elif layer_type == 'morphological':
            # Confidence based on morphological complexity
            complexity = layer_data.get('complexity', 'low')
            if complexity == 'high':
                return 0.8
            elif complexity == 'medium':
                return 0.5
            else:
                return 0.3
        
        elif layer_type == 'semantic':
            # Confidence from semantic marker detection
            return layer_data.get('confidence', 0.0)
        
        elif layer_type == 'context':
            # Confidence from context integration
            return layer_data.get('context_confidence', 0.0)
        
        return 0.0
    
    def detect_unknown_word(self, layer_confidences: Dict[str, float]) -> bool:
        """
        Detect if word is unknown (no semantic/context signals).
        
        Args:
            layer_confidences: Confidence scores for each layer
            
        Returns:
            True if word appears to be unknown
        """
        semantic_conf = layer_confidences.get('semantic', 0.0)
        context_conf = layer_confidences.get('context', 0.0)
        
        # Unknown if both semantic and context are very low
        return (semantic_conf + context_conf) < 0.2
    
    def adaptive_weight_calculation(
        self,
        layer_confidences: Dict[str, float],
        is_unknown: bool = False
    ) -> Dict[str, float]:
        """
        Calculate adaptive weights based on layer confidences.
        
        High confidence layers get boosted, low confidence layers get reduced.
        Unknown words fall back to phonetic/morphological.
        
        Args:
            layer_confidences: Confidence scores for each layer
            is_unknown: Whether the word is unknown (no semantic/context)
            
        Returns:
            Adaptive weights for each layer
        """
        # Check if unknown word
        if not is_unknown:
            is_unknown = self.detect_unknown_word(layer_confidences)
        
        # Unknown word fallback: prioritize phonetic/morphological
        if is_unknown:
            return {
                'phonetic': 0.50,
                'morphological': 0.30,
                'semantic': 0.10,
                'context': 0.10
            }
        
        adaptive_weights = {}
        
        for layer, base_weight in self.base_weights.items():
            confidence = layer_confidences.get(layer, 0.0)
            
            # Adaptive scaling
            if confidence >= self.high_confidence_threshold:
                # Boost high-confidence layers
                scale = 1.0 + (confidence - self.high_confidence_threshold) * 1.5
            elif confidence <= self.low_confidence_threshold:
                # Reduce low-confidence layers
                scale = confidence / self.low_confidence_threshold * 0.5
            else:
                # Linear interpolation in middle range
                scale = 0.5 + (confidence - self.low_confidence_threshold) / \
                        (self.high_confidence_threshold - self.low_confidence_threshold) * 0.5
            
            adaptive_weights[layer] = base_weight * scale
        
        # Normalize weights to sum to 1.0
        total_weight = sum(adaptive_weights.values())
        if total_weight > 0:
            adaptive_weights = {k: v / total_weight for k, v in adaptive_weights.items()}
        
        return adaptive_weights
    
    def combine_signatures(
        self,
        phonetic_sig: Optional[Dict[str, float]] = None,
        morphological_sig: Optional[Dict[str, float]] = None,
        semantic_sig: Optional[Dict[str, float]] = None,
        context_sig: Optional[Dict[str, float]] = None,
        layer_confidences: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Combine multiple LJPW signatures with adaptive weighting.
        
        Args:
            phonetic_sig: LJPW signature from phonetic analysis
            morphological_sig: LJPW signature from morphological analysis
            semantic_sig: LJPW signature from semantic markers
            context_sig: LJPW signature from context integration
            layer_confidences: Confidence scores for each layer
            
        Returns:
            Combined LJPW signature with metadata
        """
        # Default empty signatures
        default_sig = {'L': 0.5, 'J': 0.5, 'P': 0.5, 'W': 0.5}
        
        phonetic_sig = phonetic_sig or default_sig
        morphological_sig = morphological_sig or default_sig
        semantic_sig = semantic_sig or default_sig
        context_sig = context_sig or default_sig
        
        # Calculate adaptive weights
        if layer_confidences is None:
            layer_confidences = {k: 0.5 for k in self.base_weights.keys()}
        
        weights = self.adaptive_weight_calculation(layer_confidences)
        
        # Combine signatures for each dimension
        combined = {}
        combination_details = {}
        
        for dim in ['L', 'J', 'P', 'W']:
            values = [
                phonetic_sig.get(dim, 0.5),
                morphological_sig.get(dim, 0.5),
                semantic_sig.get(dim, 0.5),
                context_sig.get(dim, 0.5)
            ]
            
            layer_names = ['phonetic', 'morphological', 'semantic', 'context']
            
            # Weighted combination
            combined[dim] = sum(
                values[i] * weights[layer_names[i]]
                for i in range(4)
            )
            
            # Store details for transparency
            combination_details[dim] = {
                'phonetic': (values[0], weights['phonetic']),
                'morphological': (values[1], weights['morphological']),
                'semantic': (values[2], weights['semantic']),
                'context': (values[3], weights['context']),
                'final': combined[dim]
            }
        
        # Calculate overall confidence (weighted average of layer confidences)
        overall_confidence = sum(
            layer_confidences[layer] * weights[layer]
            for layer in self.base_weights.keys()
        )
        
        return {
            'signature': combined,
            'confidence': overall_confidence,
            'weights': weights,
            'layer_confidences': layer_confidences,
            'combination_details': combination_details
        }
    
    def hierarchical_integration(
        self,
        raw_features: Dict[str, Any],
        semantic_markers: Dict[str, Any],
        context_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Hierarchically integrate detection layers.
        
        Level 1: Raw Features (Phonetic, Morphological)
        Level 2: Semantic Markers
        Level 3: Context Integration
        Level 4: Final Signature
        
        Args:
            raw_features: Phonetic and morphological data
            semantic_markers: Semantic marker detection results
            context_analysis: Context integration results
            
        Returns:
            Hierarchically integrated signature
        """
        # Level 1: Extract raw feature signatures
        phonetic_sig = raw_features.get('phonetic_signature', {})
        morphological_sig = raw_features.get('morphological_signature', {})
        
        # Level 2: Semantic markers build on raw features
        semantic_sig = semantic_markers.get('signature', {})
        semantic_conf = semantic_markers.get('confidence', 0.0)
        
        # Level 3: Context builds on everything
        context_sig = context_analysis.get('signature', {})
        context_conf = context_analysis.get('context_confidence', 0.0)
        
        # Calculate layer confidences
        layer_confidences = {
            'phonetic': raw_features.get('phonetic_confidence', 0.3),
            'morphological': raw_features.get('morphological_confidence', 0.3),
            'semantic': semantic_conf,
            'context': context_conf
        }
        
        # Combine with adaptive weighting
        result = self.combine_signatures(
            phonetic_sig=phonetic_sig,
            morphological_sig=morphological_sig,
            semantic_sig=semantic_sig,
            context_sig=context_sig,
            layer_confidences=layer_confidences
        )
        
        # Add evidence trail
        evidence = []
        evidence.extend(raw_features.get('evidence', []))
        evidence.extend(semantic_markers.get('evidence', []))
        evidence.extend(context_analysis.get('evidence', []))
        
        result['evidence'] = evidence
        
        return result
    
    def explain_combination(self, combination_result: Dict[str, Any]) -> str:
        """
        Generate human-readable explanation of how layers were combined.
        
        Args:
            combination_result: Result from combine_signatures or hierarchical_integration
            
        Returns:
            Explanation string
        """
        weights = combination_result.get('weights', {})
        confidences = combination_result.get('layer_confidences', {})
        signature = combination_result.get('signature', {})
        
        explanation = ["Layer Combination Analysis:", ""]
        
        # Show weights
        explanation.append("Adaptive Weights:")
        for layer, weight in sorted(weights.items(), key=lambda x: x[1], reverse=True):
            conf = confidences.get(layer, 0.0)
            explanation.append(f"  {layer:15s}: {weight:5.1%} (confidence: {conf:.2f})")
        
        explanation.append("")
        explanation.append("Final Signature:")
        for dim in ['L', 'J', 'P', 'W']:
            value = signature.get(dim, 0.5)
            explanation.append(f"  {dim}: {value:.3f}")
        
        explanation.append("")
        explanation.append(f"Overall Confidence: {combination_result.get('confidence', 0.0):.2f}")
        
        return "\n".join(explanation)


if __name__ == "__main__":
    # Test the multi-layer combiner
    combiner = MultiLayerCombiner()
    
    print("="*70)
    print("MULTI-LAYER COMBINER TEST")
    print("="*70)
    
    # Test 1: Adaptive weighting
    print("\n1. Adaptive Weight Calculation:")
    
    test_scenarios = [
        {
            'name': 'High Semantic Confidence',
            'confidences': {'phonetic': 0.3, 'morphological': 0.3, 'semantic': 0.9, 'context': 0.4}
        },
        {
            'name': 'High Context Confidence',
            'confidences': {'phonetic': 0.2, 'morphological': 0.2, 'semantic': 0.3, 'context': 0.85}
        },
        {
            'name': 'Balanced Confidence',
            'confidences': {'phonetic': 0.5, 'morphological': 0.5, 'semantic': 0.5, 'context': 0.5}
        }
    ]
    
    for scenario in test_scenarios:
        weights = combiner.adaptive_weight_calculation(scenario['confidences'])
        print(f"\n  {scenario['name']}:")
        for layer, weight in sorted(weights.items(), key=lambda x: x[1], reverse=True):
            print(f"    {layer:15s}: {weight:5.1%}")
    
    # Test 2: Signature combination
    print("\n\n2. Signature Combination:")
    
    # Simulate different layer signatures
    phonetic_sig = {'L': 0.6, 'J': 0.4, 'P': 0.3, 'W': 0.5}
    morphological_sig = {'L': 0.5, 'J': 0.5, 'P': 0.4, 'W': 0.6}
    semantic_sig = {'L': 0.8, 'J': 0.7, 'P': 0.5, 'W': 0.9}
    context_sig = {'L': 0.9, 'J': 0.8, 'P': 0.4, 'W': 0.85}
    
    confidences = {'phonetic': 0.3, 'morphological': 0.4, 'semantic': 0.8, 'context': 0.7}
    
    result = combiner.combine_signatures(
        phonetic_sig=phonetic_sig,
        morphological_sig=morphological_sig,
        semantic_sig=semantic_sig,
        context_sig=context_sig,
        layer_confidences=confidences
    )
    
    print("\n" + combiner.explain_combination(result))
    
    print("\n" + "="*70)
    print("Multi-Layer Combiner initialized successfully!")
    print("="*70)
