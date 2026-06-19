"""Terminal UI for calcolione using prompt_toolkit."""

from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl

from ..exercise.exercise import Exercise
from ..utils import ALLOWED_SYMBOLS
from .base_ui import UI

# ---------------------------------------------------------------------------
# Exercise screen
# ---------------------------------------------------------------------------

class ExerciseUI(UI):
    """Exercise screen - displays a question and accepts the user's answer."""

    def __init__(self) -> None:
        # answer_buffer and question must exist before super().__init__()
        # because make_body (called by the base class) references them.
        self.answer_buffer: Buffer = Buffer(name="answer")
        self.answer_buffer.accept_handler = self._handle_answer  # type: ignore[assignment]

        self._question: tuple[str, str] = ("class:question", "Question goes here: ...")
        self._feedback: tuple[str, str] = ("class:hint", " Enter your answer above.")

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
        # TODO: exercise.answer._input_answer_from_string(answer)
        # TODO: evaluate and update feedback window
        buf.reset()
        return False

    def _get_feedback_text(self) -> list[tuple[str, str]]:
        return [self._feedback]
    
    def _get_question_text(self) -> list[tuple[str, str]]:
        return [self._question]

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
            content=FormattedTextControl(self._get_question_text),
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
            content=FormattedTextControl(self._get_feedback_text),
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
