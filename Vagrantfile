# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.network "private_network", ip: "192.168.50.4"
  config.vm.hostname = "datahub-local.mit.edu"
  config.vm.provision "shell", path: "provisions/setup.sh"

  config.vm.provider "virtualbox" do |vm|
    vm.name = "datahub-local"
    vm.memory = 2048
    #vm.cpus = 2
  end
end
