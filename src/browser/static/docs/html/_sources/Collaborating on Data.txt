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

To revoke a collaborator, click the `x` next to that user's name on the same page.

--------------------
Database Permissions
--------------------
DataHub uses database permissions to control collaborator access to data. When
adding collaborators, you should consider the types of access you would
like to give them to your data.

If you trust your collaborators (which we hope you do), we suggest leaving all
options checked.

- ``SELECT`` allows users to view and operate on the data. Users whom have only been granted ``SELECT`` can *view* your data, but not change it.
- ``INSERT`` allows users to add new data.
- ``UPDATE`` allows users to change data that already exists.
- ``DELETE`` allows users to to delete data that already exists.
- ``TRUNCATE``, ``REFERENCES``, and ``TRIGGER`` require an additional understanding of databases. You can read more about them `here <https://www.postgresql.org/docs/9.0/static/sql-grant.html>`__.

----------------
File Permissions
----------------
DataHub file permissions allow people to access the files in your "Files" tab.
When adding collaborators, you should consider the types of access you would
like to give them to your files.

If you trust your collaborators (which we hope you do), we suggest leaving all
options checked.

- ``read`` allows users to view the contents of existing files.
- ``write`` allows users to write new information to existing files, and to add new files.

-----------------
Technical Details
-----------------
DataHub records *GRANTs* to schemas both in the database and via DataHub Website's `ORM <https://en.wikipedia.org/wiki/Object-relational_mapping>`__. Grants
executed via queries (in the `terminal </apps/console/>`__ or through `queries to the API <http://datahub-local.mit.edu/api-docs/#!/query>`__ are likely
to have unforeseen consequences. For instance: collaborators will not be able to
access files. (File permissions are recored only in the ORM.)

DataHub lacks the ability to ``GRANTE CREATE on SCHEMA schema_name``. It is
currently acceptable (2016-06-06) to ``GRANT CREATE`` via a query through the API or terminal.

.. note:: Given time, we would have liked to make granting create possible through the API and browser interface. See `issue 157 <https://github.com/datahuborg/datahub/issues/157>`__.

.. note:: The add collaborators (repo-settings) template could really use some love.
 See `issue 159 <https://github.com/datahuborg/datahub/issues/159>`__.

==================
Row Level Security
==================
Row Level Security (RLS) allows owner to specify what parts
of a table collaborators can access (select, insert, update) from.

For example,

.. code-block:: sql

    -- Roadrunner creates a creates a security policy for coyote.
    GRANT SELECT ACCESS to COYOTE on acme.explosives WHERE defective = 'true';

    -- Coyote executes this query
    SELECT * FROM acme.explosives;

    -- which becomes
    SELECT * FROM acme.explosives where defective = 'true';

    -- Now Coyote can only see (and purchase) defective explosives


To create a RLS policy

1. Go to `/browse/ </browse/>`__.
2. Click on the lock icon of the repo you would like to create a policy for.
3. Click "new".
4. Add the security policy type, and what the policy will be. The policy itself will be dependent on your table's structure.
5. Add the grantee.
6. Click save.

To delete or edit a RLS security policy, navigate to the same page, and click the
pencil (edit) or the trash can (delete).

Row Level Security can also be applied on tables to ALL users in the database.
This is useful if you would only like to publicly publish a subset of a
table's data. To do this, in the grantee field, add "ALL"


.. note:: Creating a RLS policy does not (by itself) allow collaborators to access a table. Users must also add collaborators via the collaborators menu described in the "Traditional Collaborators" section above. Row Level Security only provides an *additional* layer of specificity for what is shared.

-----------------
Technical Details
-----------------

The "ALL" keyword used to signify that a RLS policy applies to ALL users is
defined in `settings.py <https://github.com/datahuborg/datahub/blob/master/src/config/settings.py>`__

RLS is a result of a thesis project for her Spring 2016 Masters in Engineering Degree from MIT EECS. You can find her thesis `here <https://github.com/datahuborg/datahub/blob/master/src/browser/static/www/papers/KellyZhang_RowLevelSecurity_Thesis.pdf>`__

RLS parses queries and recursively applies security policies as defined in the table. For example,

.. code-block:: sql

    -- given the security policies
    GRANT SELECT ACCESS to MYUSER on A WHERE COUNT>10;
    GRANT SELECT ACCESS to MYUSER on B WHERE NAME='BOB';

    -- The query
    SELECT * FROM A INNER JOIN B on A.ID = B.ID;

    -- becomes
    SELECT * FROM
    (SELECT * FROM A WHERE COUNT > 10)
    INNER JOIN
    (SELECT * FROM B WHERE NAME='Bob')
    ON A.ID = B.ID;

.. note:: The Row Level Security interface could really use some love. Please see `issues 160 <https://github.com/datahuborg/datahub/issues/160>__`
