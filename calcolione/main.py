"""Entry point for calcolione."""

import argparse
import sys

from .ui.exercise_ui import ExerciseUI
from .utils import LOG_FILE, open_in_editor


def main() -> int:
    """Start the main process.

    Returns:
        int: Exit code.
    """
    parser = argparse.ArgumentParser(
        prog="calcolione",
        description="Train applied physics and math calculations.",
        epilog="Run without flags to start the exercise session.",
    )
    parser.add_argument(
        "--logfile",
        action="store_true",
        help="Open the log file in the system default editor.",
    )
    args = parser.parse_args()

    if args.logfile:
        if not LOG_FILE.exists():
            print(f"No log file found at {LOG_FILE}")
            return 1
        open_in_editor(LOG_FILE)
    else:
        ExerciseUI().run()

    return 0


if __name__ == "__main__":
    sys.exit(main())
