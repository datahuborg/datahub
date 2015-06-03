Getting Started
****************

--------------
Clone the repo
--------------

1. Make sure to clone the repo,
   ``git clone https://github.com/abhardwaj/datahub.git``
2. Navigate into the the repo, ``cd datahub``

--------------
PostgreSQL
--------------

DataHub is built on the `PostgreSQL <http://www.postgresql.org/>`__
database.

1. Install Postgres and create a user called ``postgres``. See
   `here <https://wiki.postgresql.org/wiki/First_steps>`__ for
   step-by-step instructions.
2. When the Postgres server is running, open the Postgres shell
   ``psql -U postgres``
3. Create a database for DataHub, ``CREATE DATABASE datahub;``
4. Quit the shell with ``\q``

------------------------------
Create ``user_data`` directory
------------------------------

1. Navigate to the root directory, ``cd /``
2. Create the ``user_data`` directory as root user,
   ``sudo mkdir user_data``

We realize that this is not the best location for the ``user_data``
directory. In future commits, we'll make this option configurable and
perhaps default to a different location.

----------------------------
Create a ``virtualenv``
----------------------------

It's useful to install python dependencies in a virtual environment so
they are isolated from other python packages in your system. To do this,
use `virtualenv <http://virtualenv.readthedocs.org/en/latest/>`__.

1. Install virtualenv with pip, ``pip install virtualenv``
2. Create a virtual environment (called ``venv``) within the datahub
   directory, ``virtualenv venv``
3. Activate the virtual environment, ``source venv/bin/activate``.

When you are finished with the virtual environment, run ``deactivate``
to close it.

------------------------------------------
Install dependencies with ``pip``
------------------------------------------

Installing the dependencies for DataHub is easy using the
`pip <https://pypi.python.org/pypi/pip>`__ package manager.

1. Install the dependencies with ``pip install -r requirements.txt``

------------------------------
Setup server and data models
------------------------------

1. Update ``src/settings.py`` with your postgres username and password.
2. Setup the server environment, ``source src/setup.sh`` (Please note
   that this must be sourced from the root directory.)
3. Sync with the database, ``python src/manage.py syncdb``
4. Migrate the data models, ``python src/manage.py migrate inventory``

-----------------------------
Install Berkeley DB bindings
-----------------------------

1. I haven't written this yet, so for now, please comment out
   ``import bsddb`` from ``src/apps/dbwipes/summary.py``

--------------
Run server
--------------

1. Run the server, ``python src/manage.py runserver``
2. Navigate to `localhost:8000 <http://localhost:8000>`__

**NOTE:** If the server complains that a module is missing, you may need
to ``source src/setup.sh`` and  ``pip install -r requirements.txt`` again. Then, ``python src/manage.py runserver`` and navigate to
`localhost:8000 <http://localhost:8000>`__)