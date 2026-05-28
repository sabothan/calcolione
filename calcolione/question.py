from calcolione import QVar


class Question:
    """Wrapper class to hold a question and it's information."""

    def __init__(self, message: str, vars: list[QVar]):
        self.message = message
        self.vars = vars

        # Post-init processes
        self.message = self._render_message()

    @classmethod
    def from_dict(cls, question: dict):
        """Serves as an additional constructor, but with input from a `dict`.

        Args:
            question (dict): the input dictionary

        Returns:
            The instantiated class.
        """
        return cls(
            message=question["message"],
            vars=[QVar.from_dict(var) for var in question["vars"]],
        )

    def _render_message(self):
        substitutions = {}

        # Generate subsitutions prompts for the message string
        for var in self.vars:
            substitutions[f"{var.name}.value"] = var.value
            substitutions[f"{var.name}.unit"] = var.unit

        message = self.message

        # Substitute <value, unit> tuples into messages
        for key, val in substitutions.items():
            message = message.replace("{" + key + "}", str(val))

        return message

    def _get_question(self) -> str:
        """Get the question body (message).

        Returns:
            str: the question message
        """
        return self.message

