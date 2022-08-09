import unittest
from unittest.mock import patch

from bor.color import (
    BLACK,
    BLUE,
    CYAN,
    GREEN,
    MAGENTA,
    RED,
    RESET,
    YELLOW,
    init_colors,
    set_color,
)


class TestColor(unittest.TestCase):
    def test_terminal_color_support(self):
        init_colors()

    @patch("bor.color.USE_COLOR", True)
    def test_colors(self):
        text = "this is test text"

        colored_text = set_color(BLACK, text)
        assert BLACK + text + RESET == colored_text

        colored_text = set_color(RED, text)
        assert RED + text + RESET == colored_text

        colored_text = set_color(GREEN, text)
        assert GREEN + text + RESET == colored_text

        colored_text = set_color(YELLOW, text)
        assert YELLOW + text + RESET == colored_text

        colored_text = set_color(BLUE, text)
        assert BLUE + text + RESET == colored_text

        colored_text = set_color(MAGENTA, text)
        assert MAGENTA + text + RESET == colored_text

        colored_text = set_color(CYAN, text)
        assert CYAN + text + RESET == colored_text

    @patch("bor.color.USE_COLOR", True)
    def test_false_color(self):
        text = "this is test text"
        colored_text = set_color(YELLOW, text)
        assert text != colored_text
