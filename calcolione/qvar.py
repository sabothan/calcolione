from __future__ import annotations

from pint import UnitRegistry
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
        value: float | None = None,
        unit: str = "",
    ):
        self.name = name
        self.description = description
        self.type = type
        self.value = value
        self.unit = unit

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
            value=variable["value"],
            unit=variable["unit"],
        )

    def _convert_to_si_units(self) -> None:
        """This function converts an arbitrary value with arbitrary units into SI units."""
        #  TODO: implement si converting
        pass


print(unit.Quantity(14, "km/h").to_base_units())  # should give m/s
print(unit.Quantity(25, "min").to_base_units())  # should give seconds

