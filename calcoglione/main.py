import re
import sys
import json


ALLOWED_SYMBOLS = re.compile(r"^[.,/*a-zA-Z0-9 \-+%°^()]+$")


class UI():
    def __init__(self):
        pass

    def display_menu(self):
        pass


class QVar():
    """Represents an arbitrary variable. Converts the variable into SI units for further calculations
    """
    def __init__(
            self,
            name:str = "",
            description:str = "",
            type:str = "",
            value:str = "",
            unit:str = "",
        ):
        self.name = name
        self.description = description
        self.type = type
        self.value = value
        self.unit = unit
    
    @classmethod
    def from_dict(cls, variable:dict):
        """Serves as an additional constructor, but with input from a `dict`.

        Args:
            variable (dict): the input dictionary

        Returns:
            The instantiated class.
        """
        return cls(
            name = variable["name"],
            description = variable["description"],
            type = variable["type"],
            value = variable["value"],
            unit = variable["unit"],
        )

    def _convert_to_si_units(self):
        """This function converts an arbitrary value with arbitrary units into SI units.
        """
        #  TODO: implement si converting
        pass


class Question():
    """Wrapper class to hold a question and it's information.
    """
    def __init__(self, question:dict):
        self.message : str = question["message"]
        self.vars : list[QVar] = self._read_variables(question["vars"])

        # Post-init processes
        self.message = self._render_message()

    def _read_variables(self, raw_variables:dict) -> list:
        """Read all variabels that occur in a question.

        Args:
            raw_variables (dict): the variables

        Returns:
            A list of variabels.
        """
        variable_list = []
        for variable in raw_variables:
            _var = QVar.from_dict(variable)
            variable_list.append(_var)

        return variable_list

    def _render_message(self):
        substitutions =  {}
        
        # Generate subsitutions prompts for the message string
        for var in self.vars:
            substitutions[f"{var.name}.value"] = var.value
            substitutions[f"{var.name}.unit"] = var.unit

        message = self.message

        # Substitute <value, unit> tuples into messages
        for key, val in substitutions.items():
            message = message.replace("{" + key + "}", str(val))
        
        return message

    def _get_question(self) -> str:
        """Get the question body (message).

        Returns:
            str: the question message
        """
        return self.message
        

class Answer():
    def __init__(self, exercise:dict):
        self._answer_type = exercise["answer_type"]
        self._calculation = exercise["calculation"]
        self.result = QVar(exercise["result"])

        # Initialize input variables
        self.my_answer = None

        # Post-init processing
        # TODO: implement parsing

    def _input_answer(self) -> QVar:
        """Prompts the user to input an answer.
        The answer will be parsed into a <numeric, unit> tuple accordingly,
        which will be stored in the QVar object.

        Returns:
            QVar: a variable object containing the provided answer
        """
        # Prompt an answer
        my_answer:str = input("Answer: ")

        # Parse the answer into numeric and unit and pack into QVar
        parsed_answer = self._parse(my_answer)

        return parsed_answer

    def _parse(self, answer:str) -> QVar:
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
            parsed_answer = self._parse_numeric(answer)   # value + unit
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
        unit_str  = match.group(2).strip()

        try:
            _ = float(value_str)
        except ValueError:
            # TODO: handle non numeric values
            return QVar()

        # Create an arbitry answer with numeric and value
        parsed_answer = QVar(
            value=value_str,
            unit=unit_str,
        )
        return parsed_answer

    def _parse_expression(self, answer) -> QVar:
        # TODO: implement scientific expressions
        return QVar()
    
    
class Exercise():
    """Wrapper class for a Question and an Answer.
    Implements downstream methods for user interaction.
    """
    def __init__(self):
        # Declare member variables
        self.question : Question
        self.answer : Answer
       
    def get_exercise(self):
        """Read an exercise from a template JSON file.
        The template will be filled with randomised values.
        """
        with open("questions.json", "r") as file:
            exercise = json.load(file)

        # TODO: implement randomising values
        self.question = Question(exercise["question"])
        self.answer = Answer(exercise["answer"])
 
    def display_question(self):
        """Print the question body to the terminal
        """
        print(self.question._get_question())
    
    def input_answer(self):
        """Prompt the user for an answer.
        """
        self.answer._input_answer()
    
    def evaluate_answer(self):
        """Evaluate the given answer for correctness.
        """
        pass


def main():
    my_exercise = Exercise()
    my_exercise.display_question()


if __name__ == "__main__":
    main()
    sys.exit(0)

