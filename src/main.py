import os
import sys
import math
import random

import tabulate

MENU = {
    "1" : "Basic Arithmetic Exercise",
    "2" : "Free Fall Time Calculator",
    "3" : "Time-Velocity Path Conversions",
    "4" : "Textual Problem Exercise",
    "0" : "Exit"
}

def print_menu():
    """Prints the menu information as a table."""
    print(tabulate(MENU.items(), headers=["Input", "Description"], tablefmt=simple))


def prompt_qa(question:str) -> float:
    """Asks the user a question and prompts an answer

    Args:
        question(str): The question to be asked

    Returns:
        The user's answer to the question.
    """
    print(f"Solve: \n\t{question}")
    
    while(True):
        answer = input()
        checker = is_input_float(answer)

        # Check input format
        if(checker is True):
            break

    return float(answer)


def is_input_float(user_input:str) -> bool:
    """Checks, whether the user input is a float or not.

    Args:
        user_input(str): The user input to check.

    Returns:
        `True` if the input is a float. `False` otherwise.
    """
    try:
        _ = float(user_input)
    except ValueError:
        print("Invalid input format. Please enter a valid `float`")
        return False

    return True


def generate_basic_exercise() -> tuple[str, float]:
    """Generates a basic arithmetic exercise, for example `5 + 4`.

    Returns:
        tuple(question, answer)
    """
    bounds = [-100, 100]
    operations = ["+", "-", "*", "/"]
    
    a = random.randint(bounds[0], bounds[1])
    b = random.randint(bounds[0], bounds[1])
    op = random.choice(operations)

    question = f"{a} {op} {b}"
    answer = eval(question)

    return question, answer


def exercise(option):
    question: str
    answer: float 
    print(option)
    if(option == MENU["1"]):
        question, answer = generate_basic_exercise()
    elif(option == MENU["0"]):
        print("Exiting")
        return
    else:
        return

    # Ask question and get user input
    user_answer = prompt_qa(question)

    # Check answer
    if(answer is user_answer):
        print("Correct!\n\n")

def main():
    """This executes the project."""
    # Print overall information
    print_menu()

    # Main loop
    while(True):
        selected_option:str
        menu_input = input()
        if(menu_input in MENU.keys()):
            if(menu_input == 1):
                selected_option = MENU["1"]
            elif(menu_input == 2):
                selected_option = MENU["2"]
            elif(menu_input == 3):
                selected_option = MENU["3"]
            elif(menu_input == 4):
                selected_option = MENU["4"]
            elif(menu_input == 5):
                selected_option = MENU["5"]
            else:
                selected_option = MENU["0"]

            exercise(selected_option)

        elif(menu_input == "help"):
            print_menu()
        elif(menu_input == "clear"):
            os.system("cls")
        elif(menu_input == "exit" or menu_input == "0"):
            break
        else:
            print("This menu option does not exist (yet). Try again")
            print_menu()

        user_answer = prompt_qa(question)


if __name__ == "__main__":
    main()
    sys.exit(0)

