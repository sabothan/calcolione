from typing import Optional
from typing_extensions import Self # PEP 673

from calcolione.utils import UNIT_REGISTRY as unit

class QVar:
    """Represents an arbitrary variable. Converts the variable into SI units for further calculations"""

    def __init__(
        self,
        name: str = "",
        description: str = "",
        type: str = "",
        value: Optional[float] = None,
        unit: str = "",
    ):
        self.name = name
        self.description = description
        self.type = type
        self.value = value
        self.unit = unit

        # TODO: add check whether the given unit is supported by pint.UnitRegistry

    def __add__(self, other):
        # TODO: implement qvar additon
        pass
    
    def __sub__(self, other):
        # TODO: implement qvar subtraction
        pass

    def __mul__(self, other):
        # TODO: implement qvar multiplication
        pass

    def __truediv__(self, other):
        # TODO: implement qvar division (true)
        pass

    def __floordiv__(self, other):
        # TODO: implement qvar floor division
        pass

    def __mod__(self, other):
        # TODO: implement qvar modulo
        pass

    def __pow__(self, other):
        # TODO: implement qvar power operations
        pass

    def __eq__(self, other):
        # TODO: implement qvar equality
        pass

    def __lt__(self, other):
        # TODO: implement qvar less than
        pass

    def __le__(self, other):
        # TODO impelement qvar less equan than
        pass

    def __gt__(self, other):
        # TODO: implement qvar greater than
        pass

    def __ge__(self, other):
        # TODO: implement qvar greater equal than
        pass

    def __ne__(self, other):
        # TODO: implement qvar not equal to
        pass

    @classmethod
    def from_dict(cls, variable: dict) -> Self:
        """Serves as an additional constructor, but with input from a `dict`.

        Args:
            variable (dict): the input dictionary

        Returns:
            The instantiated class.
        """
        return cls(
            name=variable["name"],
            description=variable["description"],
            type=variable["type"],
            value=variable["value"],
            unit=variable["unit"],
        )

    def _convert_to_si_units(self):
        """This function converts an arbitrary value with arbitrary units into SI units."""
        #  TODO: implement si converting
        pass

unit.Quantity(14, "km/h").to_base_units()  # should give m/s
unit.Quantity(25, "min").to_base_units()   # should give seconds