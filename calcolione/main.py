import sys

from calcolione.exercise import Exercise


def main() -> int:
    """Start the main process."""
    my_exercise = Exercise.get_exercise_from_json()
    my_exercise.display_question()
    my_exercise.input_answer()
    my_exercise.evaluate_answer()

    return 0


if __name__ == "__main__":
    sys.exit(main())
