Publishing Data
***************

===================
Public Repositories
===================
Data from public repositories is available to anyone, including DataHub users
who are unauthenticated.

To publish data

1. Go to `/browse/ </browse/>`__
2. Click on the "collaborators" link next to the repo you would like to publish.
3. Scroll down, and then click "Make Repo Public"

To unpublish data, click "Revoke Public Access" from the same page.

To view published data, click
`"Public Data" <http://datahub-local.mit.edu/browse/public>`__ at the top of
the DataHub page.

-----------------
Technical Details
-----------------
Publishing a repository adds the DataHub ``PUBLIC_ROLE`` as a collaborator on the
repo (as defined in ``settings.py`` ``PUBLIC_ROLE``). The ``PUBLIC_ROLE`` is
granted ``SELECT`` access to repo tables and ``READ`` access to repo files.

Unless users have not been explicitly (individually) granted access to a repo,
they will be able to select select data and download files, but not update or
insert into tables, or write files.

Unauthenticated DataHub users (users who view published data without logging
in) are "authenticated" as the anonymous user (as defined in ``settings.py``
``ANONYMOUS_ROLE``). ``ANONYMOUS_ROLE`` is a member of ``PUBLIC_ROLE``, and so
can access the same repos. However, ``ANONYMOUS_ROLE`` does
not own a database or schemas, so cannot ``CREATE`` tables.

The ``PUBLIC_ROLE`` and ``ANONYMOUS_ROLE`` are created in migration
`0016_public_repos_cards.py <https://github.com/datahuborg/datahub/blob/master/src/inventory/migrations/0016_public_repos_cards.py>`__
via `createpublicanonuser.py <https://github.com/datahuborg/datahub/blob/master/src/account/management/commands/createpublicanonuser.py>`__


.. note:: Given time, we would have liked to make public repos available through the api. Sadly they are not yet. See `issue 155 <https://github.com/datahuborg/datahub/issues/155>`__.

============
Public Cards
============
Published cards allow anyone to execute a pre-determined query in your
repository as the repository owner.

To publish a card

1. Create a card by successfully executing a query and clicking "Save as Card"
2. Go to the saved card
3. Click "Visibility: Private", and confirm
4. Click "Public Link" to go to the page where the data is published.
5. Anyone can see data via this link. Copy paste it and share as necessary.

To unpublish a card, click "Visibility: Public" and confirm.

-----------------
Technical Details
-----------------

Published cards are not limited to ``SELECT`` queries. They can also include
``UPDATE`` ``INSERT`` and any other statements that the repository owner can
execute.

Published cards are different from public repositories in that

1. Public card queries are executed as from the username that created the card
2. As a result, the query type is not limited.

Public cards are available through the API via ``PublicCardPermission``
and ``PublicCardAuthentication`` classes imported into
`api/views.py <https://github.com/datahuborg/datahub/blob/master/src/api/views.py>`__

.. note:: Given time, we would have liked to allow users to pass parameters into public card queries. See `issue 156 <https://github.com/datahuborg/datahub/issues/156>`__.
