<details>
  <summary>ⓘ</summary>

[![Downloads](https://static.pepy.tech/badge/getsources/month)](https://pepy.tech/project/getsources)
[![Downloads](https://static.pepy.tech/badge/getsources)](https://pepy.tech/project/getsources)
[![Coverage Status](https://coveralls.io/repos/github/mutating/getsources/badge.svg?branch=main)](https://coveralls.io/github/mutating/getsources?branch=main)
[![Lines of code](https://sloc.xyz/github/mutating/getsources/?category=code)](https://github.com/boyter/scc/)
[![Hits-of-Code](https://hitsofcode.com/github/mutating/getsources?branch=main)](https://hitsofcode.com/github/mutating/getsources/view?branch=main)
[![Test-Package](https://github.com/mutating/getsources/actions/workflows/tests_and_coverage.yml/badge.svg)](https://github.com/mutating/getsources/actions/workflows/tests_and_coverage.yml)
[![Python versions](https://img.shields.io/pypi/pyversions/getsources.svg)](https://pypi.python.org/pypi/getsources)
[![PyPI version](https://badge.fury.io/py/getsources.svg)](https://badge.fury.io/py/getsources)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/mutating/getsources)

</details>

![logo](https://raw.githubusercontent.com/mutating/getsources/develop/docs/assets/logo_1.svg)

This library lets you retrieve a function's source code at runtime. It can serve as a foundation for tools that work with [ASTs](https://en.wikipedia.org/wiki/Abstract_syntax_tree). It is a thin wrapper around [`inspect.getsource`](https://docs.python.org/3/library/inspect.html#inspect.getsource) and [`dill.source.getsource`](https://dill.readthedocs.io/en/latest/dill.html#dill.source.getsource).


## Table of contents

- [**Installation**](#installation)
- [**Get raw source**](#get-raw-source)
- [**Get cleaned source**](#get-cleaned-source)
- [**Generate source hashes**](#generate-source-hashes)


## Installation

You can install [`getsources`](https://pypi.python.org/pypi/getsources) with pip:

```bash
pip install getsources
```
You can also use [`instld`](https://github.com/pomponchik/instld) to quickly try this package and others without installing them.


## Get raw source

The standard library provides the [`getsource`](https://docs.python.org/3/library/inspect.html#inspect.getsource) function that returns the source code of functions and other objects. However, this does not work with functions defined in the [`REPL`](https://docs.python.org/3/tutorial/interpreter.html#interactive-mode).

This library provides a function with the same name and nearly the same interface, but without this limitation:

```python
# You can run this code snippet in the REPL.
from getsources import getsource

def function():
    ...

print(getsource(function))
#> def function():
#>     ...
```

This makes AST-based tools work reliably in both scripts and the REPL. All other functions in the library are built on top of it.


## Get cleaned source

The [`getsource`](#get-raw-source) function a function's source code in raw form. This means that the code snippet captures some unnecessary surrounding code.

Here is an example where the standard `getsource` output includes extra leading whitespace:

```python
if True:
    def function():
        ...

print(getsource(function))
#>     def function():
#>         ...
```

> ↑ Notice the extra leading spaces.

For lambda functions, it may also return the entire surrounding expression:

```python
print(getsource(lambda x: x))
#> print(getsource(lambda x: x))
```

To address these issues, the library provides a function called `getclearsource`, which returns the function's source with unnecessary context removed:

```python
from getsources import getclearsource

class SomeClass:
    @staticmethod
    def method():
        ...

print(getclearsource(SomeClass.method))
#> @staticmethod
#> def method():
#>     ...
print(getclearsource(lambda x: x))
#> lambda x: x
```

To extract only the substring containing a lambda function, the library uses AST parsing behind the scenes. Unfortunately, this does not allow it to distinguish between multiple lambda functions defined in a single line, so in this case you will get an exception:

```python
lambdas = [lambda: None, lambda x: x]

getclearsource(lambdas[0])
#> ...
#> getsources.errors.UncertaintyWithLambdasError: Several lambda functions are defined in a single line of code, can't pick the one.
```

If you absolutely must obtain at least some source code for these lambdas, use [`getsource`](#get-raw-source):

```python
try:
    getclearsource(function)
except UncertaintyWithLambdasError:
    getsource(function)
```

However, in general, the `getclearsource` function is recommended for retrieving the source code of functions when working with the AST.


## Generate source hashes

In some cases, you may not care about a function's exact source, but you still need to distinguish between different implementations. In this case, the `getsourcehash` function is useful. It returns a short hash string derived from the function's source code:

```python
from getsources import getsourcehash

def function():
    ...

print(getsourcehash(function))
#> 7SWJGZ
```

> ⓘ A hash string uses only characters from the [`Crockford Base32`](https://en.wikipedia.org/wiki/Base32) alphabet, which consists solely of uppercase English letters and digits; ambiguous characters are excluded, which makes the hash easier to read.

> ⓘ The `getsourcehash` function is built on top of [`getclearsource`](#get-cleaned-source) and ignores "extra" characters in the source code.

By default, the hash string length is 6 characters, but you can choose a length from 4 to 8 characters:

```python
print(getsourcehash(function, size=4))
#> WJGZ
print(getsourcehash(function, size=8))
#> XG7SWJGZ
```

By default, the full source code of a function is used, including its name and arguments. If you only want to compare function bodies, pass `only_body=True`:

```python
def function_1():
    ...

def function_2(a=5):
    ...

print(getsourcehash(function_1, only_body=True))
#> V587A6
print(getsourcehash(function_2, only_body=True))
#> V587A6
```

By default, docstrings are considered part of the function body. If you want to skip them as well, pass `skip_docstring=True`:

```python
def function_1():
    """some text"""
    ...

def function_2(a=5):
    ...

print(getsourcehash(function_1, only_body=True, skip_docstring=True))
#> V587A6
print(getsourcehash(function_2, only_body=True, skip_docstring=True))
#> V587A6
```
