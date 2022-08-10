<div align="center">
  <img src="/assets/logo/bor.png" width=300px />
  <h3>User-friendly, tiny source code searcher written in pure Python.</h3>
  <a href="https://github.com/furkanonder/bor/actions"><img alt="Actions Status" src="https://github.com/furkanonder/bor/workflows/Test/badge.svg"></a>
  <a href="https://github.com/furkanonder/bor/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/furkanonder/bor"></a>
  <a href="https://github.com/furkanonder/bor/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/furkanonder/bor"></a>
  <a href="https://github.com/furkanonder/bor/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/furkanonder/bor"></a>
  <a href="https://pepy.tech/project/bor"><img alt="Downloads" src="https://pepy.tech/badge/bor"></a>
</div>

## Installation

_bor_ can be installed by running `pip install bor`. It requires Python 3.8.0+ to run.

## Usage

_bor_ currently supports `class` and `def` keywords. Other Python keywords will be added
in the future releases.

```sh
bor {keyword} {pattern}
```

By default, _bor_ runs in your current directory. You can run _bor_ with the specific
source file or directory:

```sh
bor {keyword} {pattern} {source_file_or_directory}
```

## Configuration

By default, if _bor_ encounters an error(syntax, indentation error etc.) while analyzing
files, it will stop working. If you want to the ignore errors, you can use
`--ignore-error` or `-i` argument. For example;

```sh
bor class Cat --ignore-error
```

## Example Usages

`Cat` is equivalent in the regular expression as `^Cat$`

```sh
bor class Cat
```

Output:

```sh
Cat at examples/test.py:18
```

---

`.Cat` is equivalent in the regular expression as `Cat$`

```sh
bor class .Cat
```

Output:

```sh
Cat at examples/test.py:18
BlueCat at examples/test.py:26
```

---

`get.` is equivalent in the regular expression as `^get`

```sh
bor def get. examples/test.py
```

Output:

```sh
get_value at examples/test.py:5
get_blue_value at examples/test.py:11
get_purple_value at examples/test.py:14
get_meow at examples/test.py:22
```

---

`.cat.` is equivalent in the regular expression as `cat+`

```sh
bor def .cat.
```

Output:

```sh
catch_me_if_you_can at examples/test.py:8
am_i_blue_cat at examples/test.py:30
where_is_the_cat at examples/test.py:38
```
