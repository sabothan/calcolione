from __future__ import annotations
from typing_extensions import Self  # PEP 673
import re

from calcolione.qvar import QVar
from calcolione.utils import (
    ANSWER_TOLERANCE,
    NUMERIC_UNIT_PATTERN,
    ALLOWED_SYMBOLS,
    substitute_placeholders
)


class Answer:
    """Represents an answer object."""

    def __init__(self, answer_type: str, calculation: str, result: QVar, vars: list[QVar]):
        self._answer_type = answer_type
        self._calculation = calculation
        self.vars = vars

        # Initialize input variables
        self.my_answer = QVar()

        # Calculate result from vars
        self.result = self._calculate_answer(result)

    @classmethod
    def from_dict(cls, answer: dict, vars: list) -> Self:
        """Serves as an additional constructor, but with input from a `dict`.

        Args:
            answer (dict): the input dictionary

        Returns:
            Answer: The instantiated class.
        """
        return cls(
            answer_type=answer["answer_type"],
            calculation=answer["calculation"],
            result=QVar.from_dict(answer["result"]),
            vars=[QVar.from_dict(var) for var in vars]
        )
    
    def _calculate_answer(self, result: QVar):
        parsed_calculation = substitute_placeholders(
            vars=self.vars,
            body=self._calculation,
        )

        return QVar(
            raw_value=parsed_calculation,
            name=result.name,
            description=result.description,
            quantity_type=result.quantity_type,
        )._convert_to_si_units()
        

    def _input_answer(self) -> None:
        """Prompts the user to input an answer.
        The answer will be parsed into a pint.Quantity(numeric, unit) object,
        which will be stored in the the class's `self.my_answer`.
        """
        allowed = False
        while(not allowed):
            # Prompt an answer
            my_answer: str = input("Answer: ")

            # Check input for allowed symbols
            allowed = bool(ALLOWED_SYMBOLS.match(my_answer))
            if not allowed:
                print(" --> SyntaxError: Try again <-- ")

        # Parse the answer into numeric and unit and pack into QVar
        parsed_answer = self._parse(my_answer)

        # Manually set the quantity_type of the given answer
        parsed_answer.quantity_type = self.result.quantity_type

        # Write the parsed answer to the dedicated variable
        self.my_answer = parsed_answer

    def _parse(self, answer: str) -> QVar:
        """Parses an answer string into a QVar object.
        The string is split into a tuple pint.Quantity(numeric, unit) and
        packed into the QVar object.

        Args:
            answer (str): The answer provided by the user.

        Raises:
            NotImplementedError:    To future proof this for possible scientific
                                    expressions, a not implemented error will
                                    be raised.

        Returns:
            QVar: The parsed answer
        """
        # Numeric type: e.g. 1425.345 km/h
        if self._answer_type == "numeric":
            parsed_answer = self._parse_numeric(answer)  # value + unit
        # Expression type: e.g. 2*sin(34) * (2pi/rad)
        elif self._answer_type == "expression":
            parsed_answer = self._parse_expression(answer)  # sympy or similar
        else:
            raise ValueError(f"Unknown answer type: '{self._answer_type}'")

        return parsed_answer

    def _parse_numeric(self, answer: str) -> QVar:
        """Parses a numeric answer string into a value and an optional unit.
        (expected format: <number> <unit>).

        Arguments:
            answer (str): an answer string consisting of a numeric and a unit

        Returns:
            QVar: The answer, parsed into a numeric and a unit part

        Examples:
            "5.833 km"      -> (5.833, "km")
            "110 km/h"      -> (110.0, "km/h")
            "9.8"           -> (9.8, "")
            "-3.5 m/s"      -> (-3.5, "m/s")
        """
        match = NUMERIC_UNIT_PATTERN.match(answer.strip())

        # Handle incompatible anwers
        if not match:
            # TODO handle incompatible formats
            return QVar()

        # Convert the input string into a QVar
        parsed_answer = QVar(
            name="Result",
            description="Answer, given by the user",
            quantity_type="",
            raw_value=answer,
        )

        return parsed_answer

    def _parse_expression(self, answer: str):
        """Parses a scientific expression into a value with optional units.

        Args:
            answer (str): The answer string

        Returns:
            QVar: The answer parsed into an object
        """
        # TODO implement scientific expressions
        raise NotImplementedError("This functionality is not implemented yet")

    def evaluate_answer(self) -> bool:
        """Evaluates the answer given by the user for correctness.
        As metric for the correctness a tolerance value is applied.

        Returns:
            bool: True if correct, False otherwise
        """
        given_answer = self.my_answer.quantity.to_base_units().magnitude
        correct_answer = self.result.quantity.to_base_units().magnitude

        # TODO implement more stable approach to evaluate the answer's correctness
        return abs(given_answer - correct_answer) <= ANSWER_TOLERANCE
