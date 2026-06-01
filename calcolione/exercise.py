import json
from pathlib import Path
from typing_extensions import Self # PEP 673: The Self type annotation is also useful for classmethods that return an instance of the class that they operate on.

from calcolione.answer import Answer
from calcolione.question import Question
from calcolione.qvar import QVar


class Exercise:
    """Wrapper class for a Question and an Answer.
    Implements downstream methods for user interaction.
    """

    def __init__(self, question: Question, answer: Answer):
        self.question = question
        self.answer = answer

    @classmethod
    def get_exercise_from_json(cls) -> Self:
        """Read an exercise from a template JSON file.
        The template will be filled with randomised values.
        """
        exercise_file = Path("exercises.json")
        if exercise_file.is_file():
            with open(exercise_file) as file:
                exercise = json.load(file)

        # TODO: implement randomising values
        return cls(
            question=Question.from_dict(exercise["question"]),
            answer=Answer.from_dict(exercise["answer"]),
        )

    def display_question(self):
        """Print the question body to the terminal"""
        print(self.question._get_question())

    def input_answer(self):
        """Prompt the user for an answer."""
        self.answer._input_answer()

    def evaluate_answer(self):
        """Evaluate the given answer for correctness."""
        print(
            f"Given answer: {self.answer.my_answer.value} {self.answer.my_answer.unit}"
        )
        print(f"Correct answer: {self.answer.result.value} {self.answer.result.unit}")

        # TODO: finish evaluation
