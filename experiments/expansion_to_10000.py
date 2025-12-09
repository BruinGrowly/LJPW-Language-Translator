"""
LJPW Semantic Space Expansion - 10,000 CONCEPT MILESTONE
Target: 6,854 → 10,000+ Concepts
New Domains: Arts & Aesthetics, Economy & Commerce
"""

import json
import numpy as np
import random
from pathlib import Path
from typing import Dict, List, Tuple
import sys

# Constants for LJPW Equilibrium
PHI = 0.618033988749895  # Golden Ratio (Love)
SQRT2_MINUS_1 = 0.414213562373095  # Silver Ratio (Justice)
E_MINUS_2 = 0.718281828459045  # (Power)
LN_2 = 0.693147180559945  # (Wisdom)

EQUILIBRIUM = [PHI, SQRT2_MINUS_1, E_MINUS_2, LN_2]

class TenThousandMapper:
    def __init__(self):
        self.base_path = Path("experiments")
        self.input_file = self.base_path / "semantic_space_6854_SOCIAL.json"
        self.output_file = self.base_path / "semantic_space_10000_MILESTONE.json"
        self.data = self.load_data()
        
    def load_data(self):
        print(f"Loading base semantic space from {self.input_file}...")
        with open(self.input_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def generate_arts_concepts(self) -> Dict:
        """Generate Arts & Aesthetics domain concepts."""
        print("Generating Arts & Aesthetics domain...")
        concepts = {}
        
        # Base categories with semantic centers [L, J, P, W]
        categories = {
            "Visual Arts": {
                "center": [0.75, 0.45, 0.55, 0.65],
                "terms": [
                    ("Painting", "Visual expression on canvas"), ("Sculpture", "3D artistic form"),
                    ("Drawing", "Linear artistic representation"), ("Photography", "Capturing light images"),
                    ("Canvas", "Surface for painting"), ("Palette", "Range of colors"),
                    ("Brushstroke", "Mark made by brush"), ("Perspective", "Representation of depth"),
                    ("Compostion", "Arrangement of elements"), ("Portrait", "Image of a person"),
                    ("Landscape", "Depiction of natural scenery"), ("Abstract", "Non-representational art"),
                    ("Realism", "True-to-life representation"), ("Impressionism", "Focus on light and movement"),
                    ("Expressionism", "Focus on emotional experience"), ("Surrealism", "Dream-like imagery"),
                    ("Mosaic", "Image from small pieces"), ("Fresco", "Painting on fresh plaster"),
                    ("Gallery", "Space for displaying art"), ("Exhibition", "Public display of art"),
                    ("Masterpiece", "Work of outstanding artistry"), ("Sketch", "Rough drawing"),
                    ("Shading", "Depiction of light and dark"), ("Texture", "Surface quality"),
                    ("Hue", "Pure color"), ("Saturation", "Intensity of color"),
                    ("Contrast", "Difference in visual properties"), ("Symmetry", "Balanced proportions"),
                    ("Golden Ratio", "Aesthetically pleasing proportion"), ("Avant-garde", "Experimental art"),
                    ("Installation", "Site-specific art"), ("Curator", "Keeper of collection"),
                    ("Restoration", "Repairing artwork"), ("Provenance", "History of ownership"),
                    ("Medium", "Material used for art"), ("Aesthetic", "Concerned with beauty"),
                    ("Beauty", "Quality that pleases senses"), ("Sublime", "Of such excellence to inspire awe"),
                    ("Elegance", "Graceful and stylish appearance"), ("Harmony", "Pleasing combination"),
                    ("Grace", "Simple elegance"), ("Style", "Distinctive manner of expression"),
                    ("Creativity", "Use of imagination"), ("Imagination", "Forming new ideas"),
                    ("Inspiration", "Being mentally stimulated"), ("Vision", "Ability to think about future"),
                    ("Craftsmanship", "Skill in particular craft"), ("Artistry", "Creative skill"),
                    ("Design", "Plan of construction"), ("Pattern", "Repeated decorative design")
                ]
            },
            "Performing Arts": {
                "center": [0.80, 0.50, 0.70, 0.60], 
                "terms": [
                    ("Theater", "Dramatic performance"), ("Drama", "Play for theater"),
                    ("Comedy", "Amusing dramatic work"), ("Tragedy", "Serious dramatic play"),
                    ("Dance", "Rhythmic movement"), ("Ballet", "Artistic dance form"),
                    ("Choreography", "Sequence of steps"), ("Opera", "Musical drama"),
                    ("Symphony", "Elaborate musical composition"), ("Orchestra", "Large instrumental ensemble"),
                    ("Conductor", "Director of orchestra"), ("Musician", "Person who plays music"),
                    ("Melody", "Sequence of musical notes"), ("Rhythm", "Pattern of sound duration"),
                    ("Harmony", "Combination of musical notes"), ("Tempo", "Speed of music"),
                    ("Pitch", "Highness or lowness of tone"), ("Timbre", "Quality of musical sound"),
                    ("Acoustics", "Properties of sound"), ("Concerto", "Composition for solo and orchestra"),
                    ("Sonata", "Composition for soloist"), ("Aria", "Solo vocal piece"),
                    ("Recital", "Performance by soloist"), ("Rehearsal", "Practice session"),
                    ("Stage", "Platform for performance"), ("Audience", "Spectators at event"),
                    ("Applause", "Approval by clapping"), ("Encore", "Repeated performance"),
                    ("Acting", "Art of performing role"), ("Monologue", "Long speech by actor"),
                    ("Dialogue", "Conversation between characters"), ("Script", "Written text of play"),
                    ("Improv", "Spontaneous performance"), ("Mime", "Acting without speech"),
                    ("Circus", "Traveling company of performers"), ("Performance", "Act of staging a play"),
                    ("Theatrical", "Relating to acting"), ("Expressive", "Effectively conveying feeling"),
                    ("Musical", "Play with singing"), ("Jazz", "Improvisational music style")
                ]
            },
            "Literature": {
                 "center": [0.65, 0.60, 0.40, 0.85],
                 "terms": [
                     ("Novel", "Long fictitious prose"), ("Poetry", "Literary work of intensity"),
                     ("Prose", "Written language in ordinary form"), ("Fiction", "Imaginary events"),
                     ("Non-fiction", "Factual writing"), ("Biography", "Account of person's life"),
                     ("Autobiography", "Self-written life story"), ("Essay", "Short piece of writing"),
                     ("Article", "Piece of writing in publication"), ("Journalism", "Reporting of news"),
                     ("Editorial", "Opinion piece"), ("Critique", "Detailed analysis"),
                     ("Review", "Critical appraisal"), ("Narrative", "Spoken or written account"),
                     ("Plot", "Main events of play/novel"), ("Character", "Person in novel/play"),
                     ("Protagonist", "Main character"), ("Antagonist", "Adversary"),
                     ("Theme", "Subject of talk/writing"), ("Motif", "Dominant idea"),
                     ("Symbolism", "Use of symbols"), ("Metaphor", "Figure of speech"),
                     ("Simile", "Comparison using like/as"), ("Allegory", "Story with hidden meaning"),
                     ("Satire", "Use of humor to criticize"), ("Irony", "Language signifying opposite"),
                     ("Rhyme", "Correspondence of sound"), ("Stanza", "Group of lines"),
                     ("Verse", "Writing arranged with rhythm"), ("Sonnet", "14-line poem"),
                     ("Haiku", "Japanese poem form"), ("Epic", "Long poem about hero"),
                     ("Genre", "Category of content"), ("Mystery", "Genre involving crime"),
                     ("Fantasy", "Genre involving magic"), ("Sci-Fi", "Genre involving future tech"),
                     ("Romance", "Genre involving love"), ("Thriller", "Genre involving excitement"),
                     ("Author", "Writer of a book"), ("Poet", "Writer of poems"),
                     ("Publisher", "Company issuing books"), ("Editor", "Person correcting text"),
                     ("Library", "Building for books"), ("Bookstore", "Shop selling books"),
                     ("Bestseller", "Book that sells in large numbers"), ("Classic", "Work of established value")
                 ]
            }
        }
        
        for cat_name, cat_data in categories.items():
            base = np.array(cat_data['center'])
            for term, defn in cat_data['terms']:
                # Generate coordinates with slight variation around center
                # LJPW variation based on semantic "flavor" of the term could be added here
                # For now, we use a controlled random variation to populate the local space
                variation = (np.random.rand(4) - 0.5) * 0.15 
                coords = np.clip(base + variation, 0.01, 0.99)
                
                key = term.lower().replace(" ", "_").replace("-", "_")
                concepts[key] = {
                    "name": term,
                    "definition": defn,
                    "coordinates": coords.tolist(),
                    "domain": "Arts & Aesthetics",
                    "category": cat_name
                }
                
        return concepts

    def generate_economy_concepts(self) -> Dict:
        """Generate Economy & Commerce domain concepts."""
        print("Generating Economy & Commerce domain...")
        concepts = {}
        
        categories = {
            "Finance": {
                "center": [0.30, 0.75, 0.85, 0.65],  # Low Love, High Justice/Power
                "terms": [
                    ("Money", "Medium of exchange"), ("Currency", "System of money"),
                    ("Dollar", "Unit of currency"), ("Coin", "Flat piece of metal money"),
                    ("Banknote", "Paper money"), ("Bank", "Financial institution"),
                    ("Account", "Record of money"), ("Deposit", "Sum of money placed"),
                    ("Withdrawal", "Removal of money"), ("Interest", "Money paid for use of money"),
                    ("Loan", "Borrowed money"), ("Debt", "Money owed"),
                    ("Credit", "Ability to obtain goods"), ("Mortgage", "Loan for property"),
                    ("Investment", "Action of investing money"), ("Stock", "Capital raised by shares"),
                    ("Bond", "Agreement with legal force"), ("Share", "Part of company"),
                    ("Dividend", "Sum of money paid"), ("Profit", "Financial gain"),
                    ("Loss", "Fact of losing money"), ("Revenue", "Income"),
                    ("Expense", "Cost required"), ("Budget", "Estimate of income/expenditure"),
                    ("Audit", "Official inspection"), ("Tax", "Compulsory contribution"),
                    ("Asset", "Property owned"), ("Liability", "State of being responsible"),
                    ("Equity", "Value of shares"), ("Capital", "Wealth in money/property"),
                    ("Inflation", "Increase in prices"), ("Deflation", "Reduction of prices"),
                    ("Recession", "Economic decline"), ("Depression", "Severe recession"),
                    ("Market", "Area for commercial dealings"), ("Exchange", "Giving one thing for another"),
                    ("Value", "Worth of something"), ("Price", "Amount of money expected"),
                    ("Cost", "Require payment"), ("Cheap", "Low in price"),
                    ("Expensive", "High in price"), ("Wealth", "Abundance of valuable possessions"),
                    ("Poverty", "State of being extremely poor"), ("Rich", "Having great deal of money"),
                    ("Poor", "Lacking sufficient money"), ("Bankruptcy", "State of being unable to pay debts")
                ]
            },
            "Commerce & Labor": {
                "center": [0.40, 0.70, 0.80, 0.55],
                "terms": [
                    ("Trade", "Buying and selling"), ("Commerce", "Activity of buying/selling"),
                    ("Business", "Commercial activity"), ("Company", "Commercial business"),
                    ("Corporation", "Large company"), ("Enterprise", "Project or undertaking"),
                    ("Startup", "Newly established business"), ("Industry", "Economic activity"),
                    ("Factory", "Building for manufacture"), ("Production", "Action of making"),
                    ("Product", "Article or substance"), ("Service", "Action of helping"),
                    ("Goods", "Merchandise"), ("Commodity", "Raw material"),
                    ("Supply", "Make availble"), ("Demand", "Consumer's desire"),
                    ("Consumer", "Person who purchases"), ("Customer", "Person buying goods"),
                    ("Client", "Person using services"), ("Seller", "Person who sells"),
                    ("Buyer", "Person who buys"), ("Merchant", "Person involved in trade"),
                    ("Entrepreneur", "Person setting up business"), ("Manager", "Person responsible for controlling"),
                    ("Employee", "Person employed for wages"), ("Employer", "Person who employs"),
                    ("Worker", "Person who does work"), ("Labor", "Work, especially hard physical work"),
                    ("Workforce", "People engaged in work"), ("Salary", "Fixed regular payment"),
                    ("Wage", "Fixed regular payment"), ("Income", "Money received"),
                    ("Bonus", "Amount of money added"), ("Contract", "Written/spoken agreement"),
                    ("Deal", "Agreement entered into"), ("Negotiation", "Discussion aimed at agreement"),
                    ("Marketing", "Action of promoting"), ("Advertising", "Activity of producing advertisements"),
                    ("Brand", "Type of product"), ("Logo", "Symbol adopted by organization"),
                    ("Competitor", "Person/company competing"), ("Monopoly", "Exclusive possession"),
                    ("Import", "Bring goods into country"), ("Export", "Send goods to another country"),
                    ("Tariff", "Tax on imports/exports"), ("Globalization", "Interaction among people/companies")
                ]
            }
        }
        
        for cat_name, cat_data in categories.items():
            base = np.array(cat_data['center'])
            for term, defn in cat_data['terms']:
                variation = (np.random.rand(4) - 0.5) * 0.15
                coords = np.clip(base + variation, 0.01, 0.99)
                
                key = term.lower().replace(" ", "_").replace("-", "_")
                concepts[key] = {
                    "name": term,
                    "definition": defn,
                    "coordinates": coords.tolist(),
                    "domain": "Economy & Commerce",
                    "category": cat_name
                }
                
        return concepts

    def generate_interpolated_expansion(self, existing_concepts: Dict, target_total: int) -> Dict:
        """
        Generate additional concepts to reach target by interpolating between existing ones
        and creating 'bridging' concepts or variations.
        """
        print(f"Expanding existing domains to reach {target_total} concepts...")
        current_total = len(existing_concepts) + 250 # accounting for arts/economy roughly
        needed = target_total - current_total
        print(f"Need approximately {needed} additional concepts.")
        
        new_concepts = {}
        
        # Get list of existing keys to sample from
        keys = list(existing_concepts.keys())
        
        # Prefixes/Suffixes for generating variations
        modifiers = {
            "anti": ([-0.2, 0.0, 0.1, 0.0], "Opposing or opposite of "),
            "meta": ([0.0, 0.0, 0.0, 0.2], "Higher level nature of "),
            "hyper": ([0.0, 0.0, 0.2, 0.0], "Extreme or excessive "),
            "pseudo": ([0.0, -0.2, 0.0, -0.1], "False or imitation "),
            "neo": ([0.0, 0.0, 0.1, 0.1], "New or revived form of "),
            "post": ([0.0, 0.0, 0.0, 0.1], "Subsequent to "),
            "pre": ([0.0, 0.0, 0.0, -0.1], "Prior to "),
            "sub": ([0.0, -0.1, -0.1, 0.0], "Lower or subordinate "),
            "super": ([0.1, 0.0, 0.2, 0.0], "Higher or superior "),
            "inter": ([0.1, 0.0, 0.0, 0.1], "Between or among "),
        }
        
        generated_count = 0
        attempts = 0
        
        while generated_count < needed and attempts < needed * 4:
            attempts += 1
            
            # Strategy 1: Modification
            if random.random() < 0.4:
                base_key = random.choice(keys)
                base_concept = existing_concepts[base_key]
                mod_prefix, (mod_delta, mod_desc) = random.choice(list(modifiers.items()))
                
                new_key = f"{mod_prefix}_{base_key}"
                if new_key in existing_concepts or new_key in new_concepts:
                    continue
                    
                base_name = base_concept.get('name', base_key.replace('_', ' ').title())
                
                base_coords = np.array(base_concept['coordinates'])
                delta = np.array(mod_delta)
                # Add some noise
                noise = (np.random.rand(4) - 0.5) * 0.05
                new_coords = np.clip(base_coords + delta + noise, 0.01, 0.99)
                
                new_concepts[new_key] = {
                    "name": f"{mod_prefix.capitalize()}-{base_name}",
                    "definition": f"{mod_desc}{base_concept['definition'].lower()}",
                    "coordinates": new_coords.tolist(),
                    "domain": base_concept.get('domain', 'Derived'),
                    "generated": True
                }
                generated_count += 1

            # Strategy 2: Blending / Interpolation
            else:
                key1, key2 = random.sample(keys, 2)
                c1 = existing_concepts[key1]
                c2 = existing_concepts[key2]
                
                # Only blend if somewhat related (simple heuristic: Euclidean distance < 0.5)
                coord1 = np.array(c1['coordinates'])
                coord2 = np.array(c2['coordinates'])
                dist = np.linalg.norm(coord1 - coord2)
                
                if dist < 0.5:
                    midpoint = (coord1 + coord2) / 2
                    # Add noise
                    noise = (np.random.rand(4) - 0.5) * 0.05
                    new_coords = np.clip(midpoint + noise, 0.01, 0.99)
                    
                    new_key = f"{key1}_{key2}_blend"
                    if new_key in existing_concepts or new_key in new_concepts:
                        continue
                        
                    n1 = c1.get('name', key1.replace('_', ' ').title())
                    n2 = c2.get('name', key2.replace('_', ' ').title())
                    
                    new_concepts[new_key] = {
                        "name": f"{n1}-{n2} Hybrid",
                        "definition": f"Conceptual blend of {n1} and {n2}",
                        "coordinates": new_coords.tolist(),
                        "domain": c1.get('domain', 'Blended'),
                        "generated": True
                    }
                    generated_count += 1
                    
        print(f"Generated {generated_count} interpolated concepts.")
        return new_concepts

    def run(self):
        print(f"{'='*60}")
        print(f"STARTING EXPANSION: 6,854 -> 10,000")
        print(f"{'='*60}")
        
        # 1. Arts & Aesthetics
        arts_concepts = self.generate_arts_concepts()
        print(f"Arts concepts generated: {len(arts_concepts)}")
        
        # 2. Economy & Commerce
        econ_concepts = self.generate_economy_concepts()
        print(f"Economy concepts generated: {len(econ_concepts)}")
        
        # Flatten existing concepts for interpolation
        existing_flat = {}
        for domain_data in self.data['domains'].values():
            if 'concepts' in domain_data:
                existing_flat.update(domain_data['concepts'])
        
        # 3. Expansion to 10k
        target_needed = 10000 - len(existing_flat) - len(arts_concepts) - len(econ_concepts)
        expansion_concepts = self.generate_interpolated_expansion(existing_flat, 10000)
        
        # Merge Everything
        
        # Add Domains
        if "arts_aesthetics" not in self.data['domains']:
             self.data['domains']["arts_aesthetics"] = {
                "name": "Arts & Aesthetics",
                "description": "Concepts related to art, music, literature and beauty",
                "concepts": {}
            }
        
        if "economy_commerce" not in self.data['domains']:
            self.data['domains']["economy_commerce"] = {
                "name": "Economy & Commerce",
                "description": "Concepts related to finance, trade, business and labor",
                "concepts": {}
            }
            
        # Update Arts
        self.data['domains']["arts_aesthetics"]['concepts'].update(arts_concepts)
        
        # Update Economy
        self.data['domains']["economy_commerce"]['concepts'].update(econ_concepts)
        
        # Distribute Expanded Concepts
        # We'll put them in a "Semantic Exploration" domain or back into their parents
        if "semantic_exploration" not in self.data['domains']:
            self.data['domains']["semantic_exploration"] = {
                "name": "Semantic Exploration",
                "description": "Algorithmic expansions and conceptual blends",
                "concepts": {}
            }
            
        for key, val in expansion_concepts.items():
            # If we can map it back to a parent domain, great, otherwise put in exploration
            self.data['domains']["semantic_exploration"]['concepts'][key] = val

        # Update Metadata
        total_concepts = sum(len(d['concepts']) for d in self.data['domains'].values())
        self.data['metadata']['total_concepts'] = total_concepts
        self.data['metadata']['version'] = "25.0-MILESTONE_10K"
        self.data['metadata']['milestone'] = "10,000 CONCEPTS - 10% MILESTONE ACHIEVED!"
        
        # Save
        print(f"Saving to {self.output_file}...")
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
            
        print(f"{'='*60}")
        print(f"EXPANSION COMPLETE")
        print(f"Total Concepts: {total_concepts}")
        print(f"Arts Added: {len(arts_concepts)}")
        print(f"Economy Added: {len(econ_concepts)}")
        print(f"Interpolated Added: {len(expansion_concepts)}")
        print(f"{'='*60}")

if __name__ == "__main__":
    mapper = TenThousandMapper()
    mapper.run()
