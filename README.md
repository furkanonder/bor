## Bor
User-friendly, tiny source code searcher written by pure Python.

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
