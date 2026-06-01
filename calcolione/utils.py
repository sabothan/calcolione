import re

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
