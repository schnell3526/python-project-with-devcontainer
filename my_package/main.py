"""main.py"""

from logging import INFO, basicConfig, getLogger

basicConfig(level=INFO)
logger = getLogger(__name__)


def greet(name: str) -> str:
    """Return a greeting message."""
    return f"Hello, {name}!"


def main() -> None:
    """Main function to execute the script."""
    name = "World"
    greeting = greet(name)
    logger.info(greeting)


if __name__ == "__main__":
    main()
