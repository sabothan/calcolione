"""Terminal UI for calcolione using prompt_toolkit."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable, Any

from prompt_toolkit import PromptSession, Application
from prompt_toolkit.application import get_app
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.filters import Condition, has_focus
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.validation import ValidationError, Validator
from prompt_toolkit.layout import Layout, ScrollablePane
from prompt_toolkit.layout.containers import HSplit, VSplit, Window, ConditionalContainer, FloatContainer
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl

from ..exercise.exercise import Exercise
from ..utils import ALLOWED_SYMBOLS


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
    "correct":  "fg:#40ff80 bold",   # bright lime green
    "wrong":    "fg:#ff5555 bold",   # strong red
    "warning":  "fg:#ffb86c bold",   # orange
    "error":    "fg:#ff9500 bold",   # amber/orange, distinct from wrong
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
    COMMANDS = {
        "quit": {
            "cmd": ["q", "quit"],
            "description": "Exit the application",
        },
        "help": {
            "cmd": ["h", "help"],
            "description": "Show/hide help information",
        },
    }

    def __init__(self, screen_title: str) -> None:
        self._screen_title = screen_title
        self._help_visible : bool = False

        self._session: PromptSession = PromptSession(  # type: ignore[type-arg]
            validator=AnswerFormatValidator(),
            validate_while_typing=False,
        )

        self.kb = KeyBindings()

        # None means "show hints"; any string means "show that feedback instead"
        self._command_feedback : str | None = None

        # Layout, body, and command_buffer are built once and cached here.
        # Rebuilding them would discard the existing Window objects, causing
        # prompt_toolkit to lose focus tracking - keypresses would stop
        # registering until focus is explicitly reset.
        self.body: HSplit = self.make_body()
        self.command_buffer: Buffer = Buffer(name="command")
        self._command_window: Window = Window(
            content=BufferControl(buffer=self.command_buffer),
            height=1,
            dont_extend_height=True,
        )

        # Setup the command buffer and the keybindings
        self.command_buffer.accept_handler = self._handle_command
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
    
    @property
    @abstractmethod
    def _default_focus_target(self) -> Buffer:
        """The window that should receive focus after a command is dispatched."""
        ...

    def _register_keybindings(self) -> None:
        """Register keybindings shared across all screens.

        Subclasses should call super()._register_keybindings() first,
        then add their own bindings to self.kb.
        """
        @self.kb.add(":")
        def enter_command_mode(event: object) -> None:
            """Shift focus to the command footer on `:`, vim-style."""
            self._command_feedback = None
            self.command_buffer.reset()
            self.command_buffer.insert_text(":")
            event.app.layout.focus(self._command_window)  # type: ignore[attr-defined]
        
        @self.kb.add("enter", filter=has_focus(self.command_buffer))
        def submit_command(event: object) -> None:
            self.command_buffer.validate_and_handle()
        
        @self.kb.add("escape", eager=True)
        def close_help(event: object) -> None:
            """Close the help screen on Escape."""
            if self._help_visible:
                self._help_visible = False
                event.app.layout.focus(self._default_focus_target)  # type: ignore[attr-defined]
                event.app.invalidate()  # type: ignore[attr-defined]
        
    def _handle_command(self, buf: Buffer) -> bool:
        """Dispatch a vim-style command entered in the command footer.

        Args:
            buf (Buffer): The command buffer.

        Returns:
            bool: False to clear the buffer after submission.
        """
        cmd = buf.text.strip().lstrip(":")

        if cmd in self.COMMANDS["quit"]["cmd"]:
            get_app().exit()
        elif cmd in self.COMMANDS["help"]["cmd"]:
            self._help_visible = not self._help_visible
            get_app().invalidate()
        else:
            self._command_feedback = f"Not a command/not implemented yet: {cmd}"

        get_app().layout.focus(self._default_focus_target)
        buf.reset()
        return False

    def _footer_text(self) -> list[tuple[str, str]]:
        if self._command_feedback is not None:
            text = [("class:warning", f" {self._command_feedback}")]
        else:
            text = [("class:footer", " Type `:` to enter command mode. E.g. `:help`")]
        
        return text

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
            content=FormattedTextControl(self._footer_text),
            height=1,
        )

        help_text = "".join(text for _, text in self._help_content())
        help_buffer = Buffer(
            document=Document(help_text),
            read_only=True,
            name="help",
        )
        body_or_help_window = ConditionalContainer(
            content=self.body,
            alternative_content=ScrollablePane(
                content=Window(
                    content=BufferControl(buffer=help_buffer, focusable=True),
                    wrap_lines=True,
                ),
                show_scrollbar=True,
                keep_cursor_visible=False,
            ),
            filter=Condition(lambda: not self._help_visible),
        )

        root = HSplit([
            header,
            title,
            divider,
            Window(height=1),
            body_or_help_window,
            Window(),   # fills remaining vertical space
            divider,
            footer,
            self._command_window,
        ])

        return Layout(root, focused_element=self._default_focus_target)

    @abstractmethod
    def make_body(self) -> HSplit:
        """Build the screen-specific content container.

        Called once during __init__ and cached on self.body.

        Returns:
            HSplit: The screen content.
        """
        ...
    
    def _help_content(self) -> list[tuple[str, str]]:
        """Return formatted help text for this screen.
 
        Renders the COMMANDS registry. Subclasses should call super() and
        extend with screen-specific sections.
 
        Returns:
            list[tuple[str, str]]: Formatted text fragments for the help window.
        """
        lines: list[tuple[str, str]] = [
            ("class:label", " Keybindings\n"),
        ]
        for entry in self.COMMANDS.values():
            cmds = " / ".join(f":{c}" for c in entry["cmd"])
            lines.append(("class:hint", f"   {cmds:<20} {entry['description']}\n"))
        lines.append(("", "\n"))
        lines.append(("class:dim", " Press Escape to close\n"))
        return lines
