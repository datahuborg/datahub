REST Client API
***************

====================
Authenticating Users
====================

=============
Using the API
=============

DataHub offers a RESTful API for both internal and external applications.
You can find interactive documentation and examples at `/api-docs </api-docs>`__

.. note:: The REST API doesn't provide CSRF authentication, which prevents file upload through the `swagger UI <https://django-rest-swagger.readthedocs.io/en/latest/>`__. This isn't critical, since file upload through API Clients still works. It would be nice to resolve though. See `issue 155 <https://github.com/datahuborg/datahub/issues/155>`__.