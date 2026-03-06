"""Entry point for running AutoAnki as a module: python -m autoanki"""

import sys
from autoanki.cli import main

if __name__ == "__main__":
    sys.exit(main())
