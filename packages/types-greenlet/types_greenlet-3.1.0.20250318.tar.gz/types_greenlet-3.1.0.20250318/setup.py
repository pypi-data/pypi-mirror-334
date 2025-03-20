from setuptools import setup

name = "types-greenlet"
description = "Typing stubs for greenlet"
long_description = '''
## Typing stubs for greenlet

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`greenlet`](https://github.com/python-greenlet/greenlet) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `greenlet`. This version of
`types-greenlet` aims to provide accurate annotations for
`greenlet==3.1.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/greenlet`](https://github.com/python/typeshed/tree/main/stubs/greenlet)
directory.

This package was tested with
mypy 1.15.0,
pyright 1.1.396,
and pytype 2024.10.11.
It was generated from typeshed commit
[`b93eae52affaedfda79c00f662f50a2ef3b24c46`](https://github.com/python/typeshed/commit/b93eae52affaedfda79c00f662f50a2ef3b24c46).
'''.lstrip()

setup(name=name,
      version="3.1.0.20250318",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/greenlet.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['greenlet-stubs'],
      package_data={'greenlet-stubs': ['__init__.pyi', '_greenlet.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.9",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
