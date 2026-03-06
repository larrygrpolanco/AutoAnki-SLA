"""Command-line interface for AutoAnki."""

import argparse
import sys
from pathlib import Path


def main() -> int:
    """Main entry point for the AutoAnki CLI."""
    parser = argparse.ArgumentParser(
        prog="autoanki",
        description="Generate pedagogically-structured Anki vocabulary decks from educational text",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to configuration file (optional)",
    )

    args = parser.parse_args()

    # TODO: Launch Textual TUI when implemented
    print("AutoAnki TUI - Coming in Phase 5")
    print("Run 'autoanki --help' for available options")

    return 0


if __name__ == "__main__":
    sys.exit(main())
