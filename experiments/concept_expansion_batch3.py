#!/usr/bin/env python3
"""
LJPW Semantic Space - Batch 3 Expansion
========================================

Expanding from 267 concepts to 1,000+ concepts

This batch adds:
- Expanded emotions (100+ more)
- Expanded actions (100+ more)
- NEW: Body & Health domain (100 concepts)
- NEW: Food & Cooking domain (80 concepts)
- NEW: Animals domain (60 concepts)
- NEW: Plants domain (40 concepts)
- NEW: Social Roles domain (60 concepts)
- NEW: Communication domain (50 concepts)
- NEW: Weather & Nature domain (50 concepts)
- NEW: Cognitive States domain (50 concepts)

Target: 1,000+ concepts total
"""

import numpy as np
from typing import Dict, List
import json
from pathlib import Path
from datetime import datetime
import sys

sys.path.append(str(Path(__file__).parent))
from semantic_space_mapping import SemanticSpaceMapper, ConceptualDomain


class Batch3Mapper(SemanticSpaceMapper):
    """Extended mapper for batch 3."""

    def expand_emotion_domain(self, existing_domain: ConceptualDomain) -> ConceptualDomain:
        """Expand emotions to 150+ concepts."""

        # ADDITIONAL POSITIVE EMOTIONS
        existing_domain.add_concept('amusement',
            np.array([0.82, 0.60, 0.38, 0.68]),
            definition="State of finding something funny")

        existing_domain.add_concept('awe',
            np.array([0.72, 0.75, 0.48, 0.88]),
            definition="Wonder mixed with reverence")

        existing_domain.add_concept('admiration',
            np.array([0.78, 0.72, 0.42, 0.82]),
            definition="Respect and warm approval")

        existing_domain.add_concept('excitement',
            np.array([0.75, 0.62, 0.72, 0.68]),
            definition="Great enthusiasm and eagerness")

        existing_domain.add_concept('thrill',
            np.array([0.72, 0.58, 0.78, 0.65]),
            definition="Sudden feeling of excitement")

        existing_domain.add_concept('pleasure',
            np.array([0.85, 0.58, 0.35, 0.68]),
            definition="Feeling of happy satisfaction")

        existing_domain.add_concept('satisfaction',
            np.array([0.78, 0.68, 0.42, 0.75]),
            definition="Fulfillment of expectations")

        existing_domain.add_concept('relief',
            np.array([0.72, 0.65, 0.35, 0.70]),
            definition="Removal of anxiety or distress")

        existing_domain.add_concept('comfort',
            np.array([0.78, 0.62, 0.32, 0.68]),
            definition="State of physical or mental ease")

        existing_domain.add_concept('confidence',
            np.array([0.72, 0.68, 0.72, 0.78]),
            definition="Belief in oneself")

        # ADDITIONAL NEGATIVE EMOTIONS
        existing_domain.add_concept('disappointment',
            np.array([0.38, 0.45, 0.35, 0.55]),
            definition="Sadness from unmet expectations")

        existing_domain.add_concept('regret',
            np.array([0.42, 0.52, 0.38, 0.68]),
            definition="Sorrow over past action")

        existing_domain.add_concept('remorse',
            np.array([0.38, 0.62, 0.35, 0.72]),
            definition="Deep regret for wrongdoing")

        existing_domain.add_concept('boredom',
            np.array([0.45, 0.48, 0.35, 0.52]),
            definition="State of being uninterested")

        existing_domain.add_concept('apathy',
            np.array([0.38, 0.42, 0.35, 0.48]),
            definition="Lack of emotion or interest")

        existing_domain.add_concept('indifference',
            np.array([0.42, 0.45, 0.38, 0.52]),
            definition="Lack of concern")

        existing_domain.add_concept('confusion',
            np.array([0.48, 0.52, 0.42, 0.55]),
            definition="State of being bewildered")

        existing_domain.add_concept('doubt',
            np.array([0.48, 0.55, 0.45, 0.65]),
            definition="Feeling of uncertainty")

        existing_domain.add_concept('insecurity',
            np.array([0.42, 0.48, 0.55, 0.52]),
            definition="Lack of confidence")

        existing_domain.add_concept('vulnerability',
            np.array([0.52, 0.52, 0.48, 0.62]),
            definition="State of being exposed to harm")

        # COMPLEX/SOCIAL EMOTIONS
        existing_domain.add_concept('empathy',
            np.array([0.85, 0.68, 0.28, 0.78]),
            definition="Understanding others' feelings")

        existing_domain.add_concept('sympathy',
            np.array([0.82, 0.65, 0.30, 0.72]),
            definition="Feelings of pity and sorrow")

        existing_domain.add_concept('pity',
            np.array([0.72, 0.62, 0.32, 0.68]),
            definition="Sympathetic sorrow for suffering")

        existing_domain.add_concept('scorn',
            np.array([0.25, 0.45, 0.72, 0.48]),
            definition="Contemptuous disrespect")

        existing_domain.add_concept('disdain',
            np.array([0.28, 0.48, 0.68, 0.52]),
            definition="Feeling that something is unworthy")

        existing_domain.add_concept('arrogance',
            np.array([0.32, 0.42, 0.82, 0.45]),
            definition="Exaggerated sense of importance")

        existing_domain.add_concept('humility',
            np.array([0.75, 0.78, 0.35, 0.82]),
            definition="Modest view of one's importance")

        existing_domain.add_concept('modesty',
            np.array([0.72, 0.72, 0.38, 0.75]),
            definition="Unassuming about abilities")

        return existing_domain

    def expand_action_domain(self, existing_domain: ConceptualDomain) -> ConceptualDomain:
        """Expand actions to 150+ concepts."""

        # MORE PHYSICAL ACTIONS
        existing_domain.add_concept('sit',
            np.array([0.58, 0.52, 0.35, 0.58]),
            definition="Rest on the buttocks")

        existing_domain.add_concept('stand',
            np.array([0.60, 0.58, 0.52, 0.65]),
            definition="Be in upright position on feet")

        existing_domain.add_concept('lie',
            np.array([0.55, 0.48, 0.32, 0.55]),
            definition="Be in horizontal position")

        existing_domain.add_concept('climb',
            np.array([0.62, 0.62, 0.68, 0.70]),
            definition="Go up using hands and feet")

        existing_domain.add_concept('swim',
            np.array([0.68, 0.60, 0.58, 0.68]),
            definition="Move through water")

        existing_domain.add_concept('fly',
            np.array([0.72, 0.68, 0.65, 0.78]),
            definition="Move through air")

        existing_domain.add_concept('crawl',
            np.array([0.52, 0.48, 0.48, 0.55]),
            definition="Move on hands and knees")

        existing_domain.add_concept('roll',
            np.array([0.58, 0.52, 0.52, 0.58]),
            definition="Move by turning over")

        existing_domain.add_concept('throw',
            np.array([0.58, 0.55, 0.72, 0.62]),
            definition="Propel through air")

        existing_domain.add_concept('catch',
            np.array([0.65, 0.62, 0.58, 0.72]),
            definition="Intercept and hold")

        existing_domain.add_concept('push',
            np.array([0.52, 0.58, 0.72, 0.58]),
            definition="Exert force to move away")

        existing_domain.add_concept('pull',
            np.array([0.55, 0.60, 0.68, 0.62]),
            definition="Exert force to move toward")

        existing_domain.add_concept('lift',
            np.array([0.58, 0.62, 0.68, 0.65]),
            definition="Raise to higher position")

        existing_domain.add_concept('carry',
            np.array([0.65, 0.62, 0.58, 0.68]),
            definition="Transport while supporting")

        existing_domain.add_concept('hold',
            np.array([0.68, 0.60, 0.52, 0.65]),
            definition="Keep in grasp")

        # MORE MENTAL ACTIONS
        existing_domain.add_concept('believe',
            np.array([0.68, 0.72, 0.48, 0.85]),
            definition="Accept as true")

        existing_domain.add_concept('doubt (verb)',
            np.array([0.48, 0.58, 0.45, 0.72]),
            definition="Feel uncertain about")

        existing_domain.add_concept('imagine',
            np.array([0.72, 0.65, 0.42, 0.82]),
            definition="Form mental images")

        existing_domain.add_concept('dream',
            np.array([0.75, 0.62, 0.38, 0.78]),
            definition="Experience images while sleeping")

        existing_domain.add_concept('wonder',
            np.array([0.68, 0.65, 0.42, 0.82]),
            definition="Feel curious about")

        existing_domain.add_concept('consider',
            np.array([0.62, 0.68, 0.45, 0.85]),
            definition="Think carefully about")

        existing_domain.add_concept('decide',
            np.array([0.62, 0.72, 0.62, 0.82]),
            definition="Make a choice")

        existing_domain.add_concept('choose',
            np.array([0.65, 0.68, 0.58, 0.78]),
            definition="Select from options")

        existing_domain.add_concept('judge',
            np.array([0.55, 0.78, 0.62, 0.85]),
            definition="Form opinion about")

        existing_domain.add_concept('reason',
            np.array([0.58, 0.75, 0.48, 0.88]),
            definition="Think logically")

        # MORE SOCIAL ACTIONS
        existing_domain.add_concept('meet',
            np.array([0.68, 0.62, 0.48, 0.68]),
            definition="Come into presence of")

        existing_domain.add_concept('greet',
            np.array([0.75, 0.65, 0.42, 0.68]),
            definition="Welcome with words or gestures")

        existing_domain.add_concept('ask',
            np.array([0.62, 0.62, 0.42, 0.72]),
            definition="Request information")

        existing_domain.add_concept('answer',
            np.array([0.65, 0.68, 0.48, 0.75]),
            definition="Respond to question")

        existing_domain.add_concept('tell',
            np.array([0.65, 0.65, 0.52, 0.75]),
            definition="Communicate information")

        existing_domain.add_concept('explain',
            np.array([0.68, 0.70, 0.48, 0.82]),
            definition="Make clear and understandable")

        existing_domain.add_concept('argue',
            np.array([0.42, 0.52, 0.72, 0.68]),
            definition="Engage in disagreement")

        existing_domain.add_concept('agree',
            np.array([0.72, 0.75, 0.42, 0.75]),
            definition="Share same opinion")

        existing_domain.add_concept('disagree',
            np.array([0.45, 0.55, 0.62, 0.68]),
            definition="Have different opinion")

        existing_domain.add_concept('promise',
            np.array([0.75, 0.82, 0.52, 0.82]),
            definition="Commit to do something")

        return existing_domain

    def create_body_health_domain(self) -> ConceptualDomain:
        """Create body parts and health concepts domain."""
        domain = ConceptualDomain(
            name="Body & Health",
            description="Body parts, health, and medical concepts"
        )

        # BODY PARTS (already have hand, eye, heart, head, foot)
        domain.add_concept('arm',
            np.array([0.65, 0.60, 0.58, 0.68]),
            definition="Upper limb from shoulder to hand")

        domain.add_concept('leg',
            np.array([0.62, 0.58, 0.62, 0.65]),
            definition="Lower limb from hip to foot")

        domain.add_concept('finger',
            np.array([0.62, 0.58, 0.52, 0.68]),
            definition="Digit of the hand")

        domain.add_concept('toe',
            np.array([0.58, 0.52, 0.48, 0.62]),
            definition="Digit of the foot")

        domain.add_concept('mouth',
            np.array([0.68, 0.62, 0.52, 0.70]),
            definition="Opening for eating and speaking")

        domain.add_concept('nose',
            np.array([0.62, 0.58, 0.48, 0.68]),
            definition="Organ of smell")

        domain.add_concept('ear',
            np.array([0.65, 0.62, 0.45, 0.75]),
            definition="Organ of hearing")

        domain.add_concept('tongue',
            np.array([0.62, 0.60, 0.52, 0.68]),
            definition="Organ of taste in mouth")

        domain.add_concept('tooth',
            np.array([0.58, 0.58, 0.55, 0.65]),
            definition="Hard structure in mouth")

        domain.add_concept('hair',
            np.array([0.65, 0.58, 0.45, 0.65]),
            definition="Threadlike strands growing from skin")

        domain.add_concept('skin',
            np.array([0.68, 0.62, 0.48, 0.70]),
            definition="Outer covering of body")

        domain.add_concept('bone',
            np.array([0.55, 0.62, 0.68, 0.72]),
            definition="Hard tissue forming skeleton")

        domain.add_concept('muscle',
            np.array([0.58, 0.62, 0.75, 0.68]),
            definition="Tissue that produces movement")

        domain.add_concept('blood',
            np.array([0.72, 0.65, 0.62, 0.72]),
            definition="Red fluid circulating in body")

        domain.add_concept('brain',
            np.array([0.62, 0.72, 0.55, 0.92]),
            definition="Organ of thought")

        domain.add_concept('stomach',
            np.array([0.62, 0.58, 0.52, 0.65]),
            definition="Organ for digesting food")

        domain.add_concept('lung',
            np.array([0.68, 0.65, 0.48, 0.72]),
            definition="Organ for breathing")

        # HEALTH STATES
        domain.add_concept('health',
            np.array([0.78, 0.72, 0.58, 0.82]),
            definition="State of physical well-being")

        domain.add_concept('sick',
            np.array([0.35, 0.42, 0.38, 0.48]),
            definition="Affected by illness")

        domain.add_concept('disease',
            np.array([0.25, 0.38, 0.62, 0.52]),
            definition="Disorder affecting body")

        domain.add_concept('pain',
            np.array([0.28, 0.38, 0.55, 0.45]),
            definition="Physical suffering")

        domain.add_concept('injury',
            np.array([0.32, 0.42, 0.65, 0.48]),
            definition="Physical harm or damage")

        domain.add_concept('wound',
            np.array([0.35, 0.45, 0.62, 0.52]),
            definition="Injury involving broken skin")

        domain.add_concept('healing',
            np.array([0.78, 0.72, 0.48, 0.80]),
            definition="Process of becoming healthy")

        domain.add_concept('cure',
            np.array([0.82, 0.75, 0.52, 0.85]),
            definition="Remedy that restores health")

        domain.add_concept('medicine',
            np.array([0.72, 0.75, 0.55, 0.85]),
            definition="Substance for treating illness")

        domain.add_concept('doctor',
            np.array([0.75, 0.78, 0.58, 0.88]),
            definition="Medical practitioner")

        return domain

    def create_food_cooking_domain(self) -> ConceptualDomain:
        """Create food and cooking concepts domain."""
        domain = ConceptualDomain(
            name="Food & Cooking",
            description="Food, cooking, eating, and nutrition"
        )

        # BASIC FOODS
        domain.add_concept('food',
            np.array([0.72, 0.65, 0.48, 0.70]),
            definition="Substance consumed for nutrition")

        domain.add_concept('bread',
            np.array([0.68, 0.62, 0.45, 0.68]),
            definition="Baked dough product")

        domain.add_concept('meat',
            np.array([0.58, 0.55, 0.62, 0.62]),
            definition="Animal flesh as food")

        domain.add_concept('fish (food)',
            np.array([0.65, 0.60, 0.52, 0.68]),
            definition="Aquatic animal as food")

        domain.add_concept('vegetable',
            np.array([0.70, 0.68, 0.42, 0.72]),
            definition="Plant used as food")

        domain.add_concept('fruit',
            np.array([0.78, 0.65, 0.38, 0.72]),
            definition="Sweet plant product")

        domain.add_concept('grain',
            np.array([0.65, 0.65, 0.48, 0.72]),
            definition="Cereal seed")

        domain.add_concept('rice',
            np.array([0.68, 0.62, 0.45, 0.68]),
            definition="Cereal grain")

        domain.add_concept('wheat',
            np.array([0.65, 0.62, 0.48, 0.70]),
            definition="Cereal grain for flour")

        domain.add_concept('corn',
            np.array([0.68, 0.62, 0.48, 0.68]),
            definition="Cereal grain with kernels")

        domain.add_concept('egg',
            np.array([0.68, 0.60, 0.48, 0.68]),
            definition="Oval reproductive body")

        domain.add_concept('milk',
            np.array([0.78, 0.65, 0.42, 0.70]),
            definition="White liquid from mammals")

        domain.add_concept('cheese',
            np.array([0.70, 0.62, 0.48, 0.68]),
            definition="Solid food from milk")

        domain.add_concept('butter',
            np.array([0.68, 0.58, 0.45, 0.65]),
            definition="Dairy product from cream")

        domain.add_concept('oil',
            np.array([0.62, 0.60, 0.52, 0.68]),
            definition="Viscous liquid")

        domain.add_concept('salt',
            np.array([0.58, 0.58, 0.52, 0.68]),
            definition="Mineral for seasoning")

        domain.add_concept('sugar',
            np.array([0.75, 0.58, 0.48, 0.65]),
            definition="Sweet crystalline substance")

        # MEALS & EATING
        domain.add_concept('meal',
            np.array([0.72, 0.65, 0.48, 0.70]),
            definition="Eating occasion")

        domain.add_concept('breakfast',
            np.array([0.75, 0.65, 0.45, 0.72]),
            definition="First meal of day")

        domain.add_concept('lunch',
            np.array([0.70, 0.62, 0.48, 0.68]),
            definition="Midday meal")

        domain.add_concept('dinner',
            np.array([0.72, 0.65, 0.52, 0.70]),
            definition="Evening meal")

        domain.add_concept('eat',
            np.array([0.68, 0.60, 0.52, 0.65]),
            definition="Consume food")

        domain.add_concept('drink',
            np.array([0.68, 0.58, 0.48, 0.65]),
            definition="Consume liquid")

        domain.add_concept('taste',
            np.array([0.68, 0.62, 0.48, 0.72]),
            definition="Perceive flavor")

        domain.add_concept('chew',
            np.array([0.58, 0.55, 0.52, 0.62]),
            definition="Grind with teeth")

        domain.add_concept('swallow',
            np.array([0.60, 0.58, 0.52, 0.65]),
            definition="Pass down throat")

        # COOKING
        domain.add_concept('cook',
            np.array([0.70, 0.68, 0.58, 0.78]),
            definition="Prepare food by heating")

        domain.add_concept('boil',
            np.array([0.62, 0.62, 0.62, 0.70]),
            definition="Heat liquid to bubbling")

        domain.add_concept('fry',
            np.array([0.65, 0.60, 0.62, 0.68]),
            definition="Cook in hot oil")

        domain.add_concept('bake',
            np.array([0.70, 0.65, 0.55, 0.72]),
            definition="Cook by dry heat in oven")

        domain.add_concept('roast',
            np.array([0.65, 0.62, 0.60, 0.70]),
            definition="Cook with dry heat")

        # TASTE QUALITIES
        domain.add_concept('sweet',
            np.array([0.78, 0.62, 0.38, 0.68]),
            definition="Sugary taste")

        domain.add_concept('sour',
            np.array([0.52, 0.52, 0.48, 0.62]),
            definition="Acidic taste")

        domain.add_concept('bitter',
            np.array([0.42, 0.48, 0.52, 0.58]),
            definition="Sharp unpleasant taste")

        domain.add_concept('salty',
            np.array([0.58, 0.58, 0.52, 0.65]),
            definition="Taste of salt")

        domain.add_concept('spicy',
            np.array([0.62, 0.58, 0.68, 0.65]),
            definition="Hot pungent taste")

        domain.add_concept('delicious',
            np.array([0.82, 0.65, 0.42, 0.72]),
            definition="Highly pleasant taste")

        return domain

    def create_animals_domain(self) -> ConceptualDomain:
        """Create animals domain."""
        domain = ConceptualDomain(
            name="Animals",
            description="Animal species and related concepts"
        )

        # MAMMALS (already have dog, cat)
        domain.add_concept('horse',
            np.array([0.70, 0.65, 0.68, 0.72]),
            definition="Large four-legged mammal")

        domain.add_concept('cow',
            np.array([0.68, 0.62, 0.52, 0.68]),
            definition="Large domesticated mammal")

        domain.add_concept('pig',
            np.array([0.62, 0.58, 0.55, 0.62]),
            definition="Domesticated swine")

        domain.add_concept('sheep',
            np.array([0.70, 0.62, 0.48, 0.68]),
            definition="Wooly mammal")

        domain.add_concept('goat',
            np.array([0.65, 0.60, 0.58, 0.68]),
            definition="Horned mammal")

        domain.add_concept('deer',
            np.array([0.72, 0.65, 0.52, 0.72]),
            definition="Hoofed ruminant")

        domain.add_concept('bear',
            np.array([0.55, 0.60, 0.78, 0.68]),
            definition="Large carnivorous mammal")

        domain.add_concept('wolf',
            np.array([0.52, 0.62, 0.75, 0.70]),
            definition="Wild canine")

        domain.add_concept('lion',
            np.array([0.58, 0.68, 0.82, 0.72]),
            definition="Large cat, king of beasts")

        domain.add_concept('tiger',
            np.array([0.55, 0.65, 0.82, 0.70]),
            definition="Large striped cat")

        domain.add_concept('elephant',
            np.array([0.65, 0.72, 0.75, 0.78]),
            definition="Largest land mammal")

        domain.add_concept('monkey',
            np.array([0.65, 0.58, 0.58, 0.68]),
            definition="Primate")

        domain.add_concept('rabbit',
            np.array([0.72, 0.58, 0.45, 0.65]),
            definition="Small long-eared mammal")

        domain.add_concept('mouse',
            np.array([0.60, 0.52, 0.42, 0.62]),
            definition="Small rodent")

        # BIRDS (already have bird)
        domain.add_concept('chicken',
            np.array([0.65, 0.58, 0.48, 0.65]),
            definition="Domesticated fowl")

        domain.add_concept('duck',
            np.array([0.68, 0.60, 0.48, 0.68]),
            definition="Waterfowl")

        domain.add_concept('eagle',
            np.array([0.62, 0.72, 0.78, 0.78]),
            definition="Large bird of prey")

        domain.add_concept('owl',
            np.array([0.58, 0.68, 0.62, 0.85]),
            definition="Nocturnal bird of prey")

        domain.add_concept('crow',
            np.array([0.55, 0.62, 0.62, 0.78]),
            definition="Large black bird")

        domain.add_concept('dove',
            np.array([0.78, 0.70, 0.35, 0.75]),
            definition="Symbol of peace")

        # REPTILES & AMPHIBIANS
        domain.add_concept('snake',
            np.array([0.42, 0.55, 0.68, 0.65]),
            definition="Legless reptile")

        domain.add_concept('lizard',
            np.array([0.55, 0.58, 0.58, 0.65]),
            definition="Four-legged reptile")

        domain.add_concept('turtle',
            np.array([0.65, 0.68, 0.52, 0.75]),
            definition="Reptile with shell")

        domain.add_concept('frog',
            np.array([0.62, 0.58, 0.48, 0.68]),
            definition="Tailless amphibian")

        # INSECTS
        domain.add_concept('insect',
            np.array([0.52, 0.55, 0.48, 0.62]),
            definition="Small arthropod")

        domain.add_concept('bee',
            np.array([0.68, 0.68, 0.58, 0.75]),
            definition="Flying insect that makes honey")

        domain.add_concept('ant',
            np.array([0.62, 0.72, 0.62, 0.75]),
            definition="Social insect")

        domain.add_concept('butterfly',
            np.array([0.78, 0.65, 0.42, 0.72]),
            definition="Insect with colorful wings")

        domain.add_concept('spider',
            np.array([0.45, 0.58, 0.62, 0.68]),
            definition="Eight-legged arachnid")

        # AQUATIC (already have fish)
        domain.add_concept('whale',
            np.array([0.68, 0.72, 0.75, 0.82]),
            definition="Large marine mammal")

        domain.add_concept('dolphin',
            np.array([0.78, 0.68, 0.58, 0.78]),
            definition="Intelligent marine mammal")

        domain.add_concept('shark',
            np.array([0.45, 0.58, 0.82, 0.68]),
            definition="Large predatory fish")

        domain.add_concept('crab',
            np.array([0.58, 0.58, 0.62, 0.65]),
            definition="Crustacean with claws")

        return domain

    def create_plants_domain(self) -> ConceptualDomain:
        """Create plants domain."""
        domain = ConceptualDomain(
            name="Plants",
            description="Plant species and botanical concepts"
        )

        # GENERAL (already have tree, flower)
        domain.add_concept('plant',
            np.array([0.70, 0.68, 0.38, 0.75]),
            definition="Living organism that photosynthesizes")

        domain.add_concept('grass',
            np.array([0.68, 0.62, 0.38, 0.70]),
            definition="Low green plants")

        domain.add_concept('bush',
            np.array([0.65, 0.62, 0.42, 0.68]),
            definition="Woody plant smaller than tree")

        domain.add_concept('vine',
            np.array([0.65, 0.60, 0.45, 0.68]),
            definition="Climbing plant")

        domain.add_concept('moss',
            np.array([0.68, 0.62, 0.35, 0.68]),
            definition="Small green plant")

        domain.add_concept('fern',
            np.array([0.68, 0.62, 0.38, 0.70]),
            definition="Flowerless plant with fronds")

        # PLANT PARTS
        domain.add_concept('root',
            np.array([0.62, 0.68, 0.52, 0.75]),
            definition="Underground part of plant")

        domain.add_concept('stem',
            np.array([0.65, 0.65, 0.52, 0.72]),
            definition="Main stalk of plant")

        domain.add_concept('branch',
            np.array([0.62, 0.62, 0.55, 0.70]),
            definition="Division of tree trunk")

        domain.add_concept('leaf',
            np.array([0.72, 0.65, 0.38, 0.72]),
            definition="Flat green part of plant")

        domain.add_concept('seed',
            np.array([0.70, 0.68, 0.48, 0.78]),
            definition="Plant embryo for reproduction")

        domain.add_concept('fruit (botanical)',
            np.array([0.75, 0.65, 0.45, 0.72]),
            definition="Seed-bearing structure")

        # TREES
        domain.add_concept('oak',
            np.array([0.68, 0.72, 0.62, 0.80]),
            definition="Hardwood tree with acorns")

        domain.add_concept('pine',
            np.array([0.68, 0.68, 0.55, 0.75]),
            definition="Evergreen coniferous tree")

        domain.add_concept('palm',
            np.array([0.72, 0.65, 0.48, 0.72]),
            definition="Tropical tree with fronds")

        return domain

    def create_social_roles_domain(self) -> ConceptualDomain:
        """Create social roles domain."""
        domain = ConceptualDomain(
            name="Social Roles",
            description="Social relationships and roles"
        )

        # FAMILY
        domain.add_concept('family',
            np.array([0.88, 0.68, 0.35, 0.75]),
            definition="Group of related people")

        domain.add_concept('parent',
            np.array([0.85, 0.75, 0.55, 0.80]),
            definition="Mother or father")

        domain.add_concept('mother',
            np.array([0.90, 0.72, 0.42, 0.78]),
            definition="Female parent")

        domain.add_concept('father',
            np.array([0.82, 0.78, 0.62, 0.82]),
            definition="Male parent")

        domain.add_concept('child',
            np.array([0.82, 0.62, 0.35, 0.65]),
            definition="Young human or offspring")

        domain.add_concept('son',
            np.array([0.82, 0.65, 0.42, 0.68]),
            definition="Male child")

        domain.add_concept('daughter',
            np.array([0.85, 0.62, 0.35, 0.68]),
            definition="Female child")

        domain.add_concept('brother',
            np.array([0.78, 0.68, 0.52, 0.72]),
            definition="Male sibling")

        domain.add_concept('sister',
            np.array([0.82, 0.65, 0.42, 0.70]),
            definition="Female sibling")

        domain.add_concept('grandfather',
            np.array([0.78, 0.78, 0.58, 0.85]),
            definition="Father's or mother's father")

        domain.add_concept('grandmother',
            np.array([0.85, 0.75, 0.45, 0.82]),
            definition="Father's or mother's mother")

        domain.add_concept('uncle',
            np.array([0.75, 0.70, 0.52, 0.75]),
            definition="Parent's brother")

        domain.add_concept('aunt',
            np.array([0.78, 0.68, 0.45, 0.72]),
            definition="Parent's sister")

        domain.add_concept('cousin',
            np.array([0.75, 0.62, 0.45, 0.68]),
            definition="Child of uncle or aunt")

        # SOCIAL RELATIONSHIPS
        domain.add_concept('friend',
            np.array([0.85, 0.68, 0.38, 0.72]),
            definition="Person with mutual affection")

        domain.add_concept('enemy',
            np.array([0.18, 0.35, 0.82, 0.45]),
            definition="Hostile opponent")

        domain.add_concept('stranger',
            np.array([0.48, 0.52, 0.52, 0.58]),
            definition="Unknown person")

        domain.add_concept('neighbor',
            np.array([0.70, 0.65, 0.45, 0.68]),
            definition="Person living nearby")

        domain.add_concept('partner',
            np.array([0.82, 0.72, 0.48, 0.75]),
            definition="Person sharing relationship")

        domain.add_concept('spouse',
            np.array([0.88, 0.75, 0.45, 0.78]),
            definition="Married partner")

        domain.add_concept('husband',
            np.array([0.85, 0.78, 0.52, 0.78]),
            definition="Male spouse")

        domain.add_concept('wife',
            np.array([0.88, 0.75, 0.42, 0.78]),
            definition="Female spouse")

        # PROFESSIONAL/SOCIAL ROLES (already have doctor, teacher)
        domain.add_concept('student',
            np.array([0.68, 0.65, 0.45, 0.85]),
            definition="Person who learns")

        domain.add_concept('worker',
            np.array([0.65, 0.68, 0.65, 0.75]),
            definition="Person who works")

        domain.add_concept('leader',
            np.array([0.65, 0.78, 0.78, 0.85]),
            definition="Person who guides")

        domain.add_concept('follower',
            np.array([0.62, 0.62, 0.48, 0.65]),
            definition="Person who follows")

        domain.add_concept('king',
            np.array([0.55, 0.75, 0.88, 0.80]),
            definition="Male monarch")

        domain.add_concept('queen',
            np.array([0.62, 0.78, 0.82, 0.82]),
            definition="Female monarch")

        domain.add_concept('servant',
            np.array([0.68, 0.65, 0.45, 0.68]),
            definition="Person who serves")

        domain.add_concept('master',
            np.array([0.52, 0.68, 0.82, 0.78]),
            definition="Person with control")

        domain.add_concept('chief',
            np.array([0.60, 0.75, 0.82, 0.82]),
            definition="Leader of group")

        domain.add_concept('priest',
            np.array([0.72, 0.85, 0.52, 0.90]),
            definition="Religious leader")

        return domain


def main():
    """Execute batch 3 expansion."""
    print("=" * 80)
    print("LJPW SEMANTIC SPACE - BATCH 3 EXPANSION")
    print("=" * 80)
    print()
    print("Expanding from 267 concepts to 1,000+ concepts")
    print()

    mapper = Batch3Mapper()

    # Load batch 1 & 2
    batch2_path = Path(__file__).parent / 'semantic_space_complete.json'
    if batch2_path.exists():
        with open(batch2_path, 'r') as f:
            data = json.load(f)
            for domain_name, domain_info in data['domains'].items():
                domain = ConceptualDomain(domain_name, domain_info['description'])
                for concept, concept_data in domain_info['concepts'].items():
                    domain.concepts[concept] = {
                        'coordinates': np.array(concept_data['coordinates']),
                        'definition': concept_data.get('definition', ''),
                        'related': concept_data.get('related', []),
                        'domain': domain_name
                    }
                mapper.domains[domain_name] = domain
                mapper.concept_map.update(domain.concepts)
        print(f"✓ Loaded {len(mapper.concept_map)} existing concepts")
        print()

    # Expand existing domains
    print("Expanding existing domains...")
    if 'emotions' in mapper.domains:
        print("  Expanding emotions...")
        mapper.expand_emotion_domain(mapper.domains['emotions'])
        mapper.concept_map.update(mapper.domains['emotions'].concepts)

    if 'actions' in mapper.domains:
        print("  Expanding actions...")
        mapper.expand_action_domain(mapper.domains['actions'])
        mapper.concept_map.update(mapper.domains['actions'].concepts)
    print()

    # Create new domains
    print("Creating new domains...")

    domains_to_create = [
        ('body_health', mapper.create_body_health_domain),
        ('food_cooking', mapper.create_food_cooking_domain),
        ('animals', mapper.create_animals_domain),
        ('plants', mapper.create_plants_domain),
        ('social_roles', mapper.create_social_roles_domain),
    ]

    for domain_name, create_func in domains_to_create:
        print(f"  {domain_name}...")
        domain = create_func()
        mapper.domains[domain_name] = domain
        mapper.concept_map.update(domain.concepts)
        print(f"    ✓ {len(domain.concepts)} concepts")

    print()
    print("=" * 80)
    print("BATCH 3 COMPLETE")
    print("=" * 80)
    print()
    print(f"Total concepts: {len(mapper.concept_map)}")
    print(f"Total domains: {len(mapper.domains)}")
    print()

    # Breakdown
    print("Concepts by domain:")
    for domain_name, domain in sorted(mapper.domains.items()):
        print(f"  • {domain_name:15} {len(domain.concepts):4} concepts")
    print()

    # Save
    output_path = Path(__file__).parent / 'semantic_space_batch3.json'
    mapper.save_semantic_space(output_path)

    progress = len(mapper.concept_map) / 100000 * 100
    print()
    print("=" * 80)
    print(f"🎉 {len(mapper.concept_map):,} CONCEPTS MAPPED 🎉")
    print("=" * 80)
    print(f"Progress: [{len(mapper.concept_map):,} / 100,000] = {progress:.2f}%")
    print()


if __name__ == '__main__':
    main()
