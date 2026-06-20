"""Terminal UI for calcolione using prompt_toolkit."""

from __future__ import annotations
from enum import Enum
from pint.errors import UndefinedUnitError, DimensionalityError, OffsetUnitCalculusError
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.application import get_app
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl

from ..exercise.exercise import Exercise
from ..utils import ALLOWED_SYMBOLS, get_logger
from .base_ui import UI

# Create the logger instance
# TODO make sure the logger is created only once globally.
# Necessary, once multiple screens are implemented.
log = get_logger(__name__)

class Feedback(Enum):
    HINT = 1
    CORRECT = 2
    WRONG = 3
    ERROR = 4
    
# ---------------------------------------------------------------------------
# Exercise screen
# ---------------------------------------------------------------------------

class ExerciseUI(UI):
    """Exercise screen - displays a question and accepts the user's answer."""

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

        self.exercise.input_answer(answer=answer)
        
        is_correct = self.exercise.evaluate_answer()
        if is_correct:
            feedback = self.generate_feedback(Feedback.CORRECT)
        else:
            feedback = self.generate_feedback(Feedback.WRONG)

        self.set_feedback(feedback)
        get_app().invalidate()

        buf.reset()
        return False

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
        else:
            raise ValueError("Unknown Feedback type")
        
        return feedback
