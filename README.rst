Cooking
======

The basic Cooking app built in the Flask Cooking to organize lunch command for multiples peoples in a same place

Install
-------

**Be sure to use the same version of the code as the version of the docs
you're reading.** You probably want the latest tagged version, but the
default Git version is the master branch. ::

    # clone the repository
    $ git clone https://github.com/pallets/flask
    $ cd flask
    # checkout the correct version
    $ git tag  # shows the tagged versions
    $ git checkout latest-tag-found-above
    $ cd examples/tutorial

Create a virtualenv and activate it::

    $ python3 -m venv venv
    $ . venv/bin/activate

Or on Windows cmd::

    $ py -3 -m venv venv
    $ venv\Scripts\activate.bat

Install Cooking::

    $ pip install -e .

Or if you are using the master branch, install Flask from source before
installing Cooking:

    $ pip install -e ../..
    $ pip install -e .


Run
---

::

    $ export FLASK_APP=cooking
    $ export FLASK_ENV=development
    $ flask init-db
    $ flask run

Or on Windows cmd::

    > set FLASK_APP=cooking
    > set FLASK_ENV=development
    > flask init-db
    > flask run

Open http://127.0.0.1:5000 in a browser.


Test
----

::

    $ pip install '.[test]'
    $ pytest

Run with coverage report::

    $ coverage run -m pytest
    $ coverage report
    $ coverage html  # open htmlcov/index.html in a browser
