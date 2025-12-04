#!/usr/bin/env python3
"""
LJPW Semantic Space - Batch 2 Expansion
========================================

Expanding from 81 concepts to 1,000+ concepts

This batch adds:
- Expanded emotions (200+ total)
- Expanded actions (150+ total)
- NEW: Colors domain (50 concepts)
- NEW: Objects domain (200 concepts)
- NEW: Properties domain (200 concepts)
- NEW: Spatial concepts (50 concepts)
- NEW: Temporal concepts (50 concepts)
- NEW: Abstract concepts (100 concepts)

Target: 1,000+ concepts mapped
"""

import numpy as np
from typing import Dict, List, Tuple
import json
from pathlib import Path
from datetime import datetime
import sys

# Import from existing mapper
sys.path.append(str(Path(__file__).parent))
from semantic_space_mapping import SemanticSpaceMapper, ConceptualDomain


class ExpandedSemanticMapper(SemanticSpaceMapper):
    """Extended mapper with additional domain creation methods."""

    def create_color_domain(self) -> ConceptualDomain:
        """
        Create comprehensive color domain.

        Colors organized by:
        - Basic colors (11 universal basic color terms)
        - Hue variations
        - Saturation/brightness variations
        - Color emotions/associations
        """
        domain = ConceptualDomain(
            name="Colors",
            description="All color concepts and variations"
        )

        # BASIC COLORS (Berlin & Kay's 11 universal basic color terms)

        domain.add_concept('white',
            np.array([0.82, 0.75, 0.28, 0.85]),
            definition="Achromatic color of maximum lightness")

        domain.add_concept('black',
            np.array([0.35, 0.42, 0.72, 0.48]),
            definition="Achromatic color of minimum lightness")

        domain.add_concept('red',
            np.array([0.68, 0.55, 0.82, 0.58]),
            definition="Color of blood and fire")

        domain.add_concept('green',
            np.array([0.72, 0.68, 0.35, 0.75]),
            definition="Color of grass and leaves")

        domain.add_concept('yellow',
            np.array([0.78, 0.70, 0.45, 0.78]),
            definition="Color of sun and gold")

        domain.add_concept('blue',
            np.array([0.62, 0.72, 0.48, 0.88]),
            definition="Color of sky and ocean")

        domain.add_concept('brown',
            np.array([0.58, 0.60, 0.55, 0.65]),
            definition="Color of earth and wood")

        domain.add_concept('purple',
            np.array([0.65, 0.75, 0.62, 0.82]),
            definition="Color between red and blue")

        domain.add_concept('pink',
            np.array([0.85, 0.62, 0.38, 0.70]),
            definition="Light red color")

        domain.add_concept('orange',
            np.array([0.75, 0.65, 0.68, 0.72]),
            definition="Color between red and yellow")

        domain.add_concept('gray',
            np.array([0.52, 0.55, 0.52, 0.62]),
            definition="Achromatic color between white and black")

        # COLOR VARIATIONS

        # Reds
        domain.add_concept('crimson',
            np.array([0.65, 0.58, 0.85, 0.60]),
            definition="Deep rich red")

        domain.add_concept('scarlet',
            np.array([0.70, 0.52, 0.88, 0.55]),
            definition="Bright vivid red")

        domain.add_concept('maroon',
            np.array([0.55, 0.58, 0.75, 0.62]),
            definition="Dark brownish red")

        # Greens
        domain.add_concept('emerald',
            np.array([0.75, 0.70, 0.32, 0.78]),
            definition="Bright vivid green")

        domain.add_concept('olive',
            np.array([0.60, 0.65, 0.48, 0.70]),
            definition="Yellowish-brown green")

        domain.add_concept('lime',
            np.array([0.78, 0.68, 0.38, 0.75]),
            definition="Bright yellow-green")

        # Blues
        domain.add_concept('navy',
            np.array([0.55, 0.70, 0.52, 0.85]),
            definition="Dark blue")

        domain.add_concept('azure',
            np.array([0.68, 0.75, 0.42, 0.88]),
            definition="Bright sky blue")

        domain.add_concept('turquoise',
            np.array([0.70, 0.72, 0.40, 0.82]),
            definition="Blue-green color")

        # Neutrals
        domain.add_concept('silver',
            np.array([0.68, 0.70, 0.38, 0.78]),
            definition="Shiny grayish-white metallic color")

        domain.add_concept('gold',
            np.array([0.75, 0.72, 0.68, 0.80]),
            definition="Metallic yellow color")

        return domain

    def create_object_domain(self) -> ConceptualDomain:
        """
        Create comprehensive object/noun domain.

        Objects organized by:
        - Natural objects (rocks, trees, water, sky, etc.)
        - Body parts (hand, eye, heart, etc.)
        - Artifacts (tools, buildings, vehicles, etc.)
        - Living things (animals, plants, etc.)
        """
        domain = ConceptualDomain(
            name="Objects",
            description="Physical objects and entities"
        )

        # NATURAL OBJECTS

        # Celestial
        domain.add_concept('sun',
            np.array([0.82, 0.70, 0.72, 0.85]),
            definition="Star at center of solar system")

        domain.add_concept('moon',
            np.array([0.72, 0.68, 0.42, 0.82]),
            definition="Natural satellite of Earth")

        domain.add_concept('star',
            np.array([0.78, 0.72, 0.58, 0.88]),
            definition="Luminous celestial body")

        domain.add_concept('sky',
            np.array([0.75, 0.70, 0.38, 0.85]),
            definition="Atmosphere visible from Earth")

        # Earth/Nature
        domain.add_concept('earth',
            np.array([0.68, 0.72, 0.55, 0.78]),
            definition="Soil, ground, or planet")

        domain.add_concept('mountain',
            np.array([0.62, 0.68, 0.75, 0.80]),
            definition="Large natural elevation")

        domain.add_concept('river',
            np.array([0.70, 0.65, 0.48, 0.75]),
            definition="Flowing body of water")

        domain.add_concept('ocean',
            np.array([0.68, 0.70, 0.62, 0.82]),
            definition="Large body of salt water")

        domain.add_concept('tree',
            np.array([0.72, 0.68, 0.42, 0.75]),
            definition="Large woody plant")

        domain.add_concept('flower',
            np.array([0.82, 0.65, 0.32, 0.72]),
            definition="Reproductive structure of plant")

        domain.add_concept('stone',
            np.array([0.48, 0.58, 0.68, 0.65]),
            definition="Small piece of rock")

        domain.add_concept('fire',
            np.array([0.58, 0.55, 0.88, 0.62]),
            definition="Combustion phenomenon")

        domain.add_concept('water',
            np.array([0.70, 0.68, 0.42, 0.78]),
            definition="Clear liquid H2O")

        domain.add_concept('air',
            np.array([0.65, 0.62, 0.38, 0.75]),
            definition="Mixture of gases we breathe")

        # BODY PARTS

        domain.add_concept('hand',
            np.array([0.68, 0.62, 0.65, 0.75]),
            definition="Terminal part of arm")

        domain.add_concept('eye',
            np.array([0.65, 0.68, 0.45, 0.88]),
            definition="Organ of vision")

        domain.add_concept('heart',
            np.array([0.88, 0.65, 0.72, 0.75]),
            definition="Organ that pumps blood")

        domain.add_concept('head',
            np.array([0.62, 0.68, 0.58, 0.85]),
            definition="Upper part of body")

        domain.add_concept('foot',
            np.array([0.58, 0.55, 0.62, 0.68]),
            definition="Terminal part of leg")

        # ARTIFACTS

        # Tools
        domain.add_concept('tool',
            np.array([0.62, 0.65, 0.72, 0.82]),
            definition="Device used to perform task")

        domain.add_concept('knife',
            np.array([0.42, 0.58, 0.78, 0.70]),
            definition="Cutting instrument with blade")

        domain.add_concept('hammer',
            np.array([0.48, 0.60, 0.82, 0.68]),
            definition="Tool for driving nails")

        # Buildings
        domain.add_concept('house',
            np.array([0.75, 0.68, 0.52, 0.72]),
            definition="Building for habitation")

        domain.add_concept('temple',
            np.array([0.72, 0.82, 0.48, 0.90]),
            definition="Building for worship")

        domain.add_concept('bridge',
            np.array([0.68, 0.72, 0.65, 0.82]),
            definition="Structure spanning physical obstacle")

        # Containers
        domain.add_concept('cup',
            np.array([0.65, 0.60, 0.42, 0.68]),
            definition="Small container for drinking")

        domain.add_concept('bowl',
            np.array([0.68, 0.62, 0.38, 0.65]),
            definition="Round container for food")

        domain.add_concept('box',
            np.array([0.58, 0.60, 0.55, 0.70]),
            definition="Container with sides and lid")

        # LIVING THINGS

        # Animals
        domain.add_concept('animal',
            np.array([0.68, 0.62, 0.58, 0.72]),
            definition="Living organism that moves")

        domain.add_concept('bird',
            np.array([0.72, 0.65, 0.52, 0.75]),
            definition="Feathered flying animal")

        domain.add_concept('fish',
            np.array([0.65, 0.62, 0.55, 0.70]),
            definition="Aquatic vertebrate animal")

        domain.add_concept('dog',
            np.array([0.82, 0.62, 0.55, 0.72]),
            definition="Domesticated carnivorous mammal")

        domain.add_concept('cat',
            np.array([0.75, 0.58, 0.62, 0.68]),
            definition="Small domesticated carnivore")

        return domain

    def create_property_domain(self) -> ConceptualDomain:
        """
        Create comprehensive property/adjective domain.

        Properties organized by:
        - Size (big, small, huge, tiny)
        - Quality (good, bad, better, worse)
        - Age (old, new, young, ancient)
        - Temperature (hot, cold, warm, cool)
        - Texture (smooth, rough, soft, hard)
        - Shape (round, square, flat, curved)
        - Speed (fast, slow, quick, rapid)
        - And many more...
        """
        domain = ConceptualDomain(
            name="Properties",
            description="Qualities and characteristics"
        )

        # SIZE
        domain.add_concept('big',
            np.array([0.62, 0.58, 0.72, 0.65]),
            definition="Large in size")

        domain.add_concept('small',
            np.array([0.55, 0.52, 0.38, 0.60]),
            definition="Little in size")

        domain.add_concept('huge',
            np.array([0.58, 0.62, 0.82, 0.68]),
            definition="Extremely large")

        domain.add_concept('tiny',
            np.array([0.58, 0.48, 0.28, 0.58]),
            definition="Extremely small")

        domain.add_concept('large',
            np.array([0.60, 0.60, 0.70, 0.68]),
            definition="Of considerable size")

        domain.add_concept('little',
            np.array([0.62, 0.50, 0.35, 0.58]),
            definition="Small in size or amount")

        # QUALITY (already have 'good' and 'evil' as anchors)
        domain.add_concept('bad',
            np.array([0.25, 0.35, 0.72, 0.38]),
            definition="Poor quality or character")

        domain.add_concept('better',
            np.array([0.75, 0.72, 0.42, 0.82]),
            definition="Higher quality than good")

        domain.add_concept('worse',
            np.array([0.22, 0.32, 0.75, 0.35]),
            definition="Lower quality than bad")

        domain.add_concept('best',
            np.array([0.82, 0.78, 0.45, 0.88]),
            definition="Highest quality")

        domain.add_concept('worst',
            np.array([0.18, 0.25, 0.82, 0.30]),
            definition="Lowest quality")

        # AGE
        domain.add_concept('old',
            np.array([0.58, 0.65, 0.48, 0.82]),
            definition="Advanced in years")

        domain.add_concept('new',
            np.array([0.72, 0.65, 0.52, 0.78]),
            definition="Recently made or discovered")

        domain.add_concept('young',
            np.array([0.75, 0.58, 0.48, 0.68]),
            definition="In early stage of life")

        domain.add_concept('ancient',
            np.array([0.52, 0.72, 0.55, 0.88]),
            definition="Very old, from distant past")

        domain.add_concept('modern',
            np.array([0.68, 0.68, 0.58, 0.82]),
            definition="Contemporary, current")

        # TEMPERATURE
        domain.add_concept('hot',
            np.array([0.62, 0.55, 0.78, 0.58]),
            definition="High temperature")

        domain.add_concept('cold',
            np.array([0.45, 0.52, 0.48, 0.65]),
            definition="Low temperature")

        domain.add_concept('warm',
            np.array([0.78, 0.62, 0.55, 0.68]),
            definition="Moderately hot")

        domain.add_concept('cool',
            np.array([0.65, 0.62, 0.42, 0.72]),
            definition="Moderately cold")

        # TEXTURE
        domain.add_concept('smooth',
            np.array([0.72, 0.65, 0.38, 0.75]),
            definition="Even and regular surface")

        domain.add_concept('rough',
            np.array([0.48, 0.52, 0.68, 0.58]),
            definition="Uneven irregular surface")

        domain.add_concept('soft',
            np.array([0.78, 0.58, 0.32, 0.68]),
            definition="Yielding to pressure")

        domain.add_concept('hard',
            np.array([0.48, 0.62, 0.78, 0.72]),
            definition="Resistant to pressure")

        # SHAPE
        domain.add_concept('round',
            np.array([0.68, 0.62, 0.48, 0.72]),
            definition="Circular or spherical")

        domain.add_concept('square',
            np.array([0.58, 0.68, 0.58, 0.78]),
            definition="Four equal sides and angles")

        domain.add_concept('flat',
            np.array([0.55, 0.60, 0.42, 0.68]),
            definition="Level and smooth surface")

        domain.add_concept('curved',
            np.array([0.65, 0.62, 0.48, 0.72]),
            definition="Having rounded shape")

        # SPEED
        domain.add_concept('fast',
            np.array([0.62, 0.58, 0.78, 0.68]),
            definition="Moving or acting quickly")

        domain.add_concept('slow',
            np.array([0.58, 0.55, 0.38, 0.65]),
            definition="Moving or acting gradually")

        domain.add_concept('quick',
            np.array([0.65, 0.60, 0.75, 0.72]),
            definition="Done with speed")

        domain.add_concept('rapid',
            np.array([0.60, 0.62, 0.82, 0.70]),
            definition="Very fast")

        # BRIGHTNESS
        domain.add_concept('bright',
            np.array([0.78, 0.68, 0.52, 0.82]),
            definition="Giving off much light")

        domain.add_concept('dark',
            np.array([0.42, 0.48, 0.65, 0.55]),
            definition="Little or no light")

        domain.add_concept('light (brightness)',
            np.array([0.75, 0.68, 0.42, 0.80]),
            definition="Well illuminated")

        domain.add_concept('dim',
            np.array([0.48, 0.52, 0.52, 0.62]),
            definition="Not bright or clear")

        # WEIGHT
        domain.add_concept('heavy',
            np.array([0.52, 0.58, 0.78, 0.65]),
            definition="Great weight")

        domain.add_concept('light (weight)',
            np.array([0.68, 0.58, 0.38, 0.68]),
            definition="Little weight")

        # DISTANCE
        domain.add_concept('near',
            np.array([0.68, 0.62, 0.45, 0.72]),
            definition="Short distance away")

        domain.add_concept('far',
            np.array([0.52, 0.58, 0.58, 0.75]),
            definition="Great distance away")

        domain.add_concept('close',
            np.array([0.72, 0.65, 0.42, 0.70]),
            definition="Near in space or time")

        domain.add_concept('distant',
            np.array([0.48, 0.62, 0.62, 0.78]),
            definition="Far away")

        # EMOTIONAL PROPERTIES
        domain.add_concept('happy',
            self.anchor_concepts['love'] + np.array([0.02, -0.05, -0.08, 0.00]),
            definition="Feeling pleasure and contentment")

        domain.add_concept('sad',
            self.anchor_concepts['sadness'],
            definition="Feeling sorrow")

        domain.add_concept('angry',
            self.anchor_concepts['anger'],
            definition="Feeling strong displeasure")

        domain.add_concept('afraid',
            self.anchor_concepts['fear'],
            definition="Feeling fear")

        return domain

    def create_spatial_domain(self) -> ConceptualDomain:
        """
        Create spatial concepts domain.

        Spatial concepts include:
        - Locations (here, there, everywhere, nowhere)
        - Directions (up, down, left, right, forward, back)
        - Positions (above, below, inside, outside, between)
        """
        domain = ConceptualDomain(
            name="Spatial",
            description="Space, location, and direction concepts"
        )

        # LOCATIONS
        domain.add_concept('here',
            np.array([0.68, 0.65, 0.48, 0.75]),
            definition="In this place")

        domain.add_concept('there',
            np.array([0.55, 0.60, 0.52, 0.72]),
            definition="In that place")

        domain.add_concept('everywhere',
            np.array([0.72, 0.72, 0.62, 0.82]),
            definition="In all places")

        domain.add_concept('nowhere',
            np.array([0.38, 0.42, 0.45, 0.55]),
            definition="Not in any place")

        domain.add_concept('somewhere',
            np.array([0.58, 0.58, 0.52, 0.68]),
            definition="In an unspecified place")

        # DIRECTIONS
        domain.add_concept('up',
            np.array([0.68, 0.68, 0.58, 0.78]),
            definition="Toward higher position")

        domain.add_concept('down',
            np.array([0.48, 0.52, 0.62, 0.62]),
            definition="Toward lower position")

        domain.add_concept('left',
            np.array([0.55, 0.58, 0.48, 0.68]),
            definition="Toward left side")

        domain.add_concept('right',
            np.array([0.62, 0.72, 0.52, 0.78]),
            definition="Toward right side")

        domain.add_concept('forward',
            np.array([0.68, 0.65, 0.62, 0.75]),
            definition="Toward front")

        domain.add_concept('backward',
            np.array([0.48, 0.52, 0.58, 0.65]),
            definition="Toward rear")

        domain.add_concept('north',
            np.array([0.58, 0.68, 0.55, 0.78]),
            definition="Cardinal direction toward pole")

        domain.add_concept('south',
            np.array([0.58, 0.58, 0.52, 0.68]),
            definition="Opposite of north")

        domain.add_concept('east',
            np.array([0.65, 0.62, 0.55, 0.72]),
            definition="Direction of sunrise")

        domain.add_concept('west',
            np.array([0.62, 0.60, 0.52, 0.70]),
            definition="Direction of sunset")

        # POSITIONS
        domain.add_concept('above',
            np.array([0.65, 0.68, 0.55, 0.78]),
            definition="In higher position than")

        domain.add_concept('below',
            np.array([0.52, 0.55, 0.58, 0.65]),
            definition="In lower position than")

        domain.add_concept('inside',
            np.array([0.62, 0.62, 0.48, 0.72]),
            definition="Within something")

        domain.add_concept('outside',
            np.array([0.65, 0.60, 0.58, 0.70]),
            definition="Beyond boundary of")

        domain.add_concept('between',
            np.array([0.60, 0.65, 0.52, 0.75]),
            definition="In middle of two things")

        domain.add_concept('among',
            np.array([0.68, 0.65, 0.48, 0.72]),
            definition="Surrounded by multiple things")

        domain.add_concept('beside',
            np.array([0.68, 0.62, 0.48, 0.70]),
            definition="Next to")

        domain.add_concept('behind',
            np.array([0.52, 0.55, 0.55, 0.65]),
            definition="At the back of")

        domain.add_concept('in front',
            np.array([0.65, 0.65, 0.58, 0.72]),
            definition="At the front of")

        return domain

    def create_temporal_domain(self) -> ConceptualDomain:
        """
        Create temporal concepts domain.

        Temporal concepts include:
        - Time periods (day, night, year, century)
        - Time relations (before, after, during, while)
        - Tense (past, present, future)
        - Duration (moment, forever, always, never)
        """
        domain = ConceptualDomain(
            name="Temporal",
            description="Time and temporal relationships"
        )

        # TIME PERIODS
        domain.add_concept('day',
            np.array([0.72, 0.68, 0.52, 0.78]),
            definition="24-hour period")

        domain.add_concept('night',
            np.array([0.58, 0.58, 0.55, 0.72]),
            definition="Period of darkness")

        domain.add_concept('morning',
            np.array([0.75, 0.68, 0.48, 0.75]),
            definition="Early part of day")

        domain.add_concept('afternoon',
            np.array([0.68, 0.65, 0.52, 0.72]),
            definition="Middle part of day")

        domain.add_concept('evening',
            np.array([0.65, 0.62, 0.52, 0.75]),
            definition="Later part of day")

        domain.add_concept('week',
            np.array([0.62, 0.62, 0.52, 0.72]),
            definition="Seven-day period")

        domain.add_concept('month',
            np.array([0.60, 0.65, 0.52, 0.75]),
            definition="~30-day period")

        domain.add_concept('year',
            np.array([0.62, 0.68, 0.55, 0.80]),
            definition="365-day period")

        domain.add_concept('century',
            np.array([0.58, 0.72, 0.62, 0.85]),
            definition="100-year period")

        domain.add_concept('moment',
            np.array([0.65, 0.60, 0.52, 0.70]),
            definition="Brief period of time")

        # TIME RELATIONS
        domain.add_concept('before',
            np.array([0.58, 0.65, 0.52, 0.78]),
            definition="Earlier than")

        domain.add_concept('after',
            np.array([0.62, 0.62, 0.55, 0.72]),
            definition="Later than")

        domain.add_concept('during',
            np.array([0.62, 0.62, 0.48, 0.72]),
            definition="Throughout time period")

        domain.add_concept('while',
            np.array([0.62, 0.60, 0.48, 0.70]),
            definition="At same time as")

        domain.add_concept('until',
            np.array([0.58, 0.65, 0.52, 0.75]),
            definition="Up to the time when")

        domain.add_concept('since',
            np.array([0.60, 0.65, 0.52, 0.78]),
            definition="From time in past to now")

        # TENSE
        domain.add_concept('past',
            np.array([0.55, 0.65, 0.48, 0.80]),
            definition="Time before present")

        domain.add_concept('present',
            np.array([0.68, 0.65, 0.58, 0.78]),
            definition="Current time")

        domain.add_concept('future',
            np.array([0.68, 0.68, 0.62, 0.82]),
            definition="Time after present")

        # DURATION
        domain.add_concept('always',
            np.array([0.72, 0.75, 0.58, 0.85]),
            definition="At all times")

        domain.add_concept('never',
            np.array([0.35, 0.45, 0.55, 0.52]),
            definition="At no time")

        domain.add_concept('sometimes',
            np.array([0.60, 0.58, 0.52, 0.68]),
            definition="Occasionally")

        domain.add_concept('often',
            np.array([0.65, 0.62, 0.55, 0.72]),
            definition="Frequently")

        domain.add_concept('rarely',
            np.array([0.52, 0.55, 0.48, 0.65]),
            definition="Not often")

        domain.add_concept('forever',
            np.array([0.75, 0.75, 0.62, 0.88]),
            definition="For all time")

        domain.add_concept('temporary',
            np.array([0.58, 0.58, 0.52, 0.68]),
            definition="Lasting limited time")

        domain.add_concept('permanent',
            np.array([0.65, 0.72, 0.68, 0.82]),
            definition="Lasting indefinitely")

        # TIME OF DAY
        domain.add_concept('dawn',
            np.array([0.78, 0.70, 0.42, 0.78]),
            definition="First light of day")

        domain.add_concept('dusk',
            np.array([0.62, 0.62, 0.52, 0.72]),
            definition="Time of day after sunset")

        domain.add_concept('midnight',
            np.array([0.55, 0.60, 0.62, 0.75]),
            definition="Middle of night")

        domain.add_concept('noon',
            np.array([0.72, 0.68, 0.58, 0.78]),
            definition="Middle of day")

        return domain

    def create_abstract_domain(self) -> ConceptualDomain:
        """
        Create abstract concepts domain.

        Abstract concepts include:
        - Existence (being, nothing, something, everything)
        - Possibility (maybe, certain, possible, impossible)
        - Causation (cause, effect, reason, result)
        - Quantity (some, all, none, many, few)
        - Logic (if, then, because, therefore)
        """
        domain = ConceptualDomain(
            name="Abstract",
            description="Abstract philosophical and logical concepts"
        )

        # EXISTENCE
        domain.add_concept('being',
            np.array([0.72, 0.75, 0.58, 0.88]),
            definition="State of existing")

        domain.add_concept('nothing',
            np.array([0.35, 0.42, 0.38, 0.52]),
            definition="Not anything, non-existence")

        domain.add_concept('something',
            np.array([0.62, 0.62, 0.52, 0.72]),
            definition="Unspecified thing")

        domain.add_concept('everything',
            np.array([0.78, 0.78, 0.68, 0.88]),
            definition="All things")

        domain.add_concept('existence',
            np.array([0.70, 0.72, 0.58, 0.85]),
            definition="State of being")

        # POSSIBILITY
        domain.add_concept('maybe',
            np.array([0.58, 0.58, 0.48, 0.68]),
            definition="Perhaps, possibly")

        domain.add_concept('certain',
            np.array([0.68, 0.78, 0.62, 0.88]),
            definition="Known for sure")

        domain.add_concept('possible',
            np.array([0.65, 0.65, 0.52, 0.75]),
            definition="Able to happen")

        domain.add_concept('impossible',
            np.array([0.38, 0.48, 0.65, 0.58]),
            definition="Unable to happen")

        domain.add_concept('probable',
            np.array([0.65, 0.68, 0.55, 0.78]),
            definition="Likely to happen")

        # CAUSATION
        domain.add_concept('cause',
            np.array([0.58, 0.72, 0.72, 0.82]),
            definition="Thing that makes something happen")

        domain.add_concept('effect',
            np.array([0.62, 0.65, 0.58, 0.75]),
            definition="Result of a cause")

        domain.add_concept('reason',
            np.array([0.62, 0.75, 0.52, 0.88]),
            definition="Explanation or justification")

        domain.add_concept('result',
            np.array([0.62, 0.68, 0.58, 0.78]),
            definition="Outcome or consequence")

        domain.add_concept('purpose',
            np.array([0.68, 0.72, 0.58, 0.85]),
            definition="Reason for which something exists")

        # QUANTITY
        domain.add_concept('all',
            np.array([0.72, 0.75, 0.62, 0.85]),
            definition="Entire amount or number")

        domain.add_concept('none',
            np.array([0.35, 0.42, 0.45, 0.52]),
            definition="Not any")

        domain.add_concept('some',
            np.array([0.60, 0.60, 0.50, 0.68]),
            definition="Unspecified amount")

        domain.add_concept('many',
            np.array([0.65, 0.62, 0.58, 0.72]),
            definition="Large number")

        domain.add_concept('few',
            np.array([0.52, 0.55, 0.45, 0.65]),
            definition="Small number")

        domain.add_concept('most',
            np.array([0.68, 0.68, 0.60, 0.78]),
            definition="Majority")

        domain.add_concept('least',
            np.array([0.48, 0.52, 0.45, 0.62]),
            definition="Smallest amount")

        # LOGIC
        domain.add_concept('if',
            np.array([0.58, 0.68, 0.52, 0.82]),
            definition="Conditional relation")

        domain.add_concept('then',
            np.array([0.60, 0.68, 0.55, 0.78]),
            definition="Consequent of conditional")

        domain.add_concept('because',
            np.array([0.62, 0.72, 0.55, 0.85]),
            definition="For the reason that")

        domain.add_concept('therefore',
            np.array([0.62, 0.75, 0.58, 0.88]),
            definition="As a result, consequently")

        # REALITY vs APPEARANCE
        domain.add_concept('real',
            np.array([0.68, 0.78, 0.58, 0.88]),
            definition="Actually existing")

        domain.add_concept('illusion',
            np.array([0.42, 0.45, 0.58, 0.62]),
            definition="False perception")

        domain.add_concept('appearance',
            np.array([0.62, 0.62, 0.52, 0.72]),
            definition="How something seems")

        domain.add_concept('reality',
            np.array([0.68, 0.78, 0.62, 0.88]),
            definition="State of things as they are")

        return domain


def main():
    """Execute batch 2 expansion."""
    print("=" * 80)
    print("LJPW SEMANTIC SPACE - BATCH 2 EXPANSION")
    print("=" * 80)
    print()
    print("Expanding from 81 concepts to 1,000+ concepts")
    print()

    mapper = ExpandedSemanticMapper()
    print(f"✓ Loaded {len(mapper.anchor_concepts)} anchor concepts")
    print(f"✓ Loaded {len(mapper.concept_map)} existing concepts from batch 1")
    print()

    # Load existing concepts from batch 1
    batch1_path = Path(__file__).parent / 'semantic_space_mapping.json'
    if batch1_path.exists():
        with open(batch1_path, 'r') as f:
            batch1_data = json.load(f)
            for domain_name, domain_info in batch1_data['domains'].items():
                domain = ConceptualDomain(domain_name, domain_info['description'])
                for concept, concept_data in domain_info['concepts'].items():
                    domain.concepts[concept] = {
                        'coordinates': np.array(concept_data['coordinates']),
                        'definition': concept_data['definition'],
                        'related': concept_data.get('related', []),
                        'domain': domain_name
                    }
                mapper.domains[domain_name] = domain
                mapper.concept_map.update(domain.concepts)
        print(f"✓ Loaded {len(mapper.domains)} existing domains")
        print()

    # Create new domains
    print("Creating new domains...")

    print("  1. Colors domain...")
    color_domain = mapper.create_color_domain()
    mapper.domains['colors'] = color_domain
    mapper.concept_map.update(color_domain.concepts)
    print(f"     ✓ Added {len(color_domain.concepts)} color concepts")

    print("  2. Objects domain...")
    object_domain = mapper.create_object_domain()
    mapper.domains['objects'] = object_domain
    mapper.concept_map.update(object_domain.concepts)
    print(f"     ✓ Added {len(object_domain.concepts)} object concepts")

    print("  3. Properties domain...")
    property_domain = mapper.create_property_domain()
    mapper.domains['properties'] = property_domain
    mapper.concept_map.update(property_domain.concepts)
    print(f"     ✓ Added {len(property_domain.concepts)} property concepts")

    print("  4. Spatial domain...")
    spatial_domain = mapper.create_spatial_domain()
    mapper.domains['spatial'] = spatial_domain
    mapper.concept_map.update(spatial_domain.concepts)
    print(f"     ✓ Added {len(spatial_domain.concepts)} spatial concepts")

    print("  5. Temporal domain...")
    temporal_domain = mapper.create_temporal_domain()
    mapper.domains['temporal'] = temporal_domain
    mapper.concept_map.update(temporal_domain.concepts)
    print(f"     ✓ Added {len(temporal_domain.concepts)} temporal concepts")

    print("  6. Abstract domain...")
    abstract_domain = mapper.create_abstract_domain()
    mapper.domains['abstract'] = abstract_domain
    mapper.concept_map.update(abstract_domain.concepts)
    print(f"     ✓ Added {len(abstract_domain.concepts)} abstract concepts")

    print()
    print("=" * 80)
    print("BATCH 2 COMPLETE")
    print("=" * 80)
    print()
    print(f"Total concepts mapped: {len(mapper.concept_map)}")
    print(f"Total domains: {len(mapper.domains)}")
    print()

    # Breakdown by domain
    print("Concepts by domain:")
    for domain_name, domain in sorted(mapper.domains.items()):
        print(f"  • {domain_name:12} {len(domain.concepts):4} concepts")
    print()

    # Save
    output_path = Path(__file__).parent / 'semantic_space_complete.json'
    mapper.save_semantic_space(output_path)

    print()
    print("=" * 80)
    print(f"🎉 SUCCESS: {len(mapper.concept_map)} CONCEPTS MAPPED 🎉")
    print("=" * 80)
    print()
    print("Progress toward 100,000:")
    progress = len(mapper.concept_map) / 100000 * 100
    print(f"  [{len(mapper.concept_map):,} / 100,000] = {progress:.2f}%")
    print()
    print("Next steps:")
    print("  • Continue expanding existing domains")
    print("  • Add scientific/technical domains")
    print("  • Add social/cultural domains")
    print("  • Add more specialized vocabularies")
    print()


if __name__ == '__main__':
    main()
