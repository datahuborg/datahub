*Note: The project is under development. It is not ready for deployment yet.*

DataHub
===========
DataHub is an experimental hosted platform (GitHub-like) for organizing, managing, sharing, collaborating, and making sense of data. It provides an efficient platform and easy to use tools/interfaces for:

* Publishing of your own data (hosting, sharing, collaboration)
* Using other’s data (querying, linking)
* Making sense of data (analysis, visualization)

### Get Started

+ [https://github.com/abhardwaj/datahub/wiki/Getting-Started](https://github.com/abhardwaj/datahub/wiki/Getting-Started)

### Example Code

+ [https://github.com/abhardwaj/datahub/tree/master/src/examples](https://github.com/abhardwaj/datahub/tree/master/src/examples)

### Demo
+ [http://datahub.csail.mit.edu](http://datahub.csail.mit.edu)

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
6. Login into vagrant:
  ```
  vagrant ssh
  ```
7. Start the app
  ```
  cd /vagrant
  sudo -s
  source src/setup.sh
  python src/manage.py runserver 0.0.0.0:80
  ```
8. Then open the browser and go to [datahub-local.mit.edu](datahub-local.mit.edu)
9. When you are done

  1. Press `CONTROL-C`
  2. Exit the vm with `exit` (you need to execute it twice)
  3. Shutdown the vm with `vagrant halt` (next time you do `vagrant up` will be much faster as packages are already installed; there is no need for internet connection).

  4. If you want to delete the vm `vagrant destroy` (if you do `vagrant up` again, it will download and install all the packages).
