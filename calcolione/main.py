"""Entry point for calcolione."""

import sys

from .ui import ExerciseUI


def main() -> int:
    """Start the main process.

    Returns:
        int: Exit code.
    """
    ExerciseUI().run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
