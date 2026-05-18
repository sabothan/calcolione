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
    
    def read(self, variable:dict):
        self.name = variable["name"]
        self.description = variable["description"]
        self.type = variable["type"]
        self.value = variable["value"]
        self.unit = variable["unit"]

    def _convert_to_si_units(self):
        """This function converts an arbitrary value with arbitrary units into SI units.
        """
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
            _var = QVar(variable)
            variable_list.append(_var)

        return variable_list

    def _render_message(self):
        substitutions =  {}
        
        # Generate subsitutions prompts for the message string
        for var in self.vars:
            substitutions[f"{var.name}.value"] = var.value
            substitutions[f"{var.name}.unit"] = var.unit

        message = self.message

        for key, val in substitutions.items():
            message = message.replace("{" + key + "}", str(val))
        
        return message

    def _get_question(self) -> str:
        return self.message
        

class Answer():
    def __init__(self, exercise:dict):
        self._answer_type = exercise["answer_type"]
        self._calculation = exercise["calculation"]
        self.result = QVar(exercise["result"])

        # Initialize input variables
        self.my_answer = None

        # Post-init processing

    def _input_answer(self) -> QVar:
        my_answer:str = input("Answer: ")

        parsed_answer = self._parse(my_answer)
        return parsed_answer

    def _parse(self, answer) -> QVar:
        if self._answer_type == "numeric":
            parsed_answer = self._parse_numeric(answer)   # value + unit
        elif self._answer_type == "expression":
            raise NotImplementedError("This functionality is not implemented yet")
            parsed_answer = self._parse_expression(answer)  # sympy or similar
        
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
        NUMERIC_UNIT_PATTERN = re.compile(r"^([-+]?\d+[.,]?\d*)\s*(.*)$")

        match = NUMERIC_UNIT_PATTERN.match(answer.strip())

        if not match:
            return QVar()

        value_str = match.group(1).replace(",", ".")
        unit_str  = match.group(2).strip()

        try:
            _ = float(value_str)
        except ValueError:
            return QVar()

        parsed_answer = QVar(
            value=value_str,
            unit=unit_str,
        )
        return parsed_answer

    def _parse_expression(self, answer) -> QVar:
        return QVar()
    
    
class Exercise():
    def __init__(self):
       self.question : Question
       self.answer : Answer
       
    def get_exercise(self):
        with open("questions.json", "r") as file:
            exercise = json.load(file)

        self.question = Question(exercise["question"])
        self.answer = Answer(exercise["answer"])
 
    def display_question(self):
        print(self.question._get_question())
    
    def input_answer(self):
        self.answer._input_answer()
    
    def evaluate_answer(self):
        pass


def main():
    my_exercise = Exercise()
    my_exercise.display_question()


if __name__ == "__main__":
    main()
    sys.exit(0)

