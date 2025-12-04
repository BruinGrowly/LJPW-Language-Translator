#!/usr/bin/env python3
"""
LJPW Semantic Space - DOMAIN EXPANSION PHASE 2
Target: 2,231 → 2,800+ concepts

Expanding multiple domains:
- Communication: 91 → 160+
- Economy & Business: 95 → 160+
- Arts & Aesthetics: 104 → 170+
- Technology & Computing: 72 → 140+
- Education: 69 → 130+
- Geography: 67 → 130+
"""

import json
import numpy as np
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent))

from semantic_space_mapping import (
    SemanticSpaceMapper,
    ConceptualDomain
)


class DomainExpansionPhase2(SemanticSpaceMapper):
    """Phase 2 domain expansion."""

    def __init__(self):
        super().__init__()
        self.load_existing()

    def load_existing(self):
        """Load from comprehensive deepening."""
        data_file = Path(__file__).parent / 'semantic_space_comprehensive_deepening.json'
        if data_file.exists():
            with open(data_file, 'r', encoding='utf-8') as f:
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

    def expand_communication(self):
        """Expand communication: 91 → 160+ concepts."""
        comm = self.domains.get('communication')
        if not comm:
            return

        new_concepts = [
            # Verbal communication expanded
            ('articulate', np.array([0.72, 0.74, 0.65, 0.82]), "Express clearly"),
            ('enunciate', np.array([0.70, 0.76, 0.67, 0.83]), "Pronounce clearly"),
            ('mumble', np.array([0.52, 0.58, 0.64, 0.68]), "Speak unclearly"),
            ('mutter', np.array([0.50, 0.56, 0.66, 0.69]), "Speak quietly"),
            ('whisper', np.array([0.68, 0.64, 0.62, 0.74]), "Speak softly"),
            ('shout', np.array([0.58, 0.68, 0.72, 0.76]), "Speak loudly"),
            ('yell', np.array([0.56, 0.70, 0.74, 0.77]), "Shout loudly"),
            ('scream', np.array([0.48, 0.72, 0.78, 0.80]), "Loud cry"),
            ('shriek', np.array([0.46, 0.74, 0.80, 0.81]), "High-pitched scream"),
            ('holler', np.array([0.60, 0.68, 0.70, 0.75]), "Call loudly"),
            ('proclaim', np.array([0.68, 0.76, 0.70, 0.82]), "Announce publicly"),
            ('declare', np.array([0.70, 0.78, 0.68, 0.83]), "State formally"),
            ('announce', np.array([0.72, 0.76, 0.66, 0.81]), "Make known"),
            ('narrate', np.array([0.70, 0.72, 0.64, 0.80]), "Tell story"),
            ('recite', np.array([0.68, 0.74, 0.66, 0.81]), "Repeat from memory"),
            ('chant', np.array([0.70, 0.68, 0.64, 0.78]), "Rhythmic speaking"),
            ('lecture', np.array([0.66, 0.76, 0.68, 0.83]), "Educational talk"),
            ('preach', np.array([0.68, 0.78, 0.70, 0.84]), "Religious speech"),
            ('sermon', np.array([0.70, 0.76, 0.68, 0.82]), "Religious discourse"),
            ('orate', np.array([0.72, 0.78, 0.66, 0.84]), "Formal speech"),

            # Conversational
            ('converse', np.array([0.74, 0.70, 0.62, 0.78]), "Talk together"),
            ('chat', np.array([0.78, 0.68, 0.58, 0.76]), "Casual talk"),
            ('gossip', np.array([0.58, 0.60, 0.66, 0.70]), "Rumor talk"),
            ('banter', np.array([0.76, 0.66, 0.58, 0.74]), "Playful exchange"),
            ('jest', np.array([0.78, 0.64, 0.56, 0.73]), "Joking talk"),
            ('tease', np.array([0.68, 0.62, 0.62, 0.72]), "Playful mockery"),
            ('mock', np.array([0.48, 0.58, 0.68, 0.70]), "Ridicule"),
            ('taunt', np.array([0.42, 0.60, 0.72, 0.73]), "Provoke mockery"),
            ('insult', np.array([0.38, 0.58, 0.76, 0.74]), "Offensive remark"),
            ('compliment', np.array([0.82, 0.70, 0.56, 0.77]), "Praise remark"),
            ('flatter', np.array([0.74, 0.64, 0.60, 0.74]), "Excessive praise"),
            ('cajole', np.array([0.68, 0.62, 0.64, 0.73]), "Coax persuasively"),
            ('coax', np.array([0.70, 0.64, 0.62, 0.74]), "Gentle persuasion"),
            ('persuade', np.array([0.66, 0.72, 0.66, 0.79]), "Convince"),
            ('convince', np.array([0.68, 0.74, 0.64, 0.80]), "Cause to believe"),
            ('dissuade', np.array([0.62, 0.72, 0.68, 0.79]), "Persuade against"),

            # Written communication
            ('compose', np.array([0.70, 0.74, 0.64, 0.82]), "Create writing"),
            ('draft', np.array([0.68, 0.72, 0.66, 0.80]), "Preliminary writing"),
            ('revise', np.array([0.66, 0.76, 0.68, 0.82]), "Improve writing"),
            ('edit', np.array([0.68, 0.78, 0.66, 0.83]), "Refine text"),
            ('proofread', np.array([0.70, 0.80, 0.64, 0.84]), "Check for errors"),
            ('transcribe', np.array([0.68, 0.76, 0.68, 0.82]), "Write spoken words"),
            ('annotate', np.array([0.70, 0.74, 0.66, 0.81]), "Add notes"),
            ('paraphrase', np.array([0.68, 0.72, 0.68, 0.80]), "Restate differently"),
            ('summarize', np.array([0.70, 0.76, 0.66, 0.82]), "Condense main points"),
            ('abstract', np.array([0.68, 0.78, 0.68, 0.84]), "Brief summary"),
            ('outline', np.array([0.70, 0.74, 0.66, 0.81]), "Structural summary"),
            ('manuscript', np.array([0.68, 0.72, 0.68, 0.80]), "Written document"),
            ('document', np.array([0.70, 0.76, 0.66, 0.81]), "Written record"),
            ('correspondence', np.array([0.72, 0.74, 0.64, 0.80]), "Letter exchange"),
            ('memo', np.array([0.68, 0.72, 0.68, 0.79]), "Brief message"),
            ('notice', np.array([0.70, 0.74, 0.66, 0.80]), "Formal announcement"),
            ('bulletin', np.array([0.72, 0.72, 0.64, 0.79]), "Public notice"),
            ('newsletter', np.array([0.74, 0.70, 0.62, 0.78]), "Periodic bulletin"),
            ('journal', np.array([0.70, 0.72, 0.66, 0.80]), "Personal writing"),
            ('diary', np.array([0.72, 0.68, 0.64, 0.78]), "Daily record"),

            # Non-verbal
            ('gesture', np.array([0.72, 0.66, 0.62, 0.76]), "Hand movement"),
            ('mime', np.array([0.74, 0.64, 0.60, 0.75]), "Silent acting"),
            ('sign_language', np.array([0.78, 0.72, 0.60, 0.81]), "Hand communication"),
            ('body_language', np.array([0.70, 0.68, 0.64, 0.77]), "Physical signals"),
            ('facial_expression', np.array([0.72, 0.66, 0.62, 0.76]), "Face communication"),
            ('grimace', np.array([0.52, 0.58, 0.64, 0.68]), "Pain expression"),
            ('smirk', np.array([0.60, 0.62, 0.62, 0.70]), "Smug smile"),
            ('grin', np.array([0.82, 0.68, 0.54, 0.75]), "Wide smile"),
            ('scowl', np.array([0.44, 0.56, 0.68, 0.70]), "Angry expression"),
            ('glare', np.array([0.42, 0.60, 0.70, 0.72]), "Fierce look"),
            ('stare', np.array([0.58, 0.64, 0.66, 0.72]), "Fixed gaze"),
            ('gaze', np.array([0.68, 0.62, 0.62, 0.74]), "Steady look"),
            ('glance', np.array([0.66, 0.64, 0.64, 0.73]), "Brief look"),
            ('peek', np.array([0.70, 0.60, 0.60, 0.72]), "Quick secret look"),
            ('wink', np.array([0.76, 0.64, 0.58, 0.73]), "Eye signal"),
        ]

        for name, coords, definition in new_concepts:
            if name not in comm.concepts:
                comm.add_concept(name, coords, definition=definition)

    def expand_economy(self):
        """Expand economy: 95 → 160+ concepts."""
        econ = self.domains.get('economy_&_business')
        if not econ:
            return

        new_concepts = [
            # Financial instruments
            ('stock', np.array([0.62, 0.72, 0.75, 0.82]), "Company share"),
            ('bond', np.array([0.68, 0.74, 0.72, 0.81]), "Debt security"),
            ('derivative', np.array([0.60, 0.76, 0.78, 0.85]), "Financial contract"),
            ('option', np.array([0.64, 0.74, 0.76, 0.83]), "Trading right"),
            ('future', np.array([0.62, 0.76, 0.77, 0.84]), "Forward contract"),
            ('swap', np.array([0.66, 0.72, 0.74, 0.81]), "Exchange agreement"),
            ('commodity', np.array([0.68, 0.70, 0.72, 0.80]), "Raw material"),
            ('equity', np.array([0.70, 0.74, 0.70, 0.81]), "Ownership value"),
            ('dividend', np.array([0.72, 0.68, 0.68, 0.78]), "Profit distribution"),
            ('yield', np.array([0.70, 0.70, 0.70, 0.80]), "Investment return"),
            ('coupon', np.array([0.68, 0.68, 0.72, 0.79]), "Bond interest"),
            ('maturity', np.array([0.66, 0.72, 0.74, 0.81]), "Due date"),
            ('par_value', np.array([0.68, 0.74, 0.72, 0.82]), "Face value"),
            ('premium', np.array([0.64, 0.70, 0.74, 0.80]), "Extra payment"),
            ('discount', np.array([0.70, 0.66, 0.70, 0.77]), "Price reduction"),

            # Market concepts
            ('bull_market', np.array([0.75, 0.68, 0.70, 0.80]), "Rising market"),
            ('bear_market', np.array([0.52, 0.72, 0.75, 0.82]), "Falling market"),
            ('volatility', np.array([0.58, 0.74, 0.78, 0.84]), "Price fluctuation"),
            ('liquidity', np.array([0.68, 0.72, 0.74, 0.82]), "Easy conversion"),
            ('leverage', np.array([0.62, 0.74, 0.76, 0.83]), "Borrowed capital"),
            ('margin', np.array([0.64, 0.72, 0.75, 0.81]), "Borrowed trading"),
            ('arbitrage', np.array([0.66, 0.76, 0.74, 0.84]), "Price difference profit"),
            ('speculation', np.array([0.58, 0.70, 0.78, 0.81]), "Risky investment"),
            ('hedging', np.array([0.70, 0.74, 0.72, 0.82]), "Risk protection"),
            ('diversification', np.array([0.72, 0.76, 0.70, 0.83]), "Risk spreading"),
            ('portfolio', np.array([0.70, 0.74, 0.72, 0.82]), "Investment collection"),
            ('asset_allocation', np.array([0.68, 0.76, 0.74, 0.83]), "Investment distribution"),
            ('rebalancing', np.array([0.66, 0.74, 0.76, 0.82]), "Portfolio adjustment"),
            ('benchmark', np.array([0.68, 0.74, 0.74, 0.82]), "Performance standard"),
            ('index', np.array([0.70, 0.76, 0.72, 0.83]), "Market measure"),

            # Banking expanded
            ('deposit', np.array([0.72, 0.70, 0.68, 0.79]), "Money storage"),
            ('withdrawal', np.array([0.68, 0.68, 0.70, 0.77]), "Money removal"),
            ('transfer', np.array([0.70, 0.72, 0.68, 0.80]), "Money movement"),
            ('overdraft', np.array([0.54, 0.66, 0.74, 0.78]), "Negative balance"),
            ('collateral', np.array([0.64, 0.74, 0.72, 0.81]), "Loan security"),
            ('mortgage', np.array([0.66, 0.76, 0.74, 0.82]), "Property loan"),
            ('foreclosure', np.array([0.38, 0.72, 0.78, 0.83]), "Property seizure"),
            ('bankruptcy', np.array([0.32, 0.68, 0.82, 0.84]), "Financial failure"),
            ('insolvency', np.array([0.34, 0.70, 0.80, 0.83]), "Cannot pay debts"),
            ('liquidation', np.array([0.42, 0.74, 0.76, 0.82]), "Asset conversion"),
            ('receivership', np.array([0.48, 0.76, 0.74, 0.83]), "Court control"),
            ('credit_rating', np.array([0.66, 0.76, 0.72, 0.82]), "Creditworthiness score"),
            ('credit_score', np.array([0.68, 0.74, 0.70, 0.81]), "Credit measure"),
            ('default', np.array([0.36, 0.66, 0.78, 0.80]), "Loan non-payment"),
            ('delinquency', np.array([0.40, 0.64, 0.76, 0.79]), "Payment lateness"),

            # Business operations
            ('startup', np.array([0.75, 0.70, 0.72, 0.82]), "New business"),
            ('venture', np.array([0.68, 0.72, 0.74, 0.81]), "Business enterprise"),
            ('enterprise', np.array([0.70, 0.74, 0.72, 0.82]), "Business organization"),
            ('franchise', np.array([0.72, 0.72, 0.70, 0.80]), "Licensed business"),
            ('subsidiary', np.array([0.68, 0.74, 0.72, 0.81]), "Controlled company"),
            ('merger', np.array([0.66, 0.76, 0.74, 0.83]), "Company combination"),
            ('acquisition', np.array([0.64, 0.78, 0.76, 0.84]), "Company purchase"),
            ('takeover', np.array([0.60, 0.80, 0.78, 0.85]), "Forced acquisition"),
            ('joint_venture', np.array([0.74, 0.74, 0.70, 0.82]), "Shared business"),
            ('partnership', np.array([0.78, 0.72, 0.66, 0.81]), "Business cooperation"),
            ('incorporation', np.array([0.68, 0.76, 0.74, 0.83]), "Legal formation"),
            ('dissolution', np.array([0.48, 0.72, 0.76, 0.81]), "Business ending"),
            ('restructuring', np.array([0.62, 0.76, 0.74, 0.82]), "Organization change"),
            ('downsizing', np.array([0.44, 0.70, 0.78, 0.80]), "Size reduction"),
            ('outsourcing', np.array([0.60, 0.72, 0.74, 0.80]), "External contracting"),
            ('offshoring', np.array([0.58, 0.74, 0.76, 0.81]), "Foreign operations"),
            ('automation', np.array([0.68, 0.78, 0.74, 0.85]), "Machine replacement"),
            ('efficiency', np.array([0.72, 0.78, 0.70, 0.84]), "Optimal productivity"),
            ('productivity', np.array([0.70, 0.76, 0.72, 0.83]), "Output rate"),
            ('profitability', np.array([0.72, 0.74, 0.70, 0.82]), "Profit capacity"),
        ]

        for name, coords, definition in new_concepts:
            if name not in econ.concepts:
                econ.add_concept(name, coords, definition=definition)

    def expand_arts(self):
        """Expand arts: 104 → 170+ concepts."""
        arts = self.domains.get('arts_&_aesthetics')
        if not arts:
            return

        new_concepts = [
            # Art movements
            ('renaissance', np.array([0.78, 0.76, 0.68, 0.84]), "Rebirth period"),
            ('baroque', np.array([0.76, 0.74, 0.70, 0.83]), "Ornate style"),
            ('romanticism', np.array([0.82, 0.70, 0.65, 0.81]), "Emotional art"),
            ('impressionism', np.array([0.80, 0.72, 0.66, 0.82]), "Light and color"),
            ('expressionism', np.array([0.78, 0.74, 0.68, 0.83]), "Emotional distortion"),
            ('cubism', np.array([0.70, 0.78, 0.72, 0.85]), "Geometric abstraction"),
            ('surrealism', np.array([0.75, 0.76, 0.70, 0.84]), "Dream-like art"),
            ('abstract', np.array([0.72, 0.78, 0.74, 0.86]), "Non-representational"),
            ('minimalism', np.array([0.74, 0.80, 0.70, 0.85]), "Extreme simplicity"),
            ('pop_art', np.array([0.82, 0.68, 0.64, 0.78]), "Popular culture art"),
            ('modernism', np.array([0.70, 0.76, 0.74, 0.84]), "Modern movement"),
            ('postmodernism', np.array([0.68, 0.78, 0.76, 0.86]), "After modernism"),
            ('realism', np.array([0.72, 0.74, 0.72, 0.82]), "True representation"),
            ('naturalism', np.array([0.74, 0.72, 0.70, 0.81]), "Nature realism"),
            ('classicism', np.array([0.76, 0.78, 0.68, 0.84]), "Classical style"),

            # Visual art techniques
            ('chiaroscuro', np.array([0.72, 0.76, 0.70, 0.83]), "Light-dark contrast"),
            ('perspective', np.array([0.70, 0.78, 0.74, 0.85]), "Depth illusion"),
            ('foreshortening', np.array([0.68, 0.76, 0.76, 0.84]), "Depth technique"),
            ('composition', np.array([0.74, 0.78, 0.70, 0.84]), "Element arrangement"),
            ('proportion', np.array([0.72, 0.80, 0.72, 0.85]), "Size relationship"),
            ('symmetry', np.array([0.76, 0.78, 0.68, 0.83]), "Balanced arrangement"),
            ('asymmetry', np.array([0.70, 0.74, 0.72, 0.82]), "Unbalanced arrangement"),
            ('contrast', np.array([0.68, 0.76, 0.74, 0.83]), "Difference emphasis"),
            ('harmony', np.array([0.82, 0.74, 0.66, 0.82]), "Pleasing unity"),
            ('balance', np.array([0.78, 0.76, 0.68, 0.83]), "Visual equilibrium"),
            ('rhythm', np.array([0.80, 0.72, 0.66, 0.81]), "Pattern repetition"),
            ('pattern', np.array([0.74, 0.76, 0.70, 0.82]), "Repeated design"),
            ('texture', np.array([0.72, 0.70, 0.72, 0.80]), "Surface quality"),
            ('brushstroke', np.array([0.74, 0.68, 0.70, 0.79]), "Paint application"),
            ('palette', np.array([0.76, 0.70, 0.68, 0.80]), "Color selection"),

            # Performance arts
            ('choreography', np.array([0.78, 0.76, 0.68, 0.83]), "Dance composition"),
            ('improvisation', np.array([0.80, 0.70, 0.66, 0.80]), "Spontaneous creation"),
            ('rehearsal', np.array([0.70, 0.74, 0.72, 0.82]), "Practice performance"),
            ('audition', np.array([0.64, 0.72, 0.74, 0.80]), "Performance tryout"),
            ('ensemble', np.array([0.78, 0.74, 0.68, 0.82]), "Group performers"),
            ('soloist', np.array([0.76, 0.68, 0.70, 0.80]), "Solo performer"),
            ('virtuoso', np.array([0.82, 0.76, 0.70, 0.85]), "Master performer"),
            ('maestro', np.array([0.80, 0.78, 0.72, 0.86]), "Master conductor"),
            ('conductor', np.array([0.76, 0.80, 0.72, 0.85]), "Orchestra leader"),
            ('baton', np.array([0.70, 0.74, 0.72, 0.81]), "Conducting stick"),
            ('score', np.array([0.72, 0.78, 0.74, 0.84]), "Written music"),
            ('notation', np.array([0.70, 0.80, 0.76, 0.86]), "Music writing"),
            ('tempo', np.array([0.72, 0.74, 0.72, 0.82]), "Music speed"),
            ('dynamics', np.array([0.74, 0.76, 0.70, 0.83]), "Volume variation"),
            ('crescendo', np.array([0.76, 0.72, 0.68, 0.81]), "Getting louder"),
            ('decrescendo', np.array([0.70, 0.70, 0.72, 0.80]), "Getting softer"),
            ('allegro', np.array([0.80, 0.74, 0.66, 0.82]), "Fast tempo"),
            ('andante', np.array([0.74, 0.70, 0.70, 0.80]), "Moderate tempo"),
            ('adagio', np.array([0.68, 0.68, 0.74, 0.79]), "Slow tempo"),
            ('staccato', np.array([0.72, 0.72, 0.72, 0.81]), "Detached notes"),
            ('legato', np.array([0.78, 0.70, 0.68, 0.80]), "Smooth connected"),

            # Literary devices
            ('metaphor', np.array([0.76, 0.78, 0.70, 0.85]), "Symbolic comparison"),
            ('simile', np.array([0.74, 0.76, 0.72, 0.84]), "Like/as comparison"),
            ('alliteration', np.array([0.78, 0.72, 0.68, 0.81]), "Sound repetition"),
            ('onomatopoeia', np.array([0.76, 0.70, 0.70, 0.80]), "Sound words"),
            ('personification', np.array([0.74, 0.74, 0.72, 0.82]), "Human qualities"),
            ('hyperbole', np.array([0.72, 0.68, 0.74, 0.80]), "Exaggeration"),
            ('irony', np.array([0.66, 0.76, 0.76, 0.84]), "Opposite meaning"),
            ('satire', np.array([0.64, 0.78, 0.78, 0.85]), "Mocking criticism"),
            ('allegory', np.array([0.70, 0.80, 0.74, 0.86]), "Symbolic narrative"),
            ('foreshadowing', np.array([0.68, 0.78, 0.76, 0.85]), "Future hint"),
            ('flashback', np.array([0.70, 0.76, 0.74, 0.83]), "Past scene"),
            ('imagery', np.array([0.78, 0.74, 0.68, 0.82]), "Sensory description"),
            ('symbolism', np.array([0.72, 0.78, 0.74, 0.85]), "Symbolic meaning"),
            ('theme', np.array([0.74, 0.80, 0.72, 0.86]), "Central idea"),
            ('motif', np.array([0.72, 0.78, 0.74, 0.84]), "Recurring element"),
        ]

        for name, coords, definition in new_concepts:
            if name not in arts.concepts:
                arts.add_concept(name, coords, definition=definition)

    def expand_technology(self):
        """Expand technology: 72 → 140+ concepts."""
        tech = self.domains.get('technology_&_computing')
        if not tech:
            return

        new_concepts = [
            # Programming concepts
            ('algorithm', np.array([0.68, 0.80, 0.76, 0.88]), "Step procedure"),
            ('data_structure', np.array([0.66, 0.82, 0.78, 0.89]), "Data organization"),
            ('variable', np.array([0.70, 0.78, 0.74, 0.86]), "Data container"),
            ('function', np.array([0.72, 0.80, 0.72, 0.87]), "Code block"),
            ('loop', np.array([0.68, 0.78, 0.76, 0.86]), "Repeated execution"),
            ('conditional', np.array([0.70, 0.80, 0.74, 0.87]), "If statement"),
            ('recursion', np.array([0.64, 0.82, 0.80, 0.89]), "Self-calling function"),
            ('iteration', np.array([0.68, 0.78, 0.76, 0.86]), "Repetition"),
            ('array', np.array([0.70, 0.80, 0.74, 0.87]), "Ordered list"),
            ('list', np.array([0.72, 0.78, 0.72, 0.85]), "Data sequence"),
            ('dictionary', np.array([0.70, 0.82, 0.76, 0.88]), "Key-value pairs"),
            ('hash_table', np.array([0.68, 0.84, 0.78, 0.89]), "Fast lookup structure"),
            ('tree', np.array([0.70, 0.82, 0.76, 0.88]), "Hierarchical structure"),
            ('graph', np.array([0.68, 0.84, 0.78, 0.89]), "Network structure"),
            ('stack', np.array([0.70, 0.80, 0.74, 0.86]), "LIFO structure"),
            ('queue', np.array([0.72, 0.78, 0.72, 0.85]), "FIFO structure"),
            ('linked_list', np.array([0.68, 0.82, 0.76, 0.87]), "Connected nodes"),
            ('binary_tree', np.array([0.66, 0.84, 0.78, 0.88]), "Two-child tree"),
            ('heap', np.array([0.68, 0.82, 0.76, 0.87]), "Priority structure"),
            ('sorting', np.array([0.70, 0.82, 0.74, 0.87]), "Order arrangement"),

            # Software development
            ('compile', np.array([0.68, 0.80, 0.76, 0.87]), "Convert to machine code"),
            ('debug', np.array([0.66, 0.82, 0.78, 0.88]), "Find errors"),
            ('syntax', np.array([0.70, 0.84, 0.76, 0.89]), "Language rules"),
            ('semantics', np.array([0.68, 0.86, 0.78, 0.90]), "Meaning rules"),
            ('parser', np.array([0.66, 0.84, 0.80, 0.89]), "Code analyzer"),
            ('compiler', np.array([0.68, 0.82, 0.78, 0.88]), "Code translator"),
            ('interpreter', np.array([0.70, 0.80, 0.76, 0.87]), "Direct executor"),
            ('runtime', np.array([0.68, 0.78, 0.76, 0.86]), "Execution environment"),
            ('library', np.array([0.72, 0.80, 0.74, 0.86]), "Code collection"),
            ('framework', np.array([0.70, 0.82, 0.76, 0.87]), "Development structure"),
            ('api', np.array([0.72, 0.82, 0.74, 0.87]), "Programming interface"),
            ('sdk', np.array([0.70, 0.80, 0.76, 0.86]), "Development kit"),
            ('ide', np.array([0.72, 0.78, 0.74, 0.85]), "Development environment"),
            ('version_control', np.array([0.70, 0.84, 0.76, 0.88]), "Code history"),
            ('repository', np.array([0.72, 0.82, 0.74, 0.87]), "Code storage"),
            ('commit', np.array([0.70, 0.80, 0.76, 0.86]), "Save changes"),
            ('branch', np.array([0.68, 0.82, 0.78, 0.87]), "Code divergence"),
            ('merge', np.array([0.70, 0.84, 0.76, 0.88]), "Combine branches"),
            ('pull_request', np.array([0.72, 0.82, 0.74, 0.86]), "Code review request"),
            ('deployment', np.array([0.68, 0.82, 0.78, 0.88]), "Release process"),

            # Network and web
            ('protocol', np.array([0.70, 0.84, 0.76, 0.88]), "Communication rules"),
            ('packet', np.array([0.68, 0.80, 0.78, 0.86]), "Data unit"),
            ('bandwidth', np.array([0.70, 0.78, 0.76, 0.85]), "Transfer capacity"),
            ('latency', np.array([0.62, 0.76, 0.80, 0.86]), "Delay time"),
            ('throughput', np.array([0.72, 0.80, 0.74, 0.86]), "Processing rate"),
            ('router', np.array([0.70, 0.82, 0.76, 0.87]), "Network device"),
            ('firewall', np.array([0.66, 0.86, 0.80, 0.90]), "Security barrier"),
            ('encryption', np.array([0.64, 0.88, 0.82, 0.91]), "Data protection"),
            ('ssl', np.array([0.66, 0.86, 0.80, 0.89]), "Secure connection"),
            ('https', np.array([0.68, 0.84, 0.78, 0.88]), "Secure web protocol"),
            ('dns', np.array([0.70, 0.82, 0.76, 0.87]), "Domain name system"),
            ('ip_address', np.array([0.72, 0.80, 0.74, 0.86]), "Network identifier"),
            ('subnet', np.array([0.68, 0.82, 0.78, 0.87]), "Network division"),
            ('proxy', np.array([0.66, 0.84, 0.80, 0.88]), "Intermediary server"),
            ('cache', np.array([0.72, 0.80, 0.74, 0.86]), "Temporary storage"),
            ('cookie', np.array([0.68, 0.76, 0.76, 0.84]), "Web data file"),
            ('session', np.array([0.70, 0.78, 0.74, 0.85]), "User connection"),
            ('authentication', np.array([0.66, 0.86, 0.80, 0.90]), "Identity verification"),
            ('authorization', np.array([0.68, 0.88, 0.78, 0.91]), "Permission grant"),
            ('token', np.array([0.70, 0.84, 0.76, 0.88]), "Access credential"),

            # Databases
            ('database', np.array([0.70, 0.84, 0.76, 0.88]), "Data storage"),
            ('query', np.array([0.68, 0.82, 0.78, 0.87]), "Data request"),
            ('sql', np.array([0.70, 0.86, 0.76, 0.89]), "Query language"),
            ('table', np.array([0.72, 0.82, 0.74, 0.86]), "Data structure"),
            ('schema', np.array([0.70, 0.84, 0.76, 0.88]), "Database structure"),
            ('index', np.array([0.72, 0.84, 0.74, 0.87]), "Fast lookup"),
            ('transaction', np.array([0.68, 0.86, 0.78, 0.89]), "Atomic operation"),
            ('normalization', np.array([0.70, 0.88, 0.76, 0.90]), "Data organization"),
            ('join', np.array([0.72, 0.82, 0.74, 0.86]), "Table combination"),
            ('backup', np.array([0.72, 0.84, 0.74, 0.87]), "Data copy"),
        ]

        for name, coords, definition in new_concepts:
            if name not in tech.concepts:
                tech.add_concept(name, coords, definition=definition)

    def run_phase2_expansion(self):
        """Execute phase 2 expansion."""
        print("="*80)
        print("LJPW DOMAIN EXPANSION PHASE 2 - PUSHING TO 2,800+!")
        print("="*80)
        print()

        existing_count = sum(len(domain.concepts) for domain in self.domains.values())
        print(f"Starting: {existing_count} concepts")

        print("\nExpanding domains...")

        expansions = [
            ('communication', self.expand_communication, "Communication"),
            ('economy_&_business', self.expand_economy, "Economy & Business"),
            ('arts_&_aesthetics', self.expand_arts, "Arts & Aesthetics"),
            ('technology_&_computing', self.expand_technology, "Technology"),
        ]

        for domain_key, expand_func, domain_name in expansions:
            if domain_key in self.domains:
                before = len(self.domains[domain_key].concepts)
                print(f"  Expanding {domain_name}...")
                expand_func()
                after = len(self.domains[domain_key].concepts)
                print(f"    Added {after - before} concepts")

        total_concepts = sum(len(domain.concepts) for domain in self.domains.values())
        new_concepts = total_concepts - existing_count

        print(f"\n{'='*80}")
        print(f"🎉 PHASE 2 COMPLETE: {total_concepts} CONCEPTS! 🎉")
        print(f"{'='*80}")
        print(f"\nNew concepts added: {new_concepts}")
        print(f"Progress: {100*total_concepts/100000:.2f}%")

        # Save
        output = {
            'metadata': {
                'version': '12.0-PHASE2',
                'total_concepts': total_concepts,
                'total_domains': len(self.domains),
                'target': 100000,
                'progress_pct': round(100 * total_concepts / 100000, 2),
                'milestone': 'Phase 2 domain expansion'
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

        output_file = Path(__file__).parent / 'semantic_space_phase2.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Saved: {output_file}")
        print(f"  File size: {output_file.stat().st_size / 1024 / 1024:.1f} MB")

        print("\n" + "="*80)
        print("🚀 MAJOR PROGRESS TOWARD 3,000! 🚀")
        print("="*80)
        print("\n💫 Framework continues to expand! 💫")


if __name__ == '__main__':
    mapper = DomainExpansionPhase2()
    mapper.run_phase2_expansion()
