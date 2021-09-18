import argparse
import ast
import re
import sys
from pathlib import Path

var_types = {"def": ast.FunctionDef, "class": ast.ClassDef}


def analyzer(data, pattern):
    nodes = data.get("nodes")
    if nodes == {}:
        return

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
            print(key, "at", path, ":", value)


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


def file_parser(file):
    try:
        file = file.resolve().as_posix()
        with open(file) as f:
            source = ast.parse(f.read())
            return source
    except Exception as error:
        print(error, " at " + file)
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


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="User friendly, tiny source code searcher written by pure Python."
    )
    parser.add_argument("-v", "--version", action="version", version="0.0.1")

    args, params = parser.parse_known_args()
    var_type, pattern = params[0], params[1]
    path = params[2] if len(params) > 2 else "."

    if len(params) < 2 or var_type not in var_types or not pattern_is_valid(pattern):
        print("Please, check your inputs.")
        sys.exit(1)

    for file in get_paths(Path(path)):
        try:
            source = file_parser(file)
            if source:
                analyzer(searcher(source, file, var_type), pattern)
        except KeyboardInterrupt:
            sys.exit(1)


if __name__ == "__main__":
    main()
