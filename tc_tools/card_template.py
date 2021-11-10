"""
Contains functions to create and handle card templates.
"""

from tc_tools import FORMATS


class CardTemplate:
    """
    A card template contains all information how to render a card.

    Parameter
    ----------

    fmt: str or (int, int),
        either the name of a format supported by the constants submodule or a tuple of the width and height as integers
        in the unit defined by unit.
        Defaults to "poker".

    dpi: int,
        The resolution of the card.
        Defaults to 300.

    unit: str,
        The name of the unit in which the format is given.
        Supported strings are:

        -in

        Defaults to "in".

    """
    def __init__(self, fmt: str or (int, int) = "poker", dpi: int = 300, unit: str = "in"):
        
        # better to ask for forgiveness then for permission
        try:
            self._fmt = FORMATS[fmt]
        except KeyError:
            self._fmt = fmt

        self._dpi = dpi
        self._shape = (self._fmt[0]*self._dpi, self._fmt[1]*self._dpi)

