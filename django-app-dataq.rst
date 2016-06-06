.. _django-app-dataq:

DataQ
**********

| primary(s): `Harihar Subramanyam <https://github.com/hariharsubramanyam>`_
| maintainer(s): `Gina Yuan <https://github.com/ygina>`_
| location: ``src/apps/dataq``

DataQ allows you to write SQL queries using a simple checklist-like user interface.

==========
How to use
==========
* Run DataHub
* Select a repo
* Click the "DataQ" button, which will be next to the text box in which you would type your SQL

============
How to build
============
* Go to ``datahub/src/apps/dataq``
* ``$ npm install`` to install dependencies in package.json (Note: DataQ is not compatible with more recent versions of gulp-handlebars)
* ``$ gulp`` to build existing files to ``/src/browser/static/``
* ``$ gulp watch`` to automatically compile files as you edit them
* To make changes to the current configuration, edit the files in ``datahub/src/apps/dataq/client_src/``
* In vagrant, ``dh-rebuild-and-collect-static-files``
* Clear cache and view changes in browser

-------------------
Building a Query
-------------------
1. **Pick Columns**: Click "Add Table" and select the columns to include in the query (click columns to apply aggregates)
2. **Filter**: Click "Add Filter" and specify a filter condition of the form ``<expr> <operator> <expr>``
3. **Group**: If you have an aggregate, click "Edit Grouping" and reorder the columns (click and drag)
4. **Sort**: Click "Edit Sorting" and reorder the order of sorting.
