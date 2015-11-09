Getting Started
****************

==========
Quickstart
==========

-------------------
Set up with Vagrant
-------------------

Vagrant is the recommend method for developing with DataHub. It provides a VM matching the DataHub production server, regardless of your host operating system.



1. Install VirtualBox `<https://www.virtualbox.org/>`_.
2. Install Vagrant `<https://www.vagrantup.com/downloads.html>`_.
3. Clone DataHub:
    .. code-block:: bash
    
        $ git clone https://github.com/datahuborg/datahub.git
4. Add this line to your hosts file (/etc/hosts on most systems):
    .. code-block:: bash
    
        192.168.50.4    datahub-local.mit.edu
5. From your clone, start the VM:
    .. code-block:: bash
    
        $ vagrant up

This last step could take several minutes depending on the speed of your connection and computer.

Once ``vagrant up`` finishes, you can see your environment running at `<http://datahub-local.mit.edu>`_.

Note that datahub-local.mit.edu is local to your computer and unreachable by other machines. Because it is local, you can edit DataHub's files on your computer, and those changes will be reflected on datahub-local.mit.edu.

==============
Standard Setup
==============

--------------
Clone the repo
--------------

1. Make sure to clone the repo,
   ``git clone https://github.com/abhardwaj/datahub.git``
2. Navigate into the the repo, ``cd datahub``

----------
PostgreSQL
----------

DataHub is built on the `PostgreSQL <http://www.postgresql.org/>`__
database.

1. `Install Postgres <http://www.postgresql.org/download/>`__ and create a user called ``postgres``. See
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

-----------------------
Create a ``virtualenv``
-----------------------

It's useful to install python dependencies in a virtual environment so
they are isolated from other python packages in your system. To do this,
use `virtualenv <http://virtualenv.readthedocs.org/en/latest/>`__.

1. Install virtualenv with pip, ``pip install virtualenv``
2. Create a virtual environment (called ``venv``) within the datahub
   directory, ``virtualenv venv``
3. Activate the virtual environment, ``source venv/bin/activate``.

When you are finished with the virtual environment, run ``deactivate``
to close it.

---------------------------------
Install dependencies with ``pip``
---------------------------------

Installing the dependencies for DataHub is easy using the
`pip <https://pypi.python.org/pypi/pip>`__ package manager.

1. Install the dependencies with ``pip install -r requirements.txt``

----------------------------
Setup server and data models
----------------------------

1. Update ``src/settings.py`` with your postgres username and password.
2. Setup the server environment, ``source src/setup.sh`` (Please note
   that this must be sourced from the root directory.)
3. Sync with the database, ``python src/manage.py migrate``
4. Migrate the data models, ``python src/manage.py migrate inventory``

----------------------------
Install Berkeley DB bindings
----------------------------

1. I haven't written this yet, so for now, please comment out
   ``import bsddb`` from ``src/apps/dbwipes/summary.py``

----------
Run server
----------

1. Run the server, ``python src/manage.py runserver``
2. Navigate to `localhost:8000 <http://localhost:8000>`__

**NOTE:** If the server complains that a module is missing, you may need
to ``source src/setup.sh`` and  ``pip install -r requirements.txt`` again. Then, ``python src/manage.py runserver`` and navigate to
`localhost:8000 <http://localhost:8000>`__

------------------------
Run test with ``behave``
------------------------

``cd /datahub/src behave``

====================
Building Sphinx Docs
====================

`Sphinx <http://sphinx-doc.org>`__ is included in ``requirements.txt``.

``make html`` rebuilds the documentation.

When submitting a pull request, you must include sphinx documentation. You can achieve this by adding ``*.rst`` and linking them from other ``*.rst`` files. See `the sphinx tutorial <http://sphinx-doc.org/tutorial.html>`__ for more information.

===============
Testing DataHub
===============

----------------
Functional Tests
----------------

Functional tests are used to test DataHub's functionality

Run them from the ``/src`` directory:

| ``$ cd src``
| ``$ python manage.py test functional_tests``

---------
Unittests
---------

Unitests are used to test DataHub's models and views.

Run them from the ``/src`` directory:

| ``$ cd src``
| ``$ python manage.py test``

Alternatively, they can be run individually:

| ``$ cd src``
| ``$ python manage.py test inventory`` - tests models
| ``$ python manage.py test www`` - tests home page
| ``$ python manage.py test account`` - tests account management views
| ``$ python manage.py test browser`` - tests datahub core views

-----------------------
BDD Testing with Behave
-----------------------

DataHub uses `Behave <https://pythonhosted.org/behave/>`__ for behavior driven development.

Run it from the the ``/src`` directory:

| ``$ cd src``
| ``$ behave``