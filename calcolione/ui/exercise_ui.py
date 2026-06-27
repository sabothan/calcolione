"""Terminal UI for calcolione using prompt_toolkit."""

from __future__ import annotations
from enum import Enum
from pint.errors import UndefinedUnitError, DimensionalityError, OffsetUnitCalculusError
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.application import get_app
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl

from ..exercise.exercise import Exercise
from ..utils import ALLOWED_SYMBOLS, get_logger, InvalidInputFormatError
from .base_ui import UI

# Create the logger instance
log = get_logger(__name__)

class Feedback(Enum):
    HINT = 1
    CORRECT = 2
    WRONG = 3
    ERROR_UNDEFINED_UNIT = 4
    ERROR_DIMENSIONALITY = 5
    ERROR_OFFSET_UNIT = 6
    ERROR_ASSERTION = 7
    ERROR_UNEXPECTED = 8
    ERROR_INVALID_FORMAT = 9

# ---------------------------------------------------------------------------
# Exercise screen
# ---------------------------------------------------------------------------

class ExerciseUI(UI):
    """Exercise screen - displays a question and accepts the user's answer."""

    COMMANDS = {
        **UI.COMMANDS,
        "next": {
            "cmd": ["n", "next"],
            "description": "Go to next exercise.",
        },
        "restart": {
            "cmd": ["restart"],
            "description": "Restart this exercise from scratch.",
        },
    }
    def __init__(self) -> None:
        # answer_buffer and question must exist before super().__init__()
        # because make_body (called by the base class) references them.
        self.answer_buffer: Buffer = Buffer(name="answer", multiline=False)
        self.answer_buffer.accept_handler = self._handle_answer  # type: ignore[assignment]

        # Load an exercise and generate an initial navigation hint
        self.load_exercise_and_init_feedback()
        

        super().__init__(screen_title="Exercise")

    @property
    def _default_focus_target(self) -> Buffer:
        return self.answer_buffer

    def _register_keybindings(self) -> None:
        super()._register_keybindings()  # inherit shared bindings (`:` command mode)

    def _handle_answer(self, buf: Buffer) -> bool:
        """Process the submitted answer.

        Args:
            buf (Buffer): The answer buffer.

        Returns:
            bool: False to clear the buffer after submission.
        """
        answer = buf.text.strip()
        if not answer:
            buf.reset()
            return False

        # Catch pint-specific errors and set the feedback accordingly
        try:
            self.exercise.input_answer(answer=answer)
        except UndefinedUnitError:
            self.set_feedback(self.generate_feedback(Feedback.ERROR_UNDEFINED_UNIT))
        except DimensionalityError:
            self.set_feedback(self.generate_feedback(Feedback.ERROR_DIMENSIONALITY))
        except OffsetUnitCalculusError:
            self.set_feedback(self.generate_feedback(Feedback.ERROR_OFFSET_UNIT))
        except AssertionError:
            self.set_feedback(self.generate_feedback(Feedback.ERROR_ASSERTION))
        except InvalidInputFormatError:
            self.set_feedback(self.generate_feedback(Feedback.ERROR_INVALID_FORMAT))
        except Exception as e:
            log.error(
                "Unhandled exception in _handle_answer",
                exc_info=True,
                extra={"answer": answer, "question": self.exercise.get_question()},
            )
            self.set_feedback(self.generate_feedback(Feedback.ERROR_UNEXPECTED))
        else:
            is_correct = self.exercise.evaluate_answer()
            if is_correct:
                feedback = self.generate_feedback(Feedback.CORRECT)
            else:
                feedback = self.generate_feedback(Feedback.WRONG)

            self.set_feedback(feedback)

        get_app().invalidate()

        buf.reset()
        return False
    
    def _help_content(self) -> list[tuple[str, str]]:
        """Return help text including exercise-specific sections.

        Returns:
            list[tuple[str, str]]: Formatted text fragments for the help window.
        """
        lines = super()._help_content()  # keybindings + "Press Escape" line
        lines = lines[:-1]              # drop "Press Escape" - re-added at the end

        lines.append(("class:label", " Answer format\n"))
        lines += [
            ("class:hint", "   <number> <unit>       e.g. 5.833 km, 99 m, 3.5 m/s\n"),
            ("class:hint", "   Negative values        e.g. -5 m\n"),
            ("class:hint", "   Unit-less              e.g. 9.8  (dimensionless answers)\n"),
        ]
        lines.append(("", "\n"))

        lines.append(("class:label", " Behaviors to be aware of\n"))
        lines += [
            ("class:hint", "   Adjacent numerics are multiplied:  5 5 km = 25 km\n"),
            ("class:hint", "   Compound units are valid:          5 km h = 5 km*h\n"),
            ("class:hint", "   1% tolerance applied to evaluation\n"),
        ]
        lines.append(("", "\n"))
        lines.append(("class:dim", " Press Escape to close\n"))
        return lines

    def make_body(self) -> HSplit:
        """Build the exercise content: question, input row, and feedback line.

        Returns:
            HSplit: The exercise content container.
        """
        question_label = Window(
            content=FormattedTextControl([("class:label", " Exercise")]),
            height=1,
        )
        question_body = Window(
            content=FormattedTextControl(self.get_question),
            height=3,
            wrap_lines=True,
        )
        answer_label = Window(
            content=FormattedTextControl([("class:label", " Your answer (press Enter to submit):")]),
            height=1,
        )
        input_prefix = Window(
            content=FormattedTextControl([("class:prompt", " > ")]),
            width=3,
            dont_extend_width=True,
        )

        # _input_field is a member variable intentionally,
        # so _default_focus_target can return it by reference
        # prompt_toolkit tracks focus by Window identity, so the
        # command handler must refocus the exact same object that is in the layout.
        self._input_field = Window(
            content=BufferControl(buffer=self.answer_buffer),
            height=1,
        )

        input_row = VSplit([input_prefix, self._input_field])

        feedback_window = Window(
            content=FormattedTextControl(self.get_feedback),
            height=1,
        )

        return HSplit([
            question_label,
            question_body,
            answer_label,
            input_row,
            Window(height=1),
            feedback_window,
        ])
        
    def run(self) -> None:
        self.app.run()
    
    def load_exercise_and_init_feedback(self) -> None:
        self.exercise = Exercise.get_exercise_from_json()
        self.set_feedback(feedback=self.generate_feedback(Feedback.HINT))            
    
    def get_question(self) -> list[tuple[str, str]]:
        return [("class:question", f" {self.exercise.get_question()}")]
    
    def get_feedback(self) -> list[tuple[str, str]]:
        return self._feedback
    
    def set_feedback(self, feedback:list[tuple[str,str]]) -> None:
        self._feedback = feedback

    def generate_feedback(self, feedback_type:Feedback) -> list[tuple[str, str]]:
        if feedback_type is Feedback.HINT:
            feedback = [("class:hint", f" Enter your answer above.")]
        elif feedback_type is Feedback.CORRECT:
            feedback = [("class:correct", f" Correct.")]
        elif feedback_type is Feedback.WRONG:
            feedback = [("class:wrong", f" Wrong! Try again.")]
        elif feedback_type is Feedback.ERROR_UNDEFINED_UNIT:
            feedback = [("class:error", " Unknown unit")]
        elif feedback_type is Feedback.ERROR_DIMENSIONALITY:
            feedback = [("class:error", " Incompatible dimensions")]
        elif feedback_type is Feedback.ERROR_OFFSET_UNIT:
            feedback = [("class:error", " Offset units (e.g. degC) not supported here")]
        elif feedback_type is Feedback.ERROR_ASSERTION:
            feedback = [("class:error", " Malformed expression")]
        elif feedback_type is Feedback.ERROR_UNEXPECTED:
            feedback = [("class:error", " Unexpected error - see log")]
        elif feedback_type is Feedback.ERROR_INVALID_FORMAT:
            feedback = [("class:error", " Invalid input format - expected a number followed by a unit")]
        else:
            raise ValueError("Unknown Feedback type")
        return feedback