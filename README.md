<h1 align="center">Bor</h1>
<h4 align="center">User-friendly, tiny source code searcher written by pure Python.</h4>

<p align="center">
  <a href="https://github.com/furkanonder/bor/actions"><img alt="Actions Status" src="https://github.com/furkanonder/bor/workflows/Test/badge.svg"></a>
  <a href="https://github.com/furkanonder/bor/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/furkanonder/bor"></a>
  <a href="https://github.com/furkanonder/bor/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/furkanonder/bor"></a>
  <a href="https://github.com/furkanonder/bor/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/furkanonder/bor"></a>
  <a href="https://pepy.tech/project/bor"><img alt="Downloads" src="https://pepy.tech/badge/bor"></a>
</p>

## Example Usages

Cat is equivalent in the regular expression as '^Cat$'
```
bor class Cat
```
Output:
```
Cat at /home/arf/bor/examples/test.py : 18
```

***

.Cat is equivalent in the regular expression as 'Cat$'
```
bor class .Cat
```
Output:
```
Cat at /home/arf/bor/examples/test.py : 18
BlueCat at /home/arf/bor/examples/test.py : 26
```

***

get. is equivalent in the regular expression as '^get'
```
bor def get. examples/test.py
```
Output:
```
get_value at /home/arf/bor/examples/test.py : 5
get_blue_value at /home/arf/bor/examples/test.py : 11
get_purple_value at /home/arf/bor/examples/test.py : 14
get_meow at /home/arf/bor/examples/test.py : 22
```

***

.cat. is equivalent in the regular expression as 'cat+'
```
bor def .cat.
```
Output:
```
catch_me_if_you_can at /home/arf/bor/example/test.py : 8
am_i_blue_cat at /home/arf/bor/example/test.py : 30
where_is_the_cat at /home/arf/bor/example/test.py : 38
```
