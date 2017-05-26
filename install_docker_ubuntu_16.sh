#!/bin/bash

###############################################################################
# Install docker daemon on ubuntu-xenial
# See https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04

# Update the package database
sudo apt-get update

# Add the GPG key for the official Docker repository to the system
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D

# Add the Docker repository to APT sources
sudo apt-add-repository 'deb https://apt.dockerproject.org/repo ubuntu-xenial main'

# Update the package database with the Docker packages from the newly added repo
sudo apt-get update

# Make sure you are about to install from the Docker repo instead of the
# default Ubuntu 16.04 repo
apt-cache policy docker-engine

# Finally install Docker
sudo apt-get install -y docker-engine

# Docker should now be installed, the daemon started, and the process enabled
# to start on boot. Check that it's running
sudo systemctl status docker

# Add your username to the docker group
sudo usermod -aG docker $(whoami)
