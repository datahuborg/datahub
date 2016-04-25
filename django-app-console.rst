.. _django-app-console:

Console App
***********
| primary(s):   `Gina Yuan <https://github.com/ygina>`_
| maintainer(s): `Gina Yuan <https://github.com/ygina>`_
| location: ``src/apps/console``

Console is a database terminal for datahub. It provides a way for users to
interact directly with their database and repos/schemas, and is a consumer of
the DataHub API.

==========
How to use
==========
* Run DataHub
* Navigate to `apps\/console <apps/console>`_
* Type SQL or bash commands

-------------------
Available Commands:
-------------------

| ``help``: lists available commands
| e.g. ``help``

| ``connect <repo-base>``: connect to a datahub user
| e.g. ``connect username``

| ``mkrepo <repo-name>``: create a new repository
| e.g. ``mkrepo myrepo``

| ``rm <repo-name [-f]>``: remove a repository
| e.g. ``rm myrepo``

| ``ls`` : list repositories
| e.g. ``ls``

| ``collab <repo-name>`` : list collaborators of a repository
| e.g. ``collab myrepo``

| ``ls <repo-name>`` : list tables and views in a repository
| e.g. ``ls myrepo``

| ``desc <table-name [-l]>`` : print schema info of a table [with data type]
| e.g. ``schema myrepo.mytable``

| ``<other DML>``: execute arbitrary DML on a repo.tablename in your currently connected repo-base
| e.g. ``select * from myrepo.mytable``