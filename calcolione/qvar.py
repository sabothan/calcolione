from __future__ import annotations

from pint import UnitRegistry, Quantity
from typing_extensions import Self  # PEP 673

# Define the unit registry
unit = UnitRegistry()


# QVar specific decorator for magic methods:
#   __add__
#   __sub__
#   __eq__
#   __le__
#   __lt__
#   __ge__
#   __gt__
def require_same_quantity_type(f):
    def wrapper(self:QVar, other:QVar):
        if not isinstance(other, QVar):
            raise TypeError(f"Unsupported operant type: {type(other)}")

        if self.quantity_type != other.quantity_type:
            raise TypeError(
                f"Type mismatch: cannot operate on '{self.quantity_type}' and '{other.quantity_type}'"
            )
        
        if not self.quantity.is_compatible_with(other.quantity):
            raise TypeError(
                f"Type mismatch: cannot operate on '{self.quantity.dimensionality}' and '{other.quantity.dimensionality}"
            )

        return f(self, other)
    return wrapper


class QVar:
    """Represents an arbitrary variable.
    Optionally converts the variable into SI units for further calculations.

    Args:
        name (str): The variable name.
        description (str): The variable description.
        quantity_type (str): The variable quantity_type.
        raw_value (str): The raw numeric-unit expression.

    Attributes:
        quantity (pint.Quantity): A numeric-unit tuple, parsed as an object.
        _raw_value (str): The raw numeric-unit expression.
    
    Methods:
        from_dict: Construct a QVar from an input dictionary.
        _convert_to_si_units(): Convert the quantity into base SI units.
    """

    def __init__(
        self,
        name: str = "",
        description: str = "",
        quantity_type: str = "",
        raw_value: str = "",
    ):
        self.name = name
        self.description = description
        self.quantity_type = quantity_type
        self._raw_value = raw_value
        
        # Post init processing of value
        # TODO: add check whether the given unit is supported by pint.UnitRegistry
        # Maybe initialise as a NaN until raw_value is specified? (see answer calculation in answer.py)
        self.quantity = Quantity(self._raw_value)

    @require_same_quantity_type
    def __add__(self, other: QVar):
        result = self.quantity + other.quantity
        return QVar(quantity_type=self.quantity_type, raw_value=str(result))

    @require_same_quantity_type
    def __sub__(self, other: QVar):
        result = self.quantity - other.quantity
        return QVar(quantity_type=self.quantity_type, raw_value=str(result))

    def __mul__(self, other: QVar):
        result = self.quantity * other.quantity
        result_type = f"{self.quantity_type} * {other.quantity_type}"
        return QVar(quantity_type=result_type, raw_value=str(result))

    def __truediv__(self, other: QVar):
        result = self.quantity / other.quantity
        result_type = f"{self.quantity_type} / {other.quantity_type}"
        return QVar(quantity_type=result_type, raw_value=str(result))

    def __floordiv__(self, other: QVar):
        result = self.quantity // other.quantity
        result_type = f"{self.quantity_type} / {other.quantity_type}"
        return QVar(quantity_type=result_type, raw_value=str(result))

    def __mod__(self, other: QVar):
        result = self.quantity % other.quantity
        result_type = f"{self.quantity_type} / {other.quantity_type}"
        return QVar(quantity_type=result_type, raw_value=str(result))

    def __eq__(self, other: QVar):
        result = self.quantity == other.quantity
        return result

    def __lt__(self, other: QVar):
        result = self.quantity < other.quantity
        return result

    def __le__(self, other: QVar):
        result = self.quantity <= other.quantity
        return result

    def __gt__(self, other: QVar):
        result = self.quantity > other.quantity
        return result

    def __ge__(self, other: QVar):
        result = self.quantity >= other.quantity
        return result

    def __ne__(self, other: QVar):
        result = self.quantity != other.quantity
        return result

    @classmethod
    def from_dict(cls, variable: dict) -> Self:
        """Serves as an additional constructor, but with input from a `dict`.

        Args:
            variable (dict): the input dictionary

        Returns:
            QVar: The instantiated class.
        """
        return cls(
            name=variable["name"],
            description=variable["description"],
            quantity_type=variable["quantity_type"],
            raw_value=variable["value"],
        )

    def _convert_to_si_units(self) -> None:
        """This function converts an arbitrary value with arbitrary units into SI units."""
        #  TODO: implement si converting
        pass


