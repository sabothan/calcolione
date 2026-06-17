from __future__ import annotations
import re
from pathlib import Path


# Allowed symbols for user input
ALLOWED_SYMBOLS = re.compile(r"^[.,/*a-zA-Z0-9 \-+%°^()]+$")

# <numeric, unit>
# Regex pattern:
# - `^` — start of string
# - `([-+]?\d+[.,]?\d*)` — **capture group 1: the number**
#   - `[-+]?` — optional sign
#   - `\d+` — one or more digits (required)
#   - `[.,]?` — optional decimal separator, either `.` or `,`
#   - `\d*` — zero or more digits after the separator
# - `\s*` — zero or more whitespace between number and unit
# - `(.*)` — **capture group 2: the unit**, anything remaining
# - `$` - end of string
NUMERIC_UNIT_PATTERN = re.compile(r"^([-+]?\d+[.,]?\d*)\s*(.*)$")

# Tolerance to evaluate a given answer its correctness
ANSWER_TOLERANCE = 0.01

# Quantity format specifier
QUANTITY_FORMAT_SPECIFIER = "~P"    # short, pretty
#QUANTITY_FORMAT_SPECIFIER = "~#P"   # short, compact, pretty (does type conversions: 1000m -> 1km)

# Path to the JSON exercise file
EXERCISE_FILE = Path(__file__).resolve().parent / "exercises.json"



def substitute_placeholders(vars: list, body: str):
    """Substitutes the actual values for the placeholders in a question's body.

    Args:
        vars (list[QVar]): A list of variables.
        body (str): A string containing placeholders.

    Returns:
        str: The body with substituted placeholders.
    """
    substitutions = {}

    # Generate subsitution prompts for the body string
    for var in vars:
        substitutions[f"{var.name}.value"] = str(var)
    
    # Substitute the variables into the body
    for key, val in substitutions.items():
        body = body.replace("{" + key + "}", str(val))
    
    return body