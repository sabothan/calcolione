from typing_extensions import Self  # PEP 673

from calcolione.qvar import QVar
from calcolione.utils import ANSWER_TOLERANCE, NUMERIC_UNIT_PATTERN


class Answer:
    """Represents an answer object."""

    def __init__(self, answer_type: str, calculation: str, result: QVar):
        self._answer_type: str = answer_type
        self._calculation: str = calculation
        self.result: QVar = result

        # Initialize input variables
        self.my_answer = QVar()

    @classmethod
    def from_dict(cls, answer: dict) -> Self:
        """Serves as an additional constructor, but with input from a `dict`.

        Args:
            answer (dict): the input dictionary

        Returns:
            Answer: The instantiated class.
        """
        # TODO: implement calculation of the correct answer from json variables?
        return cls(
            answer_type=answer["answer_type"],
            calculation=answer["calculation"],
            result=QVar.from_dict(answer["result"]),
        )

    def _input_answer(self) -> None:
        """Prompts the user to input an answer.
        The answer will be parsed into a pint.Quantity(numeric, unit) object,
        which will be stored in the the class's `self.my_answer`.
        """
        # Prompt an answer
        my_answer: str = input("Answer: ")

        # TODO: check input for allowed symbols

        # Parse the answer into numeric and unit and pack into QVar
        parsed_answer = self._parse(my_answer)

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
            raise NotImplementedError("This functionality is not implemented yet")

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
            # TODO: handle incompatible formats
            return QVar()

        # Convert the input string into a QVar
        parsed_answer = QVar(
            name="Result",
            description="Answer, given by the user",
            quantity_type="",
            raw_value=answer,
        )

        return parsed_answer

    def _parse_expression(self, answer: str) -> QVar:
        """Parses a scientific expression into a value with optional units.

        Args:
            answer (str): The answer string

        Returns:
            QVar: The answer parsed into an object
        """
        # TODO: implement scientific expressions
        return QVar()

    def evaluate_answer(self) -> bool:
        """Evaluates the answer given by the user for correctness.
        As metric for the correctness a tolerance value is applied.

        Returns:
            bool: True if correct, False otherwise
        """
        given_answer: QVar = self.my_answer
        correct_answer: QVar = self.result
        # TODO: implement comparison of QVar to raw tolerance
        if abs(given_answer - correct_answer) <= ANSWER_TOLERANCE:
            return True
        else:
            return False
