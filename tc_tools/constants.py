"""
Contains common constants in the context of TCG.

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
"""

#card format constants in inch
format_dict = {
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
    "square large": (4.75, 4.75)
}