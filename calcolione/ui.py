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
# UI base class
# ---------------------------------------------------------------------------

class UI(ABC):
    """Abstract base class for all UI screens.

    Subclasses must implement `make_body`, which returns the screen-specific
    content. The shared chrome (header, title, dividers, command footer) is
    assembled by `make_layout` on this base class.

    Initialisation order in `__init__` is load-bearing:
        1. `body` - built first because `make_body` may reference subclass
           state (e.g. buffers) that must exist before the layout is assembled.
        2. `command_buffer` / `_command_window` - built before keybindings
           because the `:` binding references `_command_window`.
        3. `_register_keybindings` - called before `Application` so all
           bindings are registered when the app starts.
        4. `Application` - constructed last, consuming the layout.
    """

    def __init__(self, screen_title: str) -> None:
        self._screen_title = screen_title

        # TODO: wire up once Application flow is finalised
        self._session: PromptSession = PromptSession(  # type: ignore[type-arg]
            validator=AnswerFormatValidator(),
            validate_while_typing=False,
        )

        self.kb = KeyBindings()

        # Layout, body, and command_buffer are built once and cached here.
        # Rebuilding them would discard the existing Window objects, causing
        # prompt_toolkit to lose focus tracking - keypresses would stop
        # registering until focus is explicitly reset.
        self.body: HSplit = self.make_body()

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
        """The title displayed below the header bar."""
        return self._screen_title

    @screen_title.setter
    def screen_title(self, value: str) -> None:
        self._screen_title = value

    def _register_keybindings(self) -> None:
        """Register keybindings shared across all screens.

        Subclasses should call super()._register_keybindings() first,
        then add their own bindings to self.kb.
        """
        @self.kb.add(":")
        def enter_command_mode(event: object) -> None:
            """Shift focus to the command footer on `:`, vim-style."""
            self.command_buffer.reset()
            self.command_buffer.insert_text(":")
            event.app.layout.focus(self._command_window)  # type: ignore[attr-defined]

    def make_layout(self) -> Layout:
        """Assemble the full screen layout from shared chrome and the cached body.

        Returns:
            Layout: The complete screen layout.
        """
        header = Window(
            content=FormattedTextControl([("class:header", " calcolione - calculation trainer ")]),
            height=1,
        )
        title = Window(
            content=FormattedTextControl([("class:title", f" {self.screen_title}")]),
            height=1,
        )
        divider = Window(height=1, char="-")
        footer = Window(
            content=FormattedTextControl([("class:footer", " :quit  :help")]),
            height=1,
        )

        root = HSplit([
            header,
            title,
            divider,
            Window(height=1),
            self.body,          # cached - never rebuilt after __init__
            Window(height=0),   # fills remaining vertical space
            divider,
            footer,
            self._command_window,
        ])

        return Layout(root)

    @abstractmethod
    def make_body(self) -> HSplit:
        """Build the screen-specific content container.

        Called once during __init__ and cached on self.body.

        Returns:
            HSplit: The screen content.
        """
        ...


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

        self.question = "Question goes here"

        super().__init__(screen_title="Exercise")

    def _register_keybindings(self) -> None:
        super()._register_keybindings()  # inherit shared bindings (`:` command mode)

        @self.kb.add("q", filter=Condition(lambda: self.answer_buffer.text == ""))
        def quit_app(event: object) -> None:
            """Quit when the answer buffer is empty - typing `q` still works."""
            event.app.exit()  # type: ignore[attr-defined]

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
            content=FormattedTextControl([("class:question", f" {self.question}")]),
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
        input_field = Window(
            content=BufferControl(buffer=self.answer_buffer),
            height=1,
        )
        input_row = VSplit([input_prefix, input_field])

        # TODO: make feedback dynamic - update content after each answer attempt
        feedback_window = Window(
            content=FormattedTextControl([("class:hint", " feedback goes here")]),
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
