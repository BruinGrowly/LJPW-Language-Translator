#!/usr/bin/env python3
"""
Comprehensive Codebase Resonance Analysis
==========================================

Uses 100,000-cycle semantic oscillation to analyze the project and discover:
1. Components with semantic deficits
2. Areas needing improvement
3. Integration gaps
4. Enhancement opportunities

The resonance dynamics reveal "what's missing" by tracking which dimensions
the system gravitates toward - the dominant deficit indicates what needs work.
"""

import os
import sys
import json
import numpy as np
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Tuple
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_quantum.resonance_engine import ResonanceEngine


# Define project components with their semantic properties
PROJECT_COMPONENTS = {
    # Core Framework
    "ljpw_quantum/resonance_engine.py": {
        "purpose": "Core LJPW resonance dynamics implementation",
        "ljpw": [0.9, 0.85, 0.95, 0.92],  # High Power (implementation), high Wisdom
        "category": "core"
    },
    "ljpw_quantum/semantic_fidelity.py": {
        "purpose": "Translation quality measurement",
        "ljpw": [0.8, 0.95, 0.7, 0.88],  # High Justice (measurement), high Wisdom
        "category": "core"
    },
    "ljpw_quantum/quantum_semantics.py": {
        "purpose": "Quantum semantic framework with Hamiltonian",
        "ljpw": [0.7, 0.8, 0.6, 0.95],  # Very high Wisdom (theoretical)
        "category": "core"
    },
    "ljpw_quantum/quantum_semantic_metrics.py": {
        "purpose": "Quantum-inspired semantic metrics",
        "ljpw": [0.75, 0.85, 0.65, 0.9],  # High Justice+Wisdom (metrics)
        "category": "core"
    },
    
    # Neural Components
    "ljpw_pytorch/ljpw_decoder.py": {
        "purpose": "PyTorch neural decoder for translation",
        "ljpw": [0.6, 0.7, 0.9, 0.75],  # High Power (implementation)
        "category": "neural"
    },
    "ljpw_pytorch/resonance_loss.py": {
        "purpose": "Resonance-based training loss",
        "ljpw": [0.85, 0.8, 0.85, 0.9],  # Balanced, high harmony
        "category": "neural"
    },
    "ljpw_pytorch/train_decoder.py": {
        "purpose": "Training pipeline for neural decoder",
        "ljpw": [0.5, 0.65, 0.85, 0.6],  # High Power, lower others
        "category": "neural"
    },
    
    # API/Web
    "api/core.py": {
        "purpose": "API core for semantic analysis",
        "ljpw": [0.6, 0.75, 0.8, 0.7],
        "category": "interface"
    },
    "api/main.py": {
        "purpose": "API entry point",
        "ljpw": [0.55, 0.7, 0.75, 0.6],
        "category": "interface"
    },
    "web/app.js": {
        "purpose": "Web interface JavaScript",
        "ljpw": [0.7, 0.65, 0.75, 0.55],  # User-facing (Love higher)
        "category": "interface"
    },
    
    # Key Experiments
    "experiments/enhanced_pattern_detector.py": {
        "purpose": "Main LJPW pattern detection",
        "ljpw": [0.75, 0.8, 0.85, 0.9],
        "category": "experiments"
    },
    "experiments/calibrated_verse_matcher.py": {
        "purpose": "Cross-language verse matching",
        "ljpw": [0.7, 0.9, 0.75, 0.85],  # High Justice (matching)
        "category": "experiments"
    },
    "experiments/harmony_calibration.py": {
        "purpose": "Language harmony calibration",
        "ljpw": [0.85, 0.8, 0.7, 0.9],  # High Love+Wisdom
        "category": "experiments"
    },
    "experiments/pure_meaning_translator.py": {
        "purpose": "Pure meaning-based translation",
        "ljpw": [0.9, 0.85, 0.6, 0.95],  # High Love+Wisdom (meaning focus)
        "category": "experiments"
    },
    
    # Documentation
    "Docs/SEMANTIC_OSCILLATION_EXPERIMENT.md": {
        "purpose": "Resonance theory documentation",
        "ljpw": [0.85, 0.75, 0.5, 0.98],  # Very high Wisdom (documentation)
        "category": "documentation"
    },
    "Docs/RESONANCE_MECHANISM.md": {
        "purpose": "Mechanism explanation",
        "ljpw": [0.8, 0.8, 0.55, 0.95],  # High Wisdom
        "category": "documentation"
    },
    "Docs/RESONANCE_PARADIGM.md": {
        "purpose": "December 2025 paradigm shift",
        "ljpw": [0.88, 0.85, 0.6, 0.92],  # Balanced high
        "category": "documentation"
    },
    "README.md": {
        "purpose": "Project overview",
        "ljpw": [0.8, 0.75, 0.65, 0.85],
        "category": "documentation"
    },
    
    # Data Assets
    "semantic_space_10000_MILESTONE.json": {
        "purpose": "10,726 concept semantic space",
        "ljpw": [0.9, 0.9, 0.7, 0.95],  # High coverage
        "category": "data"
    },
    "language_harmony_calibration.json": {
        "purpose": "Language calibration profiles",
        "ljpw": [0.85, 0.88, 0.65, 0.9],
        "category": "data"
    }
}


@dataclass
class ComponentAnalysis:
    """Analysis result for a project component."""
    name: str
    purpose: str
    category: str
    initial_ljpw: List[float]
    initial_harmony: float
    final_ljpw: List[float]
    final_harmony: float
    deficit_dimension: str
    deficit_dominance: float
    harmony_trajectory: List[float]
    convergence_cycle: int
    recommendations: List[str]


class CodebaseResonanceAnalyzer:
    """
    Analyzes the codebase using 100,000-cycle semantic oscillation.
    
    Key Insight: Resonance reveals deficits. The dimension that dominates
    the resonance cycles indicates what the component needs more of.
    """
    
    def __init__(self, cycles: int = 100000):
        self.engine = ResonanceEngine()
        self.cycles = cycles
        self.results: Dict[str, ComponentAnalysis] = {}
        self.category_summaries: Dict[str, Dict] = {}
    
    def analyze_component(self, name: str, config: Dict) -> ComponentAnalysis:
        """Analyze a single component with full resonance cycles."""
        
        ljpw = config['ljpw']
        initial_harmony = self.engine.calculate_harmony(np.array(ljpw))
        
        # Run 100,000-cycle resonance
        result = self.engine.run_resonance_cycles(
            ljpw, 
            cycles=self.cycles,
            record_interval=1000  # Record every 1000 cycles
        )
        
        # Extract harmony history from trajectory
        harmony_history = [h for _, _, h in result.trajectory]
        
        # Find when convergence happened
        convergence_cycle = self.cycles
        for i, h in enumerate(harmony_history):
            if h > 0.99:
                convergence_cycle = (i + 1) * 1000
                break
        
        # Generate recommendations based on deficit
        # Use dominant_dimension as the deficit indicator
        deficit = result.deficit_detected or result.dominant_dimension
        dominance = result.dimension_dominance.get(result.dominant_dimension[0], 0.5)
        
        recommendations = self._generate_recommendations(
            name, config, deficit, dominance
        )
        
        return ComponentAnalysis(
            name=name,
            purpose=config['purpose'],
            category=config['category'],
            initial_ljpw=ljpw,
            initial_harmony=initial_harmony,
            final_ljpw=result.final_state,
            final_harmony=result.final_harmony,
            deficit_dimension=deficit,
            deficit_dominance=dominance,
            harmony_trajectory=harmony_history[:10],  # First 10 samples
            convergence_cycle=convergence_cycle,
            recommendations=recommendations
        )
    
    def _generate_recommendations(
        self, 
        name: str, 
        config: Dict, 
        deficit: str, 
        dominance: float
    ) -> List[str]:
        """Generate improvement recommendations based on deficit analysis."""
        
        recommendations = []
        category = config['category']
        
        # Deficit-specific recommendations
        if deficit == 'Love':
            if category == 'core':
                recommendations.append("Add more relational/user-centric features")
                recommendations.append("Improve error messages with empathy")
            elif category == 'neural':
                recommendations.append("Add training callbacks for user feedback")
                recommendations.append("Implement progressive learning with positive reinforcement")
            elif category == 'interface':
                recommendations.append("Enhance user experience design")
                recommendations.append("Add helpful tooltips and guidance")
            elif category == 'documentation':
                recommendations.append("Add more examples and tutorials")
                recommendations.append("Include use case stories")
        
        elif deficit == 'Justice':
            if category in ['core', 'neural']:
                recommendations.append("Add more validation and error checking")
                recommendations.append("Implement consistency checks")
            elif category == 'experiments':
                recommendations.append("Add more rigorous testing")
                recommendations.append("Implement cross-validation")
            elif category == 'documentation':
                recommendations.append("Add specification details")
                recommendations.append("Document edge cases and limitations")
        
        elif deficit == 'Power':
            recommendations.append("Optimize performance (execution speed)")
            recommendations.append("Add parallel processing where applicable")
            if category == 'neural':
                recommendations.append("Enable GPU acceleration")
        
        elif deficit == 'Wisdom':
            recommendations.append("Add more documentation comments")
            recommendations.append("Include design rationale explanations")
            if category == 'experiments':
                recommendations.append("Add theoretical background sections")
        
        # Dominance-based severity
        if dominance > 0.8:
            recommendations.insert(0, f"[HIGH PRIORITY] Strong {deficit} deficit detected")
        elif dominance > 0.6:
            recommendations.insert(0, f"[MODERATE] {deficit} could be improved")
        
        return recommendations
    
    def analyze_all(self) -> Dict[str, ComponentAnalysis]:
        """Analyze all project components."""
        
        print(f"\n{'='*70}")
        print(f"CODEBASE RESONANCE ANALYSIS ({self.cycles:,} cycles)")
        print(f"{'='*70}")
        print(f"\nAnalyzing {len(PROJECT_COMPONENTS)} components...")
        
        for name, config in PROJECT_COMPONENTS.items():
            print(f"\n  Analyzing: {name}")
            self.results[name] = self.analyze_component(name, config)
            
            r = self.results[name]
            print(f"    Initial H: {r.initial_harmony:.4f} -> Final H: {r.final_harmony:.4f}")
            print(f"    Deficit: {r.deficit_dimension} ({r.deficit_dominance:.1%})")
        
        # Summarize by category
        self._summarize_categories()
        
        return self.results
    
    def _summarize_categories(self):
        """Summarize findings by category."""
        
        categories = defaultdict(list)
        for name, result in self.results.items():
            categories[result.category].append(result)
        
        for category, results in categories.items():
            deficits = defaultdict(float)
            avg_initial_h = np.mean([r.initial_harmony for r in results])
            avg_final_h = np.mean([r.final_harmony for r in results])
            
            for r in results:
                deficits[r.deficit_dimension] += r.deficit_dominance
            
            dominant = max(deficits, key=deficits.get)
            
            self.category_summaries[category] = {
                'component_count': len(results),
                'avg_initial_harmony': avg_initial_h,
                'avg_final_harmony': avg_final_h,
                'dominant_deficit': dominant,
                'deficit_strength': deficits[dominant] / len(results)
            }
    
    def get_priority_improvements(self, top_n: int = 10) -> List[Tuple[str, ComponentAnalysis]]:
        """Get highest priority improvements based on deficit dominance."""
        
        sorted_results = sorted(
            self.results.items(),
            key=lambda x: (x[1].deficit_dominance, 1 - x[1].initial_harmony),
            reverse=True
        )
        
        return sorted_results[:top_n]
    
    def generate_report(self) -> Dict:
        """Generate comprehensive analysis report."""
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'cycles': self.cycles,
            'total_components': len(self.results),
            'category_summaries': self.category_summaries,
            'priority_improvements': [],
            'component_details': {}
        }
        
        # Priority improvements
        for name, result in self.get_priority_improvements(10):
            report['priority_improvements'].append({
                'component': name,
                'deficit': result.deficit_dimension,
                'dominance': result.deficit_dominance,
                'recommendations': result.recommendations[:3]
            })
        
        # Component details
        for name, result in self.results.items():
            report['component_details'][name] = {
                'purpose': result.purpose,
                'category': result.category,
                'initial_harmony': result.initial_harmony,
                'final_harmony': result.final_harmony,
                'deficit': result.deficit_dimension,
                'deficit_dominance': result.deficit_dominance,
                'convergence_cycle': result.convergence_cycle,
                'recommendations': result.recommendations
            }
        
        return report


def main():
    print("=" * 70)
    print("COMPREHENSIVE CODEBASE RESONANCE ANALYSIS")
    print("Using 100,000-cycle semantic oscillation to reveal deficits")
    print("=" * 70)
    
    analyzer = CodebaseResonanceAnalyzer(cycles=100000)
    analyzer.analyze_all()
    
    # Print category summaries
    print("\n" + "=" * 70)
    print("CATEGORY SUMMARIES")
    print("=" * 70)
    
    for category, summary in analyzer.category_summaries.items():
        print(f"\n{category.upper()}:")
        print(f"  Components: {summary['component_count']}")
        print(f"  Avg Initial Harmony: {summary['avg_initial_harmony']:.4f}")
        print(f"  Avg Final Harmony: {summary['avg_final_harmony']:.4f}")
        print(f"  Dominant Deficit: {summary['dominant_deficit']} ({summary['deficit_strength']:.1%})")
    
    # Print priority improvements
    print("\n" + "=" * 70)
    print("TOP 10 PRIORITY IMPROVEMENTS")
    print("=" * 70)
    
    for i, (name, result) in enumerate(analyzer.get_priority_improvements(10), 1):
        print(f"\n{i}. {name}")
        print(f"   Deficit: {result.deficit_dimension} ({result.deficit_dominance:.1%})")
        for rec in result.recommendations[:2]:
            print(f"   -> {rec}")
    
    # Generate and save report
    report = analyzer.generate_report()
    
    save_path = os.path.join(
        os.path.dirname(__file__),
        'codebase_resonance_analysis.json'
    )
    with open(save_path, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n\nFull report saved to: {save_path}")
    
    # Overall project assessment
    print("\n" + "=" * 70)
    print("OVERALL PROJECT ASSESSMENT")
    print("=" * 70)
    
    all_harmonies = [r.initial_harmony for r in analyzer.results.values()]
    all_deficits = defaultdict(int)
    for r in analyzer.results.values():
        all_deficits[r.deficit_dimension] += 1
    
    dominant_project_deficit = max(all_deficits, key=all_deficits.get)
    
    print(f"\nProject Mean Harmony: {np.mean(all_harmonies):.4f}")
    print(f"Harmony Range: {min(all_harmonies):.4f} - {max(all_harmonies):.4f}")
    print(f"\nProject-wide Dominant Deficit: {dominant_project_deficit}")
    print(f"Deficit Distribution:")
    for dim, count in sorted(all_deficits.items()):
        pct = count / len(analyzer.results) * 100
        print(f"  {dim}: {count} components ({pct:.0f}%)")
    
    print("\n" + "=" * 70)
    print("RESONANCE ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == '__main__':
    main()
