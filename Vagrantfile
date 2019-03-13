# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box_url = "https://mirrors.tuna.tsinghua.edu.cn/ubuntu-cloud-images/bionic/20181212/bionic-server-cloudimg-amd64-vagrant.box"
  config.vm.box = "ubuntu/bionic"

  config.vm.synced_folder ".", "/var/www/bbs"

  config.vm.network "public_network"

  config.vm.provision "shell", inline: <<-SHELL
    sudo su
    bash /var/www/bbs/mirror.sh
    bash /var/www/bbs/deploy.sh
  SHELL
  
end
