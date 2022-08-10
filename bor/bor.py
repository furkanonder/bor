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


def get_regex(pattern: str) -> str:
    pattern = pattern.replace(".", "*")

    if pattern.startswith("*") and pattern.endswith("*"):
        regex = f'{pattern.split("*")[1]}+'
    elif not pattern.startswith("*") and pattern.endswith("*"):
        regex = f'^{pattern.split("*")[0]}'
    elif pattern.startswith("*") and not pattern.endswith("*"):
        regex = f'{pattern.split("*")[1]}$'
    else:
        regex = f"^{pattern}$"

    return regex


def analyzer(data: dict, pattern: str) -> None:
    if nodes := data.get("nodes"):
        path = data.get("path")
        rgx = get_regex(pattern)

        for key, value in nodes.items():
            if re.search(rgx, key):
                print(
                    f"{set_color(BLUE, key)} at {set_color(GREEN, path)}:{value}"
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
                node_data = {
                    named_node: f"{node.lineno}, {nodes.get(named_node)}"
                }
            nodes.update(node_data)

    return {"path": file_path.as_posix(), "nodes": nodes}


def file_parser(file_path: Path, ignore_syntax_error: bool) -> ast.Module:
    try:
        with open(file_path.resolve().as_posix()) as file:
            source = ast.parse(file.read())
            return source
    except Exception as err:
        if ignore_syntax_error:
            return None
        else:
            print(f"{set_color(RED, err)} at {set_color(BLUE, file_path)}")
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
    ignore_syntax_error = args.ignore_error

    for file_path in get_paths(Path(path)):
        try:
            if source := file_parser(file_path, ignore_syntax_error):
                analyzer(searcher(source, file_path, node_type), pattern)
        except KeyboardInterrupt:
            sys.exit(1)


if __name__ == "__main__":
    main()
