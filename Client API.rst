Client API
**********

DataHub allows developers to connect client devices to datahub, create and 
delete accounts, and manipulate data on a user's behalf.

.. _app-api-intro:

========================================
Introduction to DataHub API Applications
========================================
DataHub API applications allow...

* end users to authorize an application to view and edit their data
* developers to view and edit data in authorized DataHub accounts

For example, a user, ``grad_student`` has a datahub account. In this case, they want to authorize the ``living_lab`` app to view and edit data in their ``genome_data`` repository.

**Navigate to** `developer/apps <http://localhost:8000/developer/apps>`__ **in your DataHub installation to create a new app.**

**End users must authorize your application by visiting**  `permissions/apps/allow_access/APP_ID/REPO_NAME <https://datahub.csail.mit.edu/permissions/apps/allow_access/APP_ID/REPO_NAME>`__ **in their browser**

*Note: Make sure not to commit the App Name or App ID in any public repositories!*



======================
Generating Native Code
======================
DataHub uses `Apache Thrift <https://thrift.apache.org/>`_ to generate native
code for your datahub client. You will need to do this before connecting to user accounts.
You can generate native code using the commands below. 

---------------
C++ Sample Code
---------------

-  ``cd src/examples/cpp``
-  ``source setup.sh``
-  ``# add credentials to SampleClient.cpp`` 
-  ``./SampleClient.cpp``

----------------
Java Sample Code
----------------

-  ``cd src/examples/java``
-  ``source setup.sh``
-  ``cd src``
-  ``# add credentials to SampleClient.java and SampleAccount.java``
-  ``cd ..``
-  ``java SampleClient``
-  ``java SampleAccount``

------------------
Python Sample Code
------------------

-  ``cd src/examples/python``
-  ``source setup.sh``
-  ``mv gen-py gen_py``
-  ``# addCredentials to SampleClient.py and SampleAccount.py`` 
-  ``python SampleClient.py``
-  ``python SampleAccount.py``

--------------
Go Sample Code
--------------

-  ``cd src/examples/go``
-  ``source setup.sh``
-  ``go run SampleClient.go``

----------------------
JavaScript Sample Code
----------------------

-  ``cd src/examples/javascript``
-  open ``SampleClient.html`` in a browser

-----------------------
Objective-C Sample Code
-----------------------

- ``cd src/examples/objc``
- ``open DataHub-Example``
-  ``# add credentials to main.m``
-  run
-  not: when integrating thrift, in Build Settings:

  -  Always Search User Path: ``YES``
  -  Framework Search Paths: add ``$(SRCROOT)`` and ``$(inherited)``

===================================
Connecting with the Application API
===================================
It is possible to connect to a user's account (without using their password) after they have authorized an application.

In order to follow these steps, you will have needed to create an application, which your end user(s) will need to authorize. See :ref:`app-api-intro`.

See the src/examples/*language*/SampleAccount.*ext* for examples.

=====================================
Connecting with a username & password
=====================================
It is possible to connect to a user's account without using an application. In this case, you will need their username and password.

Connections made using a username and password are unable to create or delete accounts.

See the src/examples/*language*/SampleClient.*ext* for examples.
