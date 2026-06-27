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
    log_group = parser.add_mutually_exclusive_group()
    log_group.add_argument(
        "--logfile",
        action="store_true",
        help="Open the log file in the system default editor. (The application won't be started)",
    )
    log_group.add_argument(
        "--clear-logfile",
        action="store_true",
        help="Clear the log file.",
    )
    args = parser.parse_args()

    if args.logfile:
        if not LOG_FILE.exists():
            print(f"No log file found at {LOG_FILE}")
            return 1
        open_in_editor(LOG_FILE)
    elif args.clear_logfile:
        if not LOG_FILE.exists():
            print(f"No log file found at {LOG_FILE}")
            return 1
        LOG_FILE.write_text("")
        print(f"Log file cleared: {LOG_FILE}")
        return 0
    else:
        ExerciseUI().run()

    return 0


if __name__ == "__main__":
    sys.exit(main())
