import ast
import re
import unittest
from pathlib import Path

from bor.bor import file_parser, get_paths, pattern_is_valid, searcher


class TestBor(unittest.TestCase):
    def setUp(self):
        base_path = Path.cwd()
        test_path = Path("/examples/test.py")
        self.path = base_path / test_path.relative_to(test_path.anchor)

    def test_path(self):
        path = Path(".")
        self.assertTrue(get_paths(path), path)

    def test_file_parser(self):
        source = file_parser(self.path, ignore_error=False)
        self.assertIsInstance(source, ast.Module)

    def test_searcher(self):
        var_type = "def"

        for file in get_paths(Path(self.path)):
            source = file_parser(file, ignore_error=False)
            data = searcher(source, file, var_type)

        nodes = list(data.get("nodes"))
        self.assertIn("get_value", nodes)
        self.assertIn("catch_me_if_you_can", nodes)
        self.assertIn("am_i_blue_cat", nodes)

    def test_analyzer(self):
        results = []
        pattern = ".Cat"
        var_type = "class"
        pattern = pattern.replace(".", "*")

        for file in get_paths(Path(self.path)):
            source = file_parser(file, ignore_error=False)
            data = searcher(source, file, var_type)

        nodes = data.get("nodes")

        if pattern.startswith("*") and pattern.endswith("*"):
            regex = pattern.split("*")[1] + "+"
        elif not pattern.startswith("*") and pattern.endswith("*"):
            regex = "^" + pattern.split("*")[0]
        elif pattern.startswith("*") and not pattern.endswith("*"):
            regex = pattern.split("*")[1] + "$"
        else:
            regex = "^" + pattern + "$"

        for key, value in nodes.items():
            if re.search(regex, key):
                results.append(key)

        self.assertEqual(regex, "Cat$")
        self.assertIn("Cat", results)
        self.assertIn("BlueCat", results)

    def test_pattern(self):
        self.assertTrue(pattern_is_valid(".test."), True)
        self.assertTrue(pattern_is_valid(".get"), True)
        self.assertTrue(pattern_is_valid(".get_value"), True)
        self.assertFalse(pattern_is_valid("Turkey.23"), False)
        self.assertFalse(pattern_is_valid("Ti?ger./"), False)
        self.assertFalse(pattern_is_valid("get!"), False)
