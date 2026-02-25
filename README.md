![logo](https://raw.githubusercontent.com/mutating/getsources/develop/docs/assets/logo_1.svg)

This library is needed to obtain the source code of functions at runtime. It can be used, for example, as a basis for libraries that work with [AST](https://en.wikipedia.org/wiki/Abstract_syntax_tree) on the fly. In fact, it is a thin layer built around [`inspect.getsource`](https://docs.python.org/3/library/inspect.html#inspect.getsource) and [`dill.source.getsource`](https://dill.readthedocs.io/en/latest/dill.html#dill.source.getsource).
