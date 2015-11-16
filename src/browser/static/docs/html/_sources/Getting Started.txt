Getting Started
****************

=======================
Quickstart with Vagrant
=======================

Vagrant is the recommend method for developing with DataHub. It provides a VM matching the DataHub production server, regardless of your host operating system.

If you would prefer to install DataHub manually, see `Manual Installation`_ below.



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

This last step might take several minutes depending on your connection and computer.

Once ``vagrant up`` finishes, you can see your environment running at `<http://datahub-local.mit.edu>`_.

.. note:: Vagrant keeps your working copy and the VM in sync, so edits you make to DataHub's code will be reflected on datahub-local.mit.edu. Changes to static files like CSS, JS, and documentation must be collected before the server will notice them. For more information, see management commands below.


===================
Manual Installation
===================

Follow these steps if you would prefer to forgo Vagrant and install DataHub locally.

--------------
Clone the repo
--------------

1. Make sure to clone the repo,
   ``git clone https://github.com/datahuborg/datahub.git``
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
3. Generate a custom SECRET_KEY, ``python src/scripts/generate_secret_key.py``
4. Sync with the database, ``python src/manage.py migrate``
5. Migrate the data models, ``python src/manage.py migrate inventory``

h1.

----------
Run server
----------

1. Run the server, ``python src/manage.py runserver``
2. Navigate to `localhost:8000 <http://localhost:8000>`__

**NOTE:** If the server complains that a module is missing, you may need
to ``source src/setup.sh`` and  ``pip install -r requirements.txt`` again. Then, ``python src/manage.py runserver`` and navigate to
`localhost:8000 <http://localhost:8000>`__

==========================
Building the Documentation
==========================

DataHub uses `Sphinx <http://sphinx-doc.org>`__ to build its documentation.

Using the default Vagrant setup:

.. code-block:: bash

    $ vagrant ssh
    $ cd /vagrant
    $ sudo sh /provisions/docker/rebuild-and-collect-static-files.sh

Using a local installation of Sphinx (Sphinx is included in ``requirements.txt``):

.. code-block:: bash

    $ cd /path/to/datahub
    $ make html

When submitting a pull request, you must include Sphinx documentation. You can achieve this by adding ``*.rst`` and linking them from other ``*.rst`` files. See `the Sphinx tutorial <http://sphinx-doc.org/tutorial.html>`__ for more information.

===============
Testing DataHub
===============

.. note:: Instructions for running tests on the Vagrant setup are forthcoming.

----------------
Functional Tests
----------------

Functional tests are used to test DataHub's functionality

Run them from the ``/src`` directory:

.. code-block:: bash

    $ cd src
    $ python manage.py test functional_tests

---------
Unit Tests
---------

Unit tests are used to test DataHub's models and views.

Run them from the ``/src`` directory:

.. code-block:: bash

    $ cd src
    $ python manage.py test

Alternatively, they can be run individually:

.. code-block:: bash

    $ cd src
    $ python manage.py test inventory  # tests models
    $ python manage.py test www        # tests home page
    $ python manage.py test account    # tests account management views
    $ python manage.py test browser    # tests datahub core views

================
Managing DataHub
================

----------------------
Basic Vagrant Commands
----------------------

.. code-block:: bash

    $ cd /path/to/datahub

    # Start the VM, creating one if it doesn't exist
    $ vagrant up
    
    # Stop the VM
    $ vagrant halt
    
    # Delete the VM completely
    $ vagrant destroy
    
    # Get a shell in the VM
    $ vagrant ssh

---------------------
Basic Docker Commands
---------------------

The above Vagrant commands are sufficient for running DataHub, but if you need to troubleshoot or develop with DataHub, you will want to learn about Docker. Docker isolates processes and their dependencies by containerizing parts of a system into lightweight VMs. 

Docker can be a little odd to work with at first. Below are some common Docker commands. For Docker tutorials and documentation, see `<https://docs.docker.com/engine/userguide/>`_.

DataHub is composed of 3 process containers and 2 data containers.

- ``web`` runs nginx, a reverse proxy. It listens on ports 80 and 443, serves static content, and proxies dynamic requests to the app container.
- ``app`` runs gunicorn, a wsgi Python server. It listens on port 8000, but only to requests from other containers. app is where DataHub's code lives.
- ``db`` runs a Postgres server. It listens on port 5432, but only to connections from other containers.
- ``data`` holds user uploads and the Postgres data.
- ``logs`` holds log files for the web, app, and db containers.

After sshing into Vagrant:

.. code-block:: bash

    # List all Docker containers and their statuses
    $ sudo docker ps -a
    CONTAINER ID        IMAGE                 COMMAND                  CREATED             STATUS              PORTS                                      NAMES
    886051b04caf        datahuborg/nginx      "nginx -g 'daemon off"   22 seconds ago      Up 3 seconds        0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp   web
    fcff60382ffd        datahuborg/datahub    "gunicorn --config=pr"   22 seconds ago      Up 3 seconds        8000/tcp                                   app
    03f076daa71e        datahuborg/postgres   "/docker-entrypoint.s"   22 seconds ago      Up 14 seconds       5432/tcp                                   db
    78d6af962797        datahuborg/postgres   "/bin/true"              22 seconds ago      Created                                                        data
    e41f0f5135db        datahuborg/postgres   "/bin/true"              22 seconds ago      Created                                                        logs
    
    # Container lifecycle
    $ sudo docker start app
    $ sudo docker stop app
    $ sudo docker restart app

    # Diagnosing a container
    $ sudo docker logs app

Because the server is containerized, most server commands must be run in a container. Docker commands can be complicated, so several common tasks have been made into scripts under ``provisions/docker``:

.. code-block:: bash

    $ cd /datahub
    $ sudo sh provisions/docker/back-up-database.sh
    $ sudo sh provisions/docker/create-dev-containers.sh
    $ sudo sh provisions/docker/rebuild-and-collect-static-files.sh
    $ sudo sh provisions/docker/restore-database.sh
    $ sudo sh provisions/docker/start-containers.sh
    $ sudo sh provisions/docker/stop-containers.sh

Example Docker commands:

.. code-block:: bash

    # View nginx's access logs
    $ sudo docker run --rm \
      --volumes-from logs \
      datahuborg/postgres \
      cat /var/log/nginx/access.log
    
    # Run Django migrations
    $ sudo docker run --rm \
      --link db:db \
      datahuborg/datahub \
      python src/manage.py migrate
    
    # Collect changes to Django's static files so the web container
    # can see them.
    $ sudo docker run --rm \
      --volumes-from app
      datahuborg/datahub \
      python src/manage.py collectstatic --noinput
    
    # Note that `--rm` means it creates an ephemeral container. A new
    # lightweight VM is created just for that command, and is then
    # deleted as soon as it exits. That is useful for a number of
    # reasons, but it also means exiting the container may take a few
    # seconds as Docker deletes the container.
    
    # It is possible to execute commands inside of running containers
    # instead of creating ephemeral containers which share volumes,
    # but it is not recommended as you can change the expected state
    # of a container.
    #
    # Get a shell in an active container:
    $ sudo docker exec -ti app /bin/bash
    
    # See Docker's builtin help
    $ docker help
