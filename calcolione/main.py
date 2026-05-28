import sys

from calcolione import Exercise


def main():
    my_exercise = Exercise.get_exercise_from_json()
    my_exercise.display_question()
    my_exercise.input_answer()
    my_exercise.evaluate_answer()


if __name__ == "__main__":
    main()
    sys.exit(0)
