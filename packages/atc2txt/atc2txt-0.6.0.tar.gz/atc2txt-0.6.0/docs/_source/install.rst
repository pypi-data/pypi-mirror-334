============
Installation
============
PyPI Install
------------
This is the "regular" way to install.

* https://pypi.org/project/atc2txt/

.. code-block:: bash

  python -m venv venv
  source venv/bin/activate
  pip install -U setuptools pip wheel
  pip install atc2txt

Source Install
--------------
To install from the source code repository.

* https://spacecruft.org/aviation/atc2txt

.. code-block:: bash

  git https://spacecruft.org/aviation/atc2txt
  cd atc2txt/
  python -m venv venv
  source venv/bin/activate
  pip install -U setuptools pip wheel
  pip install -e .

Development Install
-------------------
To install for development.

* https://spacecruft.org/aviation/atc2txt

.. code-block:: bash

  git clone https://spacecruft.org/aviation/atc2txt
  cd atc2txt/
  python -m venv venv
  source venv/bin/activate
  pip install -U setuptools pip wheel
  pip install -e .[dev]
