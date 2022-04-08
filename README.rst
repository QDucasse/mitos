========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests
      - | |github-actions|
        |
    * - package
      - | |commits-since|

.. |github-actions| image:: https://github.com/QDucasse/mitos/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/QDucasse/mitos/actions

.. |commits-since| image:: https://img.shields.io/github/commits-since/QDucasse/mitos/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/QDucasse/mitos/compare/v0.0.0...main



.. end-badges

Parser Generator

* Free software: MIT license

Installation
============

::

    pip install mitos

You can also install the in-development version with::

    pip install https://github.com/QDucasse/mitos/archive/main.zip


Documentation
=============


To use the project:

.. code-block:: python

    import mitos
    mitos.longest()


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
