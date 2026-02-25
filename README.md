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
