from typing import Optional

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

    @classmethod
    def from_dict(cls, variable: dict):
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

