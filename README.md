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

-----------------------------
### Vagrant environment

Follow these steps:

1. You need internet access the first time you do these steps.
2. Download and install VirtualBox [https://www.virtualbox.org/](https://www.virtualbox.org/)
3. Download and install Vagrant [https://www.vagrantup.com/downloads.html](https://www.vagrantup.com/downloads.html)
4. Add this line to your hosts file:
  ```
  192.168.50.4    datahub-local.mit.edu
  ```
5. Then start the environment with:
  ```
  vagrant up
  ```
  After some time your environment is setup and running. You can go to [http://datahub-local.mit.edu](http://datahub-local.mit.edu) and start using Datahub.

If you want to manually stop/start your docker containers, first login into VM:
```
vagrant ssh
```
Then
* List docker containers
  ```
  sudo docker ps
  ```
* Stop docker datahub
  ```
  sudo docker stop datahub
  ```

* Start docker container
  ```
  sudo docker start datahub
  ```

* Execute command inside container, bellow is the example of getting shell access to container
  ```
  sudo docker exec -i -t datahub /bin/bash
  ```

Run test with `behave`:

1. Login in VM
  ```
  vagrant ssh
  ```
2. Get shell access to datahub container
  ```
  sudo docker exec -i -t datahub /bin/bash
  ```
3. Change directory and execute `behave`
  ```
  cd /datahub/src
  behave
  ```

Shutdown Vagrant

  1. Exit docker shell with `exit` (if you are in docker)
  2. Exit the vm with `exit` (if you are in vagrant VM)
  3. Shutdown the vm with `vagrant halt` (next time you do `vagrant up` will be much faster as packages are already installed; there is no need for internet connection).
  4. If you want to delete the vm `vagrant destroy` (if you do `vagrant up` again, it will download and install all the packages).
