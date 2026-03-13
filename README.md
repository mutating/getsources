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


This library is needed to obtain the source code of functions at runtime. It can be used, for example, as a basis for libraries that work with [AST](https://en.wikipedia.org/wiki/Abstract_syntax_tree) on the fly. In fact, it is a thin layer built around [`inspect.getsource`](https://docs.python.org/3/library/inspect.html#inspect.getsource) and [`dill.source.getsource`](https://dill.readthedocs.io/en/latest/dill.html#dill.source.getsource).


## Table of contents

- [**Installation**](#installation)
- [**Get dirty sources**](#get-dirty-sources)
- [**Get clear sources**](#get-clear-sources)
- [**Get hashes**](#get-hashes)


## Installation

You can install [`getsources`](https://pypi.python.org/pypi/getsources) using pip:

```bash
pip install getsources
```

You can also quickly try this package and others without installing them via [instld](https://github.com/pomponchik/instld).


## Get dirty sources

The standard library includes the [`getsource`](https://docs.python.org/3/library/inspect.html#inspect.getsource) function that returns the source code of functions and other objects. However, this does not work with functions defined in the [`REPL`](https://docs.python.org/3/tutorial/interpreter.html#interactive-mode).

This library defines a function of the same name that does the same thing but does not have this drawback:

```python
# You can run this code snippet in the REPL.
from getsources import getsource

def function():
    ...

print(getsource(function))
#> def function():
#>     ...
```

This way, you can ensure that your functions that work with ASTs can be executed in any way. All other functions in this library are built on top of this one.


## Get clear sources

The [`getsource`](#get-dirty-sources) function returns the source code of functions in a "raw" format. This means that the code snippet captures some unnecessary surrounding code.

Here's an example where the standard `getsources` function gets rid extra whitespace characters:

```python
if True:
    def function():
        ...

print(getsource(function))
#>     def function():
#>         ...
```

See? There are extra spaces at the beginning.

Lambda functions also capture the entire surrounding string:

```python
print(getsource(lambda x: x))
#> print(getsource(lambda x: x))
```

To address these issues, there is a special function called `getclearsource`, which returns the original function's code but stripped of any unnecessary elements:

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

When working with AST, this function is the recommended and safe way to retrieve the source code of functions.


## Get hashes

In some cases, you may not care what exactly is inside a function, but you need to distinguish between functions with different contents. In this case, the `getsourcehash` function is useful, as it returns a short string representation of the function’s source code hash:

```python
from getsources import getsourcehash

def function():
    ...

print(getsourcehash(function))
#> 7SWJGZ
```

> ⓘ A hash string contains only characters from the [`Crockford Base32`](https://en.wikipedia.org/wiki/Base32) alphabet, which consists solely of uppercase English letters and digits; letters that resemble digits are excluded from the list, making the hash easy to read.

> ⓘ The `getsourcehash` function operates on top of [`getclearsource`](#get-clear-sources) and ignores "extra" characters in the source code.

By default, the hash string length is 6 characters, but you can set your own values ranging from 4 to 8 characters:

```python
print(getsourcehash(function, size=4))
#> WJGZ
print(getsourcehash(function, size=8))
#> XG7SWJGZ
```

By default, the full text representation of a function is used, including its name and arguments. However, in some cases, we need to compare only the contents of the functions while ignoring these details; in such cases, we need to pass the argument `only_body=True`:

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
