# docker-stuff

### To build a Docker image depending on another image from Docker registry.

Edit "/etc/default/docker"
````sh
DOCKER_OPTS="--insecure-registry <docker registry url>"
````

Restart docker service

````sh
$ sudo service docker restart
````
