.. _django-app-dataq:

DataQ
**********
**NOTE: DataQ is not currently enabled in DataHub**

| primary(s): `Harihar Subramanyam <https://github.com/hariharsubramanyam>`_
| maintainer(s): `Harihar Subramanyam <https://github.com/hariharsubramanyam>`_
| location: ``src/apps/dataq``

DataQ allows you to write SQL queries using a simple checklist-like user interface.

==========
How to use
==========
* Run DataHub
* Select a repo
* Select a table to browse
* Click the "DataQ" button, which will be next to the text box in which you would type your SQL

-------------------
Building a Query
-------------------
1. **Pick Columns**: Click "Add Table" and select the columns to include in the query (click columns to apply aggregates)
2. **Filter**: Click "Add Filter" and specify a filter condition of the form "<expr> <operator> <expr>"
3. **Group**: If you have an aggregate, click "Edit Grouping" and reorder the columns (click and drag)
4. **Sort**: Click "Edit Sorting" and reorder the order of sorting.
