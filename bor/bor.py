import argparse
import ast
import re
import sys
from pathlib import Path
from typing import Dict, Final, Iterable, Type, Union, cast

from bor.color import BLUE, GREEN, RED, set_color

NamedNodeType = Union[Type[ast.FunctionDef], Type[ast.ClassDef]]
VAR_TYPES: Final[Dict[str, NamedNodeType]] = {
    "def": ast.FunctionDef,
    "class": ast.ClassDef,
}


def analyzer(data: dict, pattern: str) -> None:
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
                values = sorted(map(int, value.split(",")))[0]
                print(
                    f"{set_color(BLUE, key)} at {set_color(GREEN, path)}:{values}"
                )
    else:
        return None


def searcher(
    source: ast.AST, file_path: Path, node_type: NamedNodeType
) -> dict:
    nodes: Dict[str, str] = {}

    for node in ast.walk(source):
        if isinstance(node, node_type):
            named_node = cast(NamedNodeType, node).name
            node_data = {named_node: str(node.lineno)}
            if nodes.get(named_node, None):
                old_key = nodes.get(named_node)
                node_data = {named_node: str(node.lineno) + "," + old_key}
            nodes.update(node_data)

    return {"path": file_path.as_posix(), "nodes": nodes}


def file_parser(file_path: Path, ignore_error: bool) -> ast.Module:
    try:
        file = file_path.resolve().as_posix()
        with open(file) as f:
            source = ast.parse(f.read())
            return source
    except Exception as error:
        if ignore_error:
            return None
        print(f"{set_color(RED, error)} at {set_color(BLUE, file_path)}")
        sys.exit(1)


def get_paths(path: Path) -> Iterable[Path]:
    if path.is_dir():
        return path.glob("**/*.py")
    else:
        return [path]


def pattern_is_valid(pattern: str) -> bool:
    if pattern.startswith("."):
        pattern = pattern[1:]
    if pattern.endswith("."):
        pattern = pattern[:-1]

    return pattern.isidentifier()


def main() -> None:
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
        if var_type not in VAR_TYPES or not pattern_is_valid(pattern):
            print("Invalid keyword or pattern.")
            sys.exit(1)

    path = params[2] if len(params) > 2 else "."
    node_type = VAR_TYPES.get(var_type)
    ignore = args.ignore_error

    for file_path in get_paths(Path(path)):
        try:
            source = file_parser(file_path, ignore)
            if source:
                analyzer(searcher(source, file_path, node_type), pattern)
        except KeyboardInterrupt:
            sys.exit(1)


if __name__ == "__main__":
    main()
