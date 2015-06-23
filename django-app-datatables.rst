.. _django-app-datatables:

DataTables
**********
| primary(s): `Harihar Subramanyam <https://github.com/hariharsubramanyam>`_
| maintainer(s): `Harihar Subramanyam <https://github.com/hariharsubramanyam>`_
| location: ``src/apps/datatables``

DataTables enhances the popular `DataTables.js <http://www.datatables.net>`_ library to allow viewing and querying tables of data.

==========
How to use
==========
* Run DataHub
* Select a repo
* Select a table to browse
* The table of data should be shown on the page

--------------
Basic Features
--------------
1. **Sort**: Click a column to sort (click again to toggle ascending/descending). Shift-click to sort by multiple columns.
2. **Show/Hide Columns**: Click the blue "Show/hide columns" button and select (or deselect) the columns you want to show (or hide).
3. **Rearrange Columns**: Click and drag a column to rearrange the order of columns
4. **Paginate**: Click the desired page number (or arrow) below bottom right of table
5. **Number of Records**: Click the dropdown menu above top-left of table and select the number of records to display
6. **Aggregates**: Click the blue "Aggregate" button, select a function (ex. min, max) and a column to compute the aggregate.

-------
Filters
-------
Filters allow querying the table to display the rows which satisfy some condition.

* **Add Filter**: Flick the blue "New Filter" button, it will add a row (i.e. the filter) to the bottom of the table
* **Filter on Column**: A filter has one textbox for each column. Enter text to filter on that column
* **Change Column Filter Operator**: By default, each column of the filter checks for equality (i.e. only show rows which have col = "my value"). You can click the button next to each textbox in the filter to change the operator.
* **Multiple Filters**: If you have one filter, a row must satisfy every condition in the filter in order to appear in the table. If you have two filters (call them A and B), a row must satisfy all the conditions in filter A OR all the conditions in filter B OR both in order to appear in the table.

You can **Invert Filter** by clicking the button (i.e. any row that was in the table will be gone, and any row that wasn't in the table will be shown).