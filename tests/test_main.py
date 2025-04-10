"""Test the main module of the package."""

from my_package.main import greet


def test_greet() -> None:
    assert greet("World") == "Hello, World!"
    assert greet("Alice") == "Hello, Alice!"
    assert greet("Bob") == "Hello, Bob!"
