# Contributing

## Code Style

### PEP 8

All Python code must follow [PEP 8](https://peps.python.org/pep-0008/). Key rules:

- Indentation: 4 spaces, no tabs.
- Maximum line length: 88 characters.
- Two blank lines between top-level definitions; one blank line between methods.
- Imports: one per line, grouped in order — standard library, third-party, local. Separated by blank lines.
- Naming: `snake_case` for functions and variables, `PascalCase` for classes, `UPPER_CASE` for constants.

This project uses `ruff` to enfore this automatically.

### Type Annotations

All public and private functions and methods must have type annotations on parameters and return types.

#### Forward References and `Self` (PEP 673)

When a classmethod returns an instance of its own class, use `Self` from `typing_extensions` (Python < 3.11) or `typing` (Python ≥ 3.11):

```python
from typing_extensions import Self

class MyClass:
    def __init__(self, my_var:float):
        self.my_var = my_var

    @classmethod
    def construct_from_dict(cls, data: dict) -> Self:
        return cls(my_var=data["value"])
        ...
```

`Self` is preferred over a quoted forward reference (`-> "Answer"`) for classmethods because it is semantically accurate: it refers to whatever class `cls` is, including subclasses. A quoted string annotation would incorrectly fix the return type to the base class and break subclass correctness.

> The `Self` type annotation is also useful for classmethods that return an instance of the class that they operate on.

See [PEP 673](https://peps.python.org/pep-0673/) for the full specification.

## Docstrings

All public modules, classes, and functions must have docstrings. Use the Google style:

```python
def prompt_qa(question: str) -> float:
    """Asks the user a question and prompts an answer.

    Args:
        question(str): The question to display to the user.

    Returns:
        float: The user's answer parsed as a float.

    Raises:
        ValueError: If the input cannot be converted to float.
    """
```

Rules:

- First line: a single short sentence, imperative mood, ending with a period.
- Leave one blank line before `Args`, `Returns`, and `Raises` sections.
- Omit sections that do not apply.
- Private methods (prefixed `_`) may omit docstrings if their purpose is obvious from context, but public API must always have them.
