import sys
sys.path.append('experiments')

from enhanced_pattern_detector import EnhancedPatternDetector

d = EnhancedPatternDetector()

# Test unknown word
sig = d.calculate_field_signature_v2('xyz', None)
print("Unknown word 'xyz':")
print(f"  Weights: {sig['phase2_metadata']['layer_weights']}")
print(f"  Confidences: {sig['phase2_metadata']['layer_confidences']}")
print(f"  Overall confidence: {sig['confidence']:.2f}")

# Test random word
sig2 = d.calculate_field_signature_v2('Random word', None)
print("\n'Random word':")
print(f"  Weights: {sig2['phase2_metadata']['layer_weights']}")
print(f"  Confidences: {sig2['phase2_metadata']['layer_confidences']}")
print(f"  Overall confidence: {sig2['confidence']:.2f}")
