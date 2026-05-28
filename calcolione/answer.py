import re

from calcolione import QVar


class Answer:
    def __init__(self, answer_type: str, calculation: str, result: QVar):
        self._answer_type = answer_type
        self._calculation = calculation
        self.result = result

        # Initialize input variables
        self.my_answer = None

        # Post-init processing
        # TODO: implement parsing

    @classmethod
    def from_dict(cls, answer: dict):
        """Serves as an additional constructor, but with input from a `dict`.

        Args:
            answer (dict): the input dictionary

        Returns:
            The instantiated class.
        """
        return cls(
            answer_type=answer["answer_type"],
            calculation=answer["calculation"],
            result=QVar.from_dict(answer["result"]),
        )

    def _input_answer(self) -> QVar:
        """Prompts the user to input an answer.
        The answer will be parsed into a <numeric, unit> tuple accordingly,
        which will be stored in the QVar object.

        Returns:
            QVar: a variable object containing the provided answer
        """
        # Prompt an answer
        my_answer: str = input("Answer: ")

        # TODO: check input for allowed symbols

        # Parse the answer into numeric and unit and pack into QVar
        parsed_answer = self._parse(my_answer)

        return parsed_answer

    def _parse(self, answer: str) -> QVar:
        """Parses an answer string into a QVar object.
        The string is split into a tuple <numeric, unit> accordingly and
        packed into the QVar object.

        Args:
            answer (str): The answer provided by the user.

        Raises:
            NotImplementedError: To future proof this method for possible scientific expressions, a not implemented error will be raised.

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

    def _parse_numeric(self, answer) -> QVar:
        """
        Parses a numeric answer string into a value and an optional unit.
        Expected format: <number> <unit>
        Examples:
            "5.833 km"      -> (5.833, "km")
            "110 km/h"      -> (110.0, "km/h")
            "9.8"           -> (9.8, "")
            "-3.5 m/s"      -> (-3.5, "m/s")
        """
        # Regex pattern:
        # - `^` — start of string
        # - `([-+]?\d+[.,]?\d*)` — **capture group 1: the number**
        #   - `[-+]?` — optional sign
        #   - `\d+` — one or more digits (required)
        #   - `[.,]?` — optional decimal separator, either `.` or `,`
        #   - `\d*` — zero or more digits after the separator
        # - `\s*` — zero or more whitespace between number and unit
        # - `(.*)` — **capture group 2: the unit**, anything remaining
        # - `$` - end of string
        NUMERIC_UNIT_PATTERN = re.compile(r"^([-+]?\d+[.,]?\d*)\s*(.*)$")
        match = NUMERIC_UNIT_PATTERN.match(answer.strip())

        # Handle incompatible anwers
        if not match:
            # TODO: handle incompatible formats
            return QVar()

        # Split up answer into numeric and unit
        value_str = match.group(1).replace(",", ".")
        unit_str = match.group(2).strip()

        # Convert the string numeric into a float
        try:
            value = float(value_str)
        except ValueError:
            # TODO: handle non numeric values
            return QVar()

        # Create an arbitry answer with numeric and value
        parsed_answer = QVar(
            value=value,
            unit=unit_str,
        )
        return parsed_answer

    def _parse_expression(self, answer) -> QVar:
        # TODO: implement scientific expressions
        return QVar()

