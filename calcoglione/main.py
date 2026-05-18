import os
import sys
import json
import math
import random


class UI():
    def __init__(self):
        pass

    def display_menu(self):
        pass


class QVar():
    """Represents an arbitrary variable. Converts the variable into SI units for further calculations
    """
    def __init__(self, variable:dict):
        self.name = variable["name"]
        self.description = variable["description"]
        self.type = variable["type"]
        self.value = variable["value"]
        self.unit = variable["unit"]

    def convert_to_si_units(self):
        """This function converts an arbitrary value with arbitrary units into SI units.
        """
        pass


class QVarResult(QVar):
    def __init__(self, variable:dict):
        self.name = variable["name"]
        self.calculation = variable["calculation"]
        self.type = variable["type"]
        self.value = variable["value"]
        self.unit = variable["unit"]



class Question():
    """Wrapper class to hold a question and it's information.
    """
    def __init__(self, question:dict):
        self.message : str = question["message"]
        self.vars : list[QVar] = self._read_variables(question["vars"])
        self.result : QVar = self._read_result(question["result"])

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

    def _read_result(self, raw_result:dict) -> QVar:
        result = QVarResult(raw_result)
        return result

    def ask_question(self):
        print(self.message)
        

def read_question():
    with open("questions.json", "r") as file:
        question = json.load(file)
    
    return question

def main():
    question = read_question()
    my_question = Question(question)
    my_question.ask_question()

    my_anser = input("Answer: ")

    print(f"My answer: {my_anser}")
    print(f"Correct answer: {my_question.result.value}")


if __name__ == "__main__":
    main()
    sys.exit(0)

