import json
from pathlib import Path

from typing_extensions import Self  # PEP 673

from .answer import Answer
from .question import Question
from .utils import EXERCISE_FILE


class Exercise:
    """Wrapper class for a Question and an Answer.
    Implements downstream methods for user interaction.
    """

    def __init__(self, question: Question, answer: Answer):
        self.question = question
        self.answer = answer

    @classmethod
    def get_exercise_from_json(cls, exercise_file:Path = EXERCISE_FILE) -> Self:
        """Read an exercise from a template JSON file.
        The template will be filled with randomised values.

        Args:
            exercise_file(Path, optional): The path to the JSON file containing the exercises.
        """
        if exercise_file.is_file():
            with open(exercise_file) as file:
                exercise = json.load(file)
        else:
            raise FileNotFoundError(f"The JSON file at {str(exercise_file.absolute())} cannot be found")

        # TODO: implement randomising values
        return cls(
            question=Question.from_dict(exercise["question"]),
            answer=Answer.from_dict(exercise["answer"]),
        )

    def display_question(self) -> None:
        """Print the question body to the terminal."""
        print(self.question._get_question())

    def input_answer(self) -> None:
        """Prompt the user for an answer."""
        self.answer._input_answer()

    def evaluate_answer(self) -> None:
        """Evaluate the given answer for correctness."""
        print(
            f"Given answer: {self.answer.my_answer.quantity}"
        )
        print(f"Correct answer: {self.answer.result.quantity}")

        # TODO: finish evaluation
