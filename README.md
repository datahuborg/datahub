[![Build Status](https://travis-ci.org/datahuborg/datahub.svg?branch=master)](https://travis-ci.org/datahuborg/datahub) [![Code Climate](https://codeclimate.com/github/datahuborg/datahub/badges/gpa.svg)](https://codeclimate.com/github/datahuborg/datahub)

*Note: This project is under development. It is not yet ready for production use.*

DataHub
===========
DataHub is an experimental hosted platform (GitHub-like) for organizing, managing, sharing, collaborating, and making sense of data. It provides an efficient platform and easy to use tools/interfaces for:

* Publishing of your own data (hosting, sharing, collaboration)
* Using other’s data (querying, linking)
* Making sense of data (analysis, visualization)

### Get Started

+ [https://datahub.csail.mit.edu/static/docs/html/index.html](https://datahub.csail.mit.edu/static/docs/html/index.html)

### Example Code

+ [https://github.com/datahuborg/datahub/tree/master/src/examples](https://github.com/datahuborg/datahub/tree/master/src/examples)

### Demo
+ [https://datahub.csail.mit.edu](https://datahub.csail.mit.edu)

### Contact Info
+ [datahub@csail.mit.edu](mailto:datahub@csail.mit.edu)

## Quickstart

Vagrant is the recommend method for developing with DataHub. It provides a VM matching the DataHub production server, regardless of your host system.

1. Install VirtualBox [https://www.virtualbox.org/](https://www.virtualbox.org/).

1. Install Vagrant [https://www.vagrantup.com/downloads.html](https://www.vagrantup.com/downloads.html).

1. Clone DataHub:
    ```bash
    $ git clone https://github.com/datahuborg/datahub.git
    ```

1. Add this line to your hosts file (/etc/hosts on most systems):
    ```bash
    192.168.50.4    datahub-local.mit.edu
    ```

1. From your clone, start the VM:
    ```bash
    $ vagrant up
    ```

This last step might take several minutes depending on your connection and computer.

When `vagrant up` finishes, you can find your environment running at [http://datahub-local.mit.edu](http://datahub-local.mit.edu).

Vagrant keeps your working copy and the VM in sync, so edits you make to DataHub's code will be reflected on datahub-local.mit.edu. Changes to static files like CSS, JS, and documentation must be collected before the server will notice them. For more information, see the docs at [https://datahub.csail.mit.edu/static/docs/html/index.html](https://datahub.csail.mit.edu/static/docs/html/index.html).