# Goals 

This example Python project template attempts to use the minimal number of
project config files in addition to modern, standard packaging tools.

Python suffers from a dizzying array of package distribution tooling and
configuration options, without a single canonical method. The tooling
documentation isn't necessarily up to date. Conflicting opinions exist for
nearly all aspects of configuration. Seemingly official recommendations are
often not. 

# A Brief History


The `distutils` distribution package was added to the Python standard library
in 2000 (Python 1.6)[1]. Here lies the origin of the plethora of files
(including `setup.py`, `MANIFEST.in`, etc.) needed to create a Python
distribution. An extension called `setuptools` was introduced relatively
shortly after in 2004. While a few other contenders[2] have risen up and
subsequently fallen by the wayside, `setuptools` remains the dominant player
in distributing Python code.

Over time, `setuptools` allowed more and more configuration to be pushed into
a declarative `setup.cfg` file. Now `setuptools >= 40.9.0` supports
`setup.cfg` only projects[3]. In particular, most arguments to the `setuptools.setup`
function can be configured with default values in `setup.cfg`.

[PEP 517](https://www.python.org/dev/peps/pep-0517/) attempts to decouple `setuptools` and
from the distribution build system by allowing arbitrary build-backends to be specified and
[PEP 518](https://www.python.org/dev/peps/pep-0518/) introduces the `pyproject.toml`
file wherein this specification occurs. In late January, 2019 `pip v19.0` (the package install tool) 
implemented support for PEP 517.

Meanwhile, a number of other build tools and environment managers began to appear:
[pipenv](https://pypi.org/project/pipenv/),
[poetry](https://pypi.org/project/poetry/),
[flit](https://pypi.org/project/flit/),
[hatch](https://pypi.org/project/hatch/).
Some of these tools do much more than serve as distribution build backends, in that they handle the
creation of virtual environments, package installation, dependency resolution, and more. 
A few of these tools (such as `poetry` and `flit`) make use of the `pyproject.toml`
file to handle configuration and package metadata.

The current build tool ecosysm is likely to change even more drastically in the future due to the
added freedom of PEPs 517 and 518. For all its warts, `setuptools` adapts to change, is
maintained, widely used, and an impressive permiance.

Python packaging appears to be headed to a more universal
adoption of a declarative `pyproject.toml` file that handles all aspects of a
project's configuration, from build configuration (which was historically
configured inside `setup.py` and later `setup.cfg`), to package metadata, to
external tool configuration (e.g., for the code formatter `black`).

# Choices in the Template 

This project template makes some (not necessarily staunch) decisions in order
to achieve its liberal choices around direction combined with its
conservative choice of tooling. Be aware that almost all of these choices have well-argued 
counterpoints.

1.  All configuration is declarative (no `setup.py` unless desired for editable installs) .
2.  Version is a string in `setup.cfg` and referenced as needed using `pkg_resources`[19].
3.  Package data (non `.py` files) is included in `setup.cfg` rather than `MANIFEST.in`.
4.  Eschew the use of non-package `data_files`, since it is handled inconsistently[13]. 
5.  Dependencies are preferentially specified explicitly in `setup.cfg` rather than `requirements.txt`.
6.  Development dependencies are included in `setup.cfg` to whatever extent possible 
    instead of a separate `requirements-dev.txt`. Cf. [15] for a counterpoint.
7.  Prefer to distribution binary wheels only (`bdist`s), since source distributions (`sdist`s)
    can be handled differently[13].
8.  Utilize `twine` for uploads. (This choice is not so controversial, but a canonical tool might exist in the future).
9.  tox (TOOD)
10. pytest (TODO)


# Development

Developing a package has some special concerns. The development cycle from
source change to usable program should be as short and painless as possible.


## Standard install

The project can be installed while in the project root via
```bash
pip install .
```

## Editable Mode

Being able to install a project in editable mode, wherein source changes are
immediately usable, is a particular desirable feature.

An example cycle:
```bash
pip install -e .
# Changes to project source files.
python
# Test changes in REPL, if possible.
# Run tests
```
As of `pip<=19` a minimal `setup.py` is required to install a project in in
editable mode (via `pip install -e .`), as PEP 517 does not specify this mode
explicitly. Create this minimal file in the project root via: `echo 'from
setuptools import setup;setup()' > setup.py`

## Development dependencies

Extra dependencies, e.g., those for development, can be listed in
`extra_requires` and installed via `pip install [-e] ".[dev]"`.
Some sources discourage the use of `extra_requires` for this purpose


# Building

A source distribution can be built (assuming `setup.py` exists) via:
```bash
python setup.py sdist
```

A wheel can be built for this project via:

```bash
pip wheel . 
```

# Uploading

Twine can be used to upload a project.

```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
twine upload --repository-url https://test.pypi.org/legacy/ *.whl
```

# Libraries vs. Applications

Generally, libraries should be as flexible as possible with versions, whereas
applications need to be more careful about pinning dependencies. 

The `install_requires` of `setuptools` should be as abstract as possible, to
allow other users of the distribution to use a local version of a dependency
if necessary (e.g., in the case of patching a bug). `pip` options (either command line
or specified in a `requirements.txt` file) can in turn point to a specific index
(e.g., company PyPi mirror) in order to fetch concrete dependencies.


# References 

1.  [Python packaging - Past, Present, Future](https://www.bernat.tech/pep-517-518/). 
2.  [Myriad historic packaging tools](https://stackoverflow.com/questions/25337706/setuptools-vs-distutils-why-is-distutils-still-a-thing)
3.  [PEP 517](https://www.python.org/dev/peps/pep-0517/)
4.  [PEP 518](https://www.python.org/dev/peps/pep-0518/)
5.  [Support for setup.cfg only projects](https://github.com/pypa/setuptools/pull/1675)
6.  [pipenv](https://pypi.org/project/pipenv/)
7.  [poetry](https://pypi.org/project/poetry/)
8.  [flit](https://pypi.org/project/flit/)
9.  [hatch](https://pypi.org/project/hatch/)
10. [A tour on Python Packaging](https://manikos.github.io/a-tour-on-python-packaging)
11. [A cookiecutter template](https://github.com/audreyr/cookiecutter-pypackage)
12. [Distributing packages](https://packaging.python.org/guides/distributing-packages-using-setuptools/)
13. [bdist_wheel vs sdist handling](https://github.com/pypa/wheel/issues/92)
13. [PyPa's sample project](https://github.com/pypa/sampleproject)
14. [twine](https://pypi.org/project/twine/)
15. [Abstract vs. concrete dependencies](https://caremad.io/posts/2013/07/setup-vs-requirement/)
16. [Python dependency resolution](https://docs.google.com/document/d/1x_VrNtXCup75qA3glDd2fQOB2TakldwjKZ6pXaAjAfg)
17. [Merge setup.cfg into pyproject.toml](https://github.com/pypa/setuptools/issues/1160)
18. [Support pyproject.toml](https://github.com/pypa/setuptools/issues/1688)
19. [Single sourcing version](https://packaging.python.org/guides/single-sourcing-package-version/)

