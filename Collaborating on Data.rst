Collaborating on Data
*********************

=========================
Traditional Collaboration
=========================
You can grant other DataHub users the ability to use your data.

To add users as collaborators

1. Go to `/browse/ </browse/>`__
2. Click on the "collaborators" link next to the repo you would like to collaborate on
3. Add your collaborator's username
4. Select the permissions you would like to grant to them
5. Click "Add"

To revoke a collaborator, click the x next to that user's name on the same page.

--------------------
Database Permissions
--------------------
DataHub uses database permissions to control collaborator access to data. When
adding collaborators, you may want to think about what types of access you would
like to give them.

- ``SELECT`` allows users to view and operate on the data. Users whom have only
been granted can *view* your data, but not change it.
- ``INSERT`` allows users to add new data.
- ``UPDATE`` allows users to change data that already exists.
- ``DELETE``` allows users to to delete data that already exists
- ``TRUNCATE``, ``REFERENCES``, and ``TRIGGER`` require an additional understanding of databases. You can read more about them `here <https://www.postgresql.org/docs/9.0/static/sql-grant.html>`__.

----------------
File Permissions
----------------

-----------------
Technical Details
-----------------
DataHub records grants both in the database, and via Django's ORM. Grants
executed via queries (in the terminal or through queries to the API) are likely
to have unforseen consequences. For instance: collaborators will not be able to
access files. (File permissions are recored only in the ORM.)

DataHub lacks the ability to `GRANTE CREATE on SCHEMA schema_name`. It is
currently acceptable to `GRANT CREATE` via a query or through the terminal.

.. note:: Given time, we would have liked to make granting create possible through the API and browser interface. See `issue 157 <https://github.com/datahuborg/datahub/issues/157>`__.


==================
Row Level Security
==================