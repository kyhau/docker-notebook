## Docker Upgrade

```sh
$ sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
 
$ sudo nano /etc/apt/sources.list.d/docker.list
------
# remove: deb https://get.docker.com/ubuntu docker main
# add:
deb https://apt.dockerproject.org/repo ubuntu-trusty main
------
 
$ sudo apt-get update
$ sudo apt-get purge lxc-docker*
$ sudo apt-get install docker-engine
 
$ docker -v
# Docker version 1.8.1, build d12ea79
```
