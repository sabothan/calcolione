from __future__ import annotations
import re
from pathlib import Path
import logging
import os
import sys
import subprocess


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
ANSWER_REL_TOLERANCE = 1e-2   # 1% relative tolerance
ANSWER_ABS_TOLERANCE = 1e-9   # fallback for near-zero values

# Quantity format specifier
QUANTITY_FORMAT_SPECIFIER = "~P"    # short, pretty
#QUANTITY_FORMAT_SPECIFIER = "~#P"   # short, compact, pretty (does type conversions: 1000m -> 1km)

# Path to the JSON exercise file
EXERCISE_FILE = Path(__file__).resolve().parent / "exercises.json"

# Path to the log-file
LOG_FILE = Path.home() / ".local" / "share" / "calcolione" / "calcolione.log"

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
    
    # Check for unresolved placeholders
    unresolved = re.findall(r"\{[^}]+\}", body)
    if unresolved:
        raise ValueError(f"Unresolved placeholders: {unresolved}")

    return body

def get_logger(name:str) -> logging.Logger:
    """Return a logger that writes to LOG_FILE.

    Creates the log directory if it does not exist.
    Safe to call multiple times - handlers are only added once.

    Args:
        name (str): Logger name, typically __name__ of the calling module.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        handler.setFormatter(logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        ))
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

    return logger

def open_in_editor(file:Path) -> None:
    """Helper function to open a file (logfile) in an editor.

    Args:
        file (Path): The path to the file
    """
    if sys.platform == "win32":
        os.startfile(file)
    elif sys.platform == "darwin":
        subprocess.run(["open", file])
    else:
        subprocess.run(["xdg-open", file])

# Custom Errors and exceptions
class InvalidInputFormatError(ValueError):
    """Raised when the answer string does not match the expected numeric format."""
    pass