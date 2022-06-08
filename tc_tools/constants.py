"""
Contains common constants in the context of TCG.

`FORMATS` contains standard card format sizes in inch (given as width, height tuple).
Supported card formats are

- poker
- bridge
- business
- mini
- small
- large
- jumbo
- tarot
- domino
- index small
- index
- index large
- index giant
- square small
- square
- square large
- A4

`FACTORS` contains the factors for the conversion of a given unit to inch.

Supported units are:

- m (meter)
- dm (decimeter)
- cm (centimeter)
- mm (millimeter)
- yd (yard)
- ft (foot)
- in (inch)
- em (standard font size)
"""

FORMATS = {
    "poker":        (2.5, 3.5),
    "bridge":       (2.25, 3.5),
    "business":     (3.5, 2),
    "mini":         (1.75, 2.5),
    "small":        (3, 2),
    "large":        (3.5, 5),
    "jumbo":        (3.5, 5.5),
    "tarot":        (2.75, 4.75),
    "domino":       (1.75, 3.5),
    "index small":  (3, 4.5),
    "index":        (3, 5),
    "index large":  (3, 5.5),
    "index giant":  (4.75, 7),
    "square small": (3, 3),
    "square":       (3.5, 3.5),
    "square large": (4.75, 4.75),
    "A4":           (8.26772, 11.6929)
}

FACTORS = {
    "m":  39.3701,
    "dm": 3.93701,
    "cm": 0.393701,
    "mm": 0.0393701,
    "yd": 36,
    "ft": 12,
    "in": 1,
    "em": 0.166044
}