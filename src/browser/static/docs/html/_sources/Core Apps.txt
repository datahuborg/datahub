Core Apps
*********

Django applications are built on to of the DataHub web application. These apps
do not necessarily use the DataHub API, and are not deployed in mobile
environments. Instead, they are deployed on the DataHub website itself.

.. toctree::
    :hidden:
    
    django-app-console
    django-app-dataq
    django-app-datatables
    django-app-dbwipes
    django-app-refiner
    django-app-sentiment
    django-app-viz2


=======
Console
=======

:ref:`django-app-console`

| primary(s):   `Anant Bhardwaj <https://github.com/abhardwaj>`_
| maintiner(s): `Al Carter <https://github.com/RogerTangos>`_

Console provides a way for users to interact directly with their datahub repos.

=====
DataQ
=====

:ref:`django-app-dataq`

| primary(s):   `Harihar Subramanyam <https://github.com/hariharsubramanyam>`_
| maintiner(s): `Harihar Subramanyam <https://github.com/hariharsubramanyam>`_

DataQ is a visual SQL query builder

==========
DataTables
==========

:ref:`django-app-datatables`

| primary(s):   `Harihar Subramanyam <https://github.com/hariharsubramanyam>`_
| maintiner(s): `Harihar Subramanyam <https://github.com/hariharsubramanyam>`_

DataTables allows users to manipulate SQL tables like they would an excel table.
Users are able to sort, filter, and aggregate tables.

=======
dbWipes
=======

:ref:`django-app-dbwipes`

| primary(s):   `Eugene Wu <https://github.com/sirrice>`_
| maintiner(s): `Eugene Wu <https://github.com/sirrice>`_

`DBWipes <http://www.mit.edu/~eugenewu/dbwipes.html>`_ helps you quickly 
visualize data, identify outliers, and understand where those outliers arise 
from in the underlying data set


=======
Refiner
=======

:ref:`django-app-refiner`

| primary(s):   `Harihar Subramanyam <https://github.com/hariharsubramanyam>`_, `Anant Bhardwaj <https://github.com/abhardwaj>`_
| maintiner(s): `Harihar Subramanyam <https://github.com/hariharsubramanyam>`_, `Anant Bhardwaj <https://github.com/abhardwaj>`_

Refiner is a tool that converts poorly structured text files into structured
data for table creation. It is ongoing research, and is currently only for
demonstration purposes.

=========
Sentiment
=========

:ref:`django-app-sentiment`

| primary(s):   `Harihar Subramanyam <https://github.com/hariharsubramanyam>`_
| maintiner(s): `Harihar Subramanyam <https://github.com/hariharsubramanyam>`_

Sentiment is a sentiment analysis tool for DataHub

===================
Viz2 (formerly Viz)
===================

:ref:`django-app-viz2`

| primary(s):   `Anant Bhardwaj <https://github.com/abhardwaj>`_
| maintiner(s): `Al Carter <https://github.com/RogerTangos>`_

viz2 (renamed due to a naming collision) uses Google Charts to visualize the 
results of database queries.