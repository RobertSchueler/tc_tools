"""
Module containing everything to handle data processing.
"""


class Source:
    """
    Class handling the csv sources.
    """
    pass


_global_source = Source()


class Variable:
    """
    A class corresponding to a constant or to an attribute of the data source.

    Parameter
    ----------

    val: int or str,
        either the corresponding constant or the name of the corresponding attribute

    """
    def __init__(self, val):
        if isinstance(val, int):
            self._val = val
            self._field = None
        elif isinstance(val, str):
            self._val = None
            self._field = val
        else:
            raise ValueError("For initialization of Variable, only int and str are allowed")

    @property
    def val(self):
        """
        the corresponding constant, or None if the object corresponds to an attribute
        """
        return self._val

    @property
    def field(self):
        """
        the name of the corresponding attribute or None if corresponding to a constant
        """
        return self._field

    @val.setter
    def val(self, val):
        if isinstance(val, int):
            self._val = val
            self._field = None

    @field.setter
    def field(self, field):
        if isinstance(field, str):
            self._val = None
            self._field = field

    def __call__(self):
        if self.val:
            return self.val
        if self.field:
            return _global_source(self.field)