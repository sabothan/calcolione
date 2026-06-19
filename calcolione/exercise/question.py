from typing_extensions import Self  # PEP 673

from .qvar import QVar
from ..utils import substitute_placeholders


class Question:
    """Wrapper class to hold a question and it's information."""

    def __init__(self, message: str, vars: list[QVar]):
        self.message = message
        self.vars = vars

        # Post-init processes
        self.message = self._render_message()

    @classmethod
    def from_dict(cls, question: dict, vars: list) -> Self:
        """Serves as an additional constructor, but with input from a `dict`.

        Args:
            question (dict): the input dictionary

        Returns:
            Question: The instantiated class.
        """
        return cls(
            message=question["message"],
            vars=[QVar.from_dict(var) for var in vars],
        )

    def _render_message(self) -> str:
        """Substitutes the actual values for the placeholders in a question's body.

        Returns:
            str: The message body with substituted placeholders.
        """
        parsed_message = substitute_placeholders(vars=self.vars, body=self.message)
        return parsed_message

    def _get_question(self) -> str:
        """Get the question body (message).

        Returns:
            str: the question message
        """
        return self.message
