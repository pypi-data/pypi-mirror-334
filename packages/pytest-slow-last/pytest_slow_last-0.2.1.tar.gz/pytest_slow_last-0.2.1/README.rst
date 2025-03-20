================
pytest-slow-last
================

.. image:: https://img.shields.io/pypi/v/pytest-slow-last.svg
    :target: https://pypi.org/project/pytest-slow-last
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-slow-last.svg
    :target: https://pypi.org/project/pytest-slow-last
    :alt: Python versions

Run tests in order of execution time (faster tests first)

Usage
-----

From terminal::

    $ pytest --slow-last



Or in pytest.ini::

    [pytest]
    addopts = --slow-last

Installation
------------

You can install "pytest-slow-last" via `pip`_ from `PyPI`_::

    $ pip install pytest-slow-last


Features
--------

* Allows to run tests in order of the execution time of the last run (faster tests first, new tests even before).
* -ff option has preference: if a test fails, it will be run first.
* By default, test durations are rounded to the 2nd decimal digit: this way, tests which are "more or less of the same speed" are kept in the original order. Use `--slow-last-rounding` to change that, and set it to -1 to disable.

Requirements
------------

* Python >= 3.5
* pytest >= 3.5


Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-slow-last" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/david26694/pytest-slow-last/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project

----

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.
