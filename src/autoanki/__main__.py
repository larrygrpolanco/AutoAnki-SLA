import sys

from dotenv import load_dotenv


def main() -> None:
    # Load .env from working directory or project root
    load_dotenv()

    # Check for API key early so the error is clear
    import os
    if not os.getenv("OPENAI_API_KEY"):
        print(
            "Error: OPENAI_API_KEY is not set.\n"
            "Create a .env file in the current directory with:\n"
            "  OPENAI_API_KEY=sk-your-key-here\n"
            "Or set it as an environment variable."
        )
        sys.exit(1)

    from .cli import run
    run()


if __name__ == "__main__":
    main()
