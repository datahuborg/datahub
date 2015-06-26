Core URLs
*********

This page is meant to document some of the features of datahub 

Home Page
---------

| ``url(r'^$', 'browser.views.home')``
| serves the home page

| ``url(r'^about$', 'browser.views.about')``
| serves the home page, exists for backward compatibility

Dev Page
--------

| ``url(r'^www/', include('www.urls'))``
| some endpoints, mostly developer docs (which no longer exist there)

Account Management
------------------

| ``url(r'^account/', include('account.urls'))```
| Account creation 


Thrift Services
---------------

| ``url(r'^service$', 'browser.views.service_core_binary')``
| endpoint for thrift api 

| ``url(r'^service/account$', 'browser.views.service_account_binary')``
| endpoint for thrift api

| ``url(r'^service/json$', 'browser.views.service_core_json')``
| endpoint for thrift api


Create Repos, Table
-------------------

| ``url(r'^create/(\w+)/repo/?$', 'browser.views.repo_create')``
| create a repository


| ``url(r'^create/(\w+)/(\w+)/card/?$', 'browser.views.card_create')``
| create a card (Cards store queries at the web app level, without creating a view.
In this way, they're database independent.)

| ``url(r'^create/annotation/?$', 'browser.views.create_annotation')``
| Users create annotations to describe tables views and cards for future reference


Browse
------

| ``url(r'^browse/(\w+)/(\w+)/table/(\w+)/?$', 'browser.views.table')``
| View a table

| ``url(r'^browse/(\w+)/(\w+)/query/?$', 'browser.views.query')``
| View a query

| ``url(r'^browse/(\w+)/(\w+)/card/(.+)/?$', 'browser.views.card')``
| View a query that was previously saved in datahub (whtout a view)

| ``url(r'^browse/(\w+)/(\w+)/tables/?$', 'browser.views.repo_tables')``
| Show a list of tables, views, and cards associated with a repo

| ``url(r'^browse/(\w+)/(\w+)/files/?$', 'browser.views.repo_files')``
| Show a list of files that the user has uploaded to a repo

| ``url(r'^browse/(\w+)/(\w+)/cards/?$', 'browser.views.repo_cards')``
| Show a list of cards that the user has created for a repo

| ``url(r'^browse/(\w+)/(\w+)/dashboards/?$', 'browser.views.repo_dashboards')``
| Show a list of dashboards that the user has created for a repo

| ``url(r'^browse/(\w+)/?$', 'browser.views.user')``
| Show a list of repositories that the user has created

Delete
------

| ``url(r'^delete/(\w+)/(\w+)/?$', 'browser.views.repo_delete')``
| Delete a repo

| ``url(r'^delete/(\w+)/(\w+)/table/(\w+)/?$', 'browser.views.table_delete')``
| Delete a table

| ``url(r'^delete/(\w+)/(\w+)/card/(\w+)/?$', 'browser.views.card_delete')``
| Delete a card

| ``url(r'^delete/(\w+)/(\w+)/file/([\w\d\-\.]+)/?$', 'browser.views.file_delete')``
| Delete a file

Export
------

| ``url(r'^export/(\w+)/(\w+)/table/(\w+)/?$', 'browser.views.table_export')``
| Export a table as a CSV

Special File Operations
-----------------------

| ``url(r'^upload/(\w+)/(\w+)/file/?$', 'browser.views.file_upload')``
| Upload a file to datahub, for processing

| ``url(r'^import/(\w+)/(\w+)/file/([\w\d\-\.]+)', 'browser.views.file_import')``
| Import a file's data

| ``url(r'^download/(\w+)/(\w+)/file/([\w\d\-\.]+)', 'browser.views.file_download')``
| Download a file previously uploaded to datahub

Settings
--------

| ``url(r'^settings/(\w+)/(\w+)/?$', 'browser.views.repo_settings')``
| Manage repository settings, including collaborators

Collaborators
-------------

| ``url(r'^collaborator/repo/(\w+)/(\w+)/add/?$', 'browser.views.repo_collaborators_add')``
| Add a collaborator to a repo

| ``url(r'^collaborator/repo/(\w+)/(\w+)/remove/(\w+)/?$', 'browser.views.``repo_collaborators_remove')``
| Remove a collaborator from a repo


Client Apps
-----------
| ``url(r'^developer/apps/?$', 'browser.views.apps')``
| View a list of application tokens that the user has created

| ``url(r'^developer/apps/register/?$', 'browser.views.apps_register')``
| Register a new client application, and get authentication tokens for it

| ``url(r'^developer/apps/remove/(\w+)/?$', 'browser.views.app_remove')``
| Remove a client application

| ``url(r'^permissions/apps/allow_access/(\w+)/(\w+)$', 'browser.views.app_allow_access')``
| Grant an existing application access to a repository

Core Apps
---------

| ``url(r'^apps/console/', include('console.urls')),``
| :ref:`django-app-console`

| ``url(r'^apps/refiner/', include('refiner.urls')),``
| refiner app

| ``url(r'^apps/dbwipes/', include('dbwipes.urls')),``
| dbwipes app

| ``url(r'^apps/viz/', include('viz2.urls')),``
| viz app

| ``url(r'^apps/sentiment/', include('sentiment.urls')),``
| sentiment app

| ``url(r'^apps/dataq/', include('dataq.urls')),``
| dataq app

| ``url(r'^apps/datatables/', include('datatables.urls')),``
| datatables app