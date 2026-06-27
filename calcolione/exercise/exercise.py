from __future__ import annotations
import json
from pathlib import Path
import random

from typing_extensions import Self  # PEP 673

from .answer import Answer
from .question import Question
from ..utils import EXERCISE_FILE


class Exercise:
    """Wrapper class for a Question and an Answer.
    Implements downstream methods for user interaction.
    """

    def __init__(self, question: Question, answer: Answer, exercise_id: str):
        self.question = question
        self.answer = answer
        self.id = exercise_id

    @classmethod
    def get_exercise_from_json(cls, exercise_file: Path = EXERCISE_FILE, exclude_id: str | None = None) -> Self:
        """Read a random exercise from a JSON file.

        Args:
            exercise_file (Path, optional): Path to the JSON file containing the exercises.
            exclude_id (str, optional): The ID of the exercise that shall NOT be loaded.

        Returns:
            Exercise: A randomly selected exercise.

        Raises:
            FileNotFoundError: If the exercise file does not exist.
            ValueError: If the exercise file contains no exercises.
        """
        if not exercise_file.is_file():
            raise FileNotFoundError(f"The JSON file at {exercise_file} cannot be found")

        with open(exercise_file) as file:
            data = json.load(file)

        exercises = data["exercises"]
        if not exercises:
            raise ValueError(f"No exercises found in {exercise_file}")

        # TODO implement randomising values
        # TODO implement filtering by difficulty and category
        candidates = [e for e in exercises if e["id"] != exclude_id] if exclude_id else exercises
        if not candidates:
            candidates = exercises  # fallback if only one exercise exists
        exercise = random.choice(exercises)

        return cls(
            question=Question.from_dict(exercise["question"], vars=exercise["vars"]),
            answer=Answer.from_dict(answer=exercise["answer"], vars=exercise["vars"]),
            exercise_id=exercise["id"],
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
