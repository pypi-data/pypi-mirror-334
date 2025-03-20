<!--
SPDX-FileCopyrightText: 2025 Federico Beffa <beffa@fbengineering.ch>

SPDX-License-Identifier: GPL-3.0-or-later
-->

ICEM
====

Python library for converting integrated circuit (IC) structures described in GDS files into finite-element models for electromagnetic (EM) computation. Documentation can be found [here](https://fbengineering.gitlab.io/icem).

Dependencies
------------

`icem` depends on the following Python libraries:

* gmsh
* klayout
* more-itertools
* numpy

Installation
------------

`icem` is available on [PyPi](https://pypi.org/). The easiest way to install it on Unix-like systems is via `pip`:

```bash
pip install icem
```

Alternatively you can download the Python distribution archives from the release page, or download the source code and add its location to the environment variable `PYTHONPATH`.
