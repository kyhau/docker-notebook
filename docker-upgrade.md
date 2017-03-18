# Docker notes

KNOWN ISSUES (2017-03-17)

When updating Ubuntu packages on a Ubuntu 14.4 machine  

1. Failed on latest docker "1.12.0" (https://github.com/docker/compose/issues/3927)
1. Downgraded to 1.11.2,  "sudo apt-get install docker-engine=1.11.2-0~trusty", another error (https://github.com/docker/docker/issues/22323)
1. Rolled back to "sudo apt-get install docker-engine=1.8.2-0~trusty", fine again.



## Docker Upgrade

```bash
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
