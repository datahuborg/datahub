Application API
***************

DataHub allows developers to connect client devices to datahub, create and 
delete accounts, and manipulate data on a user's behalf.

------------------------------------
Introduction to DataHub Applications
------------------------------------
DataHub applications allow...

* developers to create and delete DataHub accounts
* developers to view and edit data in authorized DataHub accounts
* end users to authorize an application to view and edit their data

Two examples:

* ``living_lab`` may wish to create a DataHub account for an incoming ``grad_student``. ``livinglab`` will create the new account, assign it a username/password, and create a repository ``genome_data`` repository and add some tables to it.
* ``grad_student`` might already have an account. In this case, they want to authorize the ``living_lab`` app to view and edit data in their ``genome_data`` repository.

In both examples, the ``living_lab`` app has access to view and edit data in ``grad_student``'s ``genome_data`` repository.

**Navigate to** `developer/apps <http://localhost:8000/developer/apps>`__ **in your DataHub installation to create a new app.**

*Note: Make sure not to commit the App Name or App ID in any public repositories!*



----------------------
Generating Native Code
----------------------
DataHub uses `Apache Thrift <https://thrift.apache.org/>`_ to generate native
code for your datahub client. You will neeed to do this before connecting to user accounts.
You can generate native code using the commands below. 


C++ Sample Code
~~~~~~~~~~~~~~~

-  ``cd src/examples/cpp``
-  ``source setup.sh``
-  ``./SampleClient``

Java Sample Code
~~~~~~~~~~~~~~~~

-  ``cd src/examples/java``
-  ``source setup.sh``
-  ``java SampleClient``

Python Sample Code
~~~~~~~~~~~~~~~~~~

-  ``cd src/examples/python``
-  ``source setup.sh``
-  ``mv gen-py gen_py``
-  ``python SampleClient.py``

Go Sample Code
~~~~~~~~~~~~~~

-  ``cd src/examples/go``
-  ``source setup.sh``
-  ``go run SampleClient.go``

JavaScript Sample Code
~~~~~~~~~~~~~~~~~~~~~~

-  ``cd src/examples/javascript``
-  open ``SampleClient.html`` in a browser

Objective-C Sample Code
~~~~~~~~~~~~~~~~~~~~~~~

- ``cd src/examples/objc``
- ``open DataHub-Example``
-  run
-  When integrating thrift, in Build Settings:

  -  Always Search User Path: ``YES``
  -  Framework Search Paths: add ``$(SRCROOT)`` and ``$(inherited)``


-----------------------------------
Connecting with the Application API
-----------------------------------

Create a connection
~~~~~~~~~~~~~~~~~~~


Creating accounts
~~~~~~~~~~~~~~~~~

Connecting to a user account with an app ID & token
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-------------------------------------
Connecting with a username & password
-------------------------------------
It is possible to connect to a user's account without using an application. In this case, you will need their username and password.

Connections made using a username and password are unable to create or delete accounts.

.. py:class:: ConnectionParams(user, password)
  
   connection paramaters for connecting datahub using a username and password.

   :param str user: username
   :param str password: password
   :return: a connection parameters object
   :rtype: Thrift Connection