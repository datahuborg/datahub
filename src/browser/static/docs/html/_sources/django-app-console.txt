.. _django-app-console:

Console App
***********
| primary(s):   `Anant Bhardwaj <https://github.com/abhardwaj>`_
| maintiner(s): `Al Carter <https://github.com/RogerTangos>`_
| location: ``src/apps/console``

Console provides a way for users to interact directly with their datahub repos.
It's a database terminal for datahub.

==========
How to use
==========
* Run DataHub
* Navigate to `apps\/console <http://localhost:8000/apps/console>`_
* Type SQL

-------------------
Available Commands: 
-------------------

| ``connect <repo-base>``: connect to a datahub user
| e.g. ``connect username``

| ``mkrepo <repo-name>``: create a new repository
| e.g. ``mkrepo myrepo``

| ``rm <repo-name [-f]>``: to remove a repository
| e.g. ``rm myrepo``
        
| ``ls`` : to list repositories
| e.g. ``ls``

| ``ls <repo-name>`` : to list tables in a repository,
| e.g. ``ls myrepo``

| ``schema <table-name>`` : to print schema info of a table,
| e.g. ``schema myrepo.mytable``

| ``<other DML>``: execute arbitrary DML on a repo.tablename in your currently connected repo-base
| e.g. ``select * from myrepo.mytable``