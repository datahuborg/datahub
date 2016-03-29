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

If you see a ``Datahub module not found`` error, this is due to an unresolved issue with thrift code not compiling only after the first ``vagrant up``. Please see this thread for a resolution: `<https://github.com/datahuborg/datahub/issues/119>`_.

.. note:: Vagrant keeps your working copy and the VM in sync, so edits you make to DataHub's code will be reflected on datahub-local.mit.edu. Changes to static files like CSS, JS, and documentation must be collected before the server will notice them. For more information, see management commands below.

------------------------
Using non-standard ports
------------------------

If your host environment does not allow use of ports 80 and 443, it is possible to use DataHub on forwarded ports but some extra configuration is required.

1. Edit the Vagrantfile to expose ports 80 and/or 443 on usable ports.   
    .. code-block:: ruby
    
        Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
          ...
          config.vm.network "forwarded_port", guest: 80, host: 18080
          config.vm.network "forwarded_port", guest: 443, host: 18081
          ...

2. Edit the nginx configuration file at provisions/nginx/default.conf to make the reverse proxy aware of what the new ports are.
    .. code-block:: nginx
    
        # Uncomment and customize:
        map $scheme $port_to_forward {
            default 18080;
            https   18081;
        }
        ...
        location / {
            ...
            # Uncomment:
            proxy_set_header X-Forwarded-Host $host:$port_to_forward;
            proxy_set_header X-Forwarded-Server $server_name;
            proxy_set_header X-Forwarded-Port $port_to_forward;
            ...
        }

3. Edit the Django settings file at src/config/settings.py to make Django look for those headers.
    .. code-block:: python
    
        # Uncomment and set to True:
        USE_X_FORWARDED_HOST = True

4. From the host, run ``vagrant reload`` to bring up the VM with your custom ports forwarded.
   
   If you don't mind losing all of your existing DataHub data, running ``vagrant destroy -f && vagrant up`` instead will rebuild the entire site using your new custom config. If you want to keep your existing VM's data, follow step 5 below.

5. Inside the VM, run:
    .. code-block:: bash
    
        $ cd /vagrant
        $ sudo sh provisions/docker/build-images.sh
        $ sudo docker rm -f web
        $ sudo docker create --name web \
               --volumes-from logs \
               --volumes-from app \
               -v /ssl/:/etc/nginx/ssl/ \
               --net=datahub_dev \
               -p 80:80 -p 443:443 \
               datahuborg/nginx
        $ sudo docker start web

At the end of these steps, DataHub should be reachable at http://localhost:18080 and https://localhost:18081.


===================
Manual Installation
===================

Follow these steps if you would prefer to forgo Vagrant and install DataHub locally.
Please note that other sections of the documentation assume that you are using the Vagrant (quickstart) setup.

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
    $ sudo su
    $ dh-rebuild-and-collect-static-files

Using a local installation of Sphinx (Sphinx is included in ``requirements.txt``):

.. code-block:: bash

    $ cd /path/to/datahub
    $ make html

When submitting a pull request, you must include Sphinx documentation. You can achieve this by adding ``*.rst`` and linking them from other ``*.rst`` files. See `the Sphinx tutorial <http://sphinx-doc.org/tutorial.html>`__ for more information.
