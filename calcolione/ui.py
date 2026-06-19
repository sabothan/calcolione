"""Terminal UI for calcolione using prompt_toolkit."""

from abc import ABC, abstractmethod
from typing import Callable, Any

from prompt_toolkit import PromptSession, Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.filters import Condition
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.validation import ValidationError, Validator
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl

from .exercise import Exercise
from .utils import ALLOWED_SYMBOLS


# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------

STYLE = Style.from_dict({
    "header":   "bg:#1e1e2e fg:#cdd6f4 bold",
    "title":    "#89b4fa bold",
    "body":     "bg:#1e1e2e",
    "footer":   "bg:#1e1e2e fg:#6c7086",

    "label":    "fg:#89b4fa bold",
    "question": "fg:#cdd6f4",
    "prompt":   "fg:#89dceb bold",
    "hint":     "#6c7086",
    "correct":  "fg:#a6e3a1 bold",
    "wrong":    "fg:#f38ba8 bold",
    "warning":  "fg:#f9e2af",
    "dim":      "fg:#6c7086",
})


# ---------------------------------------------------------------------------
# Input validator
# ---------------------------------------------------------------------------

class AnswerFormatValidator(Validator):
    """Rejects input that contains disallowed characters."""

    def validate(self, document: object) -> None:
        """Validate the document text against the allowed symbols pattern.

        Args:
            document: The prompt_toolkit Document to validate.

        Raises:
            ValidationError: If the text contains disallowed characters.
        """
        text = document.text  # type: ignore[attr-defined]
        if text and not ALLOWED_SYMBOLS.match(text):
            raise ValidationError(
                message="Invalid characters - use digits, units (km, m/s ...), +, -, *, /",
                cursor_position=len(text),
            )


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

class UI(ABC):
    def __init__(self, screen_title:str) -> None:
        self._screen_title = screen_title

        self._session: PromptSession = PromptSession(  # type: ignore[type-arg]
            validator=AnswerFormatValidator(),
            validate_while_typing=False,
        )

        self.kb = KeyBindings()

        # Layout, body and command_buffer are built once in __init__ and cached.
        # Rebuilding them would discard the existing Window objects, causing
        # prompt_toolkit to lose focus tracking - keypresses would stop
        # registering until focus is explicitly reset.
        self.body = self.make_body()
        self.command_buffer: Buffer = Buffer(name="command")
        self._command_window: Window = Window(
            content=BufferControl(buffer=self.command_buffer),
            height=1,
        )

        self._register_keybindings()
        self.app = Application(
            layout=self.make_layout(),
            key_bindings=self.kb,
            style=STYLE,
            full_screen=True,
            mouse_support=False,
        )

    @property
    def screen_title(self) -> str:
        return self._screen_title

    @screen_title.setter
    def screen_title(self, value:str) -> None:
        self._screen_title = value

    def _register_keybindings(self) -> None:
        @self.kb.add(":")
        def enter_command_mode(event: object) -> None:
            self.command_buffer.reset()
            self.command_buffer.insert_text(":")
            event.app.layout.focus(self._command_window)  # type: ignore[attr-defined]

    def make_layout(self):
        header = Window(
            content=FormattedTextControl([("class:header", " calcolione - calculation trainer ")]),
            height=1,
        )

        title = Window(
            content=FormattedTextControl([("class:title", f"{self.screen_title}")]),
            height=1,
        )

        divider = Window(height=1, char="-")

        body = self.body # use the cached body

        footer = Window(
            content=FormattedTextControl([("class:footer", "quit, navigation, commands")]),
            height=1,
        )

        root = HSplit([
            header,
            title,
            divider,
            Window(height=1),
            body,
            Window(height=0), # fill remaining space
            divider,
            footer,
        ])

        return Layout(root)

    @abstractmethod
    def make_body(self) -> HSplit:
        ...

   
class ExerciseUI(UI):
    def __init__(self):
        # Define the answer buffer
        self.answer_buffer = Buffer(name="answer")
        self.answer_buffer.accept_handler = self._handle_answer

        # Read question
        self.question = "Question goes here"

        super().__init__(screen_title="Exercise")

    def _register_keybindings(self) -> None:
        super()._register_keybindings()  # gets the : binding

        @self.kb.add("q", filter=Condition(lambda: self.answer_buffer.text == ""))
        def quit_app(event: object) -> None:
            """Quit only when the input buffer is empty (so typing 'q' still works)."""
            get_app = event.app  # type: ignore[attr-defined]
            get_app.exit()

    def _handle_answer(self, buf: Buffer) -> bool:
        # TODO call exercise.answer._input_answer_from_string(answer), evaluate, update feedback
        answer = buf.text.strip()
        # process answer
        buf.reset()
        return False

    def make_body(self) -> HSplit:
        question_label = Window(
            content=FormattedTextControl([("class:label", " Exercise")]),
            height=1,
        )

        question_body = Window(
            content=FormattedTextControl([("class:question", f" {self.question}")]),
            height=3,
            wrap_lines=True,
        )

        answer_label = Window(
            content=FormattedTextControl([("class:label", " Your answer (press ENTER to submit):")]),
            height=1,
        )

        _input_prefix = Window(
            content=FormattedTextControl([("class:prompt", " > ")]),
            width=3,
            dont_extend_width=True,
        )

        _input_field = Window(
            content=BufferControl(buffer=self.answer_buffer),
            height=1,
        )

        input_row = VSplit([_input_prefix, _input_field])

        feedback_window = Window(
            content=FormattedTextControl([("class:feedback", "feedback goes here")])
        )

        exercise_container = HSplit([
            question_label,
            question_body,
            answer_label,
            input_row,
            Window(height=1),
            feedback_window,
        ])

        return exercise_container
