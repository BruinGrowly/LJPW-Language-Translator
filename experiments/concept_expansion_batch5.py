#!/usr/bin/env python3
"""
LJPW Semantic Space - Batch 5 Expansion
Target: 2,000+ concepts

New comprehensive domains:
- Mathematics & Numbers (150 concepts)
- Science & Physics (120 concepts)
- Living Organisms - Detailed (200 concepts)
- Human Body - Comprehensive (150 concepts)
- Arts & Aesthetics (100 concepts)
- Religion & Spirituality (100 concepts)
- Economy & Commerce (100 concepts)
- Law & Governance (100 concepts)
- Relationships & Society (150 concepts)

Plus expanding all existing domains significantly.
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List
import sys

sys.path.append(str(Path(__file__).parent))

from semantic_space_mapping import (
    SemanticSpaceMapper,
    ConceptualDomain
)


class Batch5Mapper(SemanticSpaceMapper):
    """Batch 5: Expanding to 2,000+ concepts."""

    def __init__(self):
        super().__init__()
        self.load_batch4_data()

    def load_batch4_data(self):
        """Load existing concepts from batch 4."""
        batch4_file = Path(__file__).parent / 'semantic_space_batch4.json'
        if batch4_file.exists():
            with open(batch4_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for domain_name, domain_data in data['domains'].items():
                domain = ConceptualDomain(
                    name=domain_name.replace('_', ' ').title(),
                    description=domain_data.get('description', '')
                )

                for concept_name, concept_data in domain_data['concepts'].items():
                    coords = np.array(concept_data['coordinates'])
                    domain.add_concept(
                        concept_name,
                        coords,
                        definition=concept_data.get('definition', '')
                    )

                self.domains[domain_name] = domain

    def create_mathematics_domain(self) -> ConceptualDomain:
        """150 concepts covering mathematics and numbers."""
        domain = ConceptualDomain(
            name="Mathematics & Numbers",
            description="Mathematical concepts, operations, and numbers"
        )

        # BASIC NUMBERS (0-20)
        for i in range(21):
            domain.add_concept(f'{i}',
                np.array([0.62 + i*0.005, 0.75, 0.58, 0.82 + i*0.002]),
                definition=f"Number {i}")

        # LARGER NUMBERS
        domain.add_concept('hundred',
            np.array([0.68, 0.78, 0.62, 0.88]),
            definition="Number 100")

        domain.add_concept('thousand',
            np.array([0.68, 0.80, 0.65, 0.90]),
            definition="Number 1,000")

        domain.add_concept('million',
            np.array([0.70, 0.82, 0.68, 0.92]),
            definition="Number 1,000,000")

        domain.add_concept('billion',
            np.array([0.72, 0.85, 0.72, 0.95]),
            definition="Number 1,000,000,000")

        # BASIC OPERATIONS
        domain.add_concept('addition',
            np.array([0.72, 0.78, 0.62, 0.88]),
            definition="Combining numbers")

        domain.add_concept('subtraction',
            np.array([0.62, 0.75, 0.58, 0.85]),
            definition="Taking away")

        domain.add_concept('multiplication',
            np.array([0.68, 0.80, 0.65, 0.88]),
            definition="Repeated addition")

        domain.add_concept('division',
            np.array([0.65, 0.78, 0.62, 0.88]),
            definition="Splitting into parts")

        domain.add_concept('equals',
            np.array([0.70, 0.82, 0.58, 0.90]),
            definition="Same value")

        domain.add_concept('sum',
            np.array([0.70, 0.78, 0.60, 0.85]),
            definition="Total of addition")

        domain.add_concept('difference',
            np.array([0.62, 0.75, 0.58, 0.82]),
            definition="Result of subtraction")

        domain.add_concept('product',
            np.array([0.68, 0.78, 0.62, 0.86]),
            definition="Result of multiplication")

        domain.add_concept('quotient',
            np.array([0.65, 0.76, 0.60, 0.85]),
            definition="Result of division")

        # NUMBER TYPES
        domain.add_concept('integer',
            np.array([0.65, 0.78, 0.60, 0.88]),
            definition="Whole number")

        domain.add_concept('fraction',
            np.array([0.66, 0.76, 0.58, 0.85]),
            definition="Part of whole")

        domain.add_concept('decimal',
            np.array([0.66, 0.77, 0.59, 0.86]),
            definition="Base-10 fraction")

        domain.add_concept('percentage',
            np.array([0.67, 0.76, 0.60, 0.85]),
            definition="Parts per hundred")

        domain.add_concept('ratio',
            np.array([0.66, 0.78, 0.60, 0.86]),
            definition="Relative proportion")

        domain.add_concept('prime number',
            np.array([0.68, 0.80, 0.62, 0.90]),
            definition="Divisible only by 1 and itself")

        domain.add_concept('even number',
            np.array([0.66, 0.76, 0.58, 0.84]),
            definition="Divisible by 2")

        domain.add_concept('odd number',
            np.array([0.64, 0.74, 0.60, 0.84]),
            definition="Not divisible by 2")

        domain.add_concept('negative number',
            np.array([0.48, 0.62, 0.65, 0.75]),
            definition="Less than zero")

        domain.add_concept('positive number',
            np.array([0.72, 0.78, 0.58, 0.86]),
            definition="Greater than zero")

        domain.add_concept('zero',
            np.array([0.60, 0.70, 0.60, 0.80]),
            definition="Nothing, null value")

        domain.add_concept('infinity',
            np.array([0.75, 0.85, 0.72, 0.95]),
            definition="Endless quantity")

        # GEOMETRY
        domain.add_concept('geometry',
            np.array([0.68, 0.82, 0.65, 0.90]),
            definition="Study of shapes")

        domain.add_concept('point',
            np.array([0.64, 0.78, 0.60, 0.86]),
            definition="Location with no dimension")

        domain.add_concept('line',
            np.array([0.66, 0.80, 0.62, 0.88]),
            definition="Infinite straight path")

        domain.add_concept('curve',
            np.array([0.68, 0.76, 0.58, 0.84]),
            definition="Bent line")

        domain.add_concept('angle',
            np.array([0.66, 0.78, 0.64, 0.86]),
            definition="Space between two lines")

        domain.add_concept('circle',
            np.array([0.70, 0.80, 0.60, 0.88]),
            definition="Round shape")

        domain.add_concept('square',
            np.array([0.68, 0.82, 0.65, 0.88]),
            definition="Four equal sides")

        domain.add_concept('rectangle',
            np.array([0.67, 0.80, 0.64, 0.87]),
            definition="Four right angles")

        domain.add_concept('triangle',
            np.array([0.66, 0.79, 0.63, 0.86]),
            definition="Three sides")

        domain.add_concept('sphere',
            np.array([0.70, 0.80, 0.62, 0.88]),
            definition="Round 3D shape")

        domain.add_concept('cube',
            np.array([0.68, 0.82, 0.66, 0.88]),
            definition="Six square faces")

        domain.add_concept('cylinder',
            np.array([0.67, 0.80, 0.64, 0.87]),
            definition="Tube shape")

        domain.add_concept('cone',
            np.array([0.66, 0.78, 0.63, 0.85]),
            definition="Pointed circular base")

        domain.add_concept('pyramid',
            np.array([0.67, 0.79, 0.68, 0.86]),
            definition="Pointed base")

        # MEASUREMENTS
        domain.add_concept('measurement',
            np.array([0.66, 0.78, 0.62, 0.88]),
            definition="Quantifying size/amount")

        domain.add_concept('length',
            np.array([0.66, 0.76, 0.60, 0.84]),
            definition="Distance measurement")

        domain.add_concept('width',
            np.array([0.66, 0.76, 0.60, 0.84]),
            definition="Side-to-side measurement")

        domain.add_concept('height',
            np.array([0.66, 0.76, 0.62, 0.84]),
            definition="Vertical measurement")

        domain.add_concept('depth',
            np.array([0.64, 0.74, 0.62, 0.82]),
            definition="How deep something is")

        domain.add_concept('area',
            np.array([0.67, 0.78, 0.62, 0.86]),
            definition="Surface size")

        domain.add_concept('volume',
            np.array([0.67, 0.78, 0.64, 0.86]),
            definition="3D space size")

        domain.add_concept('perimeter',
            np.array([0.66, 0.77, 0.61, 0.85]),
            definition="Outer boundary length")

        domain.add_concept('diameter',
            np.array([0.66, 0.78, 0.62, 0.86]),
            definition="Distance across circle")

        domain.add_concept('radius',
            np.array([0.66, 0.78, 0.61, 0.86]),
            definition="Distance from center")

        # ALGEBRA & FUNCTIONS
        domain.add_concept('algebra',
            np.array([0.66, 0.82, 0.64, 0.90]),
            definition="Mathematical symbols")

        domain.add_concept('equation',
            np.array([0.68, 0.80, 0.62, 0.88]),
            definition="Mathematical equality")

        domain.add_concept('variable',
            np.array([0.64, 0.76, 0.62, 0.84]),
            definition="Symbol for unknown")

        domain.add_concept('constant',
            np.array([0.68, 0.80, 0.62, 0.88]),
            definition="Fixed value")

        domain.add_concept('function',
            np.array([0.68, 0.82, 0.66, 0.90]),
            definition="Input-output relation")

        domain.add_concept('exponent',
            np.array([0.66, 0.78, 0.64, 0.86]),
            definition="Power of number")

        domain.add_concept('logarithm',
            np.array([0.64, 0.80, 0.66, 0.88]),
            definition="Inverse of exponent")

        domain.add_concept('polynomial',
            np.array([0.66, 0.80, 0.64, 0.88]),
            definition="Sum of terms")

        # CALCULUS
        domain.add_concept('calculus',
            np.array([0.66, 0.84, 0.68, 0.92]),
            definition="Study of change")

        domain.add_concept('derivative',
            np.array([0.66, 0.82, 0.66, 0.90]),
            definition="Rate of change")

        domain.add_concept('integral',
            np.array([0.66, 0.82, 0.66, 0.90]),
            definition="Accumulation")

        domain.add_concept('limit',
            np.array([0.64, 0.80, 0.64, 0.88]),
            definition="Approaching value")

        # STATISTICS & PROBABILITY
        domain.add_concept('statistics',
            np.array([0.66, 0.80, 0.64, 0.88]),
            definition="Data analysis")

        domain.add_concept('probability',
            np.array([0.64, 0.78, 0.62, 0.86]),
            definition="Likelihood measure")

        domain.add_concept('average',
            np.array([0.68, 0.76, 0.60, 0.84]),
            definition="Mean value")

        domain.add_concept('median',
            np.array([0.67, 0.76, 0.60, 0.84]),
            definition="Middle value")

        domain.add_concept('mode',
            np.array([0.66, 0.75, 0.60, 0.83]),
            definition="Most frequent value")

        domain.add_concept('range',
            np.array([0.65, 0.74, 0.60, 0.82]),
            definition="Spread of values")

        domain.add_concept('variance',
            np.array([0.64, 0.76, 0.62, 0.84]),
            definition="Measure of spread")

        domain.add_concept('distribution',
            np.array([0.66, 0.78, 0.62, 0.86]),
            definition="Pattern of data")

        # LOGIC & SET THEORY
        domain.add_concept('logic',
            np.array([0.64, 0.84, 0.60, 0.92]),
            definition="Principles of reasoning")

        domain.add_concept('set',
            np.array([0.66, 0.78, 0.62, 0.86]),
            definition="Collection of elements")

        domain.add_concept('subset',
            np.array([0.65, 0.77, 0.61, 0.85]),
            definition="Part of set")

        domain.add_concept('union',
            np.array([0.68, 0.78, 0.60, 0.86]),
            definition="Combined sets")

        domain.add_concept('intersection',
            np.array([0.66, 0.78, 0.62, 0.86]),
            definition="Common elements")

        domain.add_concept('complement',
            np.array([0.64, 0.76, 0.62, 0.84]),
            definition="Elements not in set")

        # MATHEMATICAL PROPERTIES
        domain.add_concept('symmetry',
            np.array([0.75, 0.82, 0.58, 0.90]),
            definition="Balanced proportion")

        domain.add_concept('asymmetry',
            np.array([0.55, 0.68, 0.62, 0.78]),
            definition="Lack of balance")

        domain.add_concept('pattern',
            np.array([0.70, 0.78, 0.60, 0.88]),
            definition="Repeated design")

        domain.add_concept('sequence',
            np.array([0.68, 0.78, 0.62, 0.86]),
            definition="Ordered list")

        domain.add_concept('series',
            np.array([0.68, 0.78, 0.62, 0.86]),
            definition="Sum of sequence")

        domain.add_concept('progression',
            np.array([0.70, 0.78, 0.62, 0.86]),
            definition="Sequential development")

        # MATHEMATICAL OPERATIONS
        domain.add_concept('square root',
            np.array([0.66, 0.78, 0.62, 0.86]),
            definition="Number multiplied by itself")

        domain.add_concept('factorial',
            np.array([0.66, 0.78, 0.64, 0.86]),
            definition="Product of integers")

        domain.add_concept('absolute value',
            np.array([0.68, 0.78, 0.60, 0.86]),
            definition="Distance from zero")

        domain.add_concept('reciprocal',
            np.array([0.66, 0.76, 0.60, 0.84]),
            definition="Multiplicative inverse")

        # MATHEMATICAL CONCEPTS
        domain.add_concept('proof',
            np.array([0.70, 0.84, 0.62, 0.92]),
            definition="Logical demonstration")

        domain.add_concept('theorem',
            np.array([0.70, 0.82, 0.62, 0.90]),
            definition="Proven statement")

        domain.add_concept('axiom',
            np.array([0.70, 0.82, 0.60, 0.90]),
            definition="Self-evident truth")

        domain.add_concept('conjecture',
            np.array([0.64, 0.74, 0.58, 0.82]),
            definition="Unproven proposition")

        domain.add_concept('lemma',
            np.array([0.68, 0.80, 0.62, 0.88]),
            definition="Preliminary theorem")

        domain.add_concept('corollary',
            np.array([0.68, 0.80, 0.62, 0.88]),
            definition="Consequence of theorem")

        # MATHEMATICAL RELATIONS
        domain.add_concept('greater than',
            np.array([0.68, 0.76, 0.64, 0.84]),
            definition="Larger value")

        domain.add_concept('less than',
            np.array([0.62, 0.74, 0.58, 0.82]),
            definition="Smaller value")

        domain.add_concept('maximum',
            np.array([0.70, 0.78, 0.66, 0.86]),
            definition="Largest value")

        domain.add_concept('minimum',
            np.array([0.62, 0.74, 0.58, 0.82]),
            definition="Smallest value")

        domain.add_concept('optimal',
            np.array([0.75, 0.82, 0.62, 0.90]),
            definition="Best possible")

        return domain

    def run_expansion(self):
        """Execute full batch 5 expansion."""
        print("="*80)
        print("LJPW SEMANTIC SPACE - BATCH 5 EXPANSION")
        print("="*80)
        print("\nExpanding from 815 concepts to 2,000+ concepts\n")

        existing_count = sum(
            len(domain.concepts)
            for domain in self.domains.values()
        )
        print(f"✓ Loaded {existing_count} existing concepts\n")

        print("Creating new domains...")

        print("  mathematics...")
        self.domains['mathematics'] = self.create_mathematics_domain()
        print(f"    ✓ {len(self.domains['mathematics'].concepts)} concepts")

        # Generate statistics
        total_concepts = sum(
            len(domain.concepts)
            for domain in self.domains.values()
        )

        print("\n" + "="*80)
        print("BATCH 5 IN PROGRESS")
        print("="*80)
        print(f"\nTotal concepts so far: {total_concepts}")
        print(f"Total domains: {len(self.domains)}")

        print("\nConcepts by domain:")
        for name, domain in sorted(self.domains.items()):
            count = len(domain.concepts)
            print(f"  • {domain.name:25s} {count:3d} concepts")

        # Save to JSON
        output = {
            'metadata': {
                'version': '5.0',
                'total_concepts': total_concepts,
                'total_domains': len(self.domains),
                'target': 100000,
                'progress_pct': round(100 * total_concepts / 100000, 2)
            },
            'domains': {}
        }

        for domain_name, domain in self.domains.items():
            output['domains'][domain_name] = {
                'name': domain.name,
                'description': domain.description,
                'concept_count': len(domain.concepts),
                'concepts': {}
            }

            for concept_name, concept in domain.concepts.items():
                coords = concept['coordinates']
                if isinstance(coords, np.ndarray):
                    coords = coords.tolist()
                output['domains'][domain_name]['concepts'][concept_name] = {
                    'coordinates': coords,
                    'definition': concept.get('definition', ''),
                    'domain': domain.name
                }

        output_file = Path(__file__).parent / 'semantic_space_batch5.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Saved semantic space to: {output_file}")
        print(f"  Total concepts: {total_concepts}")
        print(f"  Total domains: {len(self.domains)}")

        print("\n" + "="*80)
        print(f"🎉 {total_concepts} CONCEPTS MAPPED 🎉")
        print("="*80)
        print(f"Progress: [{total_concepts} / 100,000] = {100*total_concepts/100000:.2f}%")


if __name__ == '__main__':
    mapper = Batch5Mapper()
    mapper.run_expansion()
