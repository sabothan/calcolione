from __future__ import annotations

from pint import UnitRegistry, Quantity
from typing_extensions import Self  # PEP 673

# Define the unit registry
unit = UnitRegistry()


class QVar:
    """Represents an arbitrary variable.
    Converts the variable into SI units for further calculations.
    """

    def __init__(
        self,
        name: str = "",
        description: str = "",
        type: str = "",
        raw_value: str = "",
    ):
        self.name = name
        self.description = description
        self.type = type
        self._raw_value = raw_value
        
        # Post init processing of value
        self.quantity = Quantity(self._raw_value)

        # TODO: add check whether the given unit is supported by pint.UnitRegistry

    def __add__(self, other: QVar):
        # TODO: implement qvar additon
        pass

    def __sub__(self, other: QVar):
        # TODO: implement qvar subtraction
        pass

    def __mul__(self, other: QVar):
        # TODO: implement qvar multiplication
        pass

    def __truediv__(self, other: QVar):
        # TODO: implement qvar division (true)
        pass

    def __floordiv__(self, other: QVar):
        # TODO: implement qvar floor division
        pass

    def __mod__(self, other: QVar):
        # TODO: implement qvar modulo
        pass

    def __pow__(self, other: QVar):
        # TODO: implement qvar power operations
        pass

    def __eq__(self, other: QVar):
        # TODO: implement qvar equality
        pass

    def __lt__(self, other: QVar):
        # TODO: implement qvar less than
        pass

    def __le__(self, other: QVar):
        # TODO impelement qvar less equan than
        pass

    def __gt__(self, other: QVar):
        # TODO: implement qvar greater than
        pass

    def __ge__(self, other: QVar):
        # TODO: implement qvar greater equal than
        pass

    def __ne__(self, other: QVar):
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
            raw_value=variable["value"],
        )

    def _convert_to_si_units(self) -> None:
        """This function converts an arbitrary value with arbitrary units into SI units."""
        #  TODO: implement si converting
        pass


var1 = unit.Quantity(1, "km/h").to_base_units() # should give m/s
var2 = unit.Quantity(1, "m/s").to_base_units()  # should give seconds

print(var1.dimensionality)
print(var2.dimensionality)

print(var1.to_base_units())
print(var2.to_base_units())

result:Quantity = var1 + var2
print(result)
print(result.to("km/h"))

print(unit.Quantity("1km/h + 1m/s"))
