import json
from pathlib import Path

from calcolione import Question, Answer, QVar


class Exercise:
    """Wrapper class for a Question and an Answer.
    Implements downstream methods for user interaction.
    """

    def __init__(self, question: Question, answer: Answer):
        self.question = question
        self.answer = answer

        # Initialise user prompt answer
        self.user_answer = Answer(
            answer_type="",
            calculation="",
            result=QVar(),
        )

    @classmethod
    def get_exercise_from_json(cls):
        """Read an exercise from a template JSON file.
        The template will be filled with randomised values.
        """
        exercise_file = Path("exercises.json")
        if exercise_file.is_file():
            with open(exercise_file, "r") as file:
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
        self.user_answer._input_answer()

    def evaluate_answer(self):
        """Evaluate the given answer for correctness."""
        print(
            f"Given answer: {self.user_answer.result.value} {self.user_answer.result.unit}"
        )
        print(f"Correct answer: {self.answer.result.value} {self.answer.result.unit}")

        # TODO: finish evaluation

