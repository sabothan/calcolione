import json
from pathlib import Path

from typing_extensions import Self  # PEP 673

from .answer import Answer
from .question import Question
from ..utils import EXERCISE_FILE


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
            raise FileNotFoundError(f"The JSON file at {exercise_file} cannot be found")

        # TODO implement randomising values

        return cls(
            question=Question.from_dict(exercise["question"], vars=exercise["vars"]),
            answer=Answer.from_dict(answer=exercise["answer"], vars=exercise["vars"]),
        )

    def get_question(self) -> str:
        """Returns the question body as a string.
        
        Returns:
            str: The question body.
        """
        return self.question._get_question()

    def input_answer(self, answer: str) -> None:
        """Prompt the user for an answer.
        
        Used by the UI layer, which owns input collection and format validation.
        The string is expected to have already passed ``ALLOWED_SYMBOLS`` validation.

        Args:
            answer (str): The raw answer string provided by the user.
        """
        self.answer._input_answer(answer)

    def evaluate_answer(self) -> bool:
        """Evaluate the given answer for correctness."""
        return self.answer.evaluate_answer()
