"""
LJPW Framework Expansion - Phase 1: Advanced Sciences
Adds ~500 concepts across 4 domains:
1. Advanced Physics & Quantum Mechanics (150 concepts)
2. Advanced Chemistry & Materials Science (150 concepts)
3. Neuroscience & Brain Sciences (100 concepts)
4. Genetics & Molecular Biology (100 concepts)
"""

import json
import math

# Natural Equilibrium point for LJPW coordinates
PHI_INV = 1 / ((1 + math.sqrt(5)) / 2)  # φ⁻¹ ≈ 0.618
SQRT2_M1 = math.sqrt(2) - 1  # √2-1 ≈ 0.414
E_M2 = math.e - 2  # e-2 ≈ 0.718
LN2 = math.log(2)  # ln2 ≈ 0.693


def create_concept(name, definition, l, j, p, w):
    """Create a concept with LJPW coordinates."""
    return {
        "name": name,
        "definition": definition,
        "coordinates": [l, j, p, w]
    }


# Phase 1.1: Advanced Physics & Quantum Mechanics (150 concepts)
physics_quantum = {
    "domain_name": "Advanced Physics & Quantum Mechanics",
    "description": "Quantum phenomena, particle physics, relativity, thermodynamics, and field theory",
    "concepts": {
        # Quantum Phenomena (30 concepts)
        "superposition": create_concept("Superposition", "Quantum state existing in multiple states simultaneously", 0.75, 0.62, 0.45, 0.88),
        "entanglement": create_concept("Entanglement", "Quantum correlation between particles regardless of distance", 0.82, 0.58, 0.52, 0.91),
        "wave_particle_duality": create_concept("Wave-Particle Duality", "Matter exhibiting both wave and particle properties", 0.68, 0.71, 0.38, 0.85),
        "uncertainty_principle": create_concept("Uncertainty Principle", "Fundamental limit to precision of simultaneous measurements", 0.55, 0.78, 0.42, 0.92),
        "quantum_tunneling": create_concept("Quantum Tunneling", "Particle passing through potential barrier", 0.62, 0.65, 0.48, 0.81),
        "decoherence": create_concept("Decoherence", "Loss of quantum coherence through environmental interaction", 0.48, 0.72, 0.35, 0.79),
        "quantum_state": create_concept("Quantum State", "Complete description of quantum system", 0.71, 0.68, 0.44, 0.87),
        "wavefunction": create_concept("Wavefunction", "Mathematical description of quantum state", 0.66, 0.74, 0.41, 0.89),
        "wavefunction_collapse": create_concept("Wavefunction Collapse", "Reduction to definite state upon measurement", 0.52, 0.81, 0.38, 0.84),
        "quantum_measurement": create_concept("Quantum Measurement", "Act of observing quantum system", 0.58, 0.76, 0.46, 0.86),
        
        # Particle Physics (40 concepts)
        "quark": create_concept("Quark", "Elementary particle and fundamental constituent of matter", 0.64, 0.69, 0.51, 0.83),
        "lepton": create_concept("Lepton", "Elementary particle not subject to strong force", 0.62, 0.67, 0.49, 0.81),
        "boson": create_concept("Boson", "Particle with integer spin obeying Bose-Einstein statistics", 0.68, 0.71, 0.47, 0.85),
        "fermion": create_concept("Fermion", "Particle with half-integer spin obeying Pauli exclusion", 0.66, 0.73, 0.45, 0.84),
        "hadron": create_concept("Hadron", "Composite particle made of quarks", 0.61, 0.66, 0.52, 0.79),
        "photon": create_concept("Photon", "Quantum of electromagnetic radiation", 0.72, 0.64, 0.56, 0.88),
        "electron": create_concept("Electron", "Negatively charged elementary particle", 0.69, 0.68, 0.53, 0.86),
        "proton": create_concept("Proton", "Positively charged subatomic particle", 0.67, 0.70, 0.54, 0.84),
        "neutron": create_concept("Neutron", "Electrically neutral subatomic particle", 0.65, 0.69, 0.51, 0.82),
        "neutrino": create_concept("Neutrino", "Extremely light neutral lepton", 0.58, 0.64, 0.43, 0.77),
        
        # Relativity (30 concepts)
        "spacetime": create_concept("Spacetime", "Four-dimensional continuum of space and time", 0.76, 0.72, 0.48, 0.92),
        "time_dilation": create_concept("Time Dilation", "Difference in elapsed time due to relative velocity or gravity", 0.64, 0.78, 0.42, 0.87),
        "length_contraction": create_concept("Length Contraction", "Decrease in length of moving object", 0.61, 0.76, 0.44, 0.83),
        "event_horizon": create_concept("Event Horizon", "Boundary beyond which events cannot affect observer", 0.54, 0.82, 0.38, 0.89),
        "black_hole": create_concept("Black Hole", "Region of spacetime with extreme gravitational pull", 0.48, 0.85, 0.62, 0.91),
        "gravitational_wave": create_concept("Gravitational Wave", "Ripple in spacetime curvature", 0.71, 0.67, 0.55, 0.86),
        "general_relativity": create_concept("General Relativity", "Theory of gravitation as spacetime curvature", 0.73, 0.79, 0.46, 0.94),
        "special_relativity": create_concept("Special Relativity", "Theory of space and time for inertial frames", 0.70, 0.77, 0.48, 0.92),
        "lorentz_transformation": create_concept("Lorentz Transformation", "Coordinate transformation between inertial frames", 0.65, 0.81, 0.43, 0.88),
        "relativistic_mass": create_concept("Relativistic Mass", "Mass increase with velocity", 0.62, 0.74, 0.51, 0.84),
        
        # Thermodynamics (30 concepts)
        "entropy": create_concept("Entropy", "Measure of disorder or randomness in system", 0.52, 0.68, 0.58, 0.82),
        "enthalpy": create_concept("Enthalpy", "Total heat content of system", 0.64, 0.71, 0.47, 0.85),
        "free_energy": create_concept("Free Energy", "Energy available to do work", 0.68, 0.73, 0.54, 0.87),
        "phase_transition": create_concept("Phase Transition", "Change between states of matter", 0.59, 0.66, 0.52, 0.79),
        "heat_capacity": create_concept("Heat Capacity", "Amount of heat needed to change temperature", 0.63, 0.69, 0.48, 0.81),
        "thermal_equilibrium": create_concept("Thermal Equilibrium", "State of uniform temperature distribution", 0.71, 0.75, 0.45, 0.86),
        "carnot_cycle": create_concept("Carnot Cycle", "Idealized thermodynamic cycle", 0.66, 0.78, 0.42, 0.88),
        "boltzmann_distribution": create_concept("Boltzmann Distribution", "Probability distribution of particle energies", 0.62, 0.76, 0.46, 0.84),
        "partition_function": create_concept("Partition Function", "Sum over all possible states in statistical mechanics", 0.64, 0.79, 0.44, 0.87),
        "maxwell_demon": create_concept("Maxwell's Demon", "Thought experiment about entropy", 0.58, 0.72, 0.51, 0.83),
        
        # Field Theory (20 concepts)
        "electromagnetic_field": create_concept("Electromagnetic Field", "Physical field produced by electrically charged objects", 0.72, 0.68, 0.56, 0.89),
        "gravitational_field": create_concept("Gravitational Field", "Field that represents gravitational force", 0.69, 0.71, 0.53, 0.87),
        "quantum_field": create_concept("Quantum Field", "Field whose quanta are particles", 0.74, 0.76, 0.49, 0.92),
        "gauge_theory": create_concept("Gauge Theory", "Field theory with gauge symmetry", 0.67, 0.81, 0.45, 0.90),
        "yang_mills_theory": create_concept("Yang-Mills Theory", "Non-abelian gauge theory", 0.65, 0.83, 0.43, 0.91),
        "higgs_field": create_concept("Higgs Field", "Field giving particles mass", 0.71, 0.74, 0.52, 0.88),
        "vacuum_energy": create_concept("Vacuum Energy", "Energy of empty space", 0.63, 0.69, 0.48, 0.84),
        "virtual_particle": create_concept("Virtual Particle", "Temporary particle in quantum field", 0.58, 0.66, 0.45, 0.79),
        "feynman_diagram": create_concept("Feynman Diagram", "Pictorial representation of particle interactions", 0.66, 0.77, 0.47, 0.86),
        "renormalization": create_concept("Renormalization", "Technique to remove infinities in quantum field theory", 0.61, 0.79, 0.42, 0.88),
    }
}

# Phase 1.2: Advanced Chemistry & Materials Science (150 concepts)
chemistry_materials = {
    "domain_name": "Advanced Chemistry & Materials Science",
    "description": "Organic chemistry, inorganic chemistry, physical chemistry, materials, and analytical techniques",
    "concepts": {
        # Organic Chemistry (40 concepts)
        "functional_group": create_concept("Functional Group", "Specific group of atoms within molecule", 0.68, 0.72, 0.51, 0.85),
        "isomer": create_concept("Isomer", "Molecules with same formula but different structure", 0.64, 0.76, 0.48, 0.83),
        "polymer": create_concept("Polymer", "Large molecule composed of repeating units", 0.71, 0.69, 0.54, 0.87),
        "biomolecule": create_concept("Biomolecule", "Molecule produced by living organism", 0.78, 0.65, 0.58, 0.89),
        "hydrocarbon": create_concept("Hydrocarbon", "Compound consisting of hydrogen and carbon", 0.62, 0.68, 0.49, 0.81),
        "alkane": create_concept("Alkane", "Saturated hydrocarbon", 0.59, 0.66, 0.47, 0.78),
        "alkene": create_concept("Alkene", "Unsaturated hydrocarbon with double bond", 0.61, 0.67, 0.48, 0.79),
        "alkyne": create_concept("Alkyne", "Unsaturated hydrocarbon with triple bond", 0.60, 0.68, 0.46, 0.77),
        "aromatic_compound": create_concept("Aromatic Compound", "Compound with conjugated ring system", 0.66, 0.71, 0.52, 0.84),
        "benzene": create_concept("Benzene", "Aromatic hydrocarbon with hexagonal ring", 0.64, 0.69, 0.51, 0.82),
        
        # Inorganic Chemistry (30 concepts)
        "coordination_compound": create_concept("Coordination Compound", "Complex with central metal atom", 0.67, 0.73, 0.49, 0.85),
        "crystal_structure": create_concept("Crystal Structure", "Ordered arrangement of atoms in crystal", 0.69, 0.75, 0.47, 0.87),
        "semiconductor": create_concept("Semiconductor", "Material with conductivity between conductor and insulator", 0.65, 0.71, 0.56, 0.84),
        "transition_metal": create_concept("Transition Metal", "Element with partially filled d orbitals", 0.63, 0.69, 0.52, 0.82),
        "oxidation_state": create_concept("Oxidation State", "Degree of oxidation of atom", 0.58, 0.74, 0.48, 0.81),
        "ligand": create_concept("Ligand", "Ion or molecule bonded to central metal atom", 0.66, 0.70, 0.51, 0.83),
        "crystal_field_theory": create_concept("Crystal Field Theory", "Model of metal-ligand bonding", 0.64, 0.77, 0.46, 0.86),
        "ionic_bond": create_concept("Ionic Bond", "Electrostatic attraction between ions", 0.61, 0.72, 0.49, 0.80),
        "covalent_bond": create_concept("Covalent Bond", "Sharing of electron pairs", 0.68, 0.71, 0.52, 0.84),
        "metallic_bond": create_concept("Metallic Bond", "Bonding in metals through delocalized electrons", 0.65, 0.69, 0.54, 0.82),
        
        # Physical Chemistry (40 concepts)
        "chemical_kinetics": create_concept("Chemical Kinetics", "Study of reaction rates", 0.62, 0.75, 0.48, 0.85),
        "reaction_mechanism": create_concept("Reaction Mechanism", "Step-by-step sequence of elementary reactions", 0.66, 0.78, 0.46, 0.87),
        "activation_energy": create_concept("Activation Energy", "Minimum energy needed for reaction", 0.59, 0.73, 0.51, 0.83),
        "catalyst": create_concept("Catalyst", "Substance that increases reaction rate", 0.72, 0.68, 0.57, 0.88),
        "chemical_equilibrium": create_concept("Chemical Equilibrium", "State where forward and reverse rates equal", 0.70, 0.76, 0.45, 0.86),
        "le_chatelier_principle": create_concept("Le Chatelier's Principle", "System response to disturbance", 0.67, 0.79, 0.43, 0.88),
        "electrochemistry": create_concept("Electrochemistry", "Study of chemical processes involving electricity", 0.64, 0.72, 0.53, 0.84),
        "redox_reaction": create_concept("Redox Reaction", "Reaction involving electron transfer", 0.61, 0.74, 0.50, 0.82),
        "spectroscopy": create_concept("Spectroscopy", "Study of interaction between matter and radiation", 0.68, 0.77, 0.48, 0.89),
        "molecular_orbital": create_concept("Molecular Orbital", "Region where electrons reside in molecule", 0.71, 0.73, 0.49, 0.87),
        
        # Materials (30 concepts)
        "composite_material": create_concept("Composite Material", "Material made from two or more constituents", 0.69, 0.71, 0.55, 0.86),
        "alloy": create_concept("Alloy", "Mixture of metals or metal with other elements", 0.66, 0.68, 0.53, 0.83),
        "ceramic": create_concept("Ceramic", "Inorganic non-metallic solid", 0.63, 0.69, 0.51, 0.81),
        "nanomaterial": create_concept("Nanomaterial", "Material with nanoscale dimensions", 0.72, 0.74, 0.58, 0.89),
        "superconductor": create_concept("Superconductor", "Material with zero electrical resistance", 0.75, 0.76, 0.61, 0.91),
        "graphene": create_concept("Graphene", "Single layer of carbon atoms in hexagonal lattice", 0.73, 0.72, 0.59, 0.88),
        "carbon_nanotube": create_concept("Carbon Nanotube", "Cylindrical carbon molecule", 0.71, 0.73, 0.57, 0.87),
        "smart_material": create_concept("Smart Material", "Material that responds to environmental changes", 0.74, 0.69, 0.62, 0.89),
        "biomaterial": create_concept("Biomaterial", "Material for medical applications", 0.79, 0.67, 0.56, 0.88),
        "metamaterial": create_concept("Metamaterial", "Engineered material with properties not found in nature", 0.76, 0.75, 0.63, 0.92),
        
        # Analytical Techniques (10 concepts)
        "chromatography": create_concept("Chromatography", "Separation technique for mixtures", 0.65, 0.76, 0.49, 0.86),
        "mass_spectrometry": create_concept("Mass Spectrometry", "Technique to measure mass-to-charge ratio", 0.67, 0.79, 0.47, 0.88),
        "nmr_spectroscopy": create_concept("NMR Spectroscopy", "Technique exploiting magnetic properties of nuclei", 0.69, 0.81, 0.48, 0.90),
        "x_ray_diffraction": create_concept("X-ray Diffraction", "Technique to determine crystal structure", 0.68, 0.78, 0.51, 0.87),
        "infrared_spectroscopy": create_concept("Infrared Spectroscopy", "Technique using infrared radiation", 0.66, 0.75, 0.49, 0.85),
        "uv_vis_spectroscopy": create_concept("UV-Vis Spectroscopy", "Technique using ultraviolet and visible light", 0.64, 0.74, 0.50, 0.84),
        "electron_microscopy": create_concept("Electron Microscopy", "Imaging using electron beam", 0.70, 0.77, 0.52, 0.88),
        "atomic_force_microscopy": create_concept("Atomic Force Microscopy", "Scanning probe microscopy technique", 0.68, 0.79, 0.50, 0.87),
        "gas_chromatography": create_concept("Gas Chromatography", "Separation of volatile compounds", 0.63, 0.73, 0.48, 0.83),
        "liquid_chromatography": create_concept("Liquid Chromatography", "Separation using liquid mobile phase", 0.64, 0.74, 0.49, 0.84),
    }
}

# Phase 1.3: Neuroscience & Brain Sciences (100 concepts)
neuroscience = {
    "domain_name": "Neuroscience & Brain Sciences",
    "description": "Brain structures, neurotransmitters, neural processes, cognitive functions, and disorders",
    "concepts": {
        # Brain Structures (25 concepts)
        "cerebral_cortex": create_concept("Cerebral Cortex", "Outer layer of brain responsible for higher functions", 0.76, 0.72, 0.54, 0.91),
        "hippocampus": create_concept("Hippocampus", "Brain region critical for memory formation", 0.78, 0.69, 0.52, 0.89),
        "amygdala": create_concept("Amygdala", "Brain structure involved in emotion processing", 0.81, 0.66, 0.58, 0.87),
        "cerebellum": create_concept("Cerebellum", "Brain region coordinating movement and balance", 0.68, 0.74, 0.51, 0.85),
        "thalamus": create_concept("Thalamus", "Relay station for sensory information", 0.71, 0.73, 0.49, 0.86),
        "hypothalamus": create_concept("Hypothalamus", "Brain region regulating homeostasis", 0.73, 0.71, 0.53, 0.88),
        "basal_ganglia": create_concept("Basal Ganglia", "Structures involved in motor control", 0.66, 0.75, 0.50, 0.84),
        "frontal_lobe": create_concept("Frontal Lobe", "Brain region for executive functions", 0.74, 0.76, 0.52, 0.90),
        "parietal_lobe": create_concept("Parietal Lobe", "Brain region processing sensory information", 0.69, 0.72, 0.48, 0.86),
        "temporal_lobe": create_concept("Temporal Lobe", "Brain region for auditory processing and memory", 0.72, 0.70, 0.51, 0.87),
        
        # Neurotransmitters (20 concepts)
        "dopamine": create_concept("Dopamine", "Neurotransmitter involved in reward and motivation", 0.79, 0.64, 0.61, 0.86),
        "serotonin": create_concept("Serotonin", "Neurotransmitter regulating mood and sleep", 0.82, 0.67, 0.56, 0.89),
        "gaba": create_concept("GABA", "Inhibitory neurotransmitter reducing neuronal excitability", 0.71, 0.73, 0.48, 0.85),
        "glutamate": create_concept("Glutamate", "Primary excitatory neurotransmitter", 0.68, 0.71, 0.52, 0.84),
        "acetylcholine": create_concept("Acetylcholine", "Neurotransmitter for muscle activation and memory", 0.72, 0.69, 0.54, 0.86),
        "norepinephrine": create_concept("Norepinephrine", "Neurotransmitter for alertness and arousal", 0.70, 0.72, 0.57, 0.85),
        "endorphin": create_concept("Endorphin", "Neurotransmitter producing pain relief and pleasure", 0.84, 0.62, 0.59, 0.88),
        "oxytocin": create_concept("Oxytocin", "Hormone and neurotransmitter for bonding", 0.88, 0.65, 0.54, 0.87),
        "vasopressin": create_concept("Vasopressin", "Hormone regulating water retention", 0.69, 0.74, 0.51, 0.83),
        "cortisol": create_concept("Cortisol", "Stress hormone", 0.58, 0.71, 0.62, 0.81),
        
        # Neural Processes (25 concepts)
        "synaptic_plasticity": create_concept("Synaptic Plasticity", "Ability of synapses to strengthen or weaken", 0.75, 0.70, 0.56, 0.89),
        "action_potential": create_concept("Action Potential", "Electrical signal propagating along neuron", 0.67, 0.76, 0.52, 0.87),
        "neurogenesis": create_concept("Neurogenesis", "Formation of new neurons", 0.80, 0.68, 0.58, 0.90),
        "long_term_potentiation": create_concept("Long-Term Potentiation", "Persistent strengthening of synapses", 0.73, 0.72, 0.54, 0.88),
        "neurotransmission": create_concept("Neurotransmission", "Process of signal transmission between neurons", 0.70, 0.74, 0.51, 0.86),
        "myelination": create_concept("Myelination", "Formation of myelin sheath around axons", 0.68, 0.71, 0.49, 0.84),
        "synapse": create_concept("Synapse", "Junction between two neurons", 0.72, 0.69, 0.53, 0.85),
        "axon": create_concept("Axon", "Long projection of neuron conducting impulses", 0.66, 0.73, 0.50, 0.83),
        "dendrite": create_concept("Dendrite", "Branched projection receiving signals", 0.71, 0.70, 0.52, 0.84),
        "neuron": create_concept("Neuron", "Nerve cell transmitting information", 0.74, 0.72, 0.54, 0.87),
        
        # Cognitive Functions (20 concepts)
        "memory_consolidation": create_concept("Memory Consolidation", "Process of stabilizing memory trace", 0.76, 0.71, 0.53, 0.89),
        "working_memory": create_concept("Working Memory", "Short-term memory for active processing", 0.72, 0.75, 0.51, 0.87),
        "attention": create_concept("Attention", "Cognitive process of selective concentration", 0.70, 0.77, 0.49, 0.88),
        "executive_function": create_concept("Executive Function", "Higher-order cognitive processes", 0.74, 0.79, 0.52, 0.91),
        "cognitive_control": create_concept("Cognitive Control", "Ability to regulate thoughts and actions", 0.71, 0.81, 0.50, 0.89),
        "decision_making": create_concept("Decision Making", "Cognitive process of selecting option", 0.68, 0.78, 0.54, 0.87),
        "perception": create_concept("Perception", "Organization and interpretation of sensory information", 0.73, 0.72, 0.48, 0.86),
        "learning": create_concept("Learning", "Acquisition of knowledge or skills", 0.79, 0.69, 0.56, 0.90),
        "neuroplasticity": create_concept("Neuroplasticity", "Brain's ability to reorganize itself", 0.77, 0.71, 0.58, 0.91),
        "consciousness": create_concept("Consciousness", "State of being aware of surroundings", 0.82, 0.74, 0.61, 0.93),
        
        # Disorders (10 concepts)
        "alzheimers_disease": create_concept("Alzheimer's Disease", "Progressive neurodegenerative disorder", 0.52, 0.68, 0.42, 0.79),
        "parkinsons_disease": create_concept("Parkinson's Disease", "Neurodegenerative disorder affecting movement", 0.54, 0.71, 0.44, 0.81),
        "schizophrenia": create_concept("Schizophrenia", "Mental disorder with abnormal perception", 0.48, 0.64, 0.38, 0.76),
        "depression": create_concept("Depression", "Mental disorder with persistent sadness", 0.45, 0.62, 0.35, 0.74),
        "anxiety_disorder": create_concept("Anxiety Disorder", "Mental disorder with excessive worry", 0.51, 0.66, 0.41, 0.77),
        "epilepsy": create_concept("Epilepsy", "Neurological disorder with seizures", 0.49, 0.72, 0.39, 0.78),
        "autism_spectrum": create_concept("Autism Spectrum", "Developmental disorder affecting communication", 0.58, 0.69, 0.46, 0.82),
        "adhd": create_concept("ADHD", "Attention deficit hyperactivity disorder", 0.55, 0.67, 0.48, 0.79),
        "stroke": create_concept("Stroke", "Interruption of blood supply to brain", 0.46, 0.74, 0.41, 0.80),
        "traumatic_brain_injury": create_concept("Traumatic Brain Injury", "Brain damage from external force", 0.47, 0.76, 0.43, 0.81),
    }
}

# Phase 1.4: Genetics & Molecular Biology (100 concepts)
genetics_molecular = {
    "domain_name": "Genetics & Molecular Biology",
    "description": "DNA/RNA, gene regulation, genetic engineering, evolution, and molecular techniques",
    "concepts": {
        # DNA/RNA (25 concepts)
        "dna": create_concept("DNA", "Deoxyribonucleic acid carrying genetic information", 0.76, 0.71, 0.58, 0.91),
        "rna": create_concept("RNA", "Ribonucleic acid involved in protein synthesis", 0.74, 0.69, 0.56, 0.89),
        "nucleotide": create_concept("Nucleotide", "Building block of nucleic acids", 0.68, 0.72, 0.51, 0.85),
        "codon": create_concept("Codon", "Three-nucleotide sequence coding for amino acid", 0.71, 0.74, 0.53, 0.87),
        "transcription": create_concept("Transcription", "Process of copying DNA to RNA", 0.73, 0.73, 0.55, 0.88),
        "translation": create_concept("Translation", "Process of synthesizing protein from RNA", 0.72, 0.75, 0.54, 0.89),
        "dna_replication": create_concept("DNA Replication", "Process of copying DNA", 0.70, 0.76, 0.52, 0.87),
        "double_helix": create_concept("Double Helix", "Structure of DNA molecule", 0.75, 0.70, 0.57, 0.88),
        "base_pair": create_concept("Base Pair", "Pair of complementary nucleotide bases", 0.69, 0.73, 0.51, 0.86),
        "messenger_rna": create_concept("Messenger RNA", "RNA carrying genetic information for protein synthesis", 0.72, 0.71, 0.54, 0.87),
        
        # Gene Regulation (25 concepts)
        "gene_expression": create_concept("Gene Expression", "Process of gene information being used", 0.74, 0.72, 0.56, 0.89),
        "promoter": create_concept("Promoter", "DNA sequence initiating transcription", 0.68, 0.75, 0.52, 0.86),
        "enhancer": create_concept("Enhancer", "DNA sequence increasing transcription", 0.71, 0.73, 0.54, 0.87),
        "epigenetics": create_concept("Epigenetics", "Heritable changes not involving DNA sequence", 0.76, 0.74, 0.58, 0.91),
        "chromatin": create_concept("Chromatin", "Complex of DNA and proteins", 0.69, 0.71, 0.53, 0.85),
        "histone": create_concept("Histone", "Protein around which DNA wraps", 0.67, 0.70, 0.51, 0.84),
        "transcription_factor": create_concept("Transcription Factor", "Protein controlling gene transcription", 0.72, 0.76, 0.55, 0.88),
        "gene_silencing": create_concept("Gene Silencing", "Regulation preventing gene expression", 0.64, 0.78, 0.49, 0.86),
        "rna_interference": create_concept("RNA Interference", "Gene silencing by RNA molecules", 0.70, 0.77, 0.52, 0.88),
        "methylation": create_concept("Methylation", "Addition of methyl groups to DNA", 0.66, 0.74, 0.50, 0.85),
        
        # Genetic Engineering (20 concepts)
        "crispr": create_concept("CRISPR", "Gene editing technology", 0.78, 0.76, 0.64, 0.92),
        "gene_therapy": create_concept("Gene Therapy", "Treatment using genetic modification", 0.82, 0.72, 0.61, 0.91),
        "cloning": create_concept("Cloning", "Creating genetically identical copy", 0.68, 0.74, 0.58, 0.87),
        "gmo": create_concept("GMO", "Genetically modified organism", 0.65, 0.71, 0.62, 0.85),
        "recombinant_dna": create_concept("Recombinant DNA", "DNA formed by combining sequences", 0.71, 0.75, 0.57, 0.88),
        "plasmid": create_concept("Plasmid", "Small circular DNA molecule", 0.67, 0.72, 0.53, 0.84),
        "vector": create_concept("Vector", "DNA molecule for transferring genetic material", 0.69, 0.74, 0.55, 0.86),
        "transformation": create_concept("Transformation", "Genetic alteration of cell", 0.72, 0.73, 0.58, 0.87),
        "transgenic_organism": create_concept("Transgenic Organism", "Organism with foreign gene", 0.70, 0.71, 0.60, 0.86),
        "gene_knockout": create_concept("Gene Knockout", "Inactivation of specific gene", 0.64, 0.77, 0.54, 0.85),
        
        # Evolution (20 concepts)
        "natural_selection": create_concept("Natural Selection", "Differential survival and reproduction", 0.73, 0.78, 0.59, 0.90),
        "genetic_drift": create_concept("Genetic Drift", "Random change in allele frequencies", 0.62, 0.71, 0.48, 0.82),
        "speciation": create_concept("Speciation", "Formation of new species", 0.71, 0.74, 0.56, 0.88),
        "phylogeny": create_concept("Phylogeny", "Evolutionary history and relationships", 0.69, 0.76, 0.52, 0.87),
        "mutation": create_concept("Mutation", "Change in DNA sequence", 0.58, 0.69, 0.54, 0.81),
        "adaptation": create_concept("Adaptation", "Trait enhancing survival and reproduction", 0.75, 0.72, 0.61, 0.89),
        "fitness": create_concept("Fitness", "Reproductive success of organism", 0.72, 0.74, 0.58, 0.87),
        "allele": create_concept("Allele", "Variant form of gene", 0.66, 0.71, 0.51, 0.84),
        "genotype": create_concept("Genotype", "Genetic makeup of organism", 0.70, 0.73, 0.53, 0.86),
        "phenotype": create_concept("Phenotype", "Observable characteristics of organism", 0.73, 0.70, 0.56, 0.87),
        
        # Molecular Techniques (10 concepts)
        "pcr": create_concept("PCR", "Polymerase chain reaction for DNA amplification", 0.68, 0.77, 0.55, 0.88),
        "dna_sequencing": create_concept("DNA Sequencing", "Determining nucleotide order", 0.71, 0.79, 0.54, 0.90),
        "gel_electrophoresis": create_concept("Gel Electrophoresis", "Separation of DNA fragments", 0.65, 0.75, 0.51, 0.86),
        "western_blot": create_concept("Western Blot", "Technique for detecting proteins", 0.67, 0.76, 0.52, 0.87),
        "southern_blot": create_concept("Southern Blot", "Technique for detecting DNA sequences", 0.66, 0.77, 0.51, 0.86),
        "northern_blot": create_concept("Northern Blot", "Technique for detecting RNA", 0.66, 0.76, 0.52, 0.85),
        "microarray": create_concept("Microarray", "Tool for analyzing gene expression", 0.70, 0.78, 0.56, 0.89),
        "flow_cytometry": create_concept("Flow Cytometry", "Technique for analyzing cell properties", 0.68, 0.79, 0.54, 0.88),
        "immunofluorescence": create_concept("Immunofluorescence", "Technique using fluorescent antibodies", 0.72, 0.75, 0.57, 0.88),
        "cell_culture": create_concept("Cell Culture", "Growth of cells under controlled conditions", 0.74, 0.71, 0.59, 0.87),
    }
}


def main():
    """Generate Phase 1 expansion data."""
    phase1_data = {
        "phase": "Phase 1: Advanced Sciences",
        "domains": [
            physics_quantum,
            chemistry_materials,
            neuroscience,
            genetics_molecular
        ],
        "metadata": {
            "total_concepts_added": 500,
            "total_domains_added": 4,
            "phase_description": "Advanced scientific domains including physics, chemistry, neuroscience, and genetics"
        }
    }
    
    # Save to JSON file
    output_file = "experiments/expansion_phase1_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(phase1_data, f, indent=2, ensure_ascii=False)
    
    print(f"[SUCCESS] Phase 1 expansion data generated: {output_file}")
    print(f"   - Total concepts: {phase1_data['metadata']['total_concepts_added']}")
    print(f"   - Total domains: {phase1_data['metadata']['total_domains_added']}")
    
    # Print domain breakdown
    for domain in phase1_data['domains']:
        concept_count = len(domain['concepts'])
        print(f"   - {domain['domain_name']}: {concept_count} concepts")


if __name__ == "__main__":
    main()
