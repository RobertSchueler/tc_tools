"""
Module containing everything to handle data processing.
"""

# read up on dataclasses, they are cool!
from dataclasses import dataclass
from typing import Optional


class Source:
    """
    Class handling the csv sources.
    """
    pass


_global_source = Source()


@dataclass
class Variable:
    """
    A class corresponding to a constant or to an attribute of the data source.

    Parameter
    ----------

    val: int or str,
        either the corresponding constant or the name of the corresponding attribute

    """
    value: Optional[int] = None
    field_name: Optional[str] = None
        
    def __post_init__(self):
        # check if at least one attribute is initialized
        if not field_name or value is None: # check for None, bc 0 is poss.
            raise ValueError(
                "At least one of `value` or `field_name` must be set"
            )
    
    def __call__(self):
        return (
            self.value 
            if self.value is not None # check for None, bc 0 is poss.
            else _global_source(self.field_name)
        )
