*Note: This project is under development. It is not yet ready for production use.*

DataHub
===========
DataHub is an experimental hosted platform (GitHub-like) for organizing, managing, sharing, collaborating, and making sense of data. It provides an efficient platform and easy to use tools/interfaces for:

* Publishing of your own data (hosting, sharing, collaboration)
* Using other’s data (querying, linking)
* Making sense of data (analysis, visualization)

### Get Started

+ [https://github.com/datahuborg/datahub/wiki/Getting-Started](https://github.com/datahuborg/datahub/wiki/Getting-Started)

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

The last step could take several minutes depending on the speed of your connection and computer.

When `vagrant up` finishes, you can find your environment running at [http://datahub-local.mit.edu](http://datahub-local.mit.edu).

Note that datahub-local.mit.edu is local to your computer and unreachable by other machines. Because it is local, you can edit DataHub's files on your computer, and those changes will be reflected on datahub-local.mit.edu.