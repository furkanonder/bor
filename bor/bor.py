import argparse
import ast
import re
import sys
from pathlib import Path

from bor.color import BLUE, GREEN, RED, set_color

var_types = {"def": ast.FunctionDef, "class": ast.ClassDef}


def analyzer(data, pattern):
    if nodes := data.get("nodes"):
        path = data.get("path")
        pattern = pattern.replace(".", "*")

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
                values = sorted(map(int, value.split(",")))
                print(
                    set_color(BLUE, key),
                    "at",
                    set_color(GREEN, path),
                    ":",
                    values,
                )
    else:
        return None


def searcher(source, file, var_type):
    data = {"path": file.resolve().as_posix(), "nodes": {}}
    node_type = var_types.get(var_type)

    for node in ast.walk(source):
        if isinstance(node, node_type):
            node_data = {node.name: str(node.lineno)}
            nodes = data.get("nodes")
            if nodes.get(node.name):
                old_key = nodes.get(node.name)
                node_data = {node.name: str(node.lineno) + "," + old_key}
            nodes.update(node_data)

    return data


def file_parser(file, ignore_error):
    try:
        file = file.resolve().as_posix()
        with open(file) as f:
            source = ast.parse(f.read())
            return source
    except Exception as error:
        if ignore_error:
            return None
        print(set_color(RED, error), "at " + set_color(BLUE, file))
        sys.exit(1)


def get_paths(path):
    if path.is_dir():
        return path.glob("**/*.py")
    return [path]


def pattern_is_valid(pattern):
    if pattern.startswith("."):
        pattern = pattern[1:]
    if pattern.endswith("."):
        pattern = pattern[:-1]

    return pattern.isidentifier()


def main():
    parser = argparse.ArgumentParser(
        description="User friendly, tiny source code searcher written by pure Python."
    )
    parser.add_argument("-v", "--version", action="version", version="0.1.0")
    parser.add_argument(
        "-i",
        "--ignore-error",
        action="store_true",
        default=False,
        help="Ignore the errors with analyzing files.",
    )

    args, params = parser.parse_known_args()

    if len(params) < 2:
        print("No keyword or pattern provided.")
        sys.exit(1)
    else:
        var_type, pattern = params[0], params[1]
        if var_type not in var_types or not pattern_is_valid(pattern):
            print("Invalid keyword or pattern.")
            sys.exit(1)

    path = params[2] if len(params) > 2 else "."
    ignore = args.ignore_error

    for file in get_paths(Path(path)):
        try:
            source = file_parser(file, ignore)
            if source:
                analyzer(searcher(source, file, var_type), pattern)
        except KeyboardInterrupt:
            sys.exit(1)


if __name__ == "__main__":
    main()
