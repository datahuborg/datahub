Managing and Testing
********************

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

    # Connecting to a container's bash terminal
    $ sudo docker exec -ti app /bin/bash

Because the server is containerized, most server commands must be run in a container. Docker commands can be complicated, so several common tasks have been made into scripts under ``/vagrant/provisions/docker``.

.. code-block:: bash

    $ dh-build-images
    $ dh-create-dev-containers
    $ dh-create-prod-containers
    $ dh-rebuild-and-collect-static-files
    $ dh-run-test-container
    $ dh-start-containers
    $ dh-stop-containers
    $ dh-remove-all-containers
    $ dh-back-up-single-database
    $ dh-back-up-all-databases
    $ dh-restore-database
    $ dh-run-pgcli
    $ dh-codeclimate

Example Docker commands:

.. code-block:: bash

    # View nginx's access logs
    $ sudo docker run --rm \
      --volumes-from logs \
      datahuborg/postgres \
      cat /var/log/nginx/access.log
    
    # Run Django migrations
    $ sudo docker run --rm \
      --net=datahub_dev \
      --volumes-from app \
      datahuborg/datahub \
      python src/manage.py migrate --noinput
    
    # Collect changes to Django's static files so the web container
    # can see them.
    $ sudo docker run --rm \
      --volumes-from app \
      datahuborg/datahub \
      python src/manage.py collectstatic --noinput

    # Pip install -r requirements.txt
    $ sudo docker exec app pip install -r requirements.txt
    
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


===============
Testing DataHub
===============

To run tests or use the python debugger, you will need to connect to the test container.

.. code-block:: bash

    $ vagrant ssh
    $ sudo dh-run-test-container


You can exit the testing container by typing control-d or via the command ``exit``.

----------------
Functional Tests
----------------

DataHub uses Selenium and PhantomJS to test functionality from an end user's perspective. Both are installed as part of DataHub's Vagrant setup.

Once in the test container, you can run all functional tests with:

.. code-block:: bash

    $ sh /datahub/src/scripts/run-functional-tests.sh

Browser screenshots are saved in ``src/functional_tests/screenshots`` on teardown

You can run individual functional tests with:
    
.. code-block:: bash
    
    $ python manage.py test functional_tests.test_login_auth          # tests authentication
    $ python manage.py test functional_tests.test_layout_and_styling  # tests main page layout
    $ python manage.py test functional_tests.test_db                  # tests data control and sharing

Functional test files are saved in ``src/functional_tests``. 

-----------------
Integration Tests
-----------------

Integration tests verify that DataHub's components behave as expected when used as a whole with a database.

Once in the test container, you can run all integration tests with:

.. code-block:: bash

    $ sh /datahub/src/scripts/run-integration-tests.sh

----------
Unit Tests
----------

Unit tests are used to test DataHub's components in isolation from the database and each other.

Once in the test container, you can run all unit tests with:

.. code-block:: bash

    $ sh /datahub/src/scripts/run-unit-tests.sh


You can run individual unit tests:

.. code-block:: bash

    $ python manage.py test inventory  # tests models
    $ python manage.py test www        # tests home page
    $ python manage.py test account    # tests account management views
    $ python manage.py test core       # tests datahub core database access
    $ python manage.py test browser    # tests datahub core views
    $ python manage.py test api        # tests datahub RESTful API

Unit test files are saved in a ``test`` directory in their related application directory.
e.g.: ``src/browser/tests``, ``src/core/tests``